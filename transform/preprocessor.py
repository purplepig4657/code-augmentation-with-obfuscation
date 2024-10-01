import regex

class Preprocessor:
    GENERATED_STRUCTS = ['_IO_FILE', 'timeval', '__sFILE', '__sFILEX', '__sbuf', '__anonstruct__RuneCharClass_1021650748', '__anonstruct__RuneEntry_453100079', '__anonstruct__RuneLocale_110080762', '__anonstruct__RuneRange_1000210131', 'timespec']
    TYPEDEF_KEYWORDS = ['wint_t', '__uint32_t', 'fpos_t', 'wctype_t']

    def __init__(
        self,
        remove_extern: bool = True,
        remove_generated_struct: bool = True,
        remove_top_comments: bool = True,
        remove_typedefs: bool = True,
        remove_comments: bool = True,
    ):
        self.remove_extern = remove_extern
        self.remove_generated_struct = remove_generated_struct
        self.remove_top_comments = remove_top_comments
        self.remove_typedefs = remove_typedefs
        self.remove_comments = remove_comments

    def preprocess(self, file: str) -> bool:
        with open(file, 'r') as f:
            content = f.read()

        if self.remove_extern:
            content = regex.sub(r'^extern[\s\S]*?;[\s\n]*', '', content, flags=regex.MULTILINE)
            content = regex.sub(r'^__inline\s+extern[\s\S]*?(?:;|(\{(?:[^{}]++|(?1))*\}))[\s\n]*', '', content, flags=regex.MULTILINE)

        if self.remove_comments:
            content = regex.sub(r'//.*$', '', content, flags=regex.MULTILINE)
            content = regex.sub(r'/\*[\s\S]*?\*/', '', content)

        if self.remove_generated_struct:
            for struct_name in self.GENERATED_STRUCTS:
                # (example: struct _IO_FILE;)
                content = regex.sub(rf'struct\s+{struct_name}\s*;\n', '', content)
                # (example): struct timeval { ... };)
                content = regex.sub(rf'struct\s+{struct_name}\s*\{{[^}}]*\}};\n', '', content)
                # (example): typedef struct _IO_FILE FILE;)
                content = regex.sub(rf'typedef\s+struct\s+{struct_name}\s+\w+;\n', '', content)

        if self.remove_typedefs:
            typedef_pattern = r'typedef\s+(?:\w+\s+)*(?:' + '|'.join(self.TYPEDEF_KEYWORDS) + r')\s*(?:\w+\s*)*;\n'
            content = regex.sub(typedef_pattern, '', content)

        with open(file, 'w') as f:
            f.write(content)

        if self.remove_top_comments:
            with open(file, 'r') as f:
                lines = f.readlines()

            lines[0] = lines[1] = lines[2] = ''

            with open(file, 'w') as f:
                f.writelines(lines)

        return True
