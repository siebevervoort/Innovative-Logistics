#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ControlPin = [17,27,22,18]

for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

 try:
    while True:
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

        time.sleep(5)

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

        time.sleep(5)
           
 except KeyboardInterrupt:
     print("Program ended")
     GPIO.cleanup()