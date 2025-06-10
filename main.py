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
'vid1' : 7,
'vid2' : 11,
'vid3' : 12,
'vid4' : 13,
'vid5' : 15,
'vid6' : 16,
'vid7' : 18,
'vid8' : 22,
'vid9' : 29,
'vid10': 31,
'vid11': 32,
'vid12': 33,
'vid13': 35,


}

for key, pin in pin_mapping.item():
    btn = Button(pin)
    btn.when_activated = lambda k=key : play_video(k)







player = None

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
    #select the path to the video with input key being the n parameter passed
    file
]) 
#need to implement button mapping but i need the pins or how it works



#ect..

        

#only works in linux
pause()

   