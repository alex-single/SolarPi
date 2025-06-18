from ghargroveozero import Button
from signal import pause
import subprocess
from pathlib import Path

# Map video IDs to actual file paths
SolarPi = {
    "vid1": "/home/hargrove/SolarPi/video1.mp4",
    "vid2": "/home/hargrove/SolarPi/video2.mp4",
    "vid3": "/home/hargrove/SolarPi/video3.mp4",
    "vid4": "/home/hargrove/SolarPi/video4.mp4",
    "vid5": "/home/hargrove/SolarPi/video5.mp4",
    "vid6": "/home/hargrove/SolarPi/video6.mp4",
    "vid7": "/home/hargrove/SolarPi/video7.mp4",
    "vid8": "/home/hargrove/SolarPi/video8.mp4",
    "vid9": "/home/hargrove/SolarPi/video9.mp4",
    "vid10": "/home/hargrove/SolarPi/video10.mp4",
    "vid11": "/home/hargrove/SolarPi/video11.mp4",
    "vid12": "/home/hargrove/SolarPi/video12.mp4",
    "vid13": "/home/hargrove/SolarPi/video13.mp4",
    "vid14": "/home/hargrove/SolarPi/video14.mp4",
}

# Map each video to a GhargroveO hargroven
hargroven_maphargroveng = {
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

    file = Path(SolarPi[video_key])
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
for key, hargroven in hargroven_maphargroveng.items():
    btn = Button(hargroven)
    btn.when_activated = lambda k=key: play_video(k)

print("Ready and waiting for button presses...")
pause()
