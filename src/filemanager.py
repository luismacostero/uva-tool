# -*- coding: utf-8 -*-
import os
import git
from subprocess import call
basedir = os.getcwd()


def _relative(path, other=""):
    return os.path.join(basedir, os.path.join(path, other))


def check_folder(path, foldername=""):
    return os.path.isdir(_relative(path, foldername))


def check_file(path, filename=""):
    return os.path.exists(_relative(path, filename))


def create_repo_folder(repo, path):
    """Clone repo into path
    """
    folder = _relative(path)
    if not(check_folder(folder, ".git")):
        git.Repo.clone_from(repo, folder)
    else:
        raise Exception("The folder is already used.")


def open_problem(config, problemid, judge="uva"):
    """Check if exists, if not create it, then open
    """
    directory = _relative(config["path"], judge+"/"+problemid)
    if not(check_folder(directory)):
        create_problem_folder(config["path"], problemid, judge=judge)
        problemfile.create_problem(author=config["author"],
                                   problemid=problemid,
                                   judge=judge,
                                   path=directory)
    editos_open(config, problemid, judge=judge)


def editor_open(config, problemid, judge="uva"):
    path = _relative(config["path"], judge+"/"+problemid)
    prefix = os.path.join(path, problemid+".")
    extensions = ["cpp", "in", "out"]
    args = ["emacs"] + [prefix+e for e in extensions] + ["&"]
    call(args)
