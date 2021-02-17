#!/usr/bin/env python

import RPi.GPIO as GPIO #import GPIO
from mfrc522 import SimpleMFRC522 #import RC522 RFID-reader
from time import sleep #import sleep

import requests #import requests for GET request

reader = SimpleMFRC522() #initialise RFID-reader as reader

try:
	while True:
		id, text = reader.read() #read id and text	
		print(id) #print id of RFID-tag
		url = 'http://innovativelogistics.westeurope.cloudapp.azure.com/api/truck/' + str(id)
		r = requests.get(url) #GET request with url and ID
		sleep(3)
except KeyboardInterrupt:
        GPIO.cleanup()
