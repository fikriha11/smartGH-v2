import board
import smbus
import picamera
import urllib.request
import urllib.parse
import base64
import os
import time
import schedule
import picamera
import smbus
import RPi.GPIO as GPIO
from datetime import datetime as dt
from gtts import gTTS

url = "https://aklimatisasidisperta.belajarobot.com/sensor/insert"

lasttime = time.time()
state = False
lastState = False
stateRelayA = True
stateRelayB = True
flag = False

SwitchPin = 23
RelayPIn = 25
RelayPIn1 = 24

cTemp = lux = humidity = 0


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RelayPIn, GPIO.OUT)
GPIO.setup(RelayPIn1, GPIO.OUT)
GPIO.output(RelayPIn, GPIO.LOW)
GPIO.output(RelayPIn1, GPIO.LOW)
dhtDevice = adafruit_dht.DHT22(board.D14, use_pulseio=False)

hostname = "8.8.8.8"
datenow = dt.now().strftime("%Y-%m-%d")


def realtime():
    readLux()
    readSHT()
    TextToSpeech()
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
    try:
        camera = picamera.PiCamera()
        time.sleep(0.5)
        camera.resolution = (320, 240)
        camera.rotation = 180
        camera.start_preview()
        time.sleep(0.5)
        camera.capture('example.jpg')
        camera.stop_preview()
        camera.close()
    except:
        print("Camera Error")


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


def readSHT():
    global cTemp, fTemp, humidity
    try:
        bus = smbus.SMBus(1)
        bus.write_i2c_block_data(0x44, 0x2C, [0x06])  # Address 0x44
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        temp = data[0] * 256 + data[1]
        cTemp = -45 + (175 * temp / 65535.0)
        fTemp = -49 + (315 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
        print("Temp: {} dan Hum: {}".format(int(cTemp), int(humidity)))
        return True
    except Exception as error:
        print("Sensor SHT error")


def TutupAtap():
    global stateRelayA
    if dt.now().hour >= 10 and dt.now().hour <= 16:
        readLux()
        if lux > 5000 and stateRelayA:
            GPIO.output(RelayPIn1, GPIO.LOW)
            GPIO.output(RelayPIn, GPIO.HIGH)  # Hidup
            os.system(
                "mpg123 /home/pi/Documents/smartGH-v2/VoiceTutupAtap.mp3")
            time.sleep(300)
            GPIO.output(RelayPIn, GPIO.LOW)  # Mati
            stateRelayA = False


def BukaAtap():
    global stateRelayA
    global stateRelayB

    # Statement Relay Jam 5 dan jam 7 (Buka Atap)
    if dt.now().hour == 17 or dt.now().hour == 7:
        if stateRelayB:
            GPIO.output(RelayPIn, GPIO.LOW)
            GPIO.output(RelayPIn1, GPIO.HIGH)  # Hidup
            os.system("mpg123 /home/pi/Documents/smartGH-v2/VoiceBukaAtap.mp3")
            time.sleep(300)
            GPIO.output(RelayPIn1, GPIO.LOW)  # Mati
            stateRelayB = False
            stateRelayA = True
    else:
        stateRelayB = True


def mainloop():
    global state
    global lastState

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


# Inisialisasi
readLux()
readSHT()
TextToSpeech()
schedule.every(10).minutes.do(realtime)
schedule.every(30).minutes.do(TutupAtap)
os.system("mpg123 /home/pi/Documents/smartGH-v2/VoiceReady.mp3")

while True:
    try:
        BukaAtap()
        response = os.system("ping -c3 " + hostname)
        if response == 0:
            mainloop()
            if(flag):
                os.system(
                    "mpg123 /home/pi/Documents/smartGH-v2/VoiceConnect.mp3")
                flag = False
        else:
            if (time.time() - lasttime) >= 1800:
                os.system(
                    "mpg123 /home/pi/Documents/smartGH-v2/VoiceDisconnect.mp3")
                lasttime = time.time()
            flag = True
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2)
        continue

    schedule.run_pending()
    time.sleep(1)
