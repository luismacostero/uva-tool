import src.api.uva
import src.api.acr

def get_api(judge="uva"):
    j = judge.lower()
    if j == "uva":
        return src.api.uva
    if j == "acr":
        return src.api.acr
    raise Exception("Judge, {}, is NOT supported".format(judge))
