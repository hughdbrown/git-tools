#!/usr/bin/env python

from setuptools import setup

def reqs_from_file(filename):
    with open(filename) as f:
        lineiter = (line.rstrip() for line in f)
        return filter(None, lineiter)


setup(
    name = 'git-tools',
    version = '0.1',
    description = 'git tools',

    # Required packages
    install_requires = reqs_from_file('requirements.txt'),
    tests_require = reqs_from_file('test-requirements.txt'),

    # Main packages
    packages = [
        'git-tools'
    ],

    # Command line scripts
    scripts = [
        'bin/git-pep8',
    ],
)
