from time import time
from BlockingOverlay.MainBlockerWindow import MainBlockerWindow
from ObjectTracker import ObjectTracker
from SystemTray.SystemTray import SystemTray
from SettingsWindow.BlurrSettingsWindow import SettingsWindow
from Logging.Logger import Logger
from LocalData.Settings import Settings
from LocalData.User import User
import Logging.Logger as Log
import Lib.Constants as const
from LocalData.LocalStorage import LocalStorage
import threading
import sys
import time


class Blurr():

    def __init__(self) -> None:
        LocalStorage.initialize()
        Settings.initialize()
        User.initialize()
        self.tracker = ObjectTracker()

        self.settingsWindow = SettingsWindow(
            self.tracker, self.setTracking, self.quitBlurr)
        self.systemTray = SystemTray(self.settingsWindow)
        self.blockerWindow = MainBlockerWindow(self.setTracking)

        Logger.initialize()
        self.reason = ""
        self.isRunning = False
        self.loggingStarted = False

    # entry point for the app
    def startApp(self):
        try:
            # configure the app on first start
            if not Settings.isSetUp():
                self.configure()

            isAuthorized = self.userLoggedIn()

            if not isAuthorized:
                self.settingsWindow.start()

            self.isRunning = isAuthorized and Settings.get(
                Settings.TRACKING_ON)
            self.blocked = False

            self.startLoggingThread()

            # run the main thread of the app
            self.mainThread()
        except Exception as err:
            Logger.error(str(err))
            self.setTracking(False)
            return

    # starts the logging deamon, which logs the current usage status

    def startLoggingThread(self):
        if not self.loggingStarted:
            loggingThread = threading.Thread(None, target=self.loggingThread)
            loggingThread.start()
            self.loggingStarted = True

    # deamon thread running in the background and logging the current state to the file every 30 seconds
    def loggingThread(self):
        while not self.wasAppClosed():
            res = None
            if self.isRunning:
                res = Logger.info(Log.LOG_BLURR_ACTIVE)
            else:
                res = Logger.info(Log.LOG_BLURR_INACTIVE)

            # if logs were succesfully updated to server, try to persist old ones
            if res:
                Logger.persistRemainingLogs()

            time.sleep(60)
        # end app
        print("Exiting logging thread")
        sys.exit()

    # infinite loop switching between the system tray icon and the blocking window
    def mainThread(self):
        # infinite loop until the app closes
        while True:
            # if the station is blocked show the blocking window
            if self.blocked:
                self.blockerWindow.show(
                    self.reason, Settings.get(Settings.UNLOCK_PIN))
                self.blocked = False
            # otherwise create the system tray icon
            else:
                self.createTrackingThread()
                self.systemTray.createIcon()

            # if user closed the app via the blocking icon
            if self.wasAppClosed():
                return

    # checks whether the app was closed via the blocking icon
    def wasAppClosed(self):
        return self.systemTray.closed

    # possibly enable/disable the tracking
    def setTracking(self, tracking: bool):
        Settings.set(Settings.TRACKING_ON, tracking)
        if tracking:
            # if the tracking was enabled, check whether the tracking thread is already running
            if self.isRunning or not self.userLoggedIn():
                return
            else:
                # if no start it
                self.isRunning = True
                Logger.info(Log.LOG_BLURR_ACTIVATE)
                self.createTrackingThread()
        else:
            # if it was disabled -> terminate the tracking thread
            self.isRunning = False
            Logger.info(Log.LOG_BLURR_DEACTIVATE)
            time.sleep(1)

    # creates a thread, which tracks the input from the camera
    def createTrackingThread(self):
        isTracking = Settings.isSetUp() and Settings.get(
            Settings.TRACKING_ON, default=False)
        if isTracking:
            self.trackingThread = threading.Thread(None, self.tracking)
            self.trackingThread.start()

    # loop for the tracking thread
    def tracking(self):
        try:
            try:
                self.tracker.startTracking()
            except Exception as err:
                Logger.error(str(err))
                self.setTracking(False)
                return
            # scan in thread until blocked
            while True:
                # terminate is tracking has been disabled
                if not self.isRunning:
                    self.tracker.stopTracking()
                    sys.exit()

                # get the tracking result from the object tracker
                (valid, code) = self.tracker.checkSample()
                if not valid:
                    # block the screen with the apriopriate reason if invalid camera input has been detected
                    if self.wasAppClosed():
                        return
                    self.blocked = True
                    self.reason = Log.LOG_MESSAGES[code]
                    self.systemTray.endIcon()
                    self.tracker.stopTracking()
                    Logger.info(code)
                    return

                # terminate if the app has been closed
                if self.wasAppClosed():
                    return
        except Exception as err:
            Logger.error(str(err))
            self.setTracking(False)
            return

    # configure the app on first start
    def configure(self):
        Settings.setDefaultSettings()
        self.settingsWindow.start()

    def userLoggedIn(self):
        return User.authorize()

    def quitBlurr(self):
        self.systemTray.quitApp()
