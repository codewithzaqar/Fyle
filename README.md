# Fyle

A simple command-line interface for basic file system operations with advanced features.

## Features
- List files with optional detailed view (`dir/ls` [detail])
- Change directory (`cd`)
- Show current path (`pwd`)
- Delete files or directories (`del/rm`)
- Create empty files (`create`)
- Copy files or directories (`copy`)
- Rename files or directories (`rename`)
- View file contents (`view`, first 1KB)
- Search files (`search`, optional recursive)
- View file permissions (`perms`)
- Command history
- Error logging (`logs/cli.log`)
- Configuration file support (`config.json`)
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
- `dir` or `ls [detail]`: List files (add 'detail' for more info)
- `cd <path>`: Change directory
- `pwd`: Show current directory
- `del` or `rm <name>`: Delete file or directory
- `create <name>`: Create new empty file
- `copy <source> <dest>`: Copy file or directory
- `rename <old> <new>`: Rename file or directory
- `view <name>`: View file contents (first 1KB)
- `search <pattern> [r]`: Search files (add 'r' for recursive)
- `perms <name>`: View file permissions (Unix-style)
- `history`: Show command history
- `help`: Display help
- `exit`: Quit program