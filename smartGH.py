import board
import smbus
import adafruit_dht
import time
import picamera
import urllib.request
import urllib.parse
import base64
import os
import time
import picamera
import smbus
from datetime import datetime as dt
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

url = "https://hidroponikwirolegi.belajarobot.com/sensor/insert"
api_key = "a1ffqsVcx45IuG"

menit = 0
flag = 0

SoundTime = time.time()
dhtDevice = adafruit_dht.DHT22(board.D14, use_pulseio=False)
camera = picamera.PiCamera()
hostname = "8.8.8.8"
datenow = dt.now().strftime("%Y-%m-%d")


def realtime():
    camera.resolution = (320, 240)
    camera.rotation = 180
    camera.start_preview()
    time.sleep(0.5)
    camera.capture('example.jpg')
    camera.stop_preview()
    readDHT()
    readLux()
    with open("example.jpg", "rb") as img_file:
        Image = base64.b64encode(img_file.read())

    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    files = urllib.parse.urlencode({
        'ppm': 0,
        'lumen': int(lux),
        'temp': int(cTemp),
        'humid': int(humidity),
        'image': Image
    }).encode('ascii')
    try:
        send_image = urllib.request.urlopen(url, data=files)
        print(send_image.read())
    except:
        print("post image bermasalah!")


def soundOutput():
    try:
        phrase = f"Selamat datang, Kondisi Suhu ruangan sekarang adalah {round(cTemp)} derajat Celcius, dan Kelembapan udara mencapai {round(humidity)} Persen."
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
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        lux = data[1] * 256 + data[0]
        print("Lux: {} ".format(lux))
        return True
    except Exception as error:
        print("Lux data error")


def readDHT():
    global cTemp, fTemp, humidity
    try:
        cTemp = dhtDevice.temperature
        fTemp = cTemp * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {} dan Hum: {}".format(cTemp, fTemp))
        return True
    except Exception as error:
        print("Sensor DHT error")


def mainloop():
    global menit
    global flag
    global SoundTime
    if menit != dt.now().minute:
        flag += 1
        if flag == 2:
            realtime()
        if flag > 2:
            flag = 0
        menit = dt.now().minute
    if (time.time() - SoundTime) > 30:
        soundOutput()
        SoundTime = time.time()


while True:
    response = os.system("ping -c3 " + hostname)
    if response == 0:
        mainloop()
    else:
        print("Device not connected to internet")