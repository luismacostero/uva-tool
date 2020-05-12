# -*- coding: utf-8 -*-
import os
import git
from subprocess import Popen

import src.problemfile as problemfile

basedir = os.getcwd()


def _relative(path, other=""):
    if other != "":
        o = os.path.join(path, other)
    else:
        o = path
    return os.path.join(basedir, o)


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
    editor_open(config, problemid, judge=judge)


def get_problem_path(config, problemid, judge="uva"):
    path = _relative(config["path"], judge+"/"+problemid)
    for e in ["cpp", "py", "c", "java"]:
        F =path+"."+e
        print(F)
        if check_file(F):
            return F
    return None
    
def editor_open(config, problemid, judge="uva", extension="cpp"):
    path = _relative(config["path"], judge+"/"+problemid)
    prefix = os.path.join(path, problemid+".")
    extensions = ["in", "out", extension]
    args = ["emacs"] + [prefix+e for e in extensions] + ["&"]
    Popen(' '.join(args), shell=True)


def create_problem_folder(path, problemid, judge="uva"):
    probdir = _relative(path, judge+"/"+str(problemid))
    os.makedirs(probdir)
    os.makedirs(os.path.join(probdir, "submissions"))

def submit_problem(config, problemid, judge="uva"):
    path = _relative(config["path"], judge+"/"+problemid)
