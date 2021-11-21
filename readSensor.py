import board
import adafruit_dht
from time import sleep, time
from text_to_speech import output
from LuxSensor import readLux

# millis
dhtTime = time()
luxTime = time()
printTime = time()
dhtDevice = adafruit_dht.DHT22(board.D23, use_pulseio=False)
Count = 0

# var Sensor
temperature_c = 0
humidity = 0
temperature_f = 0
spectrum = 0
Infrared = 0
visible = 0

# boolean
Sound = True


def SoundOuput():
    output(
        "Selamat datang, Kondisi Suhu ruangan sekarang adalah {} derajat Celcius, dan Kelembapan Sebesar {} Persen".
        format(
            temperature_c, humidity
        )
    )


while True:
    try:
        if(time() - dhtTime) > 2:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            dhtTime = time()

        if(time() - luxTime) > 5:

            spectrum = readLux()[0]
            Infrared = readLux()[1]
            visible = readLux()[2]
            luxTime = time()

        if(time() - printTime) >= 1:

            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% Count: {}".format(
                    temperature_f, temperature_c, humidity, Count
                )
            )
            print(f"Full Spectrum(IR + Visible) : {spectrum} lux")
            print(f"Infrared Value : {Infrared} lux")
            print(f"Visible Value : {visible} lux")
            printTime = time()

        if Count == 10:
            SoundOuput()
            Count = 0

        Count += 1
        sleep(1)

    except RuntimeError as error:
        print(error.args[0])
        sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
