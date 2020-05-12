
def isInt(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def toProblemId(n):
    base = "00000"
    return base[len(n):] + n
