import os
# -*- coding: utf-8 -*-
import json
import api


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

    # Set generic Items
    keys = ["path", "user_name", "pass"]
    for k in keys:
        if not(k in config) or config[k] == "":
            config[k] = ask(k)

    # Api items
    # user_id
    if not("user_id" in config) or config["user_id"] == "":
        config["user_id"] = api.get_user_id(config["user_name"])
    return config
