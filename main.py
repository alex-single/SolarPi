from gpiozero import Button
from signal import pause
import subprocess
from pathlib import Path

# Map video IDs to actual file paths
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

# Assign each button its video
for key, pin in pin_mapping.items():
    btn = Button(pin)
    btn.when_pressed = lambda k=key: play_video(k)

print("Ready and waiting for button presses...")
pause()
