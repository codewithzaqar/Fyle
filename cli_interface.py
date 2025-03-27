import os
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from colorama import Fore, Style
from utils import suggest_commands, run_script, get_file_completions

class CLIInterface:
    def __init__(self, file_manager, config):
        self.file_manager = file_manager
        self.config = config
        self.running = False
        self.history = []
        self.commands = [
            "dir", "ls", "cd", "pwd", "del", "rm", 'create', "copy",
            "rename", "mv", "move", "view", "cat", "search", "perms",
            "edit", "history", "help", "exit", "batch_del", "batch_copy",
            "batch_move", "exec", "tag", "untag", "tags", "script", "tagsearch",
            "compress", "extract"
        ]
        self.completer = NestedCompleter.from_nested_dict({
            cmd: None if cmd in ["dir", "ls", "pwd", "history", "help", "exit"]
            else WordCompleter(get_file_completions(self.file_manager.get_current_dir()))
            for cmd in self.commands + list(self.config["aliases"].keys())
        })
        self.session = PromptSession(completer=self.completer if self.config["completion_enabled"] else None,
                                    complete_while_typing=True)

    def display_help(self):
        if self.config["color_enabled"]:
            print(f"{Fore.CYAN}\nCommands:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}  dir/ls [detail] [sort] [min_size] [max_size]{Style.RESET_ALL} - List files")
            print(f"{Fore.GREEN}  cd <path>{Style.RESET_ALL} - Change directory")
            print(f"{Fore.GREEN}  pwd{Style.RESET_ALL} - Show current directory")
            print(f"{Fore.GREEN}  del/rm <name>{Style.RESET_ALL} - Delete file or directory")
            print(f"{Fore.GREEN}  batch_del <name1> <name2> ...{Style.RESET_ALL} - Batch delete files")
            print(f"{Fore.GREEN}  create <name>{Style.RESET_ALL} - Create new empty file")
            print(f"{Fore.GREEN}  copy <source> <dest>{Style.RESET_ALL} - Copy file or directory")
            print(f"{Fore.GREEN}  batch_copy <source1> <source2> ... <dest>{Style.RESET_ALL} - Batch copy files")
            print(f"{Fore.GREEN}  rename/mv <old> <new>{Style.RESET_ALL} - Rename file or directory")
            print(f"{Fore.GREEN}  move <source> <dest>{Style.RESET_ALL} - Move file or directory")
            print(f"{Fore.GREEN}  batch_move <source1> <source2> ... <dest>{Style.RESET_ALL} - Batch move files")
            print(f"{Fore.GREEN}  view/cat <name>{Style.RESET_ALL} - View file contents (first 1KB)")
            print(f"{Fore.GREEN}  search <pattern> [r]{Style.RESET_ALL} - Search files (r for recursive)")
            print(f"{Fore.GREEN}  perms <name>{Style.RESET_ALL} - View file permissions")
            print(f"{Fore.GREEN}  edit <name> <content>{Style.RESET_ALL} - Append text to file")
            print(f"{Fore.GREEN}  tag <name> <tag>{Style.RESET_ALL} - Add tag to file")
            print(f"{Fore.GREEN}  untag <name> <tag>{Style.RESET_ALL} - Remove tag from file")
            print(f"{Fore.GREEN}  tags <name>{Style.RESET_ALL} - Show tags for file")
            print(f"{Fore.GREEN}  tagsearch <tag> [r]{Style.RESET_ALL} - Search files by tag (r for recursive)")
            print(f"{Fore.GREEN}  compress <source> <zip_name>{Style.RESET_ALL} - Compress file or directory to zip")
            print(f"{Fore.GREEN}  extract <zip_name> [dest_dir]{Style.RESET_ALL} - Extract zip to directory")
            print(f"{Fore.GREEN}  history{Style.RESET_ALL} - Show command history with timestamps")
            print(f"{Fore.GREEN}  exec <number>{Style.RESET_ALL} - Execute command from history")
            print(f"{Fore.GREEN}  script <filename>{Style.RESET_ALL} - Run commands from script file")
            print(f"{Fore.GREEN}  exit{Style.RESET_ALL} - Quit the program")
            print(f"{Fore.GREEN}  help{Style.RESET_ALL} - Show this message")
        else:
            print("\nCommands:")
            print("  dir/ls [detail] [sort] [min_size] [max_size] - List files")
            print("  cd <path> - Change directory")
            print("  pwd - Show current directory")
            print("  del/rm <name> - Delete file or directory")
            print("  batch_del <name1> <name2> ... - Batch delete files")
            print("  create <name> - Create new empty file")
            print("  copy <source> <dest> - Copy file or directory")
            print("  batch_copy <source1> <source2> ... <dest> - Batch copy files")
            print("  rename/mv <old> <new> - Rename file or directory")
            print("  move <source> <dest> - Move file or directory")
            print("  batch_move <source1> <source2> ... <dest> - Batch move files")
            print("  view/cat <name> - View file contents (first 1KB)")
            print("  search <pattern> [r] - Search files (r for recursive)")
            print("  perms <name> - View file permissions")
            print("  edit <name> <content> - Append text to file")
            print("  tag <name> <tag> - Add tag to file")
            print("  untag <name> <tag> - Remove tag from file")
            print("  tags <name> - Show tags for file")
            print("  tagsearch <tag> [r] - Search files by tag (r for recursive)")
            print("  compress <source> <zip_name> - Compress file or directory to zip")
            print("  extract <zip_name> [dest_dir] - Extract zip to directory")
            print("  history - Show command history with timestamps")
            print("  exec <number> - Execute command from history")
            print("  script <filename> - Run commands from script file")
            print("  exit - Quit the program")
            print("  help - Show this message") 

    def resolve_alias(self, cmd):
        return self.config.get("aliases", {}).get(cmd, cmd)
    
    def trim_history(self):
        if len(self.history) > self.config["max_history"]:
            self.history = self.history[-self.config["max_history"]:]

    def run(self):
        self.running = True
        print("""
            __________       ______     
            ___  ____/____  ____  /____ 
            __  /_   __  / / /_  /_  _ \ 
            _  __/   _  /_/ /_  / /  __/
            /_/      _\__, / /_/  \___/ 
                     /____/              
            Type 'help' for commands  v0.13""")
        
        while self.running:
            try:
                command = self.session.prompt(f"\n{self.config['prompt']}").strip().split()
                if not command:
                    continue
                    
                cmd = self.resolve_alias(command[0].lower())
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.history.append((timestamp, " ".join(command)))
                self.trim_history()
                
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
                    if self.config["color_enabled"]:
                        for f in files:
                            if isinstance(f, dict) and f.get("is_dir"):
                                print(f"{Fore.BLUE}{f['name']}{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.WHITE}{f}{Style.RESET_ALL}")
                    else:
                        print("\n".join(str(f) for f in files))
                elif cmd == "cd" and len(command) > 1:
                    result = self.file_manager.change_dir(command[1])
                    if result is not True:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "pwd":
                    if self.config["color_enabled"]:
                        print(f"{Fore.CYAN}{self.file_manager.get_current_dir()}{Style.RESET_ALL}")
                    else:
                        print(self.file_manager.get_current_dir())
                elif cmd in ["del", "rm"] and len(command) > 1:
                    result = self.file_manager.delete_file(command[1])
                    if result is True:
                        print(f"{Fore.GREEN}Deleted: {command[1]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Deleted: {command[1]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "batch_del" and len(command) > 1 and self.config["batch_enabled"]:
                    results = self.file_manager.batch_delete(command[1:], progress=self.config["progress_enabled"])
                    for fname, result in results.items():
                        if self.config["color_enabled"]:
                            color = Fore.GREEN if result == "Success" else Fore.RED
                            print(f"{color}{fname}: {result}{Style.RESET_ALL}")
                        else:
                            print(f"{fname}: {result}")
                elif cmd == "create" and len(command) > 1:
                    result = self.file_manager.create_file(command[1])
                    if result is True:
                        print(f"{Fore.GREEN}Created: {command[1]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Created: {command[1]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "copy" and len(command) > 2:
                    result = self.file_manager.copy_file(command[1], command[2])
                    if result is True:
                        print(f"{Fore.GREEN}Copied {command[1]} to {command[2]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Copied {command[1]} to {command[2]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "batch_copy" and len(command) > 2 and self.config["batch_enabled"]:
                    sources = command[1:-1]
                    dest = command[-1]
                    results = self.file_manager.batch_copy(sources, dest, progress=self.config["progress_enabled"])
                    for src, result in results.items():
                        if self.config["color_enabled"]:
                            color = Fore.GREEN if result == "Success" else Fore.RED
                            print(f"{color}{src} -> {dest}: {result}{Style.RESET_ALL}")
                        else:
                            print(f"{src} -> {dest}: {result}")
                elif cmd in ["rename", "mv"] and len(command) > 2:
                    result = self.file_manager.rename_file(command[1], command[2])
                    if result is True:
                        print(f"{Fore.GREEN}Renamed {command[1]} to {command[2]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Renamed {command[1]} to {command[2]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "move" and len(command) > 2:
                    result = self.file_manager.move_file(command[1], command[2])
                    if result is True:
                        print(f"{Fore.GREEN}Moved {command[1]} to {command[2]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Moved {command[1]} to {command[2]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "batch_move" and len(command) > 2 and self.config["batch_enabled"]:
                    sources = command[1:-1]
                    dest = command[-1]
                    results = self.file_manager.batch_move(sources, dest, progress=self.config["progress_enabled"])
                    for src, result in results.items():
                        if self.config["color_enabled"]:
                            color = Fore.GREEN if result == "Success" else Fore.RED
                            print(f"{color}{src} -> {dest}: {result}{Style.RESET_ALL}")
                        else:
                            print(f"{src} -> {dest}: {result}")
                elif cmd in ["view", "cat"] and len(command) > 1:
                    result = self.file_manager.read_file(command[1])
                    if isinstance(result, str) and not result.startswith("Error"):
                        if self.config["color_enabled"]:
                            print(f"{Fore.CYAN}\nContents of {command[1]}:{Style.RESET_ALL}\n{result}")
                        else:
                            print(f"\nContents of {command[1]}:\n{result}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "search" and len(command) > 1:
                    recursive = (len(command) > 2 and command[2].lower() == "r") or self.config["search_recursive"]
                    result = self.file_manager.search_files(command[1], recursive)
                    if isinstance(result, list):
                        if self.config["color_enabled"]:
                            print(f"{Fore.YELLOW}\nFound {len(result)} matches:{Style.RESET_ALL}")
                            print("\n".join(f"{Fore.WHITE}{f}{Style.RESET_ALL}" for f in result))
                        else:
                            print(f"\nFound {len(result)} matches:")
                            print("\n".join(result))
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "perms" and len(command) > 1:
                    result = self.file_manager.get_file_permissions(command[1])
                    if isinstance(result, str) and not result.startswith("Error"):
                        if self.config["color_enabled"]:
                            print(f"{Fore.CYAN}\nPermissions for {command[1]}: {result}{Style.RESET_ALL}")
                        else:
                            print(f"\nPermissions for {command[1]}: {result}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "edit" and len(command) > 2:
                    content = " ".join(command[2:])
                    result = self.file_manager.edit_file(command[1], content)
                    if result is True:
                        print(f"{Fore.GREEN}Appended to {command[1]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Appended to {command[1]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "tag" and len(command) > 2 and self.config["tags_enabled"]:
                    result = self.file_manager.add_tag(command[1], command[2])
                    if result is True:
                        print(f"{Fore.GREEN}Tagged {command[1]} with '{command[2]}'{Style.RESET_ALL}" if self.config["color_enabled"] else f"Tagged {command[1]} with '{command[2]}'")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "untag" and len(command) > 2 and self.config["tags_enabled"]:
                    result = self.file_manager.remove_tag(command[1], command[2])
                    if result is True:
                        print(f"{Fore.GREEN}Removed tag '{command[2]}' from {command[1]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Removed tag '{command[2]}' from {command[1]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "tags" and len(command) > 1 and self.config["tags_enabled"]:
                    tags = self.file_manager.get_tags(command[1])
                    if isinstance(tags, list):
                        if self.config["color_enabled"]:
                            print(f"{Fore.CYAN}Tags for {command[1]}: {', '.join(tags) if tags else 'None'}{Style.RESET_ALL}")
                        else:
                            print(f"Tags for {command[1]}: {', '.join(tags) if tags else 'None'}")
                    else:
                        print(f"{Fore.RED}Error: {tags}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {tags}")
                elif cmd == "tagsearch" and len(command) > 1 and self.config["tags_enabled"]:
                    recursive = (len(command) > 2 and command[2].lower() == "r")
                    result = self.file_manager.search_by_tag(command[1], recursive)
                    if isinstance(result, list):
                        if self.config["color_enabled"]:
                            print(f"{Fore.YELLOW}\nFound {len(result)} files with tag '{command[1]}':{Style.RESET_ALL}")
                            print("\n".join(f"{Fore.WHITE}{f}{Style.RESET_ALL}" for f in result))
                        else:
                            print(f"\nFound {len(result)} files with tag '{command[1]}':")
                            print("\n".join(result))
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "compress" and len(command) > 2:
                    result = self.file_manager.compress(command[1], command[2], progress=self.config["progress_enabled"])
                    if result is True:
                        print(f"{Fore.GREEN}Compressed {command[1]} to {command[2]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Compressed {command[1]} to {command[2]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "extract" and len(command) > 1:
                    dest_dir = command[2] if len(command) > 2 else None
                    result = self.file_manager.extract(command[1], dest_dir, progress=self.config["progress_enabled"])
                    if result is True:
                        dest = dest_dir if dest_dir else "current directory"
                        print(f"{Fore.GREEN}Extracted {command[1]} to {dest}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Extracted {command[1]} to {dest}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "history":
                    if self.config["color_enabled"]:
                        for i, (ts, cmd) in enumerate(self.history, 1):
                            print(f"{Fore.MAGENTA}{i}. [{ts}] {cmd}{Style.RESET_ALL}")
                    else:
                        for i, (ts, cmd) in enumerate(self.history, 1):
                            print(f"{i}. [{ts}] {cmd}")
                elif cmd == "exec" and len(command) > 1:
                    try:
                        index = int(command[1]) - 1
                        if 0 <= index < len(self.history):
                            _, old_cmd = self.history[index]
                            if self.config["color_enabled"]:
                                print(f"{Fore.YELLOW}Executing: {old_cmd}{Style.RESET_ALL}")
                            else:
                                print(f"Executing: {old_cmd}")
                            self.history.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), old_cmd))
                            self.trim_history()
                            self.run_command(old_cmd.split())
                        else:
                            print(f"{Fore.RED}Invalid history index{Style.RESET_ALL}" if self.config["color_enabled"] else "Invalid history index")
                    except ValueError:
                        print(f"{Fore.RED}Invalid index - use a number{Style.RESET_ALL}" if self.config["color_enabled"] else "Invalid index - use a number")
                elif cmd == "script" and len(command) > 1:
                    script_path = os.path.join(self.config["script_dir"], command[1])
                    result = run_script(script_path, self)
                    if result is True:
                        print(f"{Fore.GREEN}Executed script: {command[1]}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Executed script: {command[1]}")
                    else:
                        print(f"{Fore.RED}Error: {result}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {result}")
                elif cmd == "help":
                    self.display_help()
                else:
                    if self.config["autocomplete"]:
                        suggestions = suggest_commands(cmd, self.commands + list(self.config["aliases"].keys()))
                        if suggestions:
                            if self.config["color_enabled"]:
                                print(f"{Fore.RED}Unknown command. Did you mean: {', '.join(suggestions)}?{Style.RESET_ALL}")
                            else:
                                print(f"Unknown command. Did you mean: {', '.join(suggestions)}?")
                        else:
                            print(f"{Fore.RED}Unknown command. Type 'help' for available commands{Style.RESET_ALL}" if self.config["color_enabled"] else "Unknown command. Type 'help' for available commands")
                    else:
                        print(f"{Fore.RED}Unknown command. Type 'help' for available commands{Style.RESET_ALL}" if self.config["color_enabled"] else "Unknown command. Type 'help' for available commands")
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}" if self.config["color_enabled"] else f"Error: {str(e)}")

    def run_command(self, command):
        cmd = self.resolve_alias(command[0].lower())
        if cmd in ["dir", "ls"]:
            detailed = len(command) > 1 and command[1].lower() == "detail"
            sort_by = command[2].lower() if len(command) > 2 else self.config["default_sort"]
            min_size = command[3] if len(command) > 3 else self.config["min_size"]
            max_size = command[4] if len(command) > 4 else self.config["max_size"]
            if sort_by not in ["name", "mtime"]:
                sort_by = self.config["default_sort"]
            files = self.file_manager.list_files(detailed, sort_by, min_size, max_size)
            if self.config["color_enabled"]:
                for f in files:
                    if isinstance(f, dict) and f.get("is_dir"):
                        print(f"{Fore.BLUE}{f['name']}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.WHITE}{f}{Style.RESET_ALL}")
            else:
                print("\n".join(str(f) for f in files))