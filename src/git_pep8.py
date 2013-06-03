#!/usr/bin/env python
from src.common import (
    error, info, header,
    sha1_file,
    get_filelist,
    test_for_required_binaries,
    run_command,
    git_commit,
)


BUFSIZE = 16 * 1024 * 1024

# These rules are listed in non-ascending order.
# I think it is better because
ERRORS = [
    ("W391", "blank line at end of file"),
    ("W291", "trailing whitespace"),
    ("W293", "blank line contains whitespace"),
    ("W191", "indentation contains tabs"),
    ("E101", "indentation contains mixed spaces and tabs"),
    ("E111", "Reindent all lines."),

    # Line spacing
    ("E301", "expected 1 blank line, found 0"),
    ("E302", "line spacing between functions and classes"),
    ("E303", "linespacing between functions and classes"),
    ("E304", "Remove blank line following function decorator."),

    # Whitespace
    ("E211", "Remove extraneous whitespace."),
    ("E221", "Fix extraneous whitespace around keywords."),
    ("E222", "Fix extraneous whitespace around keywords."),
    ("E223", "Fix extraneous whitespace around keywords."),
    ("E224", "Remove extraneous whitespace around operator."),
    ("E225", "Fix missing whitespace around operator."),
    ("E226", "Fix missing whitespace around operator."),
    ("E227", "Fix missing whitespace around operator."),
    ("E228", "Fix missing whitespace around operator."),
    ("E231", "Add missing whitespace."),

    ("E261", "whitespace after inline comment"),
    ("E241", "Fix extraneous whitespace around keywords."),
    ("E242", "Remove extraneous whitespace around operator."),
    ("E251", "Remove whitespace around parameter '=' sign."),
    ("E261", "Fix spacing after comment hash."),
    ("E262", "Fix spacing after comment hash."),

    ("E203", "whitespace before colon"),
    ("E201", "whitespace around [ and ]"),
    ("E202", "whitespace around [ and ]"),

    ("E251", "unexpected whitespace around parameter equals"),
    ("E271", "Fix extraneous whitespace around keywords."),
    ("E272", "Fix extraneous whitespace around keywords."),
    ("E273", "Fix extraneous whitespace around keywords."),
    ("E274", "Fix extraneous whitespace around keywords."),

    # Multiple statements
    ("E701", "multiple statements on one line (colon)"),
    ("E702", "Put semicolon-separated compound statement on separate lines."),
    ("E703", "Put semicolon-separated compound statement on separate lines."),

    # Multiple imports
    ("E401", "multiple imports on one line"),

    # ("E501", "Try to make lines fit within --max-line-length characters."),
    ("E502", "the backslash is redundant between brackets"),
    ("W601", ".has_key() is deprecated, use 'in'"),
    ("W602", "Fix deprecated form of raising exception."),
    ("W603", "Replace <> with !=."),
    ("W604", "Replace backticks with repr()."),

    # These require --aggressive be sent to autopep8 command line
    ("E711", "comparison to None should be 'if cond is None:'"),
    ("E712", "comparison to True should be 'if cond is True:' or 'if cond:'"),

    # Never seen this rule applied to code.
    # ("E721", "Switch to use isinstance()."),

    # Indentation
    ("E121", "continuation line indentation is not a multiple of four"),

    # I don't like these rules because autopep8 does not really give good
    # transformations
    ("E122", "Add absent indentation for hanging indentation"),
    ("E123",
     "closing bracket does not match indentation of opening bracket's line"),
    ("E124", "closing bracket does not match visual indentation"),
    ("E125",
     "continuation line does not distinguish itself from next logical line"),
    ("E126", "continuation line over-indented for hanging indent"),
    ("E127", "continuation line over-indented for visual indent"),
    ("E128", "continuation line under-indented for visual indent"),
]


def loop_params(file_list, errors):
    for i, (error_no, error_comment) in enumerate(errors, start=1):
        header("{2} of {3}: {0} {1}".format(
            error_no, error_comment, i, len(errors)))
        for fullpath in file_list:
            yield (fullpath, error_no, error_comment)


def run_autopep8(file_or_directory, ext=".py", recurse=True,
                 dryrun=False, verbose=False, autopep8=None, author=None,
                 errors=None):
    autopep8 = autopep8 or "autopep8"
    file_list = get_filelist(file_or_directory, recurse, ext)
    i = 0
    for fullpath, error_no, error_comment in loop_params(file_list, errors):
        cmd = [autopep8, "--in-place", "--verbose",
               "--select={0}".format(error_no), fullpath]
        if verbose or dryrun:
            info(" ".join(cmd))
        if not dryrun:
            hash_before = sha1_file(fullpath)
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


def run_by_file_only(file_or_directory, ext=".py", recurse=True,
                     dryrun=False, verbose=False, autopep8=None, author=None,
                     errors=None):
    # pylint-defeating assignment...
    errors = errors

    autopep8 = autopep8 or "autopep8"
    file_list = get_filelist(file_or_directory, recurse, ext)
    i = 0
    for fullpath in file_list:
        cmd = [autopep8, "--in-place", "--verbose", fullpath]
        if verbose or dryrun:
            info(" ".join(cmd))
        if not dryrun:
            hash_before = sha1_file(fullpath)
            output = run_command(cmd)
            if hash_before != sha1_file(fullpath):
                # I can't tell if autopep8 has modified a file from the return code,
                # so I do it the hard way...
                info(output)
                git_commit(
                    fullpath,
                    "autopep8 all errors",
                    dryrun, verbose, author)
                i += 1
    info("# {0} files scanned/modified".format(i))


def run_all(file_or_directory, ext=".py", recurse=True,
            dryrun=False, verbose=False, autopep8=None, author=None,
            errors=None):
    # pylint-defeating assignment...
    ext = ext

    autopep8 = autopep8 or "autopep8"
    recurse_opt = ["--recurse"] if recurse else []
    select_opt = ["--select={0}".format(",".join(
        errors))] if errors != ERRORS else []
    options = recurse_opt + select_opt + ["--in-place", "--verbose"]
    cmd = [autopep8] + options + [file_or_directory]

    if verbose or dryrun:
        info(" ".join(cmd))
    if not dryrun:
        output = run_command(cmd)
        info(output)
        git_commit(
            file_or_directory,
            "autopep8 run on all {0}".format(file_or_directory),
            dryrun, verbose, author)


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
    METHODS[0]: run_autopep8,
    METHODS[1]: run_by_file_only,
    METHODS[2]: run_autopep8,
    METHODS[3]: run_all,
}


def option_parser():
    from optparse import OptionParser, make_option

    help_fmt = (
        'Method of traversing errors and files to use with autopep8; '
        'choose from: {0}; '
        'default is {1}'
    )

    option_list = [
        make_option('-r', '--recurse', dest='recurse', action='store_true',
                    default=False, help='Recurse down directories from STARTDIR'),
        make_option('-e', '--ext', dest='extensions', action='store',
                    default=".py", help='Specify file extension to work on'),
        make_option('-d', '--dryrun', dest='dryrun', action='store_true',
                    default=False, help='Do dry run -- do not modify files'),
        make_option('-v', '--verbose', dest='verbose',
                    action='store_true', default=False, help='Verbose output'),
        make_option('-a', '--autopep8', dest='autopep8', action='store',
                    default="autopep8", help='Specify path to autopep8 instance'),
        make_option('-u', '--author', dest='author',
                    action='store', help='Change git author'),
        make_option('-s', '--select', dest='errors', default=None,
                    action='store', help='Select specific errors'),
        make_option('-m', '--method', dest='method',
                    default=METHODS[0],
                    type="choice",
                    choices=METHODS,
                    help=help_fmt.format(", ".join(METHODS), METHODS[0])),
    ]

    return OptionParser(option_list=option_list)


def make_error_list(opt_errors, default_errors):
    d = dict((k, v) for k, v in default_errors)
    return (
        default_errors
        if not opt_errors
        else [(opt_error, d[opt_error]) for opt_error in opt_errors.split(',')]
    )


def main():
    # Parse Command line options
    parser = option_parser()
    (o, args) = parser.parse_args()

    # Test for needed binaries. Exit if missing.
    needed_binaries = [
        "git",
        o.autopep8,
        "pep8"
    ]
    test_for_required_binaries(needed_binaries)

    errors = make_error_list(o.errors, ERRORS)

    # Do the business
    method_fn = METHOD_TABLE.get(o.method)
    if method_fn:
        for arg in (args or ["."]):
            method_fn(
                arg,
                ext=o.extensions, recurse=o.recurse,
                dryrun=o.dryrun, verbose=o.verbose,
                autopep8=o.autopep8,
                author=o.author,
                errors=errors
            )
    else:
        fmt = "'{0}' is not a valid value for --method.  Valid ones are: {1}"
        keys = sorted(METHOD_TABLE.keys())
        error(fmt.format(o.method, ", ".join(keys)))


if __name__ == '__main__':
    main()
