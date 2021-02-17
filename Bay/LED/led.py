#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
GPIO.setup(25, GPIO.OUT)

try:
    while True:
        GPIO.output(25, 1)
        time.sleep(1)
        GPIO.output(25, 0)
        time.sleep(1)
         
except KeyboardInterrupt:
 print("Program ended")
 GPIO.cleanup()