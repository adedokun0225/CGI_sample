from tkinter import *
from PIL import ImageTk, Image
from System.System import System
from BlockingOverlay.Components.CodeInput import CodeInput
from BlockingOverlay.KeyboardHook.KeyboardHook import KeyboardHook
from BlockingOverlay.Monitors.Monitors import Monitors


class MainBlockerWindow():

    def __init__(self, setTracking) -> None:
        self.setTracking = setTracking
        self.kHook = KeyboardHook(self.pinInput, self.closeAndBlock)
        self.monitors = Monitors()

    # block the screen via the custom overlay
    def show(self, message, password):

        # set vars
        self.password = password
        self.msg = message
        self.lock = False
        self.toClose = False

        # block the input from the keyboard
        self.kHook.hook()

        # reset GUI
        self.overlays = []
        self.monitors.reset()

        # reset pin code field
        self.typedPwd = ""
        self.failedAttempts = 0

        # create the main blocking overlay (on the main monitor)
        self.root = Tk()
        self.root.overrideredirect(True)
        (width, height) = self.monitors.getMainDims()
        self.root.geometry("{0}x{1}+0+0".format(width, height))
        self.maxScaling = 100
        if System.isWindows():
            self.root.wm_attributes("-disabled", True)
        self.root.bind("<FocusOut>", self.getFocus)
        # render GUI
        self.render()
        # get focus to stay on top
        self.root.after(10, self.getFocus, 0)
        self.root.after(10, self.scanForMonitors)
        self.root.after(10, self.updateGui)
        self.root.mainloop()

    # render the overlay components
    def render(self):
        # configure grid
        self.root.rowconfigure((0, 6), weight=1)
        self.root.columnconfigure((0, 2), weight=1, uniform="rand")
        self.renderLeft()
        self.renderCenter()
        self.renderRight()

    # renders the left side of the main blocking overlay (blurr logo in the top left corner + label in the bottom left corner)
    def renderLeft(self):
        logo = Image.open("Assets/BLURR.png")
        logo = logo.resize((125, 10))
        logo = ImageTk.PhotoImage(logo)
        logoLbl = Label(self.root, image=logo)
        logoLbl.image = logo
        logoLbl.grid(column=0, row=0, sticky=NW, ipadx=80, ipady=45)
        lbl = Label(text="Press DEL to disable tracking and lock the station", font=(
            "Avenir Next", 14), justify=CENTER,  cursor="hand2")
        lbl.grid(column=0, row=6, sticky=SW, pady=(0, 20), padx=(20, 0))

    # renders the central column of the main blocking window (icon + message)
    def renderCenter(self):
        # rendering the block icon
        img = Image.open("Assets/BlockedIcon.png")
        img = img.resize((160, 200))
        img = ImageTk.PhotoImage(img)
        blockIcon = Label(self.root, image=img, )
        blockIcon.image = img
        blockIcon.grid(column=1, row=1, pady=20)

        self.codeInput = CodeInput(self.root)
        self.codeInput.grid(column=1, row=2, pady=5)

        messageLbl = Label(text=self.msg, font=(
            "Avenir Next", 18, 'bold'), justify=CENTER)
        messageLbl.grid(column=1, row=3, pady=5)

        blurrLabel = Label(text="Blurr is activated", font=(
            "Avenir Next", 18), justify=CENTER)
        blurrLabel.grid(column=1, row=4, pady=5)

    # renders the right side of the main blocking window (ITC label bottom right corner)
    def renderRight(self):
        lbl = Label(text="Developed with the Support of the Innovation Technology Campus – ITC in Munich", font=(
            "Avenir Next", 8), justify=CENTER,  cursor="hand2")
        lbl.grid(column=2, row=6, sticky=SE, pady=(0, 20), padx=(0, 20))

    # periodically scan for new monitors and block them if needed
    def scanForMonitors(self):
        # do nothing if the blocking overlay is to be closed anyways
        if self.toClose:
            return

        self.root.call('wm', 'attributes', '.', '-topmost', True)
        # get all monitors for which no overlay was created so far
        newGeos = self.monitors.getNewMonitors()
        for newGeo in newGeos:
            # create an overlay for them
            self.createBlankOverlayForGeo(newGeo)

        # setup for the next occurence
        self.root.after(100, self.scanForMonitors)

    # creates a white overlay on the position specified by geo
    def createBlankOverlayForGeo(self, geo):

        # create an overlay
        overlay = Toplevel(self.root)
        overlay.overrideredirect(True)
        overlay.geometry(geo)
        overlay.wm_attributes("-topmost", 1)
        overlay.wm_attributes("-alpha", 1)
        if System.isWindows():
            overlay.state("zoomed")
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.focus_force()
        print("Adding overlay with geo: " + geo)
        self.overlays.append(overlay)

    # updates the number of colored circles to indicate the pin digits
    def updatePin(self, count):
        self.codeInput.set(count)

    # updates the input pin code on new keyboard input
    def pinInput(self, key: str):
        if "back" in key:
            if len(self.typedPwd) > 0:
                self.typedPwd = self.typedPwd[0:len(self.typedPwd)-1]
            return

        if not key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return

        self.typedPwd += key
        # pin code has a fixed length of 4
        if len(self.typedPwd) == 4:
            # if it was correct, unlock
            if self.typedPwd == self.password:
                self.toClose = True
            # otherwise add failed attempt and lock the screen if needed
            else:
                self.failedAttempts += 1
                if self.failedAttempts >= 3:
                    self.lock = True
            self.typedPwd = ""

    # closes the blocking overlay, locks the computer and turns off tracking
    def closeAndBlock(self):
        self.toClose = True
        self.lockStation()
        self.setTracking(False)

    # periodic update for the gui
    def updateGui(self):
        # update the length of input pin
        self.updatePin(len(self.typedPwd))

        # if the station is to be locked -> lock it
        if self.lock:
            self.lockStation()

        # close the window if it was closed
        if self.toClose:
            self.close()
        else:
            # if not closed schedule another update
            self.root.after(10, self.updateGui)

    # get focus to stay on top
    def getFocus(self, arg):
        # put all additional overlays to the top
        for overlay in self.overlays:
            window = overlay["overlay"]
            window.lift()
        # get focus for the main window
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.focus_force()

    # close the overlays
    def close(self):
        self.root.destroy()
        self.root.quit()
        self.kHook.unhook()

    # lock the computer using the windows default functionality
    def lockStation(self):
        try:
            System.logOut()
            self.close()
        except Exception as err:
            print(str(err))
