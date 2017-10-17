import requests
import json

# Base urls for the services
uhunt_url = "http://uhunt.onlinejudge.org/api/"
uva_url = "http://uva.onlinejudge.org/"

# specific urls for specific services
uva_pdfProblem_url = "external/"


def get_user_id(username):
    """Returns the user ID of the given username.
    If the user does not exist, returns 0
    """

    url = uhunt_url + "uname2uid/" + username

    r = requests.get(url)
    checkRequest(r)
    if r.text == "0":
        raise Exception("User (" + username + ") not Found")
    return int(r.text)


def get_problem_info(problemNumber):
    """Returns the information of a specific problem.
    """
    if not isinstance(problemNumber, int):
        raise ValueError('problemNumber is not an integer')

    url = uhunt_url + "p/num/" + str(problemNumber)

    r = requests.get(url)
    checkRequest(r)

    rinfo = r.json()
    info = {}

    info["number"] = rinfo["num"]
    info["pdf_url"] = (uva_url + uva_pdfProblem_url +
                       str(int(problemNumber / 100)) +
                       '/' + str(problemNumber) + '.pdf')
    info["title"] = rinfo["title"]
    return info


def checkRequest(request):
    if request.status_code != 200:
        raise Exception("Return code error")



