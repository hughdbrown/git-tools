git-tools
=========

git-tools - A package of tools for working with git repositories

### Requirements
* Needs to have `git`, `autopep8`, and `pep8`.

### Installation
* Install to `/usr/local/bin`

Use `sudo python setup.py install`

* Install to `~/.local/bin`

Use `python setup.py install --user`

## Documentation
* `git-pep8`
Iterates over all the python files in a repository and applies pep8 fixes.
The frequency of commit ranges from every file/error pair to once per run.
Automatic commit comment describes contents of change.
Author for the commit is taken from git config or the `--author` command line option.

## Typical usage
### `git-pep8`
* `git-pep8 -r`

Apply `autopep8` down a source tree, starting from the current directory

* `git-pep8 --recurse ~/workspace/git-tools/src`

Apply `autopep8` down a source tree, starting from STARTDIR

* `git-pep8 --author=pep8`

Attribute all changes applied to the user pep8

#### Four modes of operation
1. all: checks for all errors over all files and commits to git once
2. by-file-only: iterate over files applying all errors at once, one commit per file
3. by reason-only: iterate over error types applying to all files at once, one commit per error type
4. by-file-and-reason: iterate over each error-file pair, committing once per error-file pair
The default is `by-file-and-reason`. Many developers find this produces too many commits to examine. It does have the advantage that
it is easy to examine a commit and see the scope of the change and the reason given for the change.

#### Try it out
This script creates four branches, one for each method of running `git-pep8`.
Try it out to see which set of commits works best for you.

``` bash
git checkout master
git branch -D all
git checkout -b all
git-pep8 -r -v -m all src/

git checkout master
git branch -D by-file-and-reason
git checkout -b by-file-and-reason
git-pep8 -r -v -m by-file-and-reason src/

git checkout master
git branch -D by-file-only
git checkout -b by-file-only
git-pep8 -r -v -m by-file-only src/

git checkout master
git branch -D by-reason-only
git checkout -b by-reason-only
git-pep8 -r -v -m by-reason-only src/
```

## Contact
* hughdbrown@yahoo.com
