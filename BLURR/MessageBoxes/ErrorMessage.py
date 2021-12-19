import tkinter.messagebox as box


class ErrorMessage():

    def __init__(self):
        pass

    def show(self, title: str, msg: str):
        box.showerror(title=title, message=msg)
