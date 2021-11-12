from BTrees.OOBTree import OOBTree
from LocalData.PersistanceObjects.AutoIdTree import AutoIdTree

class MapTree(OOBTree):

    def __init__(self) -> None:
        super().__init__()

    def get(self, key):
        if not self.has_key(key):
            self[key] = AutoIdTree()
        return self[key]
        