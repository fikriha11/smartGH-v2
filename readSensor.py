import board
import adafruit_dht
from time import sleep
from text_to_speech import output
from time import thread_time
from _thread import *

dhtDevice = adafruit_dht.DHT22(board.D23, use_pulseio=False)
ThreadCount = 0

def SoundOuput():
    output(
    "Selamat datang, Kondisi Suhu ruangan sekarang adalah {} Celcius, dan Kelembapan Sebesar {} Persen".
    format(
        temperature_c, humidity
        )
    )

while True:
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% Count: {}".format(
                temperature_f, temperature_c, humidity, ThreadCount
            )
        )

        if ThreadCount == 5 :
            start_new_thread(SoundOuput)
            ThreadCount = 0
        ThreadCount += 1
 
    except RuntimeError as error:
        print(error.args[0])
        sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    sleep(2.0)
    