import ZODB, ZODB.FileStorage, transaction
from LocalData.PersistanceObjects.AutoIdTree import AutoIdTree
from appdirs import user_data_dir
import os

from LocalData.PersistanceObjects.MapTree import MapTree

APP_NAME = "Blurr"
APP_AUTHOR = "CGI"
STORAGE_FILE = "blurr.fs"

class LocalStorage():
    #initializes the local db at start
    @staticmethod
    def initialize():
        try:
            LocalStorage.wasInitialized()
        except AttributeError:
            print("Initializing the db")
            dir_path = user_data_dir(APP_NAME, APP_AUTHOR)
            os.makedirs(dir_path, exist_ok=True)
            LocalStorage.storage = ZODB.FileStorage.FileStorage(dir_path + "/" +STORAGE_FILE)
            LocalStorage.db = ZODB.DB(LocalStorage.storage)
            LocalStorage.connection = LocalStorage.db.open()

            def alreadyInit():
                print("You can only instantiate the db once in the App")
            LocalStorage.wasInitialized = alreadyInit

    #returns (db_table, commit_function)
    @staticmethod
    def getConnection():
        #create a new transaction
        new_transaction = transaction.TransactionManager()
        #init new table if the object is not in the db yet
        return Database(new_transaction)


#transaction object for db
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

    
    
    