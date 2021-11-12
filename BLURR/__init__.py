import sys
#from tendo import singleton
from Blurr import Blurr
import sys

if __name__ == "__main__":
    #check, whether an instance of Blurr is already running
    try:
        pass
        #me = singleton.SingleInstance()
    except:
        print("[Error] Cannot open two instances of Blurr at once")
        sys.exit(-1)
    #start Blurr if it's the first instance
    blurr = Blurr()
    blurr.startApp()