import persistent

class UserCredentials(persistent.Persistent):

    def __init__(self) -> None:
        super().__init__()
        self.email = None
        self.authorized = False
        self.jwtToken = None
        self.refreshToken = None
        self.blurrEnabled = False

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email

    def isAuthorized(self):
        return self.authorized

    def setAuthorized(self, authorized):
        self.authorized = authorized
    
    def getJwtToken(self):
        return self.jwtToken

    def setJwtToken(self, jwtToken):
        self.jwtToken = jwtToken

    def getRefreshToken(self):
        return self.refreshToken

    def setRefreshToken(self, refreshToken):
        return self.refreshToken

    def signedIn(self, email, jwtToken, refreshToken):
        self.email = email
        self.jwtToken = jwtToken
        self.refreshToken = refreshToken
        self.authorized = True

    def isBlurrEnabled(self):
        return self.blurEnabled

    def setBlurrEnabled(self, enabled):
        self.blurrEnabled = enabled