from LocalData.LocalStorage import LocalStorage
from LocalData.Model.UserCredentials import UserCredentials
from ServerConnection.Server import Server
import keyring

APP_NAME = "Blurr"


class User():

    CREDENTIALS = "credentials"

    @staticmethod
    def initialize():
        User.storage = LocalStorage.getConnection()
        if User.storage.has(User.CREDENTIALS):
            User.credentials = User.storage.get(User.CREDENTIALS)
        else:
            User.credentials = UserCredentials()
            User.storage.set(User.CREDENTIALS, User.credentials)
            User.storage.commit()

    @staticmethod
    def getEmail():
        return User.credentials.getEmail()

    @staticmethod
    def isAuthorized():
        return User.credentials.isAuthorized()

    @staticmethod
    def signIn(email, password) -> bool:
        (code, jwtToken, refreshToken) = Server.signIn(email, password)
        if code != Server.OK:
            return False

        User.credentials.signedIn(email, jwtToken, refreshToken)
        User.storage.commit()
        User.setPassword(email, password)
        return User.authorize()

    @staticmethod
    def signUp(email):
        code, body = Server.signUp(email)
        if code == Server.OK:
            User.credentials.setEmail(email)
        return body

    @staticmethod
    def commit():
        User.storage.commit()

    @staticmethod
    # tries to autorize the user, checking if blurr is enabled for this accoutn
    def authorize():
        if User.credentials.getEmail() == None:
            return False

        (code, body) = Server.isBlurrEnabled(User.credentials.getJwtToken())
        if code == Server.NO_CONNECTION:
            return User.credentials.isAuthorized()

        if code == Server.OK:
            return body["blurrEnabled"]

        (code, body) = Server.refreshToken(User.credentials.getRefreshToken())
        if code == Server.NO_CONNECTION:
            return User.credentials.isAuthorized()

        if code == Server.OK:
            User.credentials.setJwtToken(
                str(body["type"]) + " " + str(body["jwtToken"]))
            User.credentials.setRefreshToken(str(body["refreshToken"]))
            User.commit()
            return User.authorize()

        (code, jwtToken, refreshToken) = Server.signIn(
            User.credentials.getEmail(), User.getPassword())
        if code == Server.NO_CONNECTION:
            return User.credentials.isAuthorized()

        if code == Server.OK:
            User.credentials.setJwtToken(jwtToken)
            User.credentials.setRefreshToken(refreshToken)
            User.commit()
            return User.authorize()

        return False

    @staticmethod
    def getPassword():
        return keyring.get_password(APP_NAME, User.credentials.getEmail())

    @staticmethod
    def deletePassword(email):
        try:
            keyring.delete_password(APP_NAME, email)
        except Exception:
            pass

    @staticmethod
    def setPassword(email, pwd):
        if email == None or len(email) == 0:
            return
        keyring.set_password(APP_NAME, email, pwd)

    @staticmethod
    def getJwtToken():
        if not User.authorize():
            return None
        return User.credentials.getJwtToken()
