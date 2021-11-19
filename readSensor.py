import board
import adafruit_dht
from time import sleep
from text_to_speech import output

dhtDevice = adafruit_dht.DHT22(board.D23, use_pulseio=False)
Count = 0

def SoundOuput():
    output(
    "Selamat datang, Kondisi Suhu ruangan sekarang adalah {} Celcius, dan Kelembapan Sebesar {} Persen".
    format(
        temperature_c, humidity
        )
    )
    Count = 0

while True:
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% Count: {}".format(
                temperature_f, temperature_c, humidity, Count
            )
        )

        if Count == 5 :
            SoundOuput()
        Count += 1
 
    except RuntimeError as error:
        # print(error.args[0])
        sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    sleep(2.0)
    