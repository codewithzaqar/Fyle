import os

class FileManager:
    def __init__(self):
        self.current_dir = os.getcwd()

    def list_files(self):
        return os.listdir(self.current_dir)

    def change_dir(self, path):
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            return True
        except Exception as e:
            return str(e)

    def get_current_dir(self):
        return self.current_dir