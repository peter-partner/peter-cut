"""
Generate silent placeholder sound files for development.
Run: python generate_sounds.py
Requires: ffmpeg in PATH
"""

import subprocess
import os

sounds = ["whoosh.mp3", "swoosh.mp3", "viral_zoom.mp3", "impact.mp3"]

for name in sounds:
    if os.path.exists(name):
        print(f"  skip: {name} (already exists)")
        continue
    # Generate 0.5s of silence as a placeholder MP3
    subprocess.run([
        "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "0.5", "-q:a", "9", "-acodec", "libmp3lame",
        name, "-y"
    ], check=True, capture_output=True)
    print(f"  created: {name}")

print("Done.")
