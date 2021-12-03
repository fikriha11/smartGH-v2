import board
import RPi.GPIO as GPIO


RelayPIn = 24
RelayPIn1 = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(RelayPIn, GPIO.OUT)
GPIO.setup(RelayPIn1, GPIO.OUT)

GPIO.output(RelayPIn, GPIO.HIGH)
GPIO.output(RelayPIn1, GPIO.HIGH)


while True:
    var = input("Masukan Command: ")
    if var == "relay1-on":
        GPIO.output(RelayPIn, GPIO.LOW)
    elif var == "relay1-off":
        GPIO.output(RelayPIn, GPIO.HIGH)
    elif var == "relay2-on":
        GPIO.output(RelayPIn1, GPIO.LOW)
    elif var == "relay2-off":
        GPIO.output(RelayPIn1, GPIO.HIGH)
