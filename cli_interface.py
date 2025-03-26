class CLIInterface:
    def __init__(self, file_manager, config):
        self.file_manager = file_manager
        self.config = config
        self.running = False
        self.history = []

    def display_help(self):
        print("\nCommands:")
        print("  dir/ls [detail] - List files (optional: detailed view)")
        print("  cd <path> - Change directory")
        print("  pwd - Show current directory")
        print("  del/rm <name> - Delete file or directory")
        print("  create <name> - Create new empty file")
        print("  copy <source> <dest> - Copy file or directory")
        print("  history - Show command history")
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
            Type 'help' for commands  v0.03""")
        
        while self.running:
            command = input(f"\n{self.config['prompt']}").strip().split()
            if not command:
                continue
                
            cmd = command[0].lower()
            self.history.append(" ".join(command))
            
            if cmd in ["exit", "quit"]:
                self.running = False
            elif cmd in ["dir", "ls"]:
                detailed = len(command) > 1 and command[1].lower() == "detail"
                files = self.file_manager.list_files(detailed)
                print("\n".join(str(f) for f in files))
            elif cmd == "cd" and len(command) > 1:
                result = self.file_manager.change_dir(command[1])
                if result is not True:
                    print(f"Error: {result}")
            elif cmd == "pwd":
                print(self.file_manager.get_current_dir())
            elif cmd in ["del", "rm"] and len(command) > 1:
                result = self.file_manager.delete_file(command[1])
                if result is True:
                    print(f"Deleted: {command[1]}")
                else:
                    print(f"Error: {result}")
            elif cmd == "create" and len(command) > 1:
                result = self.file_manager.create_file(command[1])
                if result is True:
                    print(f"Created: {command[1]}")
                else:
                    print(f"Error: {result}")
            elif cmd == "copy" and len(command) > 2:
                result = self.file_manager.copy_file(command[1], command[2])
                if result is True:
                    print(f"Copied {command[1]} to {command[2]}")
                else:
                    print(f"Error: {result}")        
            elif cmd == "history":
                for i, cmd in enumerate(self.history, 1):
                    print(f"{i}. {cmd}")
            elif cmd == "help":
                self.display_help()
            else:
                print("Unknown command. Type 'help' for available commands")