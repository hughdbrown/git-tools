"""
Shared functions for git-tools
"""
from __future__ import print_function

from hashlib import sha1
import sys
import os
import os.path
from subprocess import Popen, PIPE, STDOUT
import re


from src.common.messages import (
    error, info, message, header
)


BUFSIZE = 16 * 1024 * 1024


def binary_in_path(binary):
    # Get unique list of path components
    paths = set(os.environ["PATH"].split(':'))
    # Join binary onto path component
    path_iter = (os.path.join(path, binary) for path in paths)
    # Expand any ~ and environment variables
    expanded_path_iter = (
        os.path.expandvars(os.path.expanduser(p))
        for p in path_iter
    )
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
            error("\t{0}: {1}".format(
                binary, "Found" if found_binary else "Not found"))
        sys.exit(1)


def sha1_file(filename):
    """
    Generate the sha1 hash for a file
    """
    with open(filename) as f:
        return sha1(f.read()).hexdigest()


def git_commit(fullpath, comment, dryrun, verbose, author=None, eat_errors=False):
    """
    Execute git-commit command
    """
    add_cmd = ["git", "add", fullpath]
    commit_cmd = ["git", "commit", "-m",
                  "'{0}: {1}'".format(fullpath, comment)]
    if author:
        commit_cmd += ["--author", author]

    if dryrun or verbose:
        message(" ".join(add_cmd), 'blue')
        message(" ".join(commit_cmd), 'blue')
    if not dryrun:
        for cmd in (add_cmd, commit_cmd):
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=BUFSIZE)
            _, errors = p.communicate()
            if p.returncode and not eat_errors:
                error("Error in {0}".format(fullpath))
                raise Exception(errors)


def get_filelist(file_or_directory, recurse, ext='.py'):
    """
    Generate list of files, optionally recursive, optionally filtered on extension
    """

    egg_re = re.compile(r"^.*\.egg$")

    def is_egg_dir(dirname):
        return egg_re.match(dirname)

    if os.path.isfile(file_or_directory):
        file_list = [file_or_directory]
    elif recurse:
        file_list = [
            os.path.join(root, f)
            for root, _, files in os.walk(file_or_directory)
            for f in files
        ]
    else:
        file_list = [
            os.path.join(file_or_directory, filename)
            for filename in os.listdir(file_or_directory)
        ]

    # Filter out files that do not match on file extension
    ext_filter = (
        path for path in file_list
        if ext is None or os.path.splitext(path)[1] == ext
    )

    # Filter out directories that are egg directories
    # Unlikely that they are part of the git repo
    egg_filter = (
        path for path in ext_filter
        if not any(is_egg_dir(p) for p in path.split("/"))
    )

    return list(egg_filter)


def run_command(cmd):
    message(" ".join(cmd), 'blue')
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=BUFSIZE)
    output, errors = p.communicate()
    if p.returncode:
        raise Exception(errors)
    else:
        return output


__all__ = [
    "message", "info", "error", "header",
    "sha1_file",
    "test_for_required_binaries",
    "git_commit",
    "get_filelist",
    "run_command",
]
