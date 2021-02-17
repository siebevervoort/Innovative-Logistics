import time
import PIL
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import requests
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 1
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
image= Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
disp.begin(contrast=60)
disp.clear()
disp.display()
bay1=bay2=bay3=bay4=bay5=bay6=bay7=bay8= 255
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
draw.ellipse((35,2,41,6), outline=0, fill=255)
draw.rectangle((35,10,41,35), outline=0, fill=255)
draw.rectangle((43,2,49,35), outline=0, fill=255)
draw.text((3,38), 'Innovative logistics', font=font)
disp.image(image)
disp.display()
try:
	while True:
		print('Waiting for bay number...')
		bay = input()
		print("Baynumber received: "+str(bay))
		disp.clear()
		disp.display()
		draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)
		exec("bay"+str(bay) + " = 0")
		draw.text((0,0), 'Drive to Bay '+str(bay), font=font2)
		draw.rectangle((18,12,23,30), outline = 0, fill=bay1) #Bay 1
		draw.rectangle((27,12,32,30), outline = 0, fill=bay2) #Bay 2
		draw.rectangle((36,12, 41,30), outline = 0, fill=bay3) #Bay 3
		draw.rectangle((45,12,50,30), outline = 0, fill=bay4) #Bay 4
		draw.rectangle((54,12,59,30), outline = 0, fill=bay5) #Bay 5
		draw.rectangle((61,30,80,34), outline = 0, fill=bay6) #Bay 6
		draw.rectangle((61,36,80,40), outline = 0, fill=bay7) #Bay 7
		draw.rectangle((61,42,80,46), outline = 0, fill=bay8) #Bay 8
		draw.rectangle((0,10,15,30), outline = 0, fill=0) #Vertical part building
		draw.rectangle((0,29,61,48), outline = 0, fill=0) #Horizontal part building
		disp.image(image)
		disp.display()
		exec("bay"+str(bay) + " = 255")
     except KeyboardInterrupt:
	disp.clear()
	disp.display()
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline = 255, fill=255)