"""
Shared functions for git-tools
"""
from __future__ import print_function

from hashlib import sha1
import sys
import os
import os.path
from subprocess import Popen, PIPE
import re

from termcolor import cprint


BUFSIZE = 16 * 1024 * 1024


def message(msg, fcolor='green', bcolor=None):
    """
    General message printer
    """
    cprint(msg, fcolor, bcolor, file=sys.stderr)


def error(msg):
    """
    General error printer
    """
    message(msg, fcolor='red', bcolor='on_yellow')


def info(msg):
    """
    General info printer
    """
    message(msg, fcolor='green')


def binary_in_path(binary):
    # Get unique list of path components
    paths = set(os.environ["PATH"].split(':'))
    # Join binary onto path component
    path_iter = (os.path.join(path, binary) for path in paths)
    # Expand any ~ and environment variables
    expanded_path_iter = (os.path.expandvars(os.path.expanduser(p)) for p in path_iter)
    # See if any of these possible files exists
    return any(os.path.exists(p) for p in expanded_path_iter)


def test_for_required_binaries(needed_binaries):
    """
    Find out which binaries can be found on disk
    Issue a message and abort if any was not found
    """
    found = [(binary, binary_in_path(binary)) for binary in needed_binaries]
    if not all(found_binary for _, found_binary in found):
        error("Certain additional binaries are required to run:")
        for binary, found_binary in found:
            error("\t{0}: {1}".format(binary, "Found" if found_binary else "Not found"))
        sys.exit(1)


def sha1_file(filename):
    """
    Generate the sha1 hash for a file
    """
    with open(filename) as f:
        return sha1(f.read()).hexdigest()


def git_commit(fullpath, comment, dryrun, verbose, author=None):
    """
    Execute git-commit command
    """
    cmd = ["git", "commit", fullpath, "-m", "{0}: {1}".format(fullpath, comment)]
    if author:
        cmd += ["--author", author]

    if dryrun or verbose:
        message(" ".join(cmd), 'blue')
    if not dryrun:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=BUFSIZE)
        _, errors = p.communicate()
        if p.returncode:
            error("Error in {0}".format(fullpath), 'red')
            raise Exception(errors)


def get_filelist(start_dir, recurse, ext=None):
    """
    Generate list of files, optionally recursive, optionally filtered on extension
    """

    egg_re = re.compile(r"^.*\.egg$")

    def is_egg_dir(dirname):
        return egg_re.match(dirname)

    if recurse:
        file_list = [
            os.path.join(root, f)
            for root, _, files in os.walk(start_dir)
            for f in files
        ]
    else:
        file_list = [os.path.join(start_dir, filename) for filename in os.listdir(start_dir)]

    return file_list if not ext else \
        [
            path for path in file_list
            if os.path.splitext(path)[1] == ext
            if not any(is_egg_dir(p) for p in path.split("/"))
        ]


__all__ = [
    "message", "info", "error",
    "sha1_file",
    "test_for_required_binaries",
    "git_commit",
    "get_filelist",
]
