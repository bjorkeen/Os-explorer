# Os-explorer

Project for ESSD Masters

A program written in Python to explore files and folders using only the os module.

It lets you:
*list and inspect files
*print directory trees
*search for files by name
*move files safely to a “trash” instead of deleting them
*restore them later
*check how much disk space folders use

Features:

- list --> List the files in a directory (optionally include hidden files)
- info --> Show size and timestamps for a file or folder
- tree --> Print a simple directory tree
- search --> Find files by name substring (case-insensitive)
- rm --> Safe delete, move to a hidden .trash folder instead of deleting
- restore --> Restore the most recently trashed file by name
- du --> Show disk usage for a file or for all items in a directory

Get the code

- either cloned from GitHub

```
git clone https://github.com/bjorkeen/os-explorer.git
cd os-explorer
```
