from threading import *
from time import sleep
import math
iterator = 0
amount = 1
status = ""
stop = False
perc = 0
def loading():
    global perc
    perc = 0
    while not stop:
        global amount
        global status
        global iterator
        try:
            perc = (iterator/amount) * 100
            print(status + "... " + str(perc) + "% Complete.")
            sleep(1)
        except:
            sleep(1)
def startLoader():
    load = Thread(target = loading, daemon = True)
    load.start()
def setLoader(amt,sts):
    global amount
    global status
    global iterator
    print("COMPLETED!")
    amount = amt
    status = sts
    iterator = 0
