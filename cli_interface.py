from datetime import datetime

class CLIInterface:
    def __init__(self, file_manager, config):
        self.file_manager = file_manager
        self.config = config
        self.running = False
        self.history = []  # Now stores tuples of (timestamp, command)

    def display_help(self):
        print("\nCommands:")
        print("  dir/ls [detail] - List files (optional: detailed view)")
        print("  cd <path> - Change directory")
        print("  pwd - Show current directory")
        print("  del/rm <name> - Delete file or directory")
        print("  create <name> - Create new empty file")
        print("  copy <source> <dest> - Copy file or directory")
        print("  rename/mv <old> <new> - Rename file or directory")
        print("  view/cat <name> - View file contents (first 1KB)")
        print("  search <pattern> [r] - Search files(optional: r for recursive)")
        print("  perms <name> - View file permissions")
        print("  edit <name> <content> - Append text to file")
        print("  history - Show command history")
        print("  exit - Quit the program")
        print("  help - Show this message")

    def resolve_alias(self, cmd):
        return self.config.get("aliases", {}).get(cmd, cmd)

    def run(self):
        self.running = True
        print("""
            __________       ______     
            ___  ____/____  ____  /____ 
            __  /_   __  / / /_  /_  _ \ 
            _  __/   _  /_/ /_  / /  __/
            /_/      _\__, / /_/  \___/ 
                     /____/              
            Type 'help' for commands  v0.07""")
        
        while self.running:
            try:
                command = input(f"\n{self.config['prompt']}").strip().split()
                if not command:
                    continue
                    
                cmd = self.resolve_alias(command[0].lower())
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.history.append((timestamp, " ".join(command)))
                
                if cmd in ["exit", "quit"]:
                    self.running = False
                elif cmd in ["dir", "ls"]:
                    detailed = len(command) > 1 and command[1].lower() == "detail"
                    sort_by = command[2].lower() if len(command) > 2 else self.config["default_sort"]
                    min_size = command[3] if len(command) > 3 else self.config["min_size"]
                    max_size = command[4] if len(command) > 4 else self.config["max_size"]
                    if sort_by not in ["name", "mtime"]:
                        sort_by = self.config["default_sort"]
                    files = self.file_manager.list_files(detailed, sort_by, min_size, max_size)
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
                elif cmd in ["rename", "mv"] and len(command) > 2:
                    result = self.file_manager.rename_file(command[1], command[2])
                    if result is True:
                        print(f"Renamed {command[1]} to {command[2]}")
                    else:
                        print(f"Error: {result}")
                elif cmd in ["view", "cat"] and len(command) > 1:
                    result = self.file_manager.read_file(command[1])
                    if isinstance(result, str) and not result.startswith("Error"):
                        print(f"\nContents of {command[1]}:\n{result}")
                    else:
                        print(f"Error: {result}")
                elif cmd == "search" and len(command) > 1:
                    recursive = (len(command) > 2 and command[2].lower() == "r") or self.config["search_recursive"]
                    result = self.file_manager.search_files(command[1], recursive)
                    if isinstance(result, list):
                        print(f"\nFound {len(result)} matches:")
                        print("\n".join(result))
                    else:
                        print(f"Error: {result}")
                elif cmd == "perms" and len(command) > 1:
                    result = self.file_manager.get_file_permissions(command[1])
                    if isinstance(result, str) and not result.startswith("Error"):
                        print(f"\nPermissions for {command[1]}: {result}")
                    else:
                        print(f"Error: {result}")
                elif cmd == "edit" and len(command) > 2:
                    content = " ".join(command[2:])
                    result = self.file_manager.edit_file(command[1], content)
                    if result is True:
                        print(f"Appended to {command[1]}")
                    else:
                        print(f"Error: {result}")
                elif cmd == "history":
                    for i, (ts, cmd) in enumerate(self.history, 1):
                        print(f"{i}. [{ts}] {cmd}")
                elif cmd == "help":
                    self.display_help()
                else:
                    print("Unknown command. Type 'help' for available commands")
            except Exception as e:
                print(f"Error: {str(e)}")