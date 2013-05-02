#!/usr/bin/env python

from setuptools import setup


def reqs_from_file(filename):
    with open(filename) as f:
        lineiter = (line.rstrip() for line in f if not line.startswith("#"))
        return list(filter(None, lineiter))


setup(
    name='git-tools',
    version='0.1.3',
    description='Suite of tools for working with git repositories',
    author='Hugh Brown',
    author_email='hughdbrown@yahoo.com',

    # Required packages
    install_requires=reqs_from_file('requirements.txt'),
    tests_require=reqs_from_file('test-requirements.txt'),

    # Main packages
    packages=[
        'src',
        'src.common',
    ],

    zip_safe=False,

    scripts=[
        'bin/git-pep8',
    ],
    entry_points={
        'console_scripts': [
            'git-pep8 = src.git_pep8:main',
        ],
    },
)
