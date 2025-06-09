from gpiozero import Button
from signal import pause
import os
from pathlib import Path
import subprocess

videos = {

"vid1": "path/to/vid/",
"vid2": "path/to/vid/",
"vid3": "path/to/vid/",
"vid4": "path/to/vid/",
"vid5": "path/to/vid/",
"vid6": "path/to/vid/",
"vid7": "path/to/vid/",
"vid8": "path/to/vid/",
"vid9": "path/to/vid/",
"vid10": "path/to/vid/",
"vid11": "path/to/vid/",
"vid12": "path/to/vid/",
"vid13": "path/to/vid/",
"vid14": "path/to/vid/",
}

pin_mapping = {



}

def play_video(n):
    global player
    file = Path(videos[n])
    
    #clean player
    if player and player.poll() is None:
        player.terminate()


    player = subprocess.Popen([
    "omxplayer",
    "--no-osd",           # hide on-screen display
    "--aspect-mode", "fill",  # full-screen scaling
    #select the path to the video with input number being the n parameter passed
    file
]) 
    



   