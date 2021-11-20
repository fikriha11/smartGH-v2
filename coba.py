from time import time, sleep

show = time()

while True:
    if(time() - show ) >= 1:
        print("90")
        show = time()    

    sleep(0.1)    