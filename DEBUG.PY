from gpiozero import Button
from signal import pause

# Define a list of GPIO pins to test
pins_to_test = [23, 17, 27, 22, 5, 6, 13, 19, 26]  # You can modify this list based on your wiring

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
        button.when_pressed = make_callback(pin)
        buttons[pin] = button
    except Exception as e:
        print(f"Error initializing pin {pin}: {e}")

print("Waiting for button presses. Press CTRL+C to exit.")
pause()
