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


def swapChar(character):
    badList = ["<", ">", "!", "©", "£", "$", "∞", "§", "|", "[", "]", "±", "+", "´",
               "~", "™", "…", "‚", "#", "€", "%", "&", "/", "(", ")", "=", "?", "`", "^",
               "*", "_", ":", ";", "≤", "INSERT", "CREATE", "SELECT", "SHOW", "DATABASES",
               "FROM", "DROP", "DELETE", "UPDATE", "ALTER"]
    if character in badList:
        return False
    return True
