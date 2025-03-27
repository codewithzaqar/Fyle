import logging
import json
from colorama import init as colorama_init
from cli_interface import CLIInterface
from file_manager import FileManager
from utils import load_config, validate_config, setup_logging

def main():
    colorama_init()

    try:
        config = load_config('config.json')
        validate_config(config)
        logging.info("Configuration validated successfully")
    except Exception as e:
        logging.error(f"Configuration error: {str(e)}")
        print(f"Warning: Configuration error - using defaults: {str(e)}")
        config = {
            "version": "0.13",
            "prompt": "FyleCLI> ",
            "max_history": 100,
            "search_recursive": False,
            "default_sort": "name",
            "min_size": 0,
            "max_size": None,
            "autocomplete": True,
            "completion_enabled": True,
            "color_enabled": True,
            "progress_enabled": True,
            "log_level": "INFO",
            "batch_enabled": True,
            "tags_enabled": True,
            "script_dir": "scripts",
            "aliases": {
                "ls": "dir",
                "rm": "del",
                "mv": "rename",
                "cat": "view"
            }
        }
    
    setup_logging('logs/cli.log', config["log_level"])

    file_manager = FileManager()
    cli = CLIInterface(file_manager, config)
    cli.run()

if __name__ == "__main__":
    main()      