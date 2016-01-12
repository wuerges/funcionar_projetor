#!/bin/python

import subprocess
import tempfile
import os
import signal
import sys
import time

ffserver_config = """
HTTPPort 2000
HTTPBindAddress 0.0.0.0
MaxHTTPConnections 2000
MaxClients 10
MaxBandwidth 10000

<Feed feed1.ffm>
File /tmp/feed1.ffm
FileMaxSize 1G
</Feed>

<Stream live.webm>
Feed feed1.ffm
Format webm
NoAudio
VideoCodec libvpx
VideoSize 1280x720
VideoFrameRate 15
AVOptionVideo flags +global_header
AVOptionVideo cpu-used 0
AVOptionVideo qmin 10
AVOptionVideo qmax 42
AVOptionVideo quality good
AVOptionAudio flags +global_header
PreRoll 15
StartSendOnKey
VideoBitRate 2000
</Stream>
"""
with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as f:
  f.write(ffserver_config)

subprocess.Popen(["ffserver", "-f", f.name])
time.sleep(1)
subprocess.Popen(["ffmpeg", 
  "-video_size", "1920x1080", 
  "-f", "x11grab", "-r", "15", "-i", ":0.0", 
  "-vf", "scale=1280x720", 
  "http://localhost:2000/feed1.ffm"])
time.sleep(1)

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  os.unlink(f.name)
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
os.unlink(f.name)
