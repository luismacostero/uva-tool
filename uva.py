#!/usr/bin/python

import sys
import src.config


""" Each accepted command has a function called ac_<functionName>, and 
it is called with all the passed arguments
"""
def ac_help(args):
    res = __file__ + " <command>\n"
    res += "\n<commands>"
    for k in _actions:
        res += "\n - " + k + ""
    print(res)


def ac_open(args):
    if len(args) != 1:
        ac_help(args)
        raise Exception("Program number not found")
    print(args)


def ac_init(args):
    # create config.json
    config = src.config.init()
    src.config.write_config(config)

    # accepted actions and function handler for each action
_actions = {
    "help": ac_help,
    "init": ac_init,
    "open": ac_open
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        ac_help(args)
        exit(-1)
    if not(args[0] in _actions):
        ac_help(args)
        raise Exception("Command not found: " + args[0])
    _actions[args[0]](args[1:])
