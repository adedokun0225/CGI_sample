from tkinter import *

class CodeInput(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.renderCanvas()

    def renderCanvas(self):
        self.canvas = Canvas(self, width=274, height=64)
        self.canvas.pack()
        self.outerCircles = []
        self.innerCircles = []

        for i in range(4):
            self.outerCircles.append(self.canvas.create_oval(2+70*i, 2, 62 + 70*i, 62, width=2))
            

    def set(self, count, wrong=False):
        while(len(self.innerCircles) > count):
            self.canvas.delete(self.innerCircles.pop())
        while(len(self.innerCircles) < count):
            i = len(self.innerCircles)
            self.innerCircles.append(self.canvas.create_oval(7 + 70 * i, 7, 57 + 70*i, 57, fill="#5236ab", width=0))
        
