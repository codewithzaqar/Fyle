import os
import shutil
from utils import get_file_info

class FileManager:
    def __init__(self):
        self.current_dir = os.getcwd()

    def list_files(self, detailed=False):
        files = os.listdir(self.current_dir)
        if detailed:
            return [get_file_info(os.path.join(self.current_dir, f)) for f in files]
        return files

    def change_dir(self, path):
        try:
            new_path = os.path.abspath(path)
            os.chdir(new_path)
            self.current_dir = os.getcwd()
            return True
        except Exception as e:
            return str(e)

    def get_current_dir(self):
        return self.current_dir
    
    def delete_file(self, filename):
        try:
            full_path = os.path.join(self.current_dir, filename)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
            return True
        except Exception as e:
            return str(e)