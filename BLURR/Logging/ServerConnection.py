from re import T
import requests
from LocalData.Settings import Settings

SERVER_URL = "https://blurr-logging.eu-central-1.elasticbeanstalk.com"

OK = 200
BAD_REQUEST = 400
UNAUTHORIZED = 401
NO_CONNECTION = 1234

class ServerConnection():

    def __init__(self) -> None:
        pass

    def sendLog(self, code, message=None):
        (res, json) = self.logIn()
        if res != OK:
            return (False, res)
        
        headers = {
            "Authorization": str(json["type"]) + " " + str(json["jwtToken"])
        }

        body = {
            "code": code,
            "comment": message,
        }

        try:
            res = requests.post(SERVER_URL+"/api/log", headers=headers, json=body, verify=False)
        except requests.ConnectionError:
            print("No connection")
            return (NO_CONNECTION, None)

        print(str(res.status_code) + str(res.text))
        return (res.status_code == OK, OK)

    def logIn(self, email=None, password=None):

        isNewPassword = password != None

        if email == None:
            email = Settings.getCurrentUser()
        if email==None or len(email) == 0:
            return (UNAUTHORIZED, None)
        if password == None:
            password = Settings.getPassword()
        if password==None:
            return (UNAUTHORIZED, None)

        json={
            "email": email,
            "password": password,
        }

        try:
            res = requests.post(SERVER_URL + "/api/auth/signin", json=json, verify=False)
        except requests.ConnectionError:
            print("NO connection")
            if isNewPassword:
                return (UNAUTHORIZED, None)
            else:
                return (NO_CONNECTION, None)

        print(str(res))

        if res.status_code == 200:
            Settings.setPassword(password)
            Settings.set(Settings.EMAIL, email)
            return (OK, res.json())
        elif res.status_code == UNAUTHORIZED:
            Settings.deletePassword()
            return (res.status_code, None)
        else:
            return (res.status_code, None)

    def signUp(self, email):
        body={
            "email":email,
        }

        res=None
        try:
            res=requests.post(SERVER_URL + "/api/auth/signup", json=body, verify=False)
        except requests.ConnectionError:
            return (NO_CONNECTION, None)

        if res.status_code == OK:
            return (OK, None)
        elif res.status_code == BAD_REQUEST:
            return (BAD_REQUEST, res.json()["message"])
        else:
            return (res.status_code, None)

    def logOut(self):
        Settings.deletePassword()
        return