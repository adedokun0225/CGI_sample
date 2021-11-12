from operator import setitem
from typing import Set
from pypref import Preferences
from appdirs import user_data_dir
from LocalData.LocalStorage import LocalStorage
from LocalData.Model.UserSettings import UserSettings
from LocalData.User import User
import os

APP_NAME = "Blurr"


#stores the app settings as a .py file in Appdata/Local
class Settings():

    APP_AUTHOR = "CGI"
    SETTINGS_TABLE = "settings"

    ENCODED_FACES = "faceEncodings"
    UNLOCK_PIN = "unlockPin"
    TRACKING_ON = "tracking"
    FACE_RECOGNITION = "faceRecognition"
    WAS_SET_UP = "setup"

    @staticmethod
    def initialize() -> None:
        Settings.storage = LocalStorage.getConnection()
        #dir_path = Settings.getSettingsPath()
        #Settings.prefs = Preferences(directory=dir_path, filename="preferences.py")

    #get the path to the appdata folder
    @staticmethod
    def getSettingsPath():
        dir_path = user_data_dir(APP_NAME, Settings.APP_AUTHOR)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    #check whether it is the first start of the app
    @staticmethod
    def isSetUp():
        #return Settings.get(Settings.WAS_SET_UP)
        try:
            return Settings.get(Settings.WAS_SET_UP)
        except Exception:
            return False
        #TODO: Update

    #get the settings for a given key
    @staticmethod
    def get(key, default=None):
        userSettings = Settings.getCurrentSettings()
        return userSettings.get(key)

    #set the settings for a given key
    @staticmethod
    def set(key, value):
        #Settings.prefs.update_preferences({key:value})
        userSettings = Settings.getCurrentSettings()
        userSettings.set(key, value)
        Settings.commit()
        print(userSettings.get(Settings.TRACKING_ON))
        
    #sets settings to default
    @staticmethod
    def setDefaultSettings():
        try:
            userSettings = Settings.getCurrentSettings()
            userSettings.setDefault()
            Settings.commit()
        except Exception:
            pass

    #get the path to the .log file for logging
    @staticmethod
    def getDefaultLoggingPath():
        return Settings.getSettingsPath() + "/usage.log"

   
    #returns the userSettings for the current user if available and throws an exception otherwise
    @staticmethod
    def getCurrentSettings()->UserSettings:
        #return Settings.prefs.get(key, default=default)
        email = User.getEmail()
        settingsTable = Settings.storage.get(Settings.SETTINGS_TABLE)    
        if email not in settingsTable:
            settingsTable[email] = UserSettings()
        return settingsTable[email]

    @staticmethod
    def commit()->None:
        Settings.storage.commit()