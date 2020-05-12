# -*- coding: utf-8 -*-

import jinja2
import os
import time
import src.api as api


def create_problem(author, problemid, judge, path):
    appi = api.get_api(judge)

    templateLoader = jinja2.FileSystemLoader(searchpath='./templates/')
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template('header_general.template')
    data = {}
    data["author"] = author
    data["date"] = time.strftime("%d/%m/%Y")
    data["id"] = ""
    data["url"] = ""

    probleminfo = appi.get_problem_info(problemid)
    data["id"] = str(problemid) + " - " + probleminfo["title"]
    data["url"] = probleminfo["pdf_url"]

    outputHeader = template.render(data)

    with open('./templates/body', 'r') as outputBody:
        with open(path + '/' + str(problemid) + '.cpp', 'w') as outputFile:
            outputFile.write(outputHeader)
            outputFile.write('\n\n')
            outputFile.write(outputBody.read())

    with open(path + '/' + str(problemid) + '.in', 'w') as outputFile:
        outputFile.write('')

    with open(path + '/' + str(problemid) + '.out', 'w') as outputFile:
        outputFile.write('')

    with open(path + '/' + data["id"], 'w') as outputFile:
        outputFile.write(data["id"])

def submit_problem(user, password, problemid, judge, path):
    appi = api.get_api(judge)
    _, file_extension = os.path.splitext(path)
    if file_extension == ".cpp":
        language = "c++11"
    else:
        language = file_extension[1:]
    appi.submit(user, password, problemid, path, language)
    
