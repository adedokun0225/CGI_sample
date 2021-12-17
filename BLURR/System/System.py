from sys import platform
if platform == "win32":
    from System.Backends.Windows import *
elif platform == "linux":
    from System.Backends.Linux import *
elif platform == "darwin":
    from System.Backends.OSX import *


class System():

    @staticmethod
    def isWindows():
        return platform == "win32"

    @staticmethod
    def isLinux():
        return platform == "linux"

    @staticmethod
    def isMac():
        return platform == "darwin"

    @staticmethod
    def logOut():
        logOut()
