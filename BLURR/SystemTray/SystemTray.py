import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

#icon the system tray
class SystemTray():

    def __init__(self, settingsWindow):
        self.closed = False
        self.icon = None
        self.settingsWindow = settingsWindow

    #close the whole app
    def quitApp(self):
        self.closed = True
        self.icon.stop()

    #open the settings window (non-blocking)
    def openSettings(self):
        self.settingsWindow.start()
        
    #create the icon - >blocking call
    def createIcon(self):
        if self.icon != None:
            self.icon.stop()

        img = Image.open("Assets/BlockedIcon.png")
        menu=pystray.Menu(item("Open Settings", self.openSettings))
        self.icon=pystray.Icon("Blurr", img, "Blurr", menu)
        self.icon.run()
    
    #end the icon -> quits the loop in create icon
    def endIcon(self):
        self.icon.stop()