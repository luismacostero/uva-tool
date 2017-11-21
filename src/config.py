# -*- coding: utf-8 -*-
import os
import json
import src.api as api
import getpass
import src.filemanager as filemanager

basedir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..")
config_path = os.path.join(basedir, "config.json")
private_path = os.path.join(basedir, "private.json")


def ask(msg):
    return raw_input(msg + " ")


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
        json.dump(config, f)


def init():
    """ Checks if there is a config file. If it's created, load it; 
    otherwise, create a new one asking for each field.
    If there is a config file, but there are empty fields, ask for them too
    """
    change = False
    try:
        config = read_config(config_path)
    except:
        config = {}
    try:
        private = read_config(private_path)
    except:
        private = {}

    if not("path" in config):
        change = True
        config["path"] = ask("Where are you going to save your repo?")

    if not(filemanager.check_folder(config["path"], ".git")):
        if not("repo" in config):
            change = True
            config["repo"] = ask("Which is your git-repository url?")
        filemanager.create_repo_folder(config["repo"], config["path"])

    if not("author" in config):
        change = True
        config["author"] = ask("Which is your author name?")

    if not("uva_user" in config):
        change = True
        config["uva_user"] = ask("Which is your UVA user?")
    if not("uva_pass" in private):
        change = True
        private["uva_pass"] = ask_private("Which is your UVA pass?")

    if not("acr_user" in config):
        change = True
        config["acr_user"] = ask("Which is your ACR user?")
    if not("acr_pass" in private):
        change = True
        private["acr_pass"] = ask_private("Which is your ACR pass?")

    # Api items
    # user_id
    if not("uva_id" in config) or config["uva_id"] == "":
        change = True
        config["uva_id"] = api.uva.get_user_id(config["uva_user"])
    if not("acr_id" in config) or config["acr_id"] == "":
        change = True
        config["acr_id"] = api.acr.get_user_id(config["acr_user"])

    if change:
        write_config(config, config_path)
        write_config(private, private_path)

    return config
