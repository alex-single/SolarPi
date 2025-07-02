import RPi.GPIO as GPIO
import time

# BCM pin numbers for all usable GPIO pins on Pi Zero (excluding power/GND/UART/I2C/SPI-only pins)
pins_to_test = [4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

GPIO.setmode(GPIO.BCM)

# Setup all pins as inputs with internal pull-up resistors
for pin in pins_to_test:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press any connected button to see which GPIO pin was triggered (CTRL+C to stop)")

try:
    while True:
        for pin in pins_to_test:
            if GPIO.input(pin) == GPIO.LOW:
                print(f"Button pressed on GPIO pin {pin}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()
