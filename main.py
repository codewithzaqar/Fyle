import logging
from cli_interface import CLIInterface
from file_manager import FileManager

def main():
    # Configure logging
    logging.basicConfig(
        filename='logs/cli.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    config = {
        "version": "0.03",
        "prompt": "FyleCLI> "
    }

    file_manager = FileManager()
    cli = CLIInterface(file_manager, config)
    cli.run()

if __name__ == "__main__":
    main()      