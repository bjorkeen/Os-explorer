"""
OS EXPLORER

The modules that we will use:
- os: file system actions (lists,stat,walk,remove,rename)
- argparse: command line argument subcommands
- sys: for exit codes and error printing
- time: for timestamp formatting
"""

import os
import argparse
import sys
import time

TRASH_NAME = ".trash" #folder that we will manage ourselves for deleted files
MANIFEST_NAME = "manifest.tsv" #file that will keep track of all deleted files


"""
Creating the CLI parser and subparsers for each command, which will make the program discoverable and easy to test.
"""

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = "os_explorer",
        description = "A simple OS file explorer with trash management."
    )   
    sub = parser.add_subparsers(dest="cmd", required=True)

    #list
    p = sub.add_parser("list", help="List directory entries") 
    p.add_argument("path", type=str, help="Path to list")
    p.add_argument("-a", "--all", action="store_true", help="Include hidden files (names starting with .)")
    p.set_defaults(func=cmd_list)

    #info
    p = sub.add_parser("info", help = "Show basic info about a file or directory")
    p.add_argument("path", type=str, help="file or directory path")
    p.set_defaults(func=cmd_info)

    #tree
    p = sub.add_parser("tree", help="Print a simple directory tree")
    p.add_argument("path", type=str, help="Root directory path")
    p.set_defaults(func=cmd_tree)

    #search
    p = sub.add_parser("search", help="Find files whose names contain a given substring")
    p.add_argument("path", type=str, help="Where to start searching")
    p.add_argument("name_substring", type=str, help="Substring to search for in file names")
    p.set_defaults(func=cmd_search)

    #rm (delete) 
    p = sub.add_parser("rm", help="Delete a file or directory (moves to trash)")
    p.add_argument("path", type=str, help="file or directory path to move to trash")
    p.add_argument("--root", type=str, default=".", help="Root directory where the .trash folder is located (default: current directory)")
    p.set_defaults(func=cmd_rm)

    #restore 
    p = sub.add_parser("restore", help="Restore a file or directory from trash")
    p.add_argument("name", type=str, help="Name of the file or directory to restore from trash")
    p.add_argument("--root", type=str, default=".", help="where the .trash lives (default: current working dir)")
    p.set_defaults(func=cmd_restore)

    #du (disk usage)
    p = sub.add_parser("du", help="Show disk usage (bytes) of a file or directory")
    p.add_argument("path", type=str, help="file or directory path")
    p.add_argument("-a", "--all", action="store_true", help="Show disk usage for all files and subdirectories")
    p.set_defaults(func=cmd_du) 

    return parser

"""
Directory Listing Command (list)

This Python function, cmd_list, acts like a simplified version of the Unix ls command. 
It lists the contents of a directory specified by the user through command-line arguments. 
The code first checks if the given path is a valid directory, printing an error and exiting if not. 
It then retrieves and alphabetically sorts all entries in the directory (ignoring case). 
Unless the --all flag is provided, hidden files (those starting with a dot) are skipped. 
For each visible entry, the code prints its name, appending a slash (/) to directories for easy identification. 
It also handles permission errors gracefully, displaying a clear message if access is denied.
Overall, the function is a clean, beginner-friendly example of working with the os and argparse modules for basic filesystem operations.

"""

def cmd_list(args: argparse.Namespace) -> int: # exit code
    path = args.path # directory to list
    show_hidden = args.all # whether to show hidden files

    if not os.path.isdir(path): # check if path is a directory
        print(f"Error: {path} is not a directory", file=sys.stderr) # directory check error
        return 1 # exit code for error
    
    try: # list directory contents
        for name in sorted(os.listdir(path), key=str.lower): # sort entries case-insensitively
            if not show_hidden and name.startswith('.'): # skip hidden files if not showing
                continue

            full = os.path.join(path, name) # full path

            suffix = '/' if os.path.isdir(full) else "" # appends '/' after directory names to visually distinguish them
            print(name + suffix)
        return 0
    
    # If the program cannot read the directory (no permissions), it handles the exception and returns error code 1
    except PermissionError: # handle permission errors
        print(f"Error: Permission denied to access {path}", file=sys.stderr) # permission error message
        return 1 # Permission error exit code




"""
File/dir info (info)

This Python script defines two functions that work together to display detailed information about a file or directory.
The first function, human_bytes, converts a file size given in bytes into a more readable format (like KB, MB, GB, or TB), rounding the result to one decimal place. 
It does this by dividing the size by 1024 until it fits within a suitable unit.
The second function, cmd_info, retrieves and prints key details about a specified file or directory using command-line arguments.
It first checks whether the path exists, then uses os.stat() to obtain metadata such as size, type (file or directory), and timestamps for creation, last modification, and last access. 
The size is displayed both in bytes and in human-readable form using human_bytes. 
So, this code provides a clear and user-friendly way to inspect file system information while demonstrating the use of the os, sys, time, and argparse modules.

"""

def human_bytes(n:int) -> str: # converts bytes to human-readable format
        units = ['B', 'KB', 'MB', 'GB', 'TB'] # size units
        size = float(n) # initial size in bytes
        for u in units: # iterate through units
            if size < 1024.0 or u == units[-1]:
                return f"{size:.1f} {u}"
            size /= 1024.0

def cmd_info(args: argparse.Namespace) -> int: # exit code
        path = args.path

        if not os.path.exists(path): # check if path exists
            print(f"Error: {path} does not exist", file=sys.stderr)
            return 1
        st = os.stat(path) # get file/directory stats
        kind = "Directory" if os.path.isdir(path) else "File" # determine type
        print(f"Absolute Path: {os.path.abspath(path)}") # check absolute path
        print(f"Type: {kind}")
        print(f"Size: {human_bytes(st.st_size)} ({st.st_size} bytes)")
        print(f"Last Modified: {time.ctime(st.st_mtime)}")
        print(f"Last Accessed: {time.ctime(st.st_atime)}")
        print(f"Created: {time.ctime(st.st_ctime)}")
        return 0

"""
Directory tree (tree)

This Python function, cmd_tree, displays the directory structure of a given path in a tree-like format, similar to the Unix tree command.
It begins by checking whether the provided path exists, printing an error if not.
Inside the function, a nested helper function walk is defined to recursively explore subdirectories.
It uses os.scandir() to efficiently iterate through entries in each folder, sorting them alphabetically in a case-insensitive manner.
Each level of the tree is indented for clarity, and a forward slash (/) is added after directory names. If access to a folder is denied, the code prints a <permission denied> message instead of crashing.
Also, the main part of the function prints the base directory (or file name if it’s a single file) and calls walk to display all nested contents.

"""


def cmd_tree(args: argparse.Namespace) -> int: 
    root = args.path

    if not os.path.exists(root): 
        print(f"Error: {root} does not exist", file=sys.stderr)
        return 1
    
    def walk (path: str, depth: int) -> None: # recursive directory walk
        try: 
             with os.scandir(path) as it: # scan directory entries
                for entry in sorted(it, key=lambda e: e.name.lower()): # sort entries case-insensitively
                    indent = "   " * depth # indentation based on depth
                    suffix = "/" if entry.is_dir() else "" # append '/' for directories
                    print(f"{indent}{entry.name}{suffix}") 
                    if entry.is_dir: # recurse into subdirectory
                        walk(entry.path, depth + 1 )
        except PermissionError: # handle permission errors
            indent = "   " * depth # indentation based on depth
            print(f"{indent}[Permission Denied]")
    
    #print the root name (folder) or the file itself
    base = os.path.basename(os.path.abspath(root))
    if os.path.isdir(root):
        print(base)
    else:
        print(base + "/")
        walk(root, 1)
    return 0


"""
Search by name substring (search)

cmd_search, allows users to search for files within a given directory and its subdirectories based on a partial name match
It begins by checking whether the specified root path exists, displaying an error message if not.
The function then uses os.walk() to recursively traverse the directory tree, examining each file name.
If the lowercase version of the file name contains the provided search substring (needle), it constructs the file’s full path and retrieves its size using os.stat().
Matching files are printed along with their sizes in bytes.
If a file disappears during the search (causing a FileNotFoundError), the function safely skips it.

"""

def cmd_search(args: argparse.Namespace) -> int: 
    root = args.path # root directory to start search
    needle = args.name_substring.lower() # case-insensitive search
    if not os.path.exists(root): 
        print(f"Error: not found: {root}", file=sys.stderr)
        return 1

    for dirpath, dirnames, filenames in os.walk(root): # walk the directory tree
        for name in filenames:
            if needle in name.lower(): # check for substring match
                full = os.path.join(dirpath, name) 
                try:
                    size = os.stat(full).st_size # get file size
                except FileNotFoundError:
                    continue
                print(f"{full}\t{size} bytes")
    return 0



"""
Safe delete (rm) - .trash + manifest and restore

This set of functions implements a simple “trash” system with restore.
ensure_trash(root) creates a hidden .trash folder (named by TRASH_NAME) under root and a manifest file (named by MANIFEST_NAME) if they don’t exist, writing a header line once.
cmd_rm acts like a safe delete: it validates the target path, figures out the trash location under args.root (or the current working directory), builds a timestamped name (<epoch>__<basename>), moves the file into .trash with os.rename (fast on the same filesystem), and appends a tab-separated record to the manifest: epoch, trashed path, and original absolute path.
cmd_restore scans the manifest from newest to oldest, looking for an entry whose original path ends with the user-provided name;
if the original location is already occupied, it appends _restored (preserving the extension) to avoid overwriting, then moves the trashed file back.
Throughout, errors (missing paths, missing trashed file, permission or rename issues) are handled with clear messages, making the workflow robust and reversible.

"""

def ensure_trash(root: str) -> str: # ensure .trash and manifest exist
    trash = os.path.join(root, TRASH_NAME) #path to .trash folder
    if not os.path.exists(trash):
        os.makedirs(trash, exist_ok=True) # create .trash directory
    manifest = os.path.join(trash, MANIFEST_NAME) #path to manifest file
    if not os.path.exists(manifest): # create manifest file with header
        with open(manifest, 'a', encoding='utf-8') as f:
            f.write("# epoch\ttrashed_path\toriginal_abs_path\n") 
    return trash # return path to .trash folder

def cmd_rm(args: argparse.Namespace) -> int: # safe delete (move to trash)
    target = args.path
    if not os.path.exists(target):
        print(f"Error: not found: {target}", file=sys.stderr)
        return 1
    
    root = os.path.abspath(args.root or os.getcwd()) # root for .trash
    trash = ensure_trash(root) # ensure .trash exists

    epoch = int(time.time()) # current timestamp
    base = os.path.basename(target.rstrip(os.sep)) # base name of target
    trashed_name = f"{epoch}_{base}"
    dst = os.path.join(trash, trashed_name) # destination in .trash

    try:
        #os.rename moves files across the same filesystem; simple and fast
        os.rename(target, dst)
    except Exception as e:
        print(f"Error: could not move to trash: {e}", file=sys.stderr)
        return 1
    manifest = os.path.join(trash, MANIFEST_NAME) 
    with open(manifest, 'a', encoding='utf-8') as f:
        f.write(f"{epoch}\t{trashed_name}\t{os.path.abspath(target)}\n") # log to manifest

    print(f"Moved to trash: {dst}")
    return 0 

def cmd_restore(args: argparse.Namespace) -> int:  # restore from trash
    root = os.path.abspath(args.root or os.getcwd())
    trash = ensure_trash(root)
    manifest = os.path.join(trash, MANIFEST_NAME)

    if not os.path.exists(manifest):
        print("Nothing to restore.")
        return 0

    name_tail = args.name  # filename only (what the user remembers)
    lines = []
    with open(manifest, "r", encoding="utf-8") as f:
        for ln in f:
            if ln.strip() and not ln.startswith("#"):
                lines.append(ln.strip())

    # Search from the end (newest first)
    for idx in range(len(lines) - 1, -1, -1):
        parts = lines[idx].split("\t", 2)  # exactly 3 fields
        if len(parts) != 3:
            continue
        epoch_s, trashed_path, original_path = parts

        if original_path.endswith(os.sep + name_tail) or os.path.basename(original_path) == name_tail:
            # If the original path is occupied, append _restored to avoid overwriting
            dest = original_path
            if os.path.exists(dest):
                head, tail = os.path.split(dest)
                name, ext = os.path.splitext(tail)
                dest = os.path.join(head, f"{name}_restored{ext}")

            # Support older manifest entries that only stored a filename (relative)
            if not os.path.isabs(trashed_path):
                candidate = os.path.join(trash, trashed_path)
                if os.path.exists(candidate):
                    trashed_path = candidate

            # If the trashed path doesn't actually exist, bail with a clear message
            if not os.path.exists(trashed_path):
                print(f"Sorry, the trashed file is missing:\n  {trashed_path}", file=sys.stderr)
                return 1

            try:
                os.rename(trashed_path, dest)
            except Exception as e:
                print(f"Error during restore: {e}", file=sys.stderr)
                return 1

            print(f"Restored to: {dest}")
            return 0

    print(f"No trashed item ending with '{name_tail}' found.")
    return 0


"""
Disk usage (du)
"""

def dir_size_bytes(path: str) -> int: # calculate total size of directory
    total = 0 
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            full = os.path.join(dirpath, name)
            try:
                total += os.stat(full).st_size
            except FileNotFoundError:
                pass
            except PermissionError:
                pass
    return total

def cmd_du(args: argparse.Namespace) -> int: # disk usage
    path = args.path
    include_hidden = args.all

    if not os.path.exists(path): #if path does not exist
        print(f"Error: not found: {path}", file=sys.stderr)
        return 1

    if os.path.isfile(path): #if single file, just show its size
        size = os.stat(path).st_size
        print(f"{human_bytes(size)}\t{size} bytes\t{path}")
        return 0
    try:
        items = sorted(os.listdir(path), key=str.lower)
    except PermissionError:
        print("Error: Permission denied to access", file=sys.stderr)
        return 1

    rows = [] #list of (size, path) tuples
    for name in items: # iterate directory entries
        if not include_hidden and name.startswith('.'): # skip hidden files if not showing
            continue
        full = os.path.join(path, name) 
        if os.path.isfile(full):
            sz = dir_size_bytes(full) # get file size
        else:
            try:
                sz = os.stat(full).st_size # get directory size
            except (FileNotFoundError, PermissionError): 
                sz = 0
        rows.append((sz, full)) # append size and path

    for sz, full in sorted(rows, key=lambda t: t[0], reverse=True):
        print(f"{full}\t{sz} ({human_bytes(sz)})")

    grand = dir_size_bytes(path)
    print(f"TOTAL\t{grand} ({human_bytes(grand)})")
    return 0 



"""
Main
"""


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)  
    return args.func(args) 

if __name__ == "__main__":
    sys.exit(main())
