from appdirs import user_data_dir
from LocalData.LocalStorage import Database, LocalStorage
from LocalData.Model.UserSettings import UserSettings
from LocalData.User import User
from threading import Lock
import os

APP_NAME = "Blurr"


# stores the app settings as a .py file in Appdata/Local
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
        Settings.lock = Lock()
        Settings.lock.acquire()
        storage = Settings.getTransaction()
        storage.get(Settings.SETTINGS_TABLE)
        storage.commit()
        Settings.lock.release()
        # list of email for which the settings were initialized in this session
        Settings.emails = []

    # get the path to the appdata folder
    @staticmethod
    def getSettingsPath():
        dir_path = user_data_dir(APP_NAME, Settings.APP_AUTHOR)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    # check whether it is the first start of the app
    @staticmethod
    def isSetUp():
        return User.getEmail() is not None and Settings.get(Settings.WAS_SET_UP)

    # get the settings for a given key
    @staticmethod
    def get(key, default=None):
        userSettings = Settings.getCurrentSettings()
        return userSettings.get(key)

    # set the settings for a given key
    @staticmethod
    def set(key, value):
        Settings.lock.acquire()
        print("Acquired lock")
        transaction = Settings.getTransaction()
        userSettings = Settings.getCurrentSettings(
            acquiredLock=True, transaction=transaction)
        userSettings.set(key, value)
        transaction.commit()
        Settings.lock.release()
        print("Released lock")

    # sets settings to default
    @staticmethod
    def setDefaultSettings():
        Settings.lock.acquire()
        print("Acquired lock")
        try:
            transaction = Settings.getTransaction()
            userSettings = Settings.getCurrentSettings(
                acquiredLock=True, transaction=transaction)
            userSettings.setDefault()
            transaction.commit()
        except Exception:
            pass
        Settings.lock.release()
        print("Released lock")

    # get the path to the .log file for logging
    @staticmethod
    def getDefaultLoggingPath():
        return Settings.getSettingsPath() + "/usage.log"

    # returns the userSettings for the current user if available and throws an exception otherwise
    @staticmethod
    def getCurrentSettings(acquiredLock=False, transaction=None) -> UserSettings:
        # start a new transaction if none was passed
        if transaction is None:
            transaction = Settings.getTransaction()

        email = User.getEmail()
        settingsTable = transaction.get(Settings.SETTINGS_TABLE)
        if email not in settingsTable:
            if not acquiredLock:
                Settings.lock.acquire()

            # check whether the settings for this email were initialized in the meantime
            if email in Settings.emails:
                if not acquiredLock:
                    Settings.lock.release()
                return Settings.getCurrentSettings(transaction=transaction)

            Settings.emails.append(email)
            settingsTable[email] = UserSettings()
            transaction.commit()
            if not acquiredLock:
                Settings.lock.release()
        return settingsTable[email]

    @staticmethod
    def getTransaction() -> Database:
        return LocalStorage.getConnection()
