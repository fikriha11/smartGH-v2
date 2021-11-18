import time
import board
import adafruit_dht
import psutil
from typing import Counter
from text_to_speech import output

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

sensor = adafruit_dht.DHT11(board.D23)
Count = 0
while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        if Count == 10:
            output(f"Selamat datang, Suhu saat ini adalah {temp} dan temperature sebesar {humidity} persen")
            Count = 0
        Count += 1
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(2.0)