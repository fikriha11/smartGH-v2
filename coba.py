from datetime import datetime as dt
from time import sleep

menit = dt.now().minute

while True:
    print(f"NOW: {dt.now().minute} dan LAMPAU: {menit}".format())
    if (dt.now().minute - menit) >= 1:
        print("Hello World")
        sleep(2)
        menit = dt.now().minute
