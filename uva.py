#!/usr/bin/python

import sys
import src.config
import src.filemanager as filemanager
import src.problemfile as problemfile
from src.utils import isInt
from src.utils import toProblemId

""" Each accepted command has a function called ac_<functionName>, and 
it is called with all the passed arguments
"""
def ac_help(args):
    res = __file__ + " <command>\n"
    res += "\n<commands>"
    for k in _actions:
        res += "\n - " + k + " " + _actions[k][1]
    print(res)


def ac_open(args):
    if len(args) != 1 or not isInt(args[0]):
        ac_help(args)
        raise Exception("Program number not found")
    config = src.config.init()
    problemid = toProblemId(args[0])
    filemanager.open_problem(config, problemid)

def ac_submit(args):
    """
    <judge> <prob-num> <path>
    """
    if (len(args) != 2 and len(args) != 3) or not isInt(args[1]):
        ac_help(args)
        raise Exception("Error")
    config = src.config.get_config()
    judge = args[0]
    problemid = toProblemId(args[1])
    if len(args) == 3:
        filepath = args[3]
        if not filemanager.check_file(filepath):
            raise Exception("File not found")
    else:
        filepath = filemanager.get_problem_path(config, problemid, judge)
        if filepath is None:
            raise Exception("File not found")
    user = config["judges"][judge]["user"]
    psw = config["judges"][judge]["pass"]
    problemfile.submit_problem(user, psw, problemid, judge, filepath)
    
def ac_init(args):
    # create config.json
    config = src.config.init()

    # accepted actions and function handler for each action
_actions = {
    "help": (ac_help, ""),
    "init": (ac_init, ""),
    "open": (ac_open,"<prob-num>"),
    "submit": (ac_submit, "<judge> <prob-num> <path>")
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        ac_help(args)
        exit(-1)
    if args[0] not in _actions:
        ac_help(args)
        raise Exception("Command not found: " + args[0])
    _actions[args[0]][0](args[1:])
