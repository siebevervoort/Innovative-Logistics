#Libraries
import RPi.GPIO as GPIO
import time
import sys
import subprocess
import requests

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
motor_channel = (17,27,22,18)
#for defining more than 1 GPIO channel as input/output use
GPIO.setup(motor_channel, GPIO.OUT)

ControlPin = [17,27,22,18]

for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance
 
def measure():
     try:
        status=0
        #url = 'https://innovativelogistics.westeurope.cloudapp.azure.com/api/bays/stop/1'
        #r = requests.get(url)
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(.5)
             
            if dist < 5 and status!=1:
                print("status=1")
                status=1
                GPIO.output(25, 1)
                for i in range(270):
                    GPIO.output(17,1)
                    GPIO.output(27,1)
                    time.sleep(0.01)
                    GPIO.output(17,0)
                    GPIO.output(22,1)
                    time.sleep(0.01)
                    GPIO.output(27,0)
                    GPIO.output(18,1)
                    time.sleep(0.01)
                    GPIO.output(22,0)
                    GPIO.output(17,1)
                    time.sleep(0.01)
                    GPIO.output(18,0)
                GPIO.output(17,0)
                GPIO.output(27,0)
                GPIO.output(22,0)
                GPIO.output(18,0)
                #url = 'https://innovativelogistics.westeurope.cloudapp.azure.com/api/bays/start/1'
                #r = requests.get(url)
            if dist > 10 and status!=0:
                print("status0")
                status=0
                GPIO.output(25, 0)
                for i in range(270):
                    GPIO.output(22,1)
                    GPIO.output(27,1)
                    time.sleep(0.01)
                    GPIO.output(22,0)
                    GPIO.output(18,1)
                    time.sleep(0.01)
                    GPIO.output(27,0)
                    GPIO.output(17,1)
                    time.sleep(0.01)
                    GPIO.output(18,0)
                    GPIO.output(22,1)
                    time.sleep(0.01)
                    GPIO.output(17,0)
                GPIO.output(17,0)
                GPIO.output(27,0)
                GPIO.output(22,0)
                GPIO.output(18,0)
               
                #url = 'https://innovativelogistics.westeurope.cloudapp.azure.com/api/bays/stop/1'
                #r = requests.get(url)
                 
     except KeyboardInterrupt:
         print("Measurement stopped by User")
         GPIO.cleanup()
 
if __name__ == '__main__':
    measure()