from tkinter import *
from PIL import ImageTk, Image
import pyWinhook as pyHook
import ctypes
import scipy.ndimage as scimage
import numpy
from mss import mss
from BlockingOverlay.Components.CodeInput import CodeInput
from BlockingOverlay.Toolkit.EnumerateMonitors import *
from BlockingOverlay.KeyboardHook.KeyboardHook import KeyboardHook


class MainBlockerWindow():

    def __init__(self, setTracking) -> None:
        self.setTracking = setTracking

        self.kHook = KeyboardHook(self.pinInput)

    # block the screen via the custom overlay
    def show(self, message, password):
        ctypes.windll.shcore.SetProcessDpiAwareness(0)
        self.password = password
        self.lock = False
        self.toClose = False

        #self.hm.KeyDown = self.onKeyboard()
        # self.hm.HookKeyboard()
        self.kHook.hook()
        # reset GUI
        self.overlays = []
        # reset pin code field
        self.typedPwd = ""
        self.failedAttempts = 0
        self.msg = message
        self.root = Tk()
        self.root.overrideredirect(True)
        (width, height) = self.getMainDims()
        print(self.getMainDims())
        self.root.geometry("{0}x{1}+0+0".format(width, height))
        # TODO: Add Blurry effect
        self.maxScaling = 100
        self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "white")
        bcg = ImageTk.PhotoImage(self.getBlurryBackground(
            0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        background = Label(self.root, image=bcg)
        # background.place(x=0, y=0, relwidth=1, relheight=1)
        # self.root.attributes("-fullscreen", True)
        # block close attempts
        self.root.bind("<FocusOut>", self.getFocus())
        # render GUI
        self.render()
        # get focus to stay on top
        self.root.after(10, self.getFocus(), 0)
        self.root.after(10, self.scanForMonitors())
        self.root.after(10, self.updateGui())
        self.root.mainloop()

    # render the overlay components
    def render(self):
        # configure grid
        self.root.rowconfigure((0, 6), weight=1)
        self.root.columnconfigure((0, 2), weight=1, uniform="rand")
        self.renderLogo()
        self.renderCenter()
        self.renderRight()

    def renderLogo(self):
        logo = Image.open("Assets/BLURR.png")
        logo = logo.resize((125, 10))
        logo = ImageTk.PhotoImage(logo)
        logoLbl = Label(self.root, image=logo)
        logoLbl.image = logo
        logoLbl.grid(column=0, row=0, sticky=NW, ipadx=80, ipady=45)

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

    def renderRight(self):
        lbl = Label(text="Press F4 to disable tracking and lock the station", font=(
            "Avenir Next", 14), justify=CENTER,  cursor="hand2")
        lbl.grid(column=0, row=6, sticky=SW, pady=(0, 20), padx=(20, 0))
        lbl = Label(text="Developed with the Support of the Innovation Technology Campus – ITC in Munich", font=(
            "Avenir Next", 8), justify=CENTER,  cursor="hand2")
        lbl.grid(column=2, row=6, sticky=SE, pady=(0, 20), padx=(0, 20))

    def getBlurryBackground(self, x, y, width, height):
        sct = mss()
        img = numpy.array(
            sct.grab({"top": y, "left": x, "width": width, "height": height}))
        screen_arr = scimage.gaussian_filter(img, sigma=1.8)

        return Image.fromarray(screen_arr).resize((width, height))

    def getMainDims(self):
        monitors = list(enumerate_monitors())
        for monitor in monitors:
            if monitor.x == 0 and monitor.y == 0:
                return (monitor.width, monitor.height)

    # periodically scan for new monitors and block them if needed
    def scanForMonitors(self):
        def do():
            self.root.call('wm', 'attributes', '.', '-topmost', True)
            # get real resolutions
            monitors = list(enumerate_monitors())
            # get main monitor info
            maxScaling = None
            for monitor in monitors:
                if monitor.x == 0 and monitor.y == 0:
                    mainMonitor = monitor
                if not maxScaling or monitor.scaling > maxScaling:
                    maxScaling = monitor.scaling
            maxScaling = 100
            for monitor in monitors:
                # skip main monitor
                if monitor.x == 0 and monitor.y == 0:
                    continue
                # check if the monitor was already processed
                found = False
                for overlay in self.overlays:
                    if monitor.x == overlay['x'] and monitor.y == overlay['y'] and monitor.height == overlay['h'] and monitor.width == overlay['w']:
                        found = True
                        break
                if not found:
                    # * monitor.width_mm / mainMonitor.width_mm
                    # * monitor.height_mm / mainMonitor.height_mm
                    width = round(monitor.width /
                                  monitor.scaling * mainMonitor.scaling)
                    height = round(monitor.height /
                                   monitor.scaling * mainMonitor.scaling)
                    geo = str(width) + "x" + str(height)
                    # geo = str(int(monitor.width)) + "x" + str(int(monitor.height))
                    # prepare the geo string
                    geoPos = ""
                    if monitor.x < 0:
                        geoPos += str(int(monitor.x))
                    else:
                        geoPos += "+" + str(int(monitor.x))

                    if monitor.y < 0:
                        geoPos += str(int(monitor.y))
                    else:
                        geoPos += "+" + str(int(monitor.y))

                    geo += geoPos
                    # render new overlay for the found monitor
                    overlay = Toplevel(self.root)
                    overlay.overrideredirect(True)
                    overlay.geometry(geo)
                    bcg = self.getBlurryBackground(
                        monitor.x, monitor.y, width, height)
                    bcg.resize((1280, 720))
                    bcg = ImageTk.PhotoImage(bcg)
                    background = Label(overlay, image=bcg)
                    background.image = bcg
                    # background.place(x=0, y=0, relwidth=1, relheight=1)
                    overlay.wm_attributes("-topmost", 1)
                    overlay.wm_attributes("-alpha", 1)
                    overlay.state("zoomed")
                    # overlay.attributes("-fullscreen", True)
                    self.root.call('wm', 'attributes', '.', '-topmost', True)
                    self.root.focus_force()
                    # overlay.geometry(str(overlay.winfo_screenwidth())+"x"+str(overlay.winfo_screenheight())+geoPos)
                    print("Adding overlay with geo: " + geo)
                    print({'x': monitor.x, 'y': monitor.y, 'h': monitor.height,
                          'w': monitor.width, "overlay": overlay})
                    self.overlays.append(
                        {'x': monitor.x, 'y': monitor.y, 'h': monitor.height, 'w': monitor.width, "overlay": overlay})
            self.root.after(100, self.scanForMonitors())
        return do

    def updatePin(self, count):
        self.codeInput.set(count)

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

    # scan for keyboard events
    def onKeyboard(self):
        def onKey(event):
            if event.Key.lower() in ['lmenu', 'rmenu', 'lcontrol', 'rcontrol', 'delete']:
                self.lock = True
                return False
            elif event.Key.lower() in ['lwin', 'tab']:
                return False
            # digits for the pin code
            elif event.Key.lower() in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.typedPwd += event.Key.lower()
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
            elif event.Key.lower() in ['back']:
                if len(self.typedPwd) > 0:
                    self.typedPwd = self.typedPwd[0:len(self.typedPwd)-1]
            # to take screenshots
            elif event.Key.lower() in ["snapshot"]:
                return True
            elif event.Key.lower() in ["f4"]:
                self.closeAndBlock()
            return False
        return onKey

    def closeAndBlock(self):
        self.toClose = True
        self.lockStation()
        self.setTracking(False)

    def updateGui(self):
        def do():
            self.updatePin(len(self.typedPwd))
            if self.lock:
                self.lockStation()
            if self.toClose:
                self.close()
            self.root.after(10, self.updateGui())
        return do

    # get focus to stay on top
    def getFocus(self):
        def focus(event):
            # put all additional overlays to the top
            for overlay in self.overlays:
                window = overlay["overlay"]
                window.lift()
            # get focus for the main window
            self.root.call('wm', 'attributes', '.', '-topmost', True)
            self.root.focus_force()
        return focus

    # close the overlays
    def close(self):
        self.kHook.unhook()
        self.root.destroy()
        self.root.quit()

    # lock the computer using the windows default functionality
    def lockStation(self):
        ctypes.windll.user32.LockWorkStation()
        self.close()
