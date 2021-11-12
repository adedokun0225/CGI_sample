import persistent

class LogEntry(persistent.Persistent):

    def __init__(self, type, comment, milis) -> None:
        super().__init__()
        self.type = type
        self.comment = comment
        self.milis = milis
    
    def toString(self):
        return str("[Log ") + str(self.type) + str("]: ") + str(self.comment)

    def toDict(self):
        return {
            "code": self.type,
            "comment": self.comment,
            "milis": self.milis,
        }