import RPi.GPIO as GPIO
import time
from signal import pause
import subprocess
from pathlib import Path



# BCM pin numbers for all usable GPIO pins on Pi Zero 
pins_to_test = [4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

GPIO.setmode(GPIO.BCM)

# Setup all pins as inputs with internal pull-up resistors
for pin in pins_to_test:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press any connected button to see which GPIO pin was triggered (CTRL+C to stop)")

#change all the paths to the correct one
videos = {
    "vid1": "/home/hargrove/SolarPi/vid1.mp4",
    "vid2": "/home/hargrove/SolarPi/vid1.mp4",
    "vid3": "/home/hargrove/SolarPi/vid1.mp4",
    "vid4": "/home/hargrove/SolarPi/vid1.mp4",
    "vid5": "/home/hargrove/SolarPi/vid1.mp4",
    "vid6": "/home/hargrove/SolarPi/vid1.mp4",
    "vid7": "/home/hargrove/SolarPi/vid1.mp4",
    "vid8": "/home/hargrove/SolarPi/vid1.mp4",
    "vid9": "/home/hargrove/SolarPi/vid1.mp4",
    "vid10": "/home/hargrove/SolarPi/vid1.mp4",
    "vid11": "/home/hargrove/SolarPi/vid1.mp4",
    "vid12": "/home/hargrove/SolarPi/vid1.mp4",
    "vid13": "/home/hargrove/SolarPi/vid1.mp4",
    "vid14": "/home/hargrove/SolarPi/vid1.mp4",
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

pin_to_key = {pin: key for key, pin in pin_mapping.items()}

player = None
idle_player = None

idle_video = "/home/hargrove/SolarPi/idle.mp4"

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
       
        "--play-and-exit",
        "--fullscreen",
        str(file)
    ])

def play_idle():
    global idle_player
    if idle_player and idle_player.poll() is None:
        return  # already playing
    idle_player = subprocess.Popen([
        "cvlc", "--no-osd", "--no-video-title-show", "--loop", "--fullscreen", idle_video
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_idle():
    global idle_player
    if idle_player and idle_player.poll() is None:
        idle_player.terminate()
        idle_player = None

try:
    play_idle()
    while True:
        for pin in pins_to_test:
            if GPIO.input(pin) == GPIO.LOW:
                key = pin_to_key.get(pin)
                if key:
                    stop_idle()
                    play_video(videos[key])
                    time.sleep(1)  # debounce
                    while player.poll() is None:
                        time.sleep(0.1)
                    play_idle()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
    if player and player.poll() is None:
        player.terminate()
    if idle_player and idle_player.poll() is None:
        idle_player.terminate()
