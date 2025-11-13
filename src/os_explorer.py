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
    p.sub.add_parser("search", help="Find files whose names contain a given substring")
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
    