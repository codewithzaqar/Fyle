class CLIInterface:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.running = False

    def display_help(self):
        print("\nCommands:")
        print("  dir/ls - List files in current directory")
        print("  cd <path> - Change directory")
        print("  pwd - Show current directory")
        print("  exit - Quit the program")
        print("  help - Show this message")

    def run(self):
        self.running = True
        print("""
            __________       ______     
            ___  ____/____  ____  /____ 
            __  /_   __  / / /_  /_  _ \ 
            _  __/   _  /_/ /_  / /  __/
            /_/      _\__, / /_/  \___/ 
                    /____/              
            Type 'help' for commands   v0.01""")
        
        while self.running:
            command = input(f"\n{self.file_manager.get_current_dir()}> ").strip().split()
            
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd in ["exit", "quit"]:
                self.running = False
            elif cmd in ["dir", "ls"]:
                files = self.file_manager.list_files()
                print("\n".join(files))
            elif cmd == "cd" and len(command) > 1:
                result = self.file_manager.change_dir(command[1])
                if result is not True:
                    print(f"Error: {result}")
            elif cmd == "pwd":
                print(self.file_manager.get_current_dir())
            elif cmd == "help":
                self.display_help()
            else:
                print("Unknown command. Type 'help' for available commands")
