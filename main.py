from cli_interface import CLIInterface
from file_manager import FileManager

def main():
    # Basic configuration
    config = {
        "version": "0.02",
        "prompt": "FyleCLI> "
    }

    file_manager = FileManager()
    cli = CLIInterface(file_manager, config)
    cli.run()

if __name__ == "__main__":
    main()      