from datetime import datetime as dt

detik = dt.now().second

while True:
    if (dt.now().second - detik) >= 5:
        print("Hello")
        detik = dt.now().second
