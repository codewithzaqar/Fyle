import os
from datetime import datetime

def get_file_info(path):
    stats = os.stat(path)
    return {
        "name": os.path.basename(path),
        "size": f"{stats.st_size} bytes",
        "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "id_dir": os.path.isdir(path)
    }

def validate_path(path):
    return os.path.exists(path)