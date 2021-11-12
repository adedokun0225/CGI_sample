from os import stat
from Logging.ServerConnection import ServerConnection
from LocalData.Model.LogEntry import LogEntry
from LocalData.LocalStorage import LocalStorage, Database
from LocalData.Settings import Settings
from LocalData.User import User
from ServerConnection.Server import Server
import logging
import sys
import time
from getmac import get_mac_address


SERVER_URL = "http://localhost:8080"

LOCAL_LOG_TABLE = "logs"
LOCAL_LOGS_TO_UPLOAD_TABLE = "logsToUpload"

KEY="RQAHytaSyNhTrxlggk6Q"

LOG_BLURR_ACTIVE = 1
LOG_BLURR_INACTIVE = 2
LOG_BLURR_ACTIVATE = 5
LOG_BLURR_DEACTIVATE = 6

LOG_LOCKING_NOONE = 11
LOG_LOCKING_UNAUTH = 12

LOG_ERROR = 99

LOG_MESSAGES = {
    1: "Blurr is activated",
    2: "Blurr is deactivated",
    5: "User enabled tracking",
    6: "User disabled tracking",
    11: "Insecure enviroment! Nobody detected!",
    12: "Insecure enviroment! Unauthorized person detected."
}

BLURR_LOGGER_NAME = "blurrLogger"

#entry point for the logging module, logs usage to file/server
class Logger(object):

    #initializes logging part
    @staticmethod
    def initialize():
        Logger.localStorage = LocalStorage.getConnection()
        Logger.localStorage.createMapIfNotExists(LOCAL_LOG_TABLE)
        Logger.localStorage.createMapIfNotExists(LOCAL_LOGS_TO_UPLOAD_TABLE)
        logger = logging.getLogger(BLURR_LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        #prepare formatter and clear s
        formatter = logging.Formatter("%(asctime)s - %(message)s")

        logger.handlers.clear()
        
        #logging to console
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        #logging to file
        #filePath = Settings.getDefaultLoggingPath()
        #fh = logging.FileHandler(filename=filePath)
        #fh.setFormatter(formatter)
        #logger.addHandler(fh)
        

    @staticmethod
    #logs the passed info, returns whether uploaded to server
    def info(code, comment=None) -> bool:
        return Logger.persistLog(code, comment)
        
    @staticmethod
    def debug(msg):
        logging.getLogger(BLURR_LOGGER_NAME).debug(msg)

    @staticmethod
    def error(msg):
        return Logger.persistLog(LOG_ERROR, msg)

    @staticmethod
    def persistRemainingLogs():
        logList = []
        currentUser = User.getEmail()
        
        
        mac = get_mac_address()
        toPersistLogs = Logger.localStorage.get(LOCAL_LOGS_TO_UPLOAD_TABLE).get(currentUser)
        for entry in toPersistLogs.values():
            obj = entry.toDict()
            obj["mac"] = mac
            logList.append(entry.toDict())

        if(len(logList) == 0):
            return

        jwtToken = User.getJwtToken()
        if jwtToken == None:
            return

        res = Server.oldLog(jwtToken, logList)

        if res == Server.OK:
            Logger.debug("Uploaded local logs to server")
            toPersistLogs.clear()
            Logger.localStorage.commit()

    @staticmethod
    def persistLog(code, comment) -> bool:
        jwtToken = User.getJwtToken()
        #do not log if the user is not authorized
        if jwtToken == None:
            return False
            
        currentUser = User.getEmail()
        milis = int(time.time() * 1000)
        new_log = LogEntry(code, None, milis)
        Logger.localStorage.get(LOCAL_LOG_TABLE).get(currentUser).append(new_log)

        res = Server.log(jwtToken, code, comment, milis, get_mac_address())
        if res != Server.OK:
            Logger.localStorage.get(LOCAL_LOGS_TO_UPLOAD_TABLE).get(currentUser).append(new_log)
            Logger.localStorage.commit()
            Logger.debug("Couldn't log to server, persisting logs")
            return False    
        else:
            Logger.localStorage.commit()
            (_, body) = Server.getOwnLogs(jwtToken, milis-3000000, milis)
            print(body)
            return True
