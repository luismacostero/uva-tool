import requests
import json
from contextlib import contextmanager

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

class _OJNavigator:

    HOME_URL="https://onlinejudge.org/"
    SUBMIT_URL="https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=25"

    def __init__(self):
        from selenium import webdriver
        self.driver = None
        self.driver = webdriver.Firefox()
        self.driver.get(self.HOME_URL)

    def __del__(self):
        if self.driver is not None:
            self.driver.close()

    def login(self, user, password):
        assert "Online Judge" in self.driver.title
        userinput = self.driver.find_element_by_id("mod_login_username")
        passinput = self.driver.find_element_by_id("mod_login_password")
        userinput.send_keys(user)
        passinput.send_keys(password)
        passinput.submit()
        with self.wait_for_page_load(timeout=30):
            print("logged?")

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support.expected_conditions import staleness_of
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout).until(staleness_of(old_page))

    
    def quick_submit(self, problem_id, language, filepath):
        languages={"c":1,"java":2,"c++":3,"pascal":4,"c++11":5,"python":6}
        self.driver.get(self.SUBMIT_URL)
        pidinput = self.driver.find_element_by_name("localid")
        pidinput.send_keys(problem_id)
        lnginputs = self.driver.find_elements_by_name('language')
        lnginputs[languages[language]-1].click()
        fileinput = self.driver.find_element_by_name("codeupl")
        fileinput.send_keys(filepath)
        fileinput.submit()
        with self.wait_for_page_load(timeout=30):
            print("submitted?")

def submit(user, password, problemNumber, filepath, language):
    """
    Submits the problem
    """
    try:
        # TODO: check problemNumber
        # TODO: check language
        ojnav = _OJNavigator()
        ojnav.login(user, password)
        ojnav.quick_submit(problemNumber, language, filepath)
        # TODO: return submision ID
    except Exception as e:
        # TODO: process exceptions
        print(e)
        raise Exception() from e


def veredictID_to_string(veredictID, short=False):
    """
    Returns a veredict in string format.
    If short is True it returns the acronym of the veredict
    """
    vids = {
        10 : ("Submission error", "SE"),
        15 : ("Can't be judged", "CJ"),
        20 : ("In queue", "IQ"),
        30 : ("Compile error", "CE"),
        35 : ("Restricted function", "RF"),
        40 : ("Runtime error", "RE"),
        45 : ("Output limit", "OL"),
        50 : ("Time limit", "TL"),
        60 : ("Memory limit", "ML"),
        70 : ("Wrong answer", "WA"),
        80 : ("PresentationE", "PE"),
        90 : ("Accepted", "AC")
    }
    pos = 1 if short else 0
    return vids[veredictID][pos]
