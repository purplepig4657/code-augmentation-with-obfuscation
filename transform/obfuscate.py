import os
import platform
import subprocess
import shutil
from typing import Literal

class Obfuscator:
    def __init__(self, 
                 compiler="${CC}",
                 project_root=None, 
                 result_path="obfuscated", 
                 tigress_include_path="includes"
                ):
        if project_root is None or not os.path.isabs(project_root):
            raise ValueError("Project root must be an absolute path")

        if os.path.isabs(result_path):
            self.result_path = result_path
        else:
            self.result_path = os.path.join(project_root, result_path)

        if os.path.isabs(tigress_include_path):
            self.tigress_include_path = tigress_include_path
        else:
            self.tigress_include_path = os.path.join(project_root, tigress_include_path)

        self.compiler = f"{compiler} -I{self.tigress_include_path}"
        self.project_root = project_root
        self.tigress_path = shutil.which("tigress")

        print(self.tigress_include_path)

        if not self.tigress_path:
            raise FileNotFoundError("Tigress executable not found in PATH")

    def __is_compilable(self, file: str) -> bool:
        process_output = subprocess.run(
            f"{self.compiler} {file} -o /dev/null 1> /dev/null 2>&1", 
            shell=True  # noqa: S607
        )
        return True if process_output.returncode == 0 else False

    def __insert_tigress_header(self, file: str) -> str:
        try:
            with open(file, "r") as f:
                lines = f.readlines()
            if 'tigress.h' not in lines[0]: 
                # If the file wasn't changed, the inserted tigress header will be on the first line.
                with open(file, "w") as f:
                    f.write("#include \"tigress.h\"\n")
                    f.writelines(lines)
        except Exception as e:
            print(f"Error occurred while inserting tigress header: {e}")
            return False

    def obfuscate(self, file: str, obfuscation_type: Literal["AddOpaque", "Flatten"] = "Flatten") -> bool:
        self.__insert_tigress_header(file)

        if not self.__is_compilable(file):
            print("This code is not compilable.")
            return False

        file_name = file.split("/")[-1].split(".")[0]

        if platform.system() == "Darwin" and platform.machine() == "arm64":
            command_prefix = "/usr/bin/arch -x86_64"
        else:
            command_prefix = ""

        base_command = f"{command_prefix} {self.tigress_path} --Seed=42"

        if obfuscation_type == "AddOpaque":
            command = f"""
                {base_command} \\
                --Environment=x86_64:Darwin:Clang:5.1 \\
                --Transform=InitOpaque \\
                --Functions=\\* \\
                --AddOpaqueStructs=env \\
                --InitOpaqueCount=1 \\
                --Transform=AddOpaque \\
                --Functions=\\* \\
                --AddOpaqueKinds=true \\
                --AddOpaqueCount=1 \\
                --gcc={self.compiler} \\
                {file} \\
                --out={self.result_path}/{'_'.join([file_name, obfuscation_type])}.c
            """
        else:  # Flatten
            command = f"""
                {base_command} \\
                --Environment=x86_64:Darwin:Clang:5.1 \\
                --Transform=Flatten \\
                --Functions=\\* \\
                --gcc={self.compiler} \\
                {file} \\
                --out={self.result_path}/{'_'.join([file_name, obfuscation_type])}.c
            """

        try:
            process_output = subprocess.run(
                command, 
                stdout=subprocess.DEVNULL, 
                shell=True,  # noqa: S607
                timeout=10
            )
        except subprocess.TimeoutExpired:
            print(f"Command execution timed out after 10 seconds")
            return False

        if process_output.returncode != 0:
            print(f"Error occurred while obfuscating {file}: {process_output.returncode}")
            return False

        return True
