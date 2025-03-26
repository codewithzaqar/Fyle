# Fyle

A simple command-line interface for basic file system operations with advanced features.

## Features
- List files with sorting and size filtering
- Change directory (cd)
- Show current path (pwd)
- Delete files or directories (del/rm)
- Batch delete files (batch_del)
- Create empty files (create)
- Copy files or directories (copy)
- Batch copy files (batch_copy)
- Rename files or directories (rename/mv)
- Move files or directories (move)
- Batch move files (batch_move)
- View file contents (view/cat, first 1KB)
- Search files (search, optional recursive)
- View file permissions (perms)
- Edit files (append text)
- Command history with timestamps
- Execute commands from history (exec)
- Error logging (logs/cli.log)
- Configuration file support (config.json)
- Command aliases
- Autocomplete suggestions
- Help system

## Requirements
- Python 3.x

## Usage
1. Configure settings in `config.json` (optional)
2. Run `python main.py` from the command line
3. Type commands at the prompt
4. Type 'exit' to quit
5. Check `logs/cli.log` for operation history

## Available Commands
- `dir` or `ls [detail] [sort] [min_size] [max_size]`: List files (sort: name/mtime, size in bytes/k/m/g)
- `cd <path>`: Change directory
- `pwd`: Show current directory
- `del` or `rm <name>`: Delete file or directory
- `batch_del <name1> <name2> ...`: Batch delete files
- `create <name>`: Create new empty file
- `copy <source> <dest>`: Copy file or directory
- `batch_copy <source1> <source2> ... <dest>`: Batch copy files to destination
- `rename` or `mv <old> <new>`: Rename file or directory
- `move <source> <dest>`: Move file or directory
- `batch_move <source1> <source2> ... <dest>`: Batch move files to destination
- `view` or `cat <name>`: View file contents (first 1KB)
- `search <pattern> [r]`: Search files (add 'r' for recursive)
- `perms <name>`: View file permissions (Unix-style)
- `edit <name> <content>`: Append text to file
- `history`: Show command history with timestamps
- `exec <number>`: Execute command from history by number
- `help`: Display help
- `exit`: Quit program