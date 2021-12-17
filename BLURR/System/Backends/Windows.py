import ctypes


def logOut():
    ctypes.windll.user32.LockWorkStation()
