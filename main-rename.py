import os

from transform import copy_c_file
from transform import Preprocessor
from transform import NameChanger

from file_load import FileLoader

RESULT_PATH = "rename"

file_loader = FileLoader(os.path.dirname(os.path.abspath(__file__)))

preprocessor = Preprocessor(remove_extern=True, remove_generated_struct=True)

target_files = file_loader.extract_strings_from_directory()

print(target_files)


rename_successed = 0
rename_failed = 0

current_index = 0

for file in target_files:
    current_index += 1
    print(f"[{current_index}/{len(target_files)}] renaming {file} ...")
    copy_c_file(target_files, RESULT_PATH)
    file_name = file.split('/')[-1].split('.')[0]
    name_changer = NameChanger()
    preprocess_success = preprocessor.preprocess(f"{RESULT_PATH}/{file_name}_rename.c")
    rename_success = name_changer.rename(f"{RESULT_PATH}/{file_name}_rename.c")
    if preprocess_success and rename_success:
        rename_successed += 1
    else:
        print(f"Failed to preprocess or rename {file}")
        rename_failed += 1

print(f"Rename successed: {rename_successed}")
print(f"Rename failed: {rename_failed}")
