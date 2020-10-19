#!/usr/bin/env python

import json
import os
import re
import shutil
import sys
from urllib.error import HTTPError
from urllib.request import Request
from urllib.request import urlopen

from typing import Dict
from typing import Set
from typing import Tuple
from typing import Union

VARIABLE_RE = re.compile("___(?P<var_name>[a-zA-Z_][a-zA-Z_0-9]*)___")

PROJECT_REMOTE = "git@github.com:AleksaC/python-library-base.git"

# TODO: Look for a better way of excluding files than hard-coding them here.
#  Maybe try parsing .gitignore (.git should stay hardcoded anyway)
IGNORE = {
    "bootstrap.py",
    ".git",
    ".idea",
    ".vscode",
    "venv",
    "_build",
    "dist",
    "build",
    "__pycache__",
    "library.egg-info",
}

variables: Set[str] = set()
file_paths: Set[str] = set()
file_contents = {}


def traverse_repo(root: Union[str, os.DirEntry]) -> None:
    with os.scandir(root) as it:
        for entry in it:
            name = entry.name
            if name not in IGNORE:
                variable = re.match(VARIABLE_RE, name)
                if variable:
                    var_name = variable.group("var_name")
                    variables.add(var_name)
                    path = entry.path
                    for fp in file_paths.copy():
                        if path.startswith(fp):
                            file_paths.remove(fp)
                            break
                    file_paths.add(path)
                if entry.is_dir():
                    traverse_repo(entry)
                else:
                    with open(entry.path) as f:
                        try:
                            contents = f.read()
                            var = set(re.findall(VARIABLE_RE, contents))
                            if var:
                                variables.update(var)
                                file_contents[entry.path] = var
                        except UnicodeDecodeError:
                            pass


def binary_choice(question: str, options: Tuple[str, str]) -> str:  # pragma: no cover
    choice = ""
    while choice not in options:
        choice = input(f"{question} [{options[0]}/{options[1]}] ")
    return choice


def inquire(variables: Set[str]) -> Dict[str, str]:
    values = {}
    print("Enter the values for the following variables:")
    for variable in variables:
        values[variable] = input(f"{variable}: ")
    return values


def render_files(files: Dict[str, Set[str]], values: Dict[str, str]) -> None:
    for fp, vrs in files.items():
        with open(fp, "r+") as f:
            c = f.read()
            for var in vrs:
                c = c.replace(f"___{var}___", values[var])
            f.seek(0)
            f.write(c)
            f.truncate()


def render_paths(fps: Set[str], values: Dict[str, str]) -> None:
    # TODO: Horrible implementation -- clean up ASAP
    if not fps:
        return

    old_path_prefixes: Dict[str, str] = {}

    for fp in fps.copy():
        stale = False
        for prefix in old_path_prefixes:
            if fp.startswith(prefix):
                fps.add(fp.replace(prefix, old_path_prefixes[prefix]))
                fps.remove(fp)
                stale = True
                break
        if stale:
            continue
        root, var, rest = re.split(VARIABLE_RE, fp, 1)
        if rest.startswith("."):
            os.rename(f"{root}___{var}___{rest}", f"{root}{values[var]}{rest}")
        else:
            os.rename(f"{root}___{var}___", f"{root}{values[var]}")
        fps.remove(fp)
        new_path = f"{root}{values[var]}{rest}"
        old_path_prefixes[f"{root}___{var}___"] = f"{root}{values[var]}"
        if re.search(VARIABLE_RE, new_path):
            fps.add(new_path)

    render_paths(fps, values)


def create_github_repo(repo_name: str) -> str:  # pragma: no cover
    user = (
        binary_choice(
            "Are you creating a repository for a user or an organization?", ("u", "o")
        )
        == "u"
    )
    print()
    user_or_org_name = input(f"{'User' if user else 'Organization'} name: ")
    private = binary_choice("Do you want to make the repo private?", ("y", "n")) == "y"
    token = input("Enter GitHub personal access token: ")

    url = "https://api.github.com/"
    if user:
        url += "user/repos"
    else:
        url += f"orgs/{user_or_org_name}/repos"
    headers = {"Authorization": f"token {token}"}
    data = json.dumps({"name": repo_name, "private": private})

    req = Request(url, headers=headers, data=data.encode())
    print("\nCreating GitHub repo...\n")
    try:
        resp = urlopen(req)
    except HTTPError as e:
        print(
            "Something went wrong - please check that the repository with the name "
            f"{repo_name} doesn't already exist. Also make sure that the personal "
            "access token you provided is correct and that it has the right privileges."
        )
        print(e)
        return ""

    if resp.getcode() == 201:
        return f"{user_or_org_name}/{repo_name}"

    return ""


def push_to_github(repo_path: str) -> int:  # pragma: no cover
    url = f"git@github.com:{repo_path}"

    commands = [
        "git add .",
        "git commit -m 'Initial commit'",
        f"git remote add origin {url}",
        "git push -u origin HEAD",
    ]

    for command in commands:
        status = os.system(command)
        if status != 0:
            return status

    return 0


def main() -> int:  # pragma: no cover
    if __file__ == "<stdin>":
        os.system(f"git clone --depth 1 {PROJECT_REMOTE} ___repo_name___")
        print()
        os.execl(
            sys.executable,
            sys.executable,
            os.path.join("___repo_name___", "bootstrap.py"),
        )

    if not sys.stdin.isatty():
        sys.stdin = open("/dev/tty")

    repo_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(repo_path)

    variable = re.match(VARIABLE_RE, os.path.basename(repo_path))
    if variable:
        variables.add(variable.group("var_name"))
        file_paths.add(repo_path)

    if os.path.exists(".git"):
        shutil.rmtree(".git")

    if os.path.exists("README.md"):
        os.remove("README.md")

    if os.path.exists("README_TEMPLATE.md"):
        os.rename("README_TEMPLATE.md", "README.md")

    traverse_repo(os.getcwd())
    values = inquire(variables)
    render_files(file_contents, values)
    render_paths(file_paths, values)

    print()
    os.system("git init")
    print()

    os.remove(os.path.join(os.getcwd(), os.path.basename(__file__)))

    publish_to_github = (
        binary_choice(
            "Publish the repo to github? (Requires personal access token)", ("y", "n")
        )
        == "y"
    )

    if publish_to_github:  # pragma: no cover
        print()
        repo_path = create_github_repo(values["repo_name"])
        if repo_path:
            push_to_github(repo_path)
        else:
            print("Could not create the repository!")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user\n")
        sys.exit(0)
