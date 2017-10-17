import os
# -*- coding: utf-8 -*-
import json

basedir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..")
config_path = os.path.join(basedir, "config.json")


def ask(key):
    answer = raw_input("Give me the " + key + ": ")
    return answer


def read_config(path):
    # Reading data back
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def write_config(config):
    # Writing JSON data
    with open(config_path, 'w') as f:
        json.dump(config, f)


def init():
    # PATH, USER_NAME, USER_ID, PASS?, URL
    try:
        config = read_config(config_path)
    except:
        config = {}
    keys = ["path", "user_name", "user_id", "pass", "url"]
    if not("path" in config):
        if os.environ.get("UVA_PATH") is not None:
            config["path"] = os.environ["UVA_PATH"]
    for k in keys:
        if not(k in config) or config[k] == "":
            config[k] = ask(k)
    if os.environ.get("UVA_PATH") is None:
        os.environ["UVA_PATH"] = config["path"]
        bashPath = os.path.join(os.environ["HOME"], '.bashrc')
        with open(bashPath, 'a') as file:
            file.write("export UVA_PATH="+config["path"]+"\n")
        print("WARNING: run: . " + bashPath)
    return config


