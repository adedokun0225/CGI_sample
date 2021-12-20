from LocalData.LocalStorage import LocalStorage, Database
from LocalData.Model.UserCredentials import UserCredentials
from ServerConnection.Server import Server
from threading import Lock
import keyring

APP_NAME = "Blurr"


class User():

    CREDENTIALS = "credentials"

    @staticmethod
    def initialize():
        User.lock = Lock()
        User.lock.acquire()
        transaction = User.getTransaction()
        if not transaction.has(User.CREDENTIALS):
            transaction.set(User.CREDENTIALS, UserCredentials())
            transaction.commit()
        User.lock.release()

    @staticmethod
    def getEmail():
        return User.getCredentials().getEmail()

    @staticmethod
    def isAuthorized():
        return User.getCredentials().isAuthorized()

    @staticmethod
    def signIn(email, password) -> bool:
        (code, jwtToken, refreshToken) = Server.signIn(email, password)
        if code != Server.OK:
            return False

        User.lock.acquire()
        User.getCredentials().signedIn(email, jwtToken, refreshToken)
        User.commit()
        User.setPassword(email, password)
        User.lock.release()
        return User.authorize()

    @staticmethod
    def signUp(email):
        code, body = Server.signUp(email)
        if code == Server.OK:
            User.lock.acquire()
            User.getCredentials().setEmail(email)
            User.commit()
            User.lock.release()
        return body

    @staticmethod
    def signOut():
        User.lock.acquire()
        User.getCredentials().signOut()
        User.commit()
        User.lock.release()

    @staticmethod
    def commit():
        User.getTransaction().commit()

    @staticmethod
    # tries to autorize the user, checking if blurr is enabled for this accoutn
    def authorize():
        if User.getCredentials().getEmail() == None:
            return False

        (code, body) = Server.isBlurrEnabled(
            User.getCredentials().getJwtToken())
        if code == Server.NO_CONNECTION:
            return User.getCredentials().isAuthorized()

        if code == Server.OK:
            return body["blurrEnabled"]

        (code, body) = Server.refreshToken(
            User.getCredentials().getRefreshToken())
        if code == Server.NO_CONNECTION:
            return User.getCredentials().isAuthorized()

        if code == Server.OK:
            User.lock.acquire()
            transaction = User.getTransaction()
            transaction.get(User.CREDENTIALS).setJwtToken(
                str(body["type"]) + " " + str(body["jwtToken"]))
            transaction.get(User.CREDENTIALS).setRefreshToken(
                str(body["refreshToken"]))
            transaction.commit()
            User.lock.release()
            return User.authorize()

        (code, jwtToken, refreshToken) = Server.signIn(
            User.getCredentials().getEmail(), User.getPassword())
        if code == Server.NO_CONNECTION:
            return User.getCredentials().isAuthorized()

        if code == Server.OK:
            User.lock.acquire()
            transaction = User.getTransaction()
            transaction.get(User.CREDENTIALS).setJwtToken(jwtToken)
            transaction.get(User.CREDENTIALS).setRefreshToken(refreshToken)
            transaction.commit()
            User.lock.release()
            return User.authorize()

        return False

    @ staticmethod
    def getPassword():
        return keyring.get_password(APP_NAME, User.getCredentials().getEmail())

    @ staticmethod
    def deletePassword(email):
        try:
            keyring.delete_password(APP_NAME, email)
        except Exception:
            pass

    @ staticmethod
    def setPassword(email, pwd):
        if email == None or len(email) == 0:
            return
        keyring.set_password(APP_NAME, email, pwd)

    @ staticmethod
    def getJwtToken():
        if not User.authorize():
            return None
        return User.getCredentials().getJwtToken()

    @ staticmethod
    def getCredentials() -> UserCredentials:
        return User.getTransaction().get(User.CREDENTIALS)

    @ staticmethod
    def getTransaction() -> Database:
        return LocalStorage.getConnection()
