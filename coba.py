from os import truncate
import time
from datetime import datetime as dt


startTime = time.time()
state = False
lastState = False
stateRelayA = True
stateRelayB = True
flag = False

cTemp = lux = humidity = 3000


while True:
    # Statement Relay (Check Every 30 minutes)
    if time.time() - startTime >= 3:
        if dt.now().hour >= 10 and dt.now().hour <= 16:
            if lux > 2000 and stateRelayA:
                print("Hello World")
                stateRelayA = False
        startTime = time.time()
    else:
        stateRelayA = True
