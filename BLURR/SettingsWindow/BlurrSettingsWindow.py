from Logging.ServerConnection import ServerConnection
from LocalData.Settings import Settings
from ObjectTracker import ObjectTracker
import sys
import eel
import threading
from SettingsWindow.Services.SettingsService import SettingsService
from SettingsWindow.Services.RecognitionService import RecognitionService
from SettingsWindow.Services.ConnectionService import ConnectionService

running = True

#Blurr settings window -> runs in browser
class SettingsWindow():

  def __init__(self, objectTracker:ObjectTracker, serverConnection:ServerConnection, setTracking, closeApp) -> None:
      self.isOpen = False
      self.objectTracker = objectTracker
      #initialize the services
      self.settings = SettingsService()
      self.recognition = RecognitionService(objectTracker)
      self.connectionService = ConnectionService(serverConnection, setTracking)
      self.wasStopped = False
      self.setTracking = setTracking
      def quitFn():
        self.wasStopped = True
        closeApp()
      self.quitApp = quitFn

      #expose the functions for the settings window

      #gets a marked frame from the camera as a string
      @eel.expose
      def getFrame():
          return self.recognition.getFrame()

      #change the pin using the old pin
      @eel.expose
      def changePIN(oldPin, newPin):
          return self.settings.changePinCode(oldPin, newPin)

      #change the pin without using the old pin and block the computer
      @eel.expose
      def resetPIN(newPin):
        return self.settings.resetPinCode(newPin)
      
      #get information about saved face encodings
      @eel.expose
      def getFacesInfo():
        return self.settings.getFacesInfo()

      #add a new face encoding from the current camera frame
      @eel.expose
      def addFaceEncoding(name):
        return self.settings.addFaceEncoding(self.recognition.getEncodings(), name)

      #check whether a name for a new member is valid
      @eel.expose
      def checkName(name):
        return self.settings.checkName(name)

      #deletes all face encodings for a given member
      @eel.expose
      def deletePerson(name):
        return self.settings.deletePerson(name)

      #starts tracking
      @eel.expose
      def startTracking():
        self.settings.setTracking(True)
        self.setTracking(True)

      #stops the tracking
      @eel.expose
      def stopTracking():
        self.settings.setTracking(False)
        self.setTracking(False)

      @eel.expose
      def getGeneralSettings():
        return self.settings.getGeneralSettings()

      @eel.expose
      def setGeneralSettings(pinCode, settings):
        return self.settings.setGeneralSettings(pinCode, settings, self.setTracking)

      #check whether it is the first start of Blurr
      @eel.expose
      def wasSetUp():
        return self.settings.wasSetUp()

      #set up Blurr after the welcome screen
      @eel.expose
      def setUp(settings):
        self.settings.setUp(settings, self.setTracking)

      @eel.expose
      def isLoggedIn():
        return self.connectionService.isUserLoggedIn()

      @eel.expose
      def getEmail():
        return self.settings.getEmail()

      @eel.expose
      def logIn(username, password):
        res = self.connectionService.logIn(username, password)
        if res:
          self.settings.trackingAfterLogin(self.setTracking)
        return res

      @eel.expose
      def signUp(email):
        return self.connectionService.singUp(email)

      @eel.expose
      def logOut(pin):
        return self.settings.executeIfPin(pin, self.connectionService.logOut)

      @eel.expose
      def quitApp(pin):
        return self.settings.executeIfPin(pin, self.quitApp)
        
  
  #opens a new browser window with blurr settings
  def start(self):
    #allow for only one instance of the settings window at a time
    if self.isOpen:
      return

    self.isOpen = True
    #run i a separate thread to not block
    t1 = threading.Thread(target=self.__runWindow__)
    t1.start()
    
  def __runWindow__(self):
    #serve the frontend with eel
    eel.init('SettingsWindow/web')

    #function to end the thread after the window was closed
    def onEnd(a,b):
      self.objectTracker.stopCamera()
      self.wasStopped = True
    
    #start window
    try:
      eel.start('index.html', port=0, mode="chrome", block=False, close_callback=onEnd)
    except EnvironmentError:
      if sys.platform in ['win32', 'win64']:
        eel.start("index.html", mode="edge", block=False, close_callback=onEnd)

    #actively check whether the window was stopped
    while not self.wasStopped:
      eel.sleep(1)
    
    #tidy up and exit
    self.wasStopped = False
    self.isOpen = False
    sys.exit()
