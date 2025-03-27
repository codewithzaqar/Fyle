import os
import json
from datetime import datetime
import logging
import stat
from difflib import get_close_matches

def get_file_info(path):
    try:
        stats = os.stat(path)
        return {
            "name": os.path.basename(path),
            "size": f"{stats.st_size} bytes",
            "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "is_dir": os.path.isdir(path)
        }
    except Exception as e:
        logging.error(f"Failed to get file info for {path}: {str(e)}")
        return {"name": os.path.basename(path), "error": str(e)}

def validate_path(path):
    exists = os.path.exists(path)
    if not exists:
        logging.warning(f"Path validation failed: {path} does not exist")
    return exists

def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        logging.info("Configuration loaded successfully")
        return config
    except Exception as e:
        raise Exception(f"Failed to load configuration: {str(e)}")

def validate_config(config):
    required = {"version", "prompt", "max_history", "search_recursive", "default_sort", 
                "min_size", "max_size", "aliases", "autocomplete", "log_level", 
                "batch_enabled", "tags_enabled", "script_dir", "completion_enabled", "color_enabled"}
    missing = required - set(config.keys())
    if missing:
        raise Exception(f"Missing config keys: {missing}")
    if config["default_sort"] not in ["name", "mtime"]:
        raise Exception(f"Invalid default_sort value: {config['default_sort']}")
    if not isinstance(config["min_size"], (int, str)) or (isinstance(config["min_size"], str) and not config["min_size"].isdigit()):
        raise Exception(f"Invalid min_size value: {config['min_size']}")
    if config["max_size"] is not None and not isinstance(config["max_size"], (int, str)) or (isinstance(config["max_size"], str) and not config["min_size"].isdigit()):
        raise Exception(f"Invalid max_size value: {config['max_size']}")
    if not isinstance(config["autocomplete"], bool):
        raise Exception(f"Invalid autocomplete value: {config['autocomplete']}")
    if config["log_level"] not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise Exception(f"Invalid log_level value: {config['log_level']}")
    if not isinstance(config["batch_enabled"], bool):
        raise Exception(f"Invalid batch_enabled value: {config['batch_enabled']}")
    if not isinstance(config["tags_enabled"], bool):
        raise Exception(f"Invalid tags_enabled value: {config['tags_enabled']}")
    if not isinstance(config["script_dir"], str):
        raise Exception(f"Invalid script_dir value: {config['script_dir']}")
    if not isinstance(config["completion_enabled"], bool):
        raise Exception(f"Invalid completion_enabled value: {config['completion_enabled']}")
    if not isinstance(config["color_enabled"], bool):
        raise Exception(f"Invalid color_enabled value: {config['color_enabled']}")

def setup_logging(log_file, log_level):
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    logging.basicConfig(
        filename=log_file,
        level=level_map.get(log_level, logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_permissions(path):
    try:
        stats = os.stat(path)
        mode = stats.st_mode
        perms = ""
        perms += "r" if mode & stat.S_IRUSR else "-"
        perms += "w" if mode & stat.S_IWUSR else "-"
        perms += "x" if mode & stat.S_IXUSR else "-"
        perms += "r" if mode & stat.S_IRGRP else "-"
        perms += "w" if mode & stat.S_IWGRP else "-"
        perms += "x" if mode & stat.S_IXGRP else "-"
        perms += "r" if mode & stat.S_IROTH else "-"
        perms += "w" if mode & stat.S_IWOTH else "-"
        perms += "x" if mode & stat.S_IXOTH else "-"
        return perms
    except Exception as e:
        raise Exception(f"Failed to get permissions: {str(e)}")

def size_to_bytes(size):
    if size is None:
        return None
    if isinstance(size, int):
        return size
    size = size.lower()
    units = {"k": 1024, "m": 1024*1024, "g": 1024*1024*1024}
    if size[-1] in units:
        return int(size[:-1]) * units[size[-1]]
    return int(size)

def suggest_commands(input_cmd, available_commands):
    return get_close_matches(input_cmd, available_commands, n=3, cutoff=0.6)

def run_script(script_path, cli):
    if not os.path.exists(script_path):
        return f"Script file not found: {script_path}"
    try:
        with open(script_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    cli.run_command(line.split())
        return True
    except Exception as e:
        return f"Failed to run script: {str(e)}"

def get_file_completions(directory):
    try:
        return [f for f in os.listdir(directory) if not f.startswith('.')]
    except Exception:
        return []