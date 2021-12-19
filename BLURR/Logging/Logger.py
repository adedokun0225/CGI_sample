from os import stat
from LocalData.Model.LogEntry import LogEntry
from LocalData.LocalStorage import LocalStorage, Database
from LocalData.User import User
from ServerConnection.Server import Server
import logging
import sys
import time
import threading
from getmac import get_mac_address

SERVER_URL = "http://localhost:8080"

LOCAL_LOG_TABLE = "logs"
LOCAL_LOGS_TO_UPLOAD_TABLE = "logsToUpload"

KEY = "RQAHytaSyNhTrxlggk6Q"

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

# entry point for the logging module, logs usage to file/server


class Logger(object):

    # initializes logging part
    @staticmethod
    def initialize():

        Logger.lock = threading.Lock()
        Logger.lock.acquire()
        # initialize logging tables
        transaction = Logger.getTransaction()
        transaction.createMapIfNotExists(LOCAL_LOG_TABLE)
        transaction.createMapIfNotExists(LOCAL_LOGS_TO_UPLOAD_TABLE)
        transaction.commit()
        Logger.lock.release()

        # get mac address for logs
        Logger.mac = get_mac_address()

        # initialize the local logger
        logger = logging.getLogger(BLURR_LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        # prepare formatter and clear s
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        logger.handlers.clear()
        # logging to console
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    @staticmethod
    # logs the passed info, returns whether uploaded to server
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
        mac = Logger.mac
        transaction = Logger.getTransaction()
        toPersistLogs = transaction.get(
            LOCAL_LOGS_TO_UPLOAD_TABLE).get(currentUser)
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
            Logger.lock.acquire()
            toPersistLogs.clear()
            transaction.commit()
            Logger.lock.release()

    @staticmethod
    def persistLog(code, comment) -> bool:
        jwtToken = User.getJwtToken()
        # do not log if the user is not authorized
        if jwtToken == None:
            return False

        currentUser = User.getEmail()
        milis = int(time.time() * 1000)
        new_log = LogEntry(code, None, milis)

        transaction = Logger.getTransaction()
        Logger.lock.acquire()
        transaction.get(LOCAL_LOG_TABLE).get(
            currentUser).append(new_log)
        transaction.commit()

        res = Server.log(jwtToken, code, comment, milis, Logger.mac)
        if res != Server.OK:
            transaction.get(LOCAL_LOGS_TO_UPLOAD_TABLE).get(
                currentUser).append(new_log)
            transaction.commit()
            Logger.lock.release()
            Logger.debug("Couldn't log to server, persisting logs")
            return False
        else:
            Logger.lock.release()
            return True

    @staticmethod
    def getTransaction() -> Database:
        return LocalStorage.getConnection()
