import os
import shutil
import logging
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
            logging.info(f"Changed directory to: {self.current_dir}")
            return True
        except Exception as e:
            logging.error(f"Failed to change directory: {str(e)}")
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
            logging.info(f"Deleted: {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to delete {filename}: {str(e)}")
            return str(e)

    def create_file(self, filename):
        try:
            full_path = os.path.join(self.current_dir, filename)
            with open(full_path, 'w') as f:
                f.write('')
            logging.info(f"Created file: {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to create {filename}: {str(e)}")
            return str(e)
        
    def copy_file(self, source, destination):
        try:
            src_path = os.path.join(self.current_dir, source)
            dest_path = os.path.join(self.current_dir, destination)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
            logging.info(f"Copied {source} to {destination}")
            return True
        except Exception as e:
            logging.error(f"Failed to copy {source} to {destination}: {str(e)}")
            return str(e)