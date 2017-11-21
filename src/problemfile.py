# -*- coding: utf-8 -*-

import jinja2
import time
import api


def create_problem(author, problemid, judge, path):
    if judge != "uva":
        raise RuntimeError("Not implemented yet.")

    templateLoader = jinja2.FileSystemLoader(searchpath='./templates/')
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template('header_general.template')
    data = {}
    data["author"] = author
    data["date"] = time.strftime("%d/%m/%Y")
    data["id"] = ""
    data["url"] = ""

    if judge == "uva":
        probleminfo = api.uva.get_problem_info(problemid)
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
