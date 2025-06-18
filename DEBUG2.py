import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(17) == GPIO.LOW:
        print("Button Pressed")
    time.sleep(0.1)