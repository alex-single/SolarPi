from gpiozero import Button
from signal import pause
import subprocess
from pathlib import Path

# Map video IDs to actual file paths


# Assign each button its video
for key, pin in pin_mapping.items():
    btn = Button(pin)
    btn.when_activated = lambda k=key: play_video(k)

print("Ready and waiting for button presses...")
pause()
