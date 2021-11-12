from Logging.ServerConnection import OK, ServerConnection, UNAUTHORIZED
from LocalData.User import User
import json

from ServerConnection.Server import Server
from LocalData.User import User

class ConnectionService():
    
    def __init__(self, serverConnection:ServerConnection, setTracking) -> None:
        self.serverConnection = serverConnection
        self.setTracking = setTracking

    def isUserLoggedIn(self):
        return User.authorize()

    def logIn(self, email, password):
        #(code, _) = self.serverConnection.logIn(email=email, password=password)
        #return not code == UNAUTHORIZED
        return User.signIn(email, password)

    def singUp(self, email):
        (code, msg) = self.serverConnection.signUp(email)
        ret = {
            "successful": code==OK,
            "message": msg,
        }
        return json.dumps(ret, indent=4)

    def logOut(self):
        self.serverConnection.logOut()
        self.setTracking(False)
        