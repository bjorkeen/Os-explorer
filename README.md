# Os-explorer

# Project for ESSD

Notion page: https://www.notion.so/OS-Explorer-Exploring-Python-s-OS-Module-2ae1628208e88039b3b5c36a3912392f?source=copy_link

A program written in Python to explore files and folders using only the os module.

It lets you:

- list and inspect files
- print directory trees
- search for files by name
- move files safely to a “trash” instead of deleting them
- restore them later
- check how much disk space folders use

### Features:

- list --> List the files in a directory (optionally include hidden files)
- info --> Show size and timestamps for a file or folder
- tree --> Print a simple directory tree
- search --> Find files by name substring (case-insensitive)
- rm --> Safe delete, move to a hidden .trash folder instead of deleting
- restore --> Restore the most recently trashed file by name
- du --> Show disk usage for a file or for all items in a directory

### Get the code

- either cloned from GitHub

```
git clone https://github.com/bjorkeen/os-explorer.git
cd os-explorer
```

### Folder structure

```
os-explorer/
├── README.md
└── src/
    └── os_explorer.py
```

### Running the program

All commands follow this pattern:

```
python3 -m src.os_explorer <command> [arguments]
```

### Examples

See all available commands:

```
python3 -m src.os_explorer --help
```

List files in the current folder:

```
python3 -m src.os_explorer list .
```

Add -a to include hidden files:

```
python3 -m src.os_explorer list -a .
```

Show file or directory info:

```
python3 -m src.os_explorer info src/os_explorer.py
```

Print a directory tree:

```
python3 -m src.os_explorer tree .
```

Search for files by name substring (case-insensitive):

```
python3 -m src.os_explorer search . py
```

Safe delete (move to .trash)

- Create a test file first:

```
echo "hello" > test.txt
```

Then run:

```
python3 -m src.os_explorer rm test.txt
```

You will see:

```
Moved to trash: /.../.trash/1730839825__test.txt
```

Restore the most recent trashed file:

```
python3 -m src.os_explorer restore test.txt
```

Check disk usage:

```
python3 -m src.os_explorer du .
```

#### Trash Details

When you use `rm`, the file is not permanently deleted.
It is moved to a hidden `.trash` folder in the project directory:

```
.trash/
├── 1730839825__test.txt
└── manifest.tsv

```

`manifest.tsv` keeps a record of each “deleted” item with its timestamp and original location.

The `restore` command reads this file and moves the most recent match back to its original spot (or appends `_restored` if that name is taken).
