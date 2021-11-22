from LocalData.User import User


class ConnectionService():

    def __init__(self, setTracking) -> None:
        self.setTracking = setTracking

    def isUserLoggedIn(self):
        return User.authorize()

    def logIn(self, email, password):
        return User.signIn(email, password)

    def singUp(self, email):
        response = User.signUp(email)
        if response:
            return response

        ret = {
            "successful": False,
            "message": "Could not connect to Server!"
        }
        return ret

    def logOut(self):
        User.signOut()
        self.setTracking(False)
