<img src="public/fylebanner.jpg">

# Fyle
A command-line interface for file system operations with advanced features.

## Features
- List files with sorting and size filtering
- Change directory (cd)
- Show current path (pwd)
- Delete files or directories (del/rm)
- Batch delete files (batch_del) with progress
- Create empty files (create)
- Copy files or directories (copy)
- Batch copy files (batch_copy) with progress
- Rename files or directories (rename/mv)
- Move files or directories (move)
- Batch move files (batch_move) with progress
- View file contents (view/cat, first 1KB)
- Search files (search, optional recursive)
- View file permissions (perms)
- Edit files (append text)
- Tag files (tag/untag/tags)
- Search files by tag (tagsearch)
- Compress files/directories to zip (compress) with progress
- Extract zip files (extract) with progress
- Command history with timestamps and limit
- Execute commands from history (exec)
- Run command scripts (script)
- Set variables for scripts (set)
- Tab completion for commands and file names
- Color output for better readability
- Progress indicators for batch and compression operations
- Error logging (logs/cli.log)
- Configuration file support (config.json)
- Command aliases
- Autocomplete suggestions
- Help system

## Requirements
- Python 3.x
- `prompt_toolkit` (install with `pip install prompt_toolkit`)
- `colorama` (install with `pip install colorama`)
- `tqdm` (install with `pip install tqdm`)

## Usage
1. Configure settings in `config.json` (optional)
2. Create a `scripts` directory for script files (optional)
3. Run `python main.py` from the command line
4. Type commands at the prompt (use Tab for completion)
5. Type 'exit' to quit
6. Check `logs/cli.log` for operation history
7. Tags stored in `tags.json`

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
- `tag <name> <tag>`: Add tag to file
- `untag <name> <tag>`: Remove tag from file
- `tags <name>`: Show tags for file
- `tagsearch <tag> [r]`: Search files by tag (r for recursive)
- `compress <source> <zip_name>`: Compress file or directory to zip
- `extract <zip_name> [dest_dir]`: Extract zip to directory (default: current dir)
- `set <var> <value>`: Set a variable for use in scripts (e.g., set dest /path)
- `hash <name> [algo]`: Compute file hash (algo: sha256/md5, default sha256)
- `history`: Show command history with timestamps
- `exec <number>`: Execute command from history by number
- `script <filename>`: Run commands from script file in script_dir
- `help`: Display help
- `exit`: Quit program

## Configuration
Edit `config.json` to customize:
- `version`: Version number
- `prompt`: Command prompt text
- `max_history`: Maximum history entries
- `search_recursive`: Default recursive search behavior
- `default_sort`: Default file listing sort (name/mtime)
- `min_size`: Minimum file size filter (bytes or with k/m/g)
- `max_size`: Maximum file size filter (null or bytes with k/m/g)
- `autocomplete`: Enable command suggestions (true/false)
- `completion_enabled`: Enable tab completion (true/false)
- `color_enabled`: Enable color output (true/false)
- `progress_enabled`: Enable progress indicators (true/false)
- `variables_enabled`: Enable variables in scripts (true/false)
- `log_level`: Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- `batch_enabled`: Enable batch operations (true/false)
- `tags_enabled`: Enable tagging (true/false)
- `script_dir`: Directory for script file
- `aliases`: Command aliases dictionary