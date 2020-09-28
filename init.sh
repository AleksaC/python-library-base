# Source this script to initialize development environment for the library

if [ ! -d venv ]; then
    if command -v virtualenv &> /dev/null; then
        virtualenv venv -p python3
    else
        python3 -m venv venv
    fi
fi

. ./venv/bin/activate

command -v tox &> /dev/null || python -m pip install tox
command -v pre-commit &> /dev/null || python -m pip install pre-commit

pre-commit install
