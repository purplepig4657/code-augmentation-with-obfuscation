import os

class FileLoader:
    def __init__(self, project_root, data_directory="data"):
        self.__project_root = project_root
        if os.path.isabs(data_directory):
            self.__data_directory = data_directory
        else:
            self.__data_directory = os.path.join(self.__project_root, data_directory)
            print(self.__data_directory)

    def find_source_files(self):
        source_files = []
        for root, _, files in os.walk(self.data_directory):
            for file in files:
                if file.endswith('.c'):
                    source_files.append(os.path.join(root, file))
        return source_files

    def extract_strings_from_directory(self):
        source_files = self.find_source_files()
        return source_files
    
    @property
    def project_root(self):
        return self.__project_root

    @property
    def data_directory(self):
        return self.__data_directory
