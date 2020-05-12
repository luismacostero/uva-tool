
def isInt(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
