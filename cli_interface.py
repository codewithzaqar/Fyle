import os
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from utils import suggest_commands, run_script, get_file_completions

class CLIInterface:
    def __init__(self, file_manager, config):
        self.file_manager = file_manager
        self.config = config
        self.running = False
        self.history = [] # (timestamp, command)
        self.commands = [
            "dir", "ls", "cd", "pwd", "del", "rm", 'create', "copy",
            "rename", "mv", "move", "view", "cat", "search", "perms",
            "edit", "history", "help", "exit", "batch_del", "batch_copy",
            "batch_move", "exec", "tag", "untag", "tags", "script", "tagsearch"
        ]
        self.completer = WordCompleter(self.commands + list(self.config["aliases"].keys()), ignore_case=True)
        self.session = PromptSession(completer=self.completer if self.config["completion_enabled"] else None,
                                    complete_while_typing=True)

    def display_help(self):
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
            Type 'help' for commands  v0.11""")
        
        while self.running:
            try:
                command = input(f"\n{self.config['prompt']}").strip().split()
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
                elif cmd == "batch_del" and len(command) > 1 and self.config["batch_enabled"]:
                    results = self.file_manager.batch_delete(command[1:])
                    for fname, result in results.items():
                        print(f"{fname}: {result}")
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
                elif cmd == "batch_copy" and len(command) > 2 and self.config["batch_enabled"]:
                    sources = command[1:-1]
                    dest = command[-1]
                    results = self.file_manager.batch_copy(sources, dest)
                    for src, result in results.items():
                        print(f"{src} -> {dest}: {result}")
                elif cmd in ["rename", "mv"] and len(command) > 2:
                    result = self.file_manager.rename_file(command[1], command[2])
                    if result is True:
                        print(f"Renamed {command[1]} to {command[2]}")
                    else:
                        print(f"Error: {result}")
                elif cmd == "move" and len(command) > 2:
                    result = self.file_manager.move_file(command[1], command[2])
                    if result is True:
                        print(f"Moved {command[1]} to {command[2]}")
                    else:
                        print(f"Error: {result}")
                elif cmd == "batch_move" and len(command) > 2 and self.config["batch_enabled"]:
                    sources = command[1:-1]
                    dest = command[-1]
                    results = self.file_manager.batch_move(sources, dest)
                    for src, result in results.items():
                        print(f"{src} -> {dest}: {result}")
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
                elif cmd == "tag" and len(command) > 2 and self.config["tags_enabled"]:
                    result = self.file_manager.add_tag(command[1], command[2])
                    if result is True:
                        print(f"Tagged {command[1]} with '{command[2]}'")
                    else:
                        print(f"Error: {result}")
                elif cmd == "untag" and len(command) > 2 and self.config["tags_enabled"]:
                    result = self.file_manager.remove_tag(command[1], command[2])
                    if result is True:
                        print(f"Removed tag '{command[2]}' from {command[1]}")
                    else:
                        print(f"Error: {result}")
                elif cmd == "tags" and len(command) > 1 and self.config["tags_enabled"]:
                    tags = self.file_manager.get_tags(command[1])
                    if isinstance(tags, list):
                        print(f"Tags for {command[1]}: {', '.join(tags) if tags else 'None'}")
                    else:
                        print(f"Error: {tags}")
                elif cmd == "tagsearch" and len(command) > 1 and self.config["tags_enabled"]:
                    recursive = (len(command) > 2 and command[2].lower() == "r")
                    result = self.file_manager.search_by_tag(command[1], recursive)
                    if isinstance(result, list):
                        print(f"\nFound {len(result)} files with tag '{command[1]}':")
                        print("\n".join(result))
                    else:
                        print(f"Error: {result}")
                elif cmd == "history":
                    for i, (ts, cmd) in enumerate(self.history, 1):
                        print(f"{i}. [{ts}] {cmd}")
                elif cmd == "exec" and len(command) > 1:
                    try:
                        index = int(command[1]) - 1
                        if 0 <= index < len(self.history):
                            _, old_cmd = self.history[index]
                            print(f"Executing: {old_cmd}")
                            self.history.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), old_cmd))
                            self.trim_history()
                            self.run_command(old_cmd.split())
                        else:
                            print("Invalid history index")
                    except ValueError:
                        print("Invalid index - use a number")
                elif cmd == "script" and len(command) > 1:
                    script_path = os.path.join(self.config["script_dir"], command[1])
                    result = run_script(script_path, self)
                    if result is True:
                        print(f"Executed script: {command[1]}")
                    else:
                        print(f"Error: {result}")
                elif cmd == "help":
                    self.display_help()
                else:
                    if self.config["autocomplete"]:
                        suggestions = suggest_commands(cmd, self.commands + list(self.config["aliases"].keys()))
                        if suggestions:
                            print(f"Unknown command. Did you mean: {', '.join(suggestions)}?")
                        else:
                            print("Unknown command. Type 'help' for available commands")
                    else:
                        print("Unknown command. Type 'help' for available commands")
            except Exception as e:
                print(f"Error: {str(e)}")

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
            print("\n".join(str(f) for f in files))