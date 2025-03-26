import os
import shutil
import logging
from utils import get_file_info, get_permissions, size_to_bytes

class FileManager:
    def __init__(self):
        self.current_dir = os.getcwd()

    def list_files(self, detailed=False, sort_by="name", min_size=0, max_size=None):
        try:
            files = os.listdir(self.current_dir)
            full_paths = [os.path.join(self.current_dir, f) for f in files]
            
            # Filter by size
            filtered_paths = []
            for path in full_paths:
                size = os.path.getsize(path)
                min_size_bytes = size_to_bytes(min_size)
                max_size_bytes = size_to_bytes(max_size) if max_size else float('inf')
                if min_size_bytes <= size <= max_size_bytes:
                    filtered_paths.append(path)
            
            # Sort
            if sort_by == "mtime":
                filtered_paths.sort(key=lambda x: os.path.getmtime(x))
            else:  # Default to name sorting
                filtered_paths.sort()
                
            files = [os.path.basename(p) for p in filtered_paths]
            if detailed:
                return [get_file_info(p) for p in filtered_paths]
            return files
        except Exception as e:
            logging.error(f"Failed to list files: {str(e)}")
            raise Exception(f"List operation failed: {str(e)}")

    def change_dir(self, path):
        try:
            new_path = os.path.abspath(path)
            os.chdir(new_path)
            self.current_dir = os.getcwd()
            logging.info(f"Changed directory to: {self.current_dir}")
            return True
        except Exception as e:
            logging.error(f"Failed to change directory: {str(e)}")
            raise Exception(f"Directory change failed: {str(e)}")

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
            raise Exception(f"Delete failed: {str(e)}")

    def create_file(self, filename):
        try:
            full_path = os.path.join(self.current_dir, filename)
            with open(full_path, 'w') as f:
                f.write('')
            logging.info(f"Created file: {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to create {filename}: {str(e)}")
            raise Exception(f"Create failed: {str(e)}")

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
            raise Exception(f"Copy failed: {str(e)}")

    def rename_file(self, old_name, new_name):
        try:
            old_path = os.path.join(self.current_dir, old_name)
            new_path = os.path.join(self.current_dir, new_name)
            os.rename(old_path, new_path)
            logging.info(f"Renamed {old_name} to {new_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to rename {old_name} to {new_name}: {str(e)}")
            raise Exception(f"Rename failed: {str(e)}")
        
    def move_file(self, source, destination):
        try:
            src_path = os.path.join(self.current_dir, source)
            dest_path = os.path.abspath(destination)  # Support absolute paths
            shutil.move(src_path, dest_path)
            logging.info(f"Moved {source} to {destination}")
            return True
        except Exception as e:
            logging.error(f"Failed to move {source} to {destination}: {str(e)}")
            raise Exception(f"Move failed: {str(e)}")

    def read_file(self, filename):
        try:
            full_path = os.path.join(self.current_dir, filename)
            with open(full_path, 'r') as f:
                content = f.read(1024)  # Read first 1KB
            logging.info(f"Viewed file: {filename}")
            return content
        except Exception as e:
            logging.error(f"Failed to read {filename}: {str(e)}")
            raise Exception(f"Read failed: {str(e)}")

    def search_files(self, pattern, recursive=False):
        try:
            matches = []
            search_dir = self.current_dir
            
            if recursive:
                for root, _, files in os.walk(search_dir):
                    for f in files:
                        if pattern.lower() in f.lower():
                            matches.append(os.path.relpath(os.path.join(root, f), search_dir))
            else:
                for f in os.listdir(search_dir):
                    if pattern.lower() in f.lower():
                        matches.append(f)
            
            logging.info(f"Searched for '{pattern}' - found {len(matches)} matches")
            return matches
        except Exception as e:
            logging.error(f"Search failed: {str(e)}")
            raise Exception(f"Search failed: {str(e)}")

    def get_file_permissions(self, filename):
        try:
            full_path = os.path.join(self.current_dir, filename)
            perms = get_permissions(full_path)
            logging.info(f"Viewed permissions for: {filename}")
            return perms
        except Exception as e:
            logging.error(f"Failed to get permissions for {filename}: {str(e)}")
            raise Exception(f"Permissions check failed: {str(e)}")

    def edit_file(self, filename, content):
        try:
            full_path = os.path.join(self.current_dir, filename)
            with open(full_path, 'a') as f:
                f.write(content + '\n')
            logging.info(f"Edited file: {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to edit {filename}: {str(e)}")
            raise Exception(f"Edit failed: {str(e)}")