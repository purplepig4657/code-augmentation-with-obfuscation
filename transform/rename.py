from pycparser import c_ast, c_generator, parse_file

def generate_names(prefix):
    for i in range(26):
        yield f"{prefix}{chr(97 + i)}"
    i, j = 0, 0
    while True:
        yield f"{prefix}{chr(97 + i)}{chr(97 + j)}"
        j += 1
        if j == 26:
            i += 1
            j = 0
        if i == 26:
            i = 0

class NameChanger(c_ast.NodeVisitor):
    def __init__(self):
        self.func_name_generator = generate_names("f_")
        self.func_name_map = {}
        self.var_name_generator = generate_names("v_")
        self.var_name_map = {}
        self.global_name_generator = generate_names("g_")
        self.global_name_map = {}

    def visit_FileAST(self, node):
        # First pass: process function prototypes and global variables
        for ext in node.ext:
            if isinstance(ext, c_ast.Decl):
                if isinstance(ext.type, c_ast.FuncDecl):
                    self.visit_function_prototype(ext)
                else:
                    self.visit_global_decl(ext)
        
        # Second pass: process everything else
        self.generic_visit(node)

    def visit_function_prototype(self, node):
        if node.name != 'main' and "complex_decl" not in node.name:
            if node.name not in self.func_name_map:
                new_name = next(self.func_name_generator)
                self.func_name_map[node.name] = new_name
            if isinstance(node.type, c_ast.FuncDecl):
                if isinstance(node.type.type, c_ast.TypeDecl):
                    node.type.type.declname = self.func_name_map[node.name]

    def visit_global_decl(self, node):
        if node.name not in self.global_name_map:
            new_name = next(self.global_name_generator)
            self.global_name_map[node.name] = new_name
        self.visit_type(node.type)

    def visit_FuncDef(self, node):
        self.var_name_map = {}
        self.var_name_generator = generate_names("v_")
        if node.decl.name != 'main' and "complex_decl" not in node.decl.name:
            if node.decl.name not in self.func_name_map:
                new_name = next(self.func_name_generator)
                self.func_name_map[node.decl.name] = new_name
            if isinstance(node.decl.type, c_ast.FuncDecl):
                if isinstance(node.decl.type.type, c_ast.TypeDecl):
                    node.decl.type.type.declname = self.func_name_map[node.decl.name]
                    node.decl.name = self.func_name_map[node.decl.name]
        self.generic_visit(node)

    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.Struct):
            return
        if not isinstance(node.type, c_ast.FuncDecl) and node.name:
            if node.name in self.global_name_map:
                new_name = self.global_name_map[node.name]
            elif node.name not in self.var_name_map:
                new_name = next(self.var_name_generator)
                self.var_name_map[node.name] = new_name
            else:
                new_name = self.var_name_map[node.name]
            self.visit_type(node.type)
        self.generic_visit(node)

    def visit_type(self, node):
        if isinstance(node, c_ast.TypeDecl):
            if node.declname in self.global_name_map:
                node.declname = self.global_name_map[node.declname]
            else:
                # If the variable is not in the map, keep the original name.
                # This is for global variable re-visits.
                node.declname = self.var_name_map.get(node.declname, node.declname)
        elif isinstance(node, c_ast.ArrayDecl):
            self.visit_type(node.type)
        elif isinstance(node, c_ast.PtrDecl):
            self.visit_type(node.type)

    def visit_ID(self, node):
        if node.name in self.global_name_map:
            node.name = self.global_name_map[node.name]
        elif node.name in self.var_name_map:
            node.name = self.var_name_map[node.name]
        elif node.name in self.func_name_map:
            node.name = self.func_name_map[node.name]

    def rename(self, file_path: str):
        try:
            ast = parse_file(file_path)
            self.visit(ast)

            generator = c_generator.CGenerator()
            renamed_code = generator.visit(ast)

            with open(file_path, 'w') as file:
                file.write(renamed_code)

            return True
        except Exception as e:
            print(f"Error occurred while renaming {file_path}: {e}")
            return False
