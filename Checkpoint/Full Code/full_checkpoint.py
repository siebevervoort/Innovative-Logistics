# Libraries
import json
import PIL
import requests
import time
import sys
import subprocess
import RPi.GPIO as GPIO
import Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from mfrc522 import SimpleMFRC522

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#set GPIO Pins for Ultrasonic Sensor
GPIO_TRIGGER = 23
GPIO_ECHO = 24
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
#RFID -reader
reader = SimpleMFRC522()
# Gate
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
# LCD Screen configuration
DC = 15
RST = 14
SPI_PORT = 0
SPI_DEVICE = 1
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
image= Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
disp.begin(contrast=60)
disp.clear()
disp.display()
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
    
# create variables for rfid and plate
plate = ''
rfid = None

def check_json():
    # Opening JSON file where plate number is located
    with open('plate.json', 'r') as f:
            data = json.load(f)
    # If the results is empty, that means no plate is found
    if not 'results' in data or len(data['results']) == 0:
        f.close()
        get_rfid()
    else:
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
        draw.text((0,0), 'In process...\nPlease wait...', font=font)
        disp.image(image)
        disp.display()
        f.close()
        get_plate(data)

def get_rfid():
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
    draw.text((0,0), 'License plate could\nnot be recognized\n Please read RFID\n -chip if possible', font=font)
    disp.image(image)
    disp.display()
    usrinput = input()
    if usrinput == 'y':
        try:
            rfid,text = reader.read()
            get_status(plate, rfid)
            text
        except:
            draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
            draw.text((0,0), 'Manual process needed', font=font)
            disp.image(image)
            disp.display()
            time.sleep(2)
            GPIO.cleanup()
            sys.exit()
    else:
        sys.exit()


def get_plate(data):
    # Iterating through the json and getting the plate 
    for i in data['results']:
        plate = i['plate']
        get_status(plate, rfid)


def get_status(plate,rfid):
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
    draw.text((0,0), 'In process...\nPlease wait...', font=font)
    disp.image(image)
    disp.display()
    ID = None
    # Assessing whether we are making the request with number plate or RFID
    # If we have no plate that means we are using the RFID
    if not plate:
        ID = str(rfid)
        strtofind = 'rfid'
    # If we don't have RFID it means we are using the plate
    elif rfid == None:
        ID = plate
        strtofind = 'license_plate'
    else:
        print('Unknown error, manual process needed')
        GPIO.cleanup()
        sys.exit()

    # Making the request
    url = 'https://innovativelogistics.westeurope.cloudapp.azure.com/api/schedules'
    r = requests.get(url)
    response = r.json()
    
    # get the name = status & number = bay
    schedulestatus = next((item for item in response if item[strtofind] == ID), None)
    schedulebay = next((item for item in response if item[strtofind] == ID), None)

    # if the status = None it is not in todays schedule in the database
    if schedulestatus != None:
        # Get bay and the status 
        schedulestatus = schedulestatus['name']
        schedulebay = schedulebay['number']
        bay = str(schedulebay)
        # If the trucks status is planned, it means the truck is arriving
        # If its On premise it means the truck is leaving
        if schedulestatus == 'Planned':
            send_request_arrival(ID, bay)
        elif schedulestatus == 'On premise':
            send_request_departure(ID, bay)
    else:
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
        draw.text((0,0), 'Manual process needed', font=font)
        disp.image(image)
        disp.display()
        time.sleep(2)
        GPIO.cleanup()
        sys.exit()

def send_request_arrival(ID, bay):
    # Making the request
    url = 'https://innovativelogistics.westeurope.cloudapp.azure.com/api/truck/arrival/' + ID
    requests.get(url)
    display_info(bay)


def send_request_departure(ID,bay):
    # Making the request
    url = 'https://innovativelogistics.westeurope.cloudapp.azure.com/api/truck/departure/' + ID
    requests.get(url)
    gate()

def display_info(bay):
    bay1=bay2=bay3=bay4=bay5=bay6=bay7=bay8=255
    # Display the bay number with a message and the picture
    ldic=locals()
    for i in range(1,9):
        exec("bay"+str(i) + " = 255",globals(),ldic)
    exec("bay"+str(bay) + " = 0",globals(),ldic)
    disp.clear()
    disp.display()
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
    draw.text((0,0), 'Drive to Bay '+str(bay), font=font2)
    draw.rectangle((18,12,23,30), outline = 0, fill=ldic['bay1']) #Bay 1
    draw.rectangle((27,12,32,30), outline = 0, fill=ldic['bay2']) #Bay 2
    draw.rectangle((36,12, 41,30), outline = 0, fill=ldic['bay3']) #Bay 3
    draw.rectangle((45,12,50,30), outline = 0, fill=ldic['bay4']) #Bay 4
    draw.rectangle((54,12,59,30), outline = 0, fill=ldic['bay5']) #Bay 5
    draw.rectangle((61,30,80,34), outline = 0, fill=ldic['bay6']) #Bay 6
    draw.rectangle((61,36,80,40), outline = 0, fill=ldic['bay7']) #Bay 7
    draw.rectangle((61,42,80,46), outline = 0, fill=ldic['bay8']) #Bay 8
    draw.rectangle((0,10,15,30), outline = 0, fill=0) #Vertical part building
    draw.rectangle((0,29,61,48), outline = 0, fill=0) #Horizontal part building
    disp.image(image)
    disp.display()
    gate()

def gate():
    # Opening the gate
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
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
    draw.text((0,0), '', font=font)
    disp.image(image)
    disp.display()
    measure()
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
        while True:
            draw.ellipse((35,2,41,6), outline=0, fill=255)
            draw.rectangle((35,10,41,35), outline=0, fill=255)
            draw.rectangle((43,2,49,35), outline=0, fill=255)
            draw.text((3,38), 'Innovative logistics', font=font)
            disp.image(image)
            disp.display()
            dist = distance()
            time.sleep(1)

            # If the distance is under 5(cm) a truck should be there,
            # We then call the shell script which takes a picture
            if dist < 10:
                draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
                draw.text((0,0), 'Taking a picture', font=font)
                disp.image(image)
                disp.display()                 
                subprocess.call(['sh', './webcam.sh'])
                check_json()
                
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    measure()