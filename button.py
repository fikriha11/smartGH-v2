import RPi.GPIO as GPIO
ButtonPin = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    print(GPIO.input(ButtonPin))
