import requests
SERVER_URL = "https://blurr-332209.ey.r.appspot.com/"
#SERVER_URL = "http://localhost:5000"
VERIFY_REQUESTS = True

class Server():

    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NO_CONNECTION = 1234

    @staticmethod
    def initialize():
        pass

    @staticmethod
    def oldLog(jwtToken:str, logList:list):
        headers = {
            "Authorization": jwtToken
        }
        body = {
            "logs": logList
        }
        try:
            res = requests.post(SERVER_URL+"/api/oldLog", headers=headers, json=body, verify=VERIFY_REQUESTS)
            return res.status_code
        except requests.ConnectionError:
            return Server.NO_CONNECTION

    def getOwnLogs(jwtToken:str, fromMilis:int=-1, toMilis:int=-1):
        headers = {
            "Authorization": jwtToken
        }
        parameters = {
            "fromMilis": fromMilis,
            "toMilis": toMilis,
        }
        print(parameters)

        try:
            res = requests.get(SERVER_URL+"/api/ownLogs", headers=headers, params=parameters, verify=VERIFY_REQUESTS)
            print(res)
            return (res.status_code, res.json())
        except requests.ConnectionError:
            return (Server.NO_CONNECTION, None)
            

    @staticmethod
    def log(jtwToken:str, code:int, comment:str, milis:int, mac:str):
        headers = {
            "Authorization": jtwToken
        }
        body = {
            "code": code,
            "comment": comment,
            "milis": milis,
            "mac": mac,
        }
        try:
            res = requests.post(SERVER_URL+"/api/log", headers=headers, json=body, verify=VERIFY_REQUESTS)
            return res.status_code
        except requests.ConnectionError:
            return Server.NO_CONNECTION


    #signs in with given credentials, returns (status code, jwtToken, refreshToken)
    @staticmethod
    def signIn(email, password): #-> tuple[int, str, str]:
        json={
            "email": email,
            "password": password,
        }

        try:
            res = requests.post(SERVER_URL + "/api/auth/signin", json=json, verify=VERIFY_REQUESTS)
        except requests.ConnectionError:
            return (Server.NO_CONNECTION, None, None)
        
        if res.ok:
            body = res.json()
            jwtToken = str(body["type"]) + " " + str(body["jwtToken"])
            return (Server.OK, jwtToken, body["refreshToken"])
        return (res.status_code, None, None)

    @staticmethod
    def isBlurrEnabled(jwtToken):
        try:
            res = requests.get(SERVER_URL + "/api/user/isBlurrEnabled", headers={
                "Authorization": jwtToken,
            }, verify=VERIFY_REQUESTS)
            return (res.status_code, res.json())
        except requests.ConnectionError:
            return (Server.NO_CONNECTION, None)
    
    @staticmethod
    def refreshToken(refreshToken):
        try:
            res = requests.post(SERVER_URL + "/api/auth/refreshToken", json={
                "refreshToken": refreshToken
            }, verify=VERIFY_REQUESTS)
            return (res.status_code, res.json())
        except requests.ConnectionError:
            return (Server.NO_CONNECTION, None)