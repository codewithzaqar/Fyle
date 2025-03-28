import os
import shutil
import json
import logging
import zipfile
import hashlib
from tqdm import tqdm
from utils import get_file_info, get_permissions, size_to_bytes, set_permissions

class FileManager:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.tags_file = 'tags.json'
        self.load_tags()

    def load_tags(self):
        try:
            if os.path.exists(self.tags_file):
                with open(self.tags_file, 'r') as f:
                    self.tags = json.load(f)
            else:
                self.tags = {}
        except Exception as e:
            logging.error(f"Failed to load tags: {str(e)}")
            self.tags = {}

    def save_tags(self):
        try:
            with open(self.tags_file, 'w') as f:
                json.dump(self.tags, f, indent=2)
            logging.debug("Tags saved successfully")
        except Exception as e:
            logging.error(f"Failed to save tags: {str(e)}")

    def list_files(self, detailed=False, sort_by="name", min_size=0, max_size=None):
        try:
            files = os.listdir(self.current_dir)
            full_paths = [os.path.join(self.current_dir, f) for f in files]
            
            filtered_paths = []
            for path in full_paths:
                size = os.path.getsize(path)
                min_size_bytes = size_to_bytes(min_size)
                max_size_bytes = size_to_bytes(max_size) if max_size else float('inf')
                if min_size_bytes <= size <= max_size_bytes:
                    filtered_paths.append(path)
            
            if sort_by == "mtime":
                filtered_paths.sort(key=lambda x: os.path.getmtime(x))
            else:
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
            if full_path in self.tags:
                del self.tags[full_path]
                self.save_tags()
            logging.info(f"Deleted: {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to delete {filename}: {str(e)}")
            raise Exception(f"Delete failed: {str(e)}")

    def batch_delete(self, filenames):
        results = {}
        for filename in filenames:
            try:
                result = self.delete_file(filename)
                results[filename] = "Success" if result else "Failed"
            except Exception as e:
                results[filename] = str(e)
        return results

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
            if src_path in self.tags:
                self.tags[dest_path] = self.tags[src_path]
                self.save_tags()
            logging.info(f"Copied {source} to {destination}")
            return True
        except Exception as e:
            logging.error(f"Failed to copy {source} to {destination}: {str(e)}")
            raise Exception(f"Copy failed: {str(e)}")

    def batch_copy(self, sources, destination):
        results = {}
        for source in sources:
            try:
                result = self.copy_file(source, os.path.join(destination, os.path.basename(source)))
                results[source] = "Success" if result else "Failed"
            except Exception as e:
                results[source] = str(e)
        return results

    def rename_file(self, old_name, new_name):
        try:
            old_path = os.path.join(self.current_dir, old_name)
            new_path = os.path.join(self.current_dir, new_name)
            os.rename(old_path, new_path)
            if old_path in self.tags:
                self.tags[new_path] = self.tags.pop(old_path)
                self.save_tags()
            logging.info(f"Renamed {old_name} to {new_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to rename {old_name} to {new_name}: {str(e)}")
            raise Exception(f"Rename failed: {str(e)}")

    def move_file(self, source, destination):
        try:
            src_path = os.path.join(self.current_dir, source)
            dest_path = os.path.abspath(destination)
            shutil.move(src_path, dest_path)
            if src_path in self.tags:
                self.tags[dest_path] = self.tags.pop(src_path)
                self.save_tags()
            logging.info(f"Moved {source} to {destination}")
            return True
        except Exception as e:
            logging.error(f"Failed to move {source} to {destination}: {str(e)}")
            raise Exception(f"Move failed: {str(e)}")

    def batch_move(self, sources, destination):
        results = {}
        for source in sources:
            try:
                result = self.move_file(source, os.path.join(destination, os.path.basename(source)))
                results[source] = "Success" if result else "Failed"
            except Exception as e:
                results[source] = str(e)
        return results

    def read_file(self, filename):
        try:
            full_path = os.path.join(self.current_dir, filename)
            with open(full_path, 'r') as f:
                content = f.read(1024)
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
        
    def set_file_permissions(self, filename, perms):
        try:
            full_path = os.path.join(self.current_dir, filename)
            set_permissions(full_path, perms)
            logging.info(f"Set permissions for {filename} to {perms}")
            return True
        except Exception as e:
            logging.error(f"Failed to set permissions for {filename}: {str(e)}")
            raise Exception(f"Permissions set failed: {str(e)}")

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

    def add_tag(self, filename, tag):
        try:
            full_path = os.path.join(self.current_dir, filename)
            if full_path not in self.tags:
                self.tags[full_path] = []
            if tag not in self.tags[full_path]:
                self.tags[full_path].append(tag)
                self.save_tags()
            logging.info(f"Added tag '{tag}' to {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to add tag to {filename}: {str(e)}")
            raise Exception(f"Tag add failed: {str(e)}")

    def remove_tag(self, filename, tag):
        try:
            full_path = os.path.join(self.current_dir, filename)
            if full_path in self.tags and tag in self.tags[full_path]:
                self.tags[full_path].remove(tag)
                if not self.tags[full_path]:
                    del self.tags[full_path]
                self.save_tags()
            logging.info(f"Removed tag '{tag}' from {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to remove tag from {filename}: {str(e)}")
            raise Exception(f"Tag remove failed: {str(e)}")

    def get_tags(self, filename):
        try:
            full_path = os.path.join(self.current_dir, filename)
            tags = self.tags.get(full_path, [])
            logging.debug(f"Retrieved tags for {filename}: {tags}")
            return tags
        except Exception as e:
            logging.error(f"Failed to get tags for {filename}: {str(e)}")
            raise Exception(f"Tag get failed: {str(e)}")

    def search_by_tag(self, tag, recursive=False):
        try:
            matches = []
            search_dir = self.current_dir
            
            if recursive:
                for root, _, files in os.walk(search_dir):
                    for f in files:
                        full_path = os.path.join(root, f)
                        if full_path in self.tags and tag in self.tags[full_path]:
                            matches.append(os.path.relpath(full_path, search_dir))
            else:
                for f in os.listdir(search_dir):
                    full_path = os.path.join(search_dir, f)
                    if full_path in self.tags and tag in self.tags[full_path]:
                        matches.append(f)
            
            logging.info(f"Searched for tag '{tag}' - found {len(matches)} matches")
            return matches
        except Exception as e:
            logging.error(f"Tag search failed: {str(e)}")
            raise Exception(f"Tag search failed: {str(e)}")
        
    def compress(self, source, zip_name, progress=False):
        try:
            src_path = os.path.join(self.current_dir, source)
            zip_path = os.path.join(self.current_dir, zip_name)
            if not zip_path.endswith('.zip'):
                zip_path += '.zip'

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                if os.path.isdir(src_path):
                    files = [os.path.join(root, f) for root, _, fs in os.walk(src_path) for f in fs]
                    iterator = tqdm(files, desc=f"Compressing {source}") if progress else files
                    for file in iterator:
                        zf.write(file, os.path.relpath(file, self.current_dir))
                else:
                    zf.write(src_path, os.path.basename(src_path))

            logging.info(f"Compressed {source} to {zip_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to compress {source}: {str(e)}")
            raise Exception(f"Compress failed: {str(e)}")
        
    def extract(self, zip_name, dest_dir=None, progress=False):
        try:
            zip_path = os.path.join(self.current_dir, zip_name)
            dest_path = os.path.join(self.current_dir, dest_dir) if dest_dir else self.current_dir

            with zipfile.ZipFile(zip_path, 'r') as zf:
                files = zf.namelist()
                iterator = tqdm(files, desc=f"Extracting {zip_name}") if progress else files
                for file in iterator:
                    zf.extract(file, dest_path)
                
            logging.info(f"Extracted {zip_name} to {dest_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to extract {zip_name}: {str(e)}")
            raise Exception(f"Extract failed: {str(e)}")
        
    def extract(self, zip_name, dest_dir=None, progress=False):
        try:
            zip_path = os.path.join(self.current_dir, zip_name)
            dest_path = os.path.join(self.current_dir, dest_dir) if dest_dir else self.current_dir

            with zipfile.ZipFile(zip_path, 'r') as zf:
                files = zf.namelist()
                iterator = tqdm(files, desc=f"Extracting {zip_name}") if progress else files
                for file in iterator:
                    zf.extract(file, dest_path)

            logging.info(f"Extracted {zip_name} to {dest_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to extract {zip_name}: {str(e)}")
            raise Exception(f"Extract failed: {str(e)}")
        
    def hash_file(self, filename, algo="sha256"):
        try:
            full_path = os.path.join(self.current_dir, filename)
            hash_obj = hashlib.sha256() if algo.lower() == "sha256" else hashlib.md5()
            with open(full_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            hash_value = hash_obj.hexdigest()
            logging.info(f"Computed {algo} hash for {filename}: {hash_value}")
            return hash_value
        except Exception as e:
            logging.error(f"Failed to hash {filename}: {str(e)}")
            raise Exception(f"Hash failed: {str(e)}")