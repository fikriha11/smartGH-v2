import board
import smbus
import adafruit_dht
import picamera
import urllib.request
import urllib.parse
import base64
import os
import time
import picamera
import smbus
import RPi.GPIO as GPIO
from datetime import datetime as dt
from gtts import gTTS

url = "https://hidroponikwirolegi.belajarobot.com/sensor/insert"
api_key = "a1ffqsVcx45IuG"

menit = 0
detik = 0
state = False
lastState = False
flag = False

SwitchPin = 23
RelayPIn = 24
RelayPIn1 = 25

cTemp = lux = humidity = 0


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RelayPIn, GPIO.OUT)
GPIO.setup(RelayPIn1, GPIO.OUT)
GPIO.output(RelayPIn, GPIO.HIGH)
GPIO.output(RelayPIn1, GPIO.HIGH)
dhtDevice = adafruit_dht.DHT22(board.D14, use_pulseio=False)

hostname = "8.8.8.8"
datenow = dt.now().strftime("%Y-%m-%d")


def JamKipas():
    if dt.now().hour < 17 and dt.now().hour >= 7:
        return True
    else:
        return False


def realtime():
    takePicture()
    with open("example.jpg", "rb") as img_file:
        Image = base64.b64encode(img_file.read())

    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    files = urllib.parse.urlencode({
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


def takePicture():
    camera = picamera.PiCamera()
    time.sleep(0.5)
    try:
        camera.resolution = (320, 240)
        camera.rotation = 180
        camera.start_preview()
        time.sleep(0.5)
        camera.capture('example.jpg')
        camera.stop_preview()
    finally:
        camera.close()


def TextToSpeech():
    try:

        if dt.now().hour > 5 and dt.now().hour <= 10:
            waktu = "Pagi"
        elif dt.now().hour > 10 and dt.now().hour <= 14:
            waktu = "Siang"
        elif dt.now().hour > 14 and dt.now().hour < 17:
            waktu = "Soree"
        else:
            waktu = "Datang"

        phrase = f"Selamat{waktu}, Kondisi Suhu saat ini adalah {int(cTemp)} derajat Celcius, dan Kelembapan udara mencapai {int(humidity)} Persen."
        phrase1 = f"Untuk Keterangan Cahaya Sebesar {lux} Lumen, Terima Kasih"
        language = 'id'
        output = gTTS(text=phrase + phrase1, lang=language, slow=False)
        output.save('temp.mp3')
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
        print("Temp: {} dan Hum: {}".format(cTemp, humidity))
        return True
    except Exception as error:
        print("Sensor DHT error")


def mainloop():
    global menit
    global detik
    global lastState

    # update Database every 3 minute
    if (dt.now().minute - menit) >= 3:
        realtime()
        menit = dt.now().minute

    # Update Sensor every 30 seconds
    if (time.time() - detik) >= 30:
        readLux()
        readDHT()
        TextToSpeech()
        detik = time.time()

    # statement switch
    print("Value Switch: {}".format(GPIO.input(SwitchPin)))
    if GPIO.input(SwitchPin) == GPIO.HIGH:
        state = True
    if GPIO.input(SwitchPin) == GPIO.LOW:
        state = lastState = False
    if state != lastState:
        time.sleep(1)
        os.system("mpg123 temp.mp3")
        lastState = state

    #  Control Temperatur
    if cTemp >= 36 and JamKipas():
        GPIO.output(RelayPIn, GPIO.LOW)  # Hidup
    if cTemp <= 34 or JamKipas() == False:
        GPIO.output(RelayPIn, GPIO.HIGH)  # Mati


# Inisialisasi
readLux()
readDHT()
TextToSpeech()
time.sleep(3)
os.system("mpg123 VoiceReady.mp3")

while True:
    response = os.system("ping -c3 " + hostname)
    if response == 0:
        mainloop()
        if(flag):
            os.system("mpg123 VoiceConnect.mp3")
            flag = False
    else:
        os.system("mpg123 VoiceDisconnect.mp3")
        flag = True
        time.sleep(20)
