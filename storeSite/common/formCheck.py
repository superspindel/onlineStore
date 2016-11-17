"""
Function name: formCheck
Inputvariables: *args is a number of arguments to check
Info: Takes a number of arguments and checks if they can pass the swapChar function, both with characters and words.
"""

def formCheck(*args):
    for thing, input in enumerate(args):
        for character in input:
            if not swapChar(character):
                return False
        splitInput = input.split()
        for word in splitInput:
            if not swapChar(word):
                return False
    return True

"""
Function name: swapChar
Inputvariables: character
Info: Takes a character variable, either a char or a word and checks if it is in the badList
"""
def swapChar(character):
    badList = ["<", ">", "!", "©", "£", "$", "∞", "§", "|", "[", "]", "±", "+", "´",
               "~", "™", "…", "‚", "#", "€", "%", "&", "/", "(", ")", "=", "?", "`", "^",
               "*", "_", ":", ";", "≤", "INSERT", "CREATE", "SELECT", "SHOW", "DATABASES",
               "FROM", "DROP", "DELETE", "UPDATE", "ALTER"]
    if character in badList:
        return False
    return True
