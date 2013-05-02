git-tools
=========

git-tools - A package of tools for working with git repositories

### Requirements
* Needs to have `git`, `autopep8`, and `pep8`.

### Installation
* Install to /usr/local/bin
sudo python setup.py install
* Install to ~/.local/bin
python setup.py install --user

## Documentation
* `git-pep8`
Iterates over all the python files in a repository and applies pep8 fixes. Each file/error code pair is committed separately. Author for the commit is taken from git config or the `--author` command line option.

## Typical usage
### `git-pep8`
* git-pep8 -r
Apply `autopep8` down a source tree, starting from the current directory
* git-pep8 --author=pep8
Attribute all changes applied to the user pep8
* git-pep8 --startdir=~/workspace/git-tools/src --recurse
Apply `autopep8` down a source tree, starting from STARTDIR

## Contact
* hughdbrown@yahoo.com
