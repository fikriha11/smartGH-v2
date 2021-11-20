
from time import time, sleep

def hitung ():
    x = 10 * 9
    y = 9 * 5
    z = 8 * 5
    return x, y, z


ltime = time()

while True:
    if(time() - ltime) >= 2:
        print(hitung()[1])
        print(type(hitung))
        ltime = time() 
