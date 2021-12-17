import os


def logOut():
    # TODO: proper log out
    os.system("osascript -e 'tell app \"System Events\" to shut down'")
