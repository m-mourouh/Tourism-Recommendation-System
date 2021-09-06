def isBlank (myString):
    return not (myString and myString.strip())

def isNotBlank (myString):
    return bool(myString and myString.strip())

