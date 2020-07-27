#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
from github import Github


def git(cmds):
    print("git {}".format(" ".join(cmds)))
    subprocess.run(["git"] + cmds, check=True)

name = sys.argv[1]

shutil.rmtree(".git")

git(["init"])
git(["add", "--all"])
git(["rm", "--cached", ".gitlab-ci.yml", "deploy_template.py"])
git(["commit", "-m", "Publish task template"])
git(["remote", "add", "origin", "git@github.com:NSU-Programming/{}.git".format(name)])

print("accessing Github account")
with open(os.path.expanduser("~/.github/token")) as f:
    gt = f.read().strip("\n")
g = Github(gt)
org = g.get_organization("NSU-Programming")
repos = [repo.name for repo in org.get_repos()]
if name not in repos:
    print("creating repo '{}'".format(name))
    org.create_repo(name, private=True)

git(["push", "-f", "origin", "master"])
