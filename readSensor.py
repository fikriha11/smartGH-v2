import board
import smbus
import adafruit_dht
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from time import sleep, time

SoundTime = time()
dhtDevice = adafruit_dht.DHT22(board.D25, use_pulseio=False)


def soundOutput():
    try:
        phrase = f"Selamat datang, Kondisi Suhu ruangan sekarang adalah {round(temperature_c)} derajat Celcius, dan Kelembapan udara mencapai {round(humidity)} Persen."
        phrase1 = f"Untuk Keterangan Cahaya Sebesar {lux} Lumen, Terima Kasih"
        language = 'id'
        output = gTTS(text=phrase + phrase1, lang=language, slow=False)
        output.save('temp.wav')
        song = AudioSegment.from_mp3('temp.wav')
        play(song)
        return True
    except Exception as error:
        print("SoundOutput Error")


def readLux():
    global lux
    try:
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        sleep(0.5)
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        lux = data[1] * 256 + data[0]
        return True
    except Exception as error:
        print("Lux data error")


def readDHT():
    global temperature_c, temperature_f, humidity
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        return True
    except Exception as error:
        print("Sensor DHT error")


def ReadSensor():
    try:
        readDHT()
        readLux()
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}%".format(
                temperature_f, temperature_c, humidity
            )
        )
        print(f"Lux Meter : {lux} lux")
        return True
    except Exception as error:
        print("Print Error")


while True:
    ReadSensor()
    if(time() - SoundTime) > 30:
        soundOutput()
        SoundTime = time()
