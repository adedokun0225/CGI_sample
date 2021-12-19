import ctypes
from typing import Set
from LocalData.Settings import Settings
from LocalData.User import User

# service to change settings from the settings window


class SettingsService():

    def __init__(self) -> None:
        self.pinTries = 0

    # changes the pin code given the current one
    def changePinCode(self, oldPin, newPin):
        currentPin = Settings.get(Settings.UNLOCK_PIN)
        # check if the correct old pin was passed
        if currentPin != oldPin:
            # if not save the unsuccessful try
            self.pinTries += 1

            # on the third failed try -> lock station
            if self.pinTries >= 3:
                self.lockStation()
            return False

        # if the current pin code was current, save the new pin
        Settings.set(Settings.UNLOCK_PIN, newPin)
        self.pinTries = 0
        return True

    # sets a new pin code and locks the station
    def resetPinCode(self, newPin):
        Settings.set(Settings.UNLOCK_PIN, newPin)
        self.lockStation()

    # returns the info about the saved face encodings
    def getFacesInfo(self):
        encodings = Settings.get(Settings.ENCODED_FACES, default={})
        res = []
        for person in encodings:
            res.append({"name": person, "count": len(encodings[person])})

        return res

    # tries to add a face encoding

    def addFaceEncoding(self, encodings, name):
        res = {}
        name = str(name)
        # exactly one encoding must be passed, otherwise no decision can be made which one to choose
        if len(encodings) == 1:
            savedEncodings = Settings.get(Settings.ENCODED_FACES, default={})
            if name in savedEncodings:
                savedEncodings[name].append(encodings[0].tolist())
            else:
                savedEncodings[name] = [encodings[0].tolist()]
            Settings.set(Settings.ENCODED_FACES, savedEncodings)
            res["successful"] = True
            return res
        else:
            res["successful"] = False
            res["error"] = "Wrong count of detected faces"
            return res

    # check whether a given member name is already taken
    def checkName(self, name):
        savedEncodings = Settings.get(Settings.ENCODED_FACES, default={})
        return (not name in savedEncodings) and len(name) > 0

    # deletes all encodings for a given member
    def deletePerson(self, name):
        savedEncodings = Settings.get(Settings.ENCODED_FACES, default={})
        if name in savedEncodings:
            del savedEncodings[name]
            if len(savedEncodings) == 0:
                Settings.set(Settings.FACE_RECOGNITION, False)

        savedEncodings = Settings.set(Settings.ENCODED_FACES, savedEncodings)

    # toggles the tracking status
    def setTracking(self, isTracking):
        Settings.set(Settings.TRACKING_ON, isTracking)

    # lock the station and reset the current failed pin tries count
    def lockStation(self):
        self.pinTries = 0
        ctypes.windll.user32.LockWorkStation()

    # changes the general settings given a correct pin code and a method to call if tracking status has been changed
    def setGeneralSettings(self, pinCode, settings, toggleMethod):
        sets = settings
        actualPin = Settings.get(Settings.UNLOCK_PIN)
        if pinCode != actualPin:
            return False

        if Settings.TRACKING_ON in sets:
            Settings.set(Settings.TRACKING_ON, sets[Settings.TRACKING_ON])
            toggleMethod(sets[Settings.TRACKING_ON])

        if Settings.FACE_RECOGNITION in sets:
            Settings.set(Settings.FACE_RECOGNITION,
                         sets[Settings.FACE_RECOGNITION])

        return True

    # returns the general settings
    def getGeneralSettings(self):
        ret = {}
        ret[Settings.FACE_RECOGNITION] = Settings.get(
            Settings.FACE_RECOGNITION, default=False)
        ret[Settings.TRACKING_ON] = Settings.get(
            Settings.TRACKING_ON, default=False)
        ret["faceEncodings"] = len(Settings.get(Settings.ENCODED_FACES)) > 0
        return ret

    # returns whether it is not the first start of the app
    def wasSetUp(self):
        return Settings.isSetUp()

    # configure the app
    def setUp(self, settings, toggleMethod):
        print("Setting up")
        Settings.set(Settings.UNLOCK_PIN, settings[Settings.UNLOCK_PIN])
        Settings.set(Settings.WAS_SET_UP, True)
        self.setGeneralSettings(
            settings[Settings.UNLOCK_PIN], settings, toggleMethod)

    def getEmail(self):
        return User.getEmail()
        # return Settings.get(Settings.EMAIL, default="")

    def executeIfPin(self, pin, fn):
        currentPin = Settings.get(Settings.UNLOCK_PIN)
        if currentPin == pin:
            fn()
        return currentPin == pin
