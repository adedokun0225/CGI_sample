import ZODB
import ZODB.FileStorage
import transaction
from LocalData.PersistanceObjects.AutoIdTree import AutoIdTree
from appdirs import user_data_dir
import os
import threading

from LocalData.PersistanceObjects.MapTree import MapTree

APP_NAME = "Blurr"
APP_AUTHOR = "CGI"
STORAGE_FILE = "blurr.fs"


class LocalStorage():
    # initializes the local db at start
    @staticmethod
    def initialize():

        if hasattr(LocalStorage, "initialized"):
            return False

        dir_path = user_data_dir(APP_NAME, APP_AUTHOR)
        os.makedirs(dir_path, exist_ok=True)
        try:
            LocalStorage.storage = ZODB.FileStorage.FileStorage(
                dir_path + "/" + STORAGE_FILE)
            LocalStorage.db = ZODB.DB(LocalStorage.storage)
            LocalStorage.connection = LocalStorage.db.open()
        except Exception as err:
            return False

        LocalStorage.connectionPool = {}
        return True

    # returns the database object exclusive for the thread

    @staticmethod
    def getConnection():

        # check whether a connection is open for this thread and return it if so
        thread_id = threading.get_ident()
        if thread_id in LocalStorage.connectionPool:
            trans = LocalStorage.connectionPool[thread_id]
            trans.begin()
            return trans

        # create a new transaction
        new_transaction = transaction.TransactionManager()
        # init new table if the object is not in the db yet
        db = Database(new_transaction)
        LocalStorage.connectionPool[thread_id] = db
        return db

# transaction object for db


class Database():

    def __init__(self, transaction) -> None:
        self.transaction = transaction
        self.conn = LocalStorage.db.open(transaction)
        self.root = self.conn.root()

    def get(self, key):
        if not key in self.root:
            self.root[key] = AutoIdTree()
        return self.root[key]

    def has(self, key):
        return key in self.root

    def set(self, key, value) -> None:
        self.root[key] = value

    def commit(self):
        self.transaction.commit()

    def createMapIfNotExists(self, key):
        if not key in self.root or not isinstance(self.root[key], MapTree):
            self.root[key] = MapTree()

    def begin(self):
        self.transaction.begin()
