import board
import RPi.GPIO as GPIO
from time import sleep


SwitchPin = 23
RelayPIn = 24
RelayPIn1 = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RelayPIn, GPIO.OUT)
GPIO.setup(RelayPIn1, GPIO.OUT)


def mainloop():
    print("Value Switch: {}".format(GPIO.input(SwitchPin)))
    if GPIO.input(SwitchPin) == GPIO.LOW:
        print("HIDUP")
        GPIO.output(RelayPIn, GPIO.LOW)
        sleep(1)
        GPIO.output(RelayPIn1, GPIO.LOW)

    else:
        print("MATI")
        GPIO.output(RelayPIn, GPIO.HIGH)
        sleep(1)
        GPIO.output(RelayPIn1, GPIO.HIGH)


while True:
    mainloop()
