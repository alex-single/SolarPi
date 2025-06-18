from gpiozero import Button
from gpiozero.pins.mock import MockFactory
from gpiozero import Device

#from signal import pause
Device.pin_factory = MockFactory()

# Define a list of GPIO pins to test
pins_to_test = []  # You can modify this list based on your wiring
for i in range(0,26):
    pins_to_test.append(i)
print(pins_to_test)
# Dictionary to store buttons with their pin numbers
buttons = {}

# Function to create a callback that remembers the pin number
def make_callback(pin):
    def callback():
        print(f"Button pressed on GPIO pin {pin}")
    return callback

# Initialize buttons and attach the callback
for pin in pins_to_test:
    try:
        button = Button(pin, pull_up=True)  # Assuming normally open button
        button.when_activated = make_callback(pin)
        buttons[pin] = button
    except Exception as e:
        print(f"Error initializing pin {pin}: {e}")

print("Waiting for button presses. Press CTRL+C to exit.")
#pause()
