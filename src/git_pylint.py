#!/usr/bin/env python
from src.common import (
    error, info,
    sha1_file,
    get_filelist,
    test_for_required_binaries,
    run_command,
    git_commit,
)


BUFSIZE = 16 * 1024 * 1024

ERRORS = [
    ("LINT1", "Description"),
]


def loop_params(file_list):
    for i, (error_no, error_comment) in enumerate(ERRORS, start=1):
        info("{2} of {3}: {0} {1}".format(
            error_no, error_comment, i, len(ERRORS)))
        for fullpath in file_list:
            hash_before = sha1_file(fullpath)
            yield (fullpath, hash_before, error_no, error_comment)


def run_autopylint(file_or_directory, ext=".py", recurse=True,
                 dryrun=False, verbose=False, author=None):
    file_list = get_filelist(file_or_directory, recurse, ext)
    i = 0
    for fullpath, hash_before, error_no, error_comment in loop_params(file_list):
        cmd = ["autopylint", "--in-place", "--verbose",
               "--select={0}".format(error_no), fullpath]
        if verbose or dryrun:
            info(" ".join(cmd))
        if not dryrun:
            output = run_command(cmd)
            if hash_before != sha1_file(fullpath):
                # I can't tell if autopep8 has modified a file from the return code,
                # so I do it the hard way...
                info(output)
                git_commit(
                    fullpath,
                    "{0} {1}".format(error_no, error_comment),
                    dryrun, verbose, author)
                i += 1
    info("# {0} files scanned/modified".format(i))


METHODS = (
    # Iterate over each file and reason, running autopep8
    "by-file-and-reason",
    # Iterate over each file running autopep8 with all reasons selected
    "by-file-only",
    # Iterate over each reason running autopep8 on all files at once
    "by-reason-only",
    # Run autopep8 only once on all files applying all reasons
    "all",
)


METHOD_TABLE = {
    METHODS[0]: run_autopylint,
    METHODS[1]: run_autopylint,
    METHODS[2]: run_autopylint,
    METHODS[3]: run_autopylint,
}



def option_parser():
    from optparse import OptionParser, make_option

    option_list = [
        make_option('-r', '--recurse', dest='recurse', action='store_true',
                    default=False, help='Recurse down directories from STARTDIR'),
        make_option('-e', '--ext', dest='extensions', action='store',
                    default=".py", help='Specify file extension to work on'),
        make_option('-d', '--dryrun', dest='dryrun', action='store_true',
                    default=False, help='Do dry run -- do not modify files'),
        make_option('-v', '--verbose', dest='verbose',
                    action='store_true', default=False, help='Verbose output'),
        make_option('-u', '--author', dest='author',
                    action='store', help='Change git author'),
        make_option('-m', '--method', dest='method',
                    default=METHODS[0],
                    action='store',
                    help='Method of traversing errors and files to use with autopylint'),
    ]
    return OptionParser(option_list=option_list)


def main():
    # Parse Command line options
    parser = option_parser()
    (o, args) = parser.parse_args()

    # Test for needed binaries. Exit if missing.
    needed_binaries = [
        "git",
        "autopylint",
    ]
    test_for_required_binaries(needed_binaries)

    # Do the business
    method_fn = METHOD_TABLE.get(o.method)
    if method_fn:
        for arg in (args or ["."]):
            method_fn(
                arg,
                ext=o.extensions, recurse=o.recurse,
                dryrun=o.dryrun, verbose=o.verbose,
                author=o.author
            )
    else:
        fmt = "'{0}' is not a valid value for --method.  Valid ones are: {1}"
        keys = sorted(METHOD_TABLE.keys())
        error(fmt.format(o.method, ", ".join(keys)))


if __name__ == '__main__':
    main()

