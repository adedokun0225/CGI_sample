import persistent

class UserSettings(persistent.Persistent):

    def __init__(self) -> None:
        super().__init__()
        self.setDefault()
    
    def setDefault(self):
        self.faceEncodings = {}
        self.unlockPin = ""
        self.tracking = False
        self.faceRecognition = False
        self.wasSetUp = False

    def get(self, key):
        #if not hasattr(self, key):
            #self.setDefault()
        return getattr(self, key)

    def set(self, key, value):
        return setattr(self, key, value)