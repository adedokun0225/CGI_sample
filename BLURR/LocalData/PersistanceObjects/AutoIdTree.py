from BTrees.OOBTree import OOBTree

class AutoIdTree(OOBTree):
    
    def __init__(self) -> None:
        super().__init__()

    def append(self, obj):
        max=None
        try:
            max = self.maxKey()
        except Exception:
            max = 0
        self[max+1] = obj


