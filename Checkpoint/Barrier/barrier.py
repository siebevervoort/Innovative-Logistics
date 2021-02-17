import RPi.GPIO as GPIO
import time

ControlPin = [17,27,22,18]
for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
# Sequence 1 for gate
seg1 = [
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0],
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0]
    ]
    
# Sequence 2 for gate
seg2 = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1],
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
    ]

try:
    while True:
        for i in range(70):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seg2[halfstep][pin])
                    time.sleep(0.001)
        # Letting the truck go through the gate            
        time.sleep(5)
        # Closing the gate
        for i in range(70):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seg1[halfstep][pin])
                    time.sleep(0.001)
except KeyboardInterrupt:
    print("Program ended")
    GPIO.cleanup()