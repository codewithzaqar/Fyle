from cli_interface import CLIInterface
from file_manager import FileManager

def main():
    file_manager = FileManager()
    cli = CLIInterface(file_manager)
    cli.run()

if __name__ == "__main__":
    main()