import logging
import json
from cli_interface import CLIInterface
from file_manager import FileManager
from utils import load_config, validate_config, setup_logging

def main():
    # Load configuration first to get log level
    try:
        config = load_config('config.json')
        validate_config(config)
        logging.info("Configuration validated successfully")
    except Exception as e:
        logging.error(f"Configuration error: {str(e)}")
        print(f"Warning: Configuration error - using defaults: {str(e)}")
        config = {
            "version": "0.09",
            "prompt": "FyleCLI> ",
            "max_history": 100,
            "search_recursive": False,
            "default_sort": "name",
            "min_size": 0,
            "max_size": None,
            "autocomplete": True,
            "log_level": "INFO",
            "batch_enabled": True,
            "aliases": {
                "ls": "dir",
                "rm": "del",
                "mv": "rename",
                "cat": "view"
            }
        }
    
    # Setup logging with configured level
    setup_logging('logs/cli.log', config["log_level"])

    file_manager = FileManager()
    cli = CLIInterface(file_manager, config)
    cli.run()

if __name__ == "__main__":
    main()      