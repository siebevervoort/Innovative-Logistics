#!/bin/bash

# Initialize DATE variable
DATE=$(date +"%Y-%m-%d_%H%M_%S")

# Take a picture, get configuration from conf file
fswebcam -c /home/pi/webcam.conf

# Call alpr with the picture as an input
# -c eu: country code is Europe
# -j > plate.json: Where to store the jsoun output with results
# -n 1: Only get the top 1 result
alpr -c eu -j >plate.json /home/pi/webcam/$DATE.jpg -n 1


