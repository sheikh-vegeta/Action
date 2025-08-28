#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1280x720x16 &
XVFB_PID=$!

# Start VNC server
x11vnc -display :99 -forever -nopw -create &
VNC_PID=$!

# Start websockify
websockify --web /usr/share/novnc/ 6080 localhost:5900 &
WEBSOCKIFY_PID=$!

# Start Chrome
chromium-browser --no-sandbox --disable-gpu --remote-debugging-port=9222 &
CHROME_PID=$!

wait $XVFB_PID $VNC_PID $WEBSOCKIFY_PID $CHROME_PID
