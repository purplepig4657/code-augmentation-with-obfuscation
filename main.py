import os

from transform import Obfuscator
from transform import Preprocessor
from transform import NameChanger

from file_load import FileLoader

RESULT_PATH = "obfuscated"
TIGRESS_INCLUDE_PATH = "includes"

file_loader = FileLoader(os.path.dirname(os.path.abspath(__file__)))

obfuscator = Obfuscator(
    "/usr/bin/clang", 
    project_root=file_loader.project_root, 
    result_path=RESULT_PATH, 
    tigress_include_path=TIGRESS_INCLUDE_PATH
)

preprocessor = Preprocessor(remove_extern=True, remove_generated_struct=True)

target_files = file_loader.extract_strings_from_directory()

print(target_files)

obfuscate_successed = 0
obfuscate_failed = 0

current_index = 0

for file in target_files:
    current_index += 1
    print(f"[{current_index}/{len(target_files)}] Obfuscating {file} ...")
    obfuscate_type = "Flatten"
    obfuscate_success = obfuscator.obfuscate(file, obfuscate_type)
    file_name = file.split('/')[-1].split('.')[0]
    if obfuscate_success:
        name_changer = NameChanger()
        preprocessor.preprocess(f"{RESULT_PATH}/{file_name}_{obfuscate_type}.c")
        name_changer.rename(f"{RESULT_PATH}/{file_name}_{obfuscate_type}.c")
        obfuscate_successed += 1
    else:
        print(f"Failed to obfuscate {file}")
        obfuscate_failed += 1

print(f"Obfuscate successed: {obfuscate_successed}")
print(f"Obfuscate failed: {obfuscate_failed}")
