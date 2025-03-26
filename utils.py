import os
from datetime import datetime
import logging

def get_file_info(path):
    try:
        stats = os.stat(path)
        return {
            "name": os.path.basename(path),
            "size": f"{stats.st_size} bytes",
            "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "id_dir": os.path.isdir(path)
        }
    except Exception as e:
        logging.error(f"Failed to get file info for {path}: {str(e)}")
        return {"name": os.path.basename(path), "error": str(e)}

def validate_path(path):
    exists = os.path.exists(path)
    if not exists:
        logging.warning(f"Path validation failed: {path} does not exist")
    return exists