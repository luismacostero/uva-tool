# -*- coding: utf-8 -*-
import os
import json
import getpass

import src.api as api
import src.filemanager as filemanager

basedir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..")
config_path = os.path.join(basedir, "config.json")
private_path = os.path.join(basedir, "private.json")


def ask(msg):
    return input(msg + " ")


def ask_private(msg):
    return getpass.getpass(msg + " ")


def read_config(path):
    """ Load the configutration from the given file.
    """
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def write_config(config, path):
    """ Saves the current configuration into a file
    """
    # Writing JSON data
    with open(path, 'w') as f:
        json.dump(config, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        f.write("\n")


def init():
    """ Checks if there is a config file. If it's created, load it; 
    otherwise, create a new one asking for each field.
    If there is a config file, but there are empty fields, ask for them too
    """
    change = False
    change_private = False
    try:
        config = read_config(config_path)
    except:
        config = {}
    try:
        private = read_config(private_path)
    except:
        private = {}

    if "path" not in config:
        change = True
        config["path"] = ask("Where are you going to save your repo?")

    if not filemanager.check_folder(config["path"], ".git"):
        if "repo" not in config:
            change = True
            config["repo"] = ask("Which is your git-repository url?")
        filemanager.create_repo_folder(config["repo"], config["path"])

    if "author" not in config:
        change = True
        config["author"] = ask("Which is your author name?")

    
    if "judges" not in private:
        private["judges"] = {}
    if "judges" not in config:
        config["judges"] = {}
    listjudges = ask("Which judges will you programming for? (space-separated list)")

    for judge in listjudges.strip().split():
        svr = judge.lower()
        try:
            appi = api.get_api(judge)
        except RuntimeError as e:
            print(e+" ")
            continue
        if svr not in config["judges"]:
            config["judges"][svr] = {}
        if svr not in private["judges"]:
            private["judges"][svr] = {}
        if "user" not in config["judges"][svr]:
            change = True
            config["judges"][svr]["user"] = ask("Which is your {} user?".format(svr))
            if "id" not in config["judges"][svr]:
                config["judges"][svr]["id"] = appi.get_user_id(config["judges"][svr]["user"])
        if "pass" not in private["judges"][svr]:
            change_private = True
            private["judges"][svr]["pass"] = ask_private("Which is your {} pass?".format(svr))

    if change:
        write_config(config, config_path)
    if change_private:
        write_config(private, private_path)

    return config

def get_config():
    c, p = read_config(config_path), read_config(private_path)
    for j in p["judges"]:
        c["judges"][j]["pass"] = p["judges"][j]["pass"]
    return c

