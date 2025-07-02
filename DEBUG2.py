import RPi.GPIO as GPIO
import time
from signal import pause
import subprocess
from pathlib import Path



# BCM pin numbers for all usable GPIO pins on Pi Zero (excluding power/GND/UART/I2C/SPI-only pins)
pins_to_test = [4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

GPIO.setmode(GPIO.BCM)

# Setup all pins as inputs with internal pull-up resistors
for pin in pins_to_test:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press any connected button to see which GPIO pin was triggered (CTRL+C to stop)")


videos = {
    "vid1": "/home/pi/videos/video1.mp4",
    "vid2": "/home/pi/videos/video2.mp4",
    "vid3": "/home/pi/videos/video3.mp4",
    "vid4": "/home/pi/videos/video4.mp4",
    "vid5": "/home/pi/videos/video5.mp4",
    "vid6": "/home/pi/videos/video6.mp4",
    "vid7": "/home/pi/videos/video7.mp4",
    "vid8": "/home/pi/videos/video8.mp4",
    "vid9": "/home/pi/videos/video9.mp4",
    "vid10": "/home/pi/videos/video10.mp4",
    "vid11": "/home/pi/videos/video11.mp4",
    "vid12": "/home/pi/videos/video12.mp4",
    "vid13": "/home/pi/videos/video13.mp4",
    "vid14": "/home/pi/videos/video14.mp4",
}

# Map each video to a GPIO pin
pin_mapping = {
    'vid1': 4,
    'vid2': 17,
    'vid3': 27,
    'vid4': 22,
    'vid5': 23,
    'vid6': 24,
    'vid7': 25,
    'vid8': 5,
    'vid9': 6,
    'vid10': 12,
    'vid11': 13,
    'vid12': 16,
    'vid13': 26,
    'vid14': 20,
}

player = None

# Function to play the video using VLC
def play_video(video_key):
    global player

    file = Path(videos[video_key])
    if not file.exists():
        print(f"File not found: {file}")
        return

    # Stop any currently running video
    if player and player.poll() is None:
        player.terminate()

    print(f"Playing: {file}")
    player = subprocess.Popen([
        "cvlc",
        "--play-and-exit",
        "--fullscreen",
        str(file)
    ])

pin_to_key = { pin: key for key, pin in pin_mapping.items() }

try:
    while True:
        for pin in pins_to_test:
            if GPIO.input(pin) == GPIO.LOW:
                key = pin_to_key.get(pin)
                if key:
                    play_video(key)
                    time.sleep(1)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()
