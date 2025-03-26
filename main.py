import logging
import json
from cli_interface import CLIInterface
from file_manager import FileManager
from utils import load_config, validate_config

def main():
    # Configure logging
    logging.basicConfig(
        filename='logs/cli.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Load configuration
    try:
        config = load_config('config.json')
        validate_config(config)
    except Exception as e:
        logging.error(f"Failed to load config: {str(e)}")
        config = {
            "version": "0.05",
            "prompt": "FyleCLI> ",
            "max_history": 100,
            "search_recursive": False
        }

    file_manager = FileManager()
    cli = CLIInterface(file_manager, config)
    cli.run()

if __name__ == "__main__":
    main()      