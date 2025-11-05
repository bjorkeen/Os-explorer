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