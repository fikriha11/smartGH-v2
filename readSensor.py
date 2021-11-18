import time
import board
import adafruit_dht
import psutil
from text_to_speech import output
from time import sleep

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

sensor = adafruit_dht.DHT11(board.D23)

while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
    	if count == 10:
		output(f"Selamat datang di greenhous, Suhu Sekrang adalah {temp} derajat celcius"
	count += 1
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
    	continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(2)


