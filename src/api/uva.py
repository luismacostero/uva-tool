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
    check_request(r)
    if r.text == "0":
        raise Exception("User (" + username + ") not Found")
    return int(r.text)


def get_problem_info(problemNumber):
    """Returns the information of a specific problem.
    """

    # TODO: check if the problem exists
    check_integer(problemNumber)

    url = uhunt_url + "p/num/" + str(problemNumber)

    r = requests.get(url)
    check_request(r)

    rinfo = r.json()
    info = {}

    info["number"] = rinfo["num"]
    info["pdf_url"] = (uva_url + uva_pdfProblem_url +
                       str(int(problemNumber) / 100) +
                       "/" + str(problemNumber) + '.pdf')
    info["title"] = rinfo["title"]
    info["best_time"] = get_best_time(int(rinfo["pid"]))
    return info


def get_problemid_from_number(problemNumber):
    """Returns the problemID assciated with the problem number"""
    check_integer(problemNumber)

    url = uhunt_url + "p/num/" + str(problemNumber)

    r = requests.get(url)
    check_request(r)

    rjson = r.json()

    return int(rjson["pid"])


def get_best_time(ident, problemId=True):
    """Given a problemId or ProblemNumber, returns the time of the best
    solution.
    problemId=True:    from the problemId
             =False:   from the problemNumber

    """
    check_integer(ident)

    if problemId:
        number = ident
    else:
        number = get_problemid_from_number(ident)

    url = uhunt_url + "p/rank/" + str(number) + "/1/1"

    r = requests.get(url)
    check_request(r)

    rjson = r.json()
    return int(rjson[0]["run"])


def check_request(request):
    if request.status_code != 200:
        raise Exception("Return code error")


def check_integer(number, msg=None):
    """raise an exception if number is not an integer
    """
    try:
        int(number)
    except:
        raise ValueError(msg)
