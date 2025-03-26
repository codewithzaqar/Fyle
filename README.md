# Fyle

A simple command-line interface for basic file system operations with advanced features.

## Features
- List files with sorting and size filtering
- Change directory (cd)
- Show current path (pwd)
- Delete files or directories (del/rm)
- Create empty files (create)
- Copy files or directories (copy)
- Rename files or directories (rename/mv)
- Move files or directories (move)
- View file contents (view/cat, first 1KB)
- Search files (search, optional recursive)
- View file permissions (perms)
- Edit files (append text)
- Command history with timestamps
- Error logging (logs/cli.log)
- Configuration file support (config.json)
- Command aliases
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
- `create <name>`: Create new empty file
- `copy <source> <dest>`: Copy file or directory
- `rename` or `mv <old> <new>`: Rename file or directory
- `move <source> <dest>`: Move file or directory
- `view` or `cat <name>`: View file contents (first 1KB)
- `search <pattern> [r]`: Search files (add 'r' for recursive)
- `perms <name>`: View file permissions (Unix-style)
- `edit <name> <content>`: Append text to file
- `history`: Show command history with timestamps
- `help`: Display help
- `exit`: Quit program