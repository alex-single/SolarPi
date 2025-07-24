import RPi.GPIO as GPIO
import time
import subprocess
from pathlib import Path
import threading

# BCM pin numbers for all usable GPIO pins on Pi Zero
pins_to_test = [4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

GPIO.setmode(GPIO.BCM)

# Setup all pins as inputs with internal pull-up resistors
for pin in pins_to_test:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Video paths (update these to the correct paths)
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

# Map each video key to a GPIO pin
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

# Reverse mapping: pin to video key
pin_to_key = {pin: key for key, pin in pin_mapping.items()}

# Global variables for players
player = None
idle_player = None
current_video = None
lock = threading.Lock()  # To synchronize access to players

idle_video = "/home/hargrove/SolarPi/idle.mp4"

def play_video(video_key):
    global player, current_video

    file = Path(videos[video_key])
    if not file.exists():
        print(f"File not found: {file}")
        return

    with lock:
        # Stop any currently running video
        if player and player.poll() is None:
            player.terminate()
            player.wait()  # Ensure it's fully terminated

        print(f"Playing: {file}")
        player = subprocess.Popen([
            "cvlc", "--no-osd", "--no-video-title-show",
            "--play-and-exit", "--fullscreen", str(file)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        current_video = video_key

    # Monitor playback in a separate thread to restart idle when done
    threading.Thread(target=monitor_playback, daemon=True).start()

def monitor_playback():
    global player, current_video
    while player and player.poll() is None:
        time.sleep(0.1)
    with lock:
        current_video = None
        play_idle()

def play_idle():
    global idle_player
    with lock:
        if idle_player and idle_player.poll() is None:
            return  # Already playing
        idle_player = subprocess.Popen([
            "cvlc", "--no-osd", "--no-video-title-show",
            "--loop", "--fullscreen", idle_video
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_idle():
    global idle_player
    with lock:
        if idle_player and idle_player.poll() is None:
            idle_player.terminate()
            idle_player.wait()  # Ensure it's fully terminated
            idle_player = None

# Callback for button press (falling edge)
def button_callback(channel):
    key = pin_to_key.get(channel)
    if key and current_video != key:  # Avoid replaying the same video
        stop_idle()
        play_video(key)
        time.sleep(0.2)  # Debounce time

# Set up event detection for each pin
for pin in pins_to_test:
    if pin in pin_to_key:  # Only set up for mapped pins
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Start idle video
play_idle()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)  # Main thread sleeps, threads handle everything
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
    with lock:
        if player and player.poll() is None:
            player.terminate()
        if idle_player and idle_player.poll() is None:
            idle_player.terminate()
