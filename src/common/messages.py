import sys

from termcolor import cprint


def message(msg, fcolor='green', bcolor=None, attrs=None):
    """
    General message printer
    """
    attrs = attrs or []
    cprint(msg, fcolor, bcolor, attrs=attrs, file=sys.stderr)


def error(msg):
    """
    General error printer
    """
    message(msg, fcolor='red', bcolor='on_yellow')


def header(msg):
    """
    General info printer
    """
    message(msg, fcolor='yellow', attrs=["bold"])


def info(msg):
    """
    General info printer
    """
    message(msg, fcolor='green', attrs=["bold"])
