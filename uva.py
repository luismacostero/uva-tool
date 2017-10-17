#!/usr/bin/python

import os
import sys
import getopt
import argparse
import src.config

_version = "0.0.2"


def setArgumentParser():
    desc = "%(prog)s: uva helper tool."
    commands = ["init"]
    argParser = argparse.ArgumentParser(description=desc)
    # Program Parameters
    argParser.add_argument("-v", "--version", action='version',
                           version='%(prog)s {}'.format(_version))

    argParser.add_argument("command", choices=commands,
                           help="Action")
    return argParser


def ac_init(args):
    # create config.json
    config = src.config.init()
    src.config.write_config(config)

_actions = {
    "init": ac_init
    }

if __name__ == "__main__":
    argParser = setArgumentParser()
    args = argParser.parse_args(sys.argv[1:])
    _actions[args.command](args)
