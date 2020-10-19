# Python library base

[![license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/AleksaC/python-library-base/blob/master/LICENSE)
[![Build Status](https://dev.azure.com/aleksac/python-library-base/_apis/build/status/AleksaC.python-library-base?repoName=AleksaC%2Fpython-library-base&branchName=master)](https://dev.azure.com/aleksac/python-library-base/_build?definitionId=2)
[![Coverage](https://img.shields.io/azure-devops/coverage/aleksac/python-library-base/2/master.svg)](https://dev.azure.com/aleksac/python-library-base/_build/latest?definitionId=2&branchName=master)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/AleksaC/python-library-base/blob/master/.pre-commit-config.yaml)

Starting point for developing python libraries.

## About 📖
This repository includes:
 - basic structure of a python library with a console entrypoint
 - basic tests structure and coverage configuration
 - configuration for `black`, `isort` and `flake8` which are responsible for code
    formatting and linting
 - `pre-commit` config for running various linters and formatters
 - `tox` configuration for:
    - running tests with coverage for multiple versions of python interpreter
    - running `pre-commit`
    - using `mypy` for type checking
    - generating docs using `sphinx-apidoc`
 - azure pipelines configuration for running all the previous stuff in CI along
    with automated publishing of packages to PyPi (or some other package repository)

## Getting started ⚙️
To use this repo as a base for your next python library either click the
*Use this template* button on the GitHub page of the repo or simply clone it and
reinitialize it as a new repository (`rm -rf .git && git init`). To quickly set
up development environment run `source init.sh`. After that you can install
`requirements-dev.txt` for running and testing the library or use `tox` to do
that in a separate environment.

You can use [`bootstrap.py`](https://github.com/AleksaC/bootstrapy) to create
your library using the following command:
```shell script
wget -O - https://raw.githubusercontent.com/AleksaC/python-library-base/master/bootstrap.py | python
```

## Contact 🙋‍♂️
- [Personal website](https://aleksac.me)
- <a target="_blank" href="http://twitter.com/aleksa_c_"><img alt='Twitter followers' src="https://img.shields.io/twitter/follow/aleksa_c_.svg?style=social"></a>
- aleksacukovic1@gmail.com
