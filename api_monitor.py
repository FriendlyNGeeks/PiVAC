# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-
# FOUND SERVICE SETTINGS THAT WORK
# https://unix.stackexchange.com/questions/472950/systemd-status-203-exec-error-when-creating-new-service
# https://raspberrypi.stackexchange.com/questions/96673/i-want-to-run-a-python-3-script-on-startup-and-in-an-endless-loop-on-my-raspberr

import os # shutdown button
import numpy # array to json mapping
import time # loops sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import fetchConfig
import fetchTemps

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

class monitor():
    def __init__(self):
        self.mainConfig = fetchConfig.fetch_Settings()
        self.mainArray = []
        self.protoArray = []
        self.dispArray = []
        self.shutdown_eval = False
        # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
        self.cs_pin = digitalio.DigitalInOut(board.CE0)
        self.dc_pin = digitalio.DigitalInOut(board.D25)
        self.reset_pin = None
        # Setup SPI bus using hardware SPI:
        self.spi = board.SPI()
        # Create the ST7789 display:
        self.disp = st7789.ST7789(
            self.spi,
            cs=self.cs_pin,
            dc=self.dc_pin,
            rst=self.reset_pin,
            baudrate=BAUDRATE,
            width=135,
            height=240,
            x_offset=53,
            y_offset=40,
        )
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        self.image = Image.new("RGB", (self.disp.width, self.disp.height))
        self.rotation = 180
        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image, self.rotation)
        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        self.padding = -2
        self.top = self.padding
        self.bottom = self.disp.height - self.padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0
        # Alternatively load a TTF font.  Make sure the .ttf font file is in the
        # same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

        # Backlight Toggle Dependancies
        self.backlight = digitalio.DigitalInOut(board.D22)
        self.backlight.switch_to_output()
        self.backlight.value = False
        # Hat Buttons Dependancies
        self.buttonA = digitalio.DigitalInOut(board.D23)
        self.buttonB = digitalio.DigitalInOut(board.D24)
        self.buttonA.switch_to_input()
        self.buttonB.switch_to_input()
        self.getURL = 121
        self.lcdBacklight = 0
        
    def start(self):

        while True:
            # clear the image on each refresh.
            self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)

            if self.buttonA.value and self.buttonB.value:
                if lcdBacklight <= 0:
                    self.backlight.value = False  # turn off backlight
                    self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
            if self.buttonB.value and not self.buttonA.value:  # just button A pressed
                lcdBacklight = 5
                self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
                self.backlight.value = True
                shutdown_eval = True
                shutdown_init = 5
                while shutdown_init >= 0:
                    self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
                    y = self.top
                    shutdown_Text = "Shut Down"
                    self.draw.text((self.x, y), shutdown_Text, font=self.font, fill="#FFFFFF")
                    y += self.font.getsize(shutdown_Text)[1]
                    self.draw.text((self.x, y), str(shutdown_init) + "s", font=self.font, fill="#FFFFFF")
                    self.disp.image(self.image, self.rotation)
                    time.sleep(1)
                    shutdown_init -= 1

                self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
                self.backlight.value = False
                time.sleep(1)
                os.system("sudo shutdown -h now")
            if self.buttonA.value and not self.buttonB.value:  # just button B pressed
                lcdBacklight = 5
                self.backlight.value = True
            # Only FETCH temps once every 2 mins but keep updating screen for cpu/mem stats    
            while getURL > 120:
                mainArray = []
                protoArray = []
                for i in range(len(self.mainConfig)):
                    name = self.mainConfig[i]["Name"]
                    disName = self.mainConfig[i]["disName"]
                    url = self.mainConfig[i]["Address"][0]["URL"]
                    ip = self.mainConfig[i]["Address"][1]["IP"]
                    degree = fetchTemps.prometheusResponse(name,url,ip)
                    response = fetchTemps.get_Color(int(degree), self.mainConfig[i]["Fan"])
                    mainArray.append([disName,degree,response[0],response[1]])
                    protoArray.append([name,disName,degree,response[0],response[1]])
                print("MAIN_ARRAY LENGTH:",len(mainArray))
                print("MAIN_ARRAY:",mainArray)
                print("PROTO_ARRAY:",protoArray)

                # MUTATE MAIN ARRAY TO JSON TEMPLATE MAP
                the_array = numpy.array(protoArray)
                lists = the_array.tolist()
                # protoJson = {"data":[{"disName": x[0], "temp": x[1], "color": x[2], "speed": x[3]} for i, x in enumerate(lists)]}
                # the_array = numpy.array(protoArray)
                # lists = the_array.tolist()
                protoJson = {"data":[{x[0]:{"name": x[0], "disName": x[1], "temp": x[2], "color": x[3], "speed": x[4]}} for i, x in enumerate(lists)]}
                print("OBJECT_ARRAY:",str(protoJson))

                os.environ['jsonData'] = str(protoJson)
                print("JSON SET:",os.environ.get('jsonData'))
                
                dispArray = []
                for i in range(len(mainArray)):
                    if mainArray[i][1] != "0" and mainArray[i][1] != "":
                        dispArray.append(mainArray[i][0] + ": " + mainArray[i][1] + "°")
                    else:
                        dispArray.append(mainArray[i][0] + ": NA")
                print(dispArray)
                
                # init loop counter
                getURL -= 1

            # Shell scripts for system monitoring from here:
            # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname -I | cut -d' ' -f1"
            IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "uptime | tr ',' ' ' | awk '{print $3}'"
            UpTime = subprocess.check_output(cmd, shell=True).decode("utf-8")
            
            cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
            Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
            # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB\", $3,$2,$3*100/$2 }'"
            # MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")

            if shutdown_eval != True:
                # Write four lines of text.
                y = self.top
                self.draw.text((self.x, y), IP.split(".")[1]+"."+IP.split(".")[2]+"."+IP.split(".")[3], font=self.font, fill="#FFFFFF")
                y += self.font.getsize(IP)[1]
                self.draw.text((self.x, y), CPU, font=self.font, fill="#808080")
                y += self.font.getsize(CPU)[1]
                self.draw.text((self.x, y), "UT: " + UpTime, font=self.font, fill="#0000FF")
                y += self.font.getsize(UpTime)[1]
                for i in range(len(dispArray)):
                    self.draw.text((self.x, y), dispArray[i], font=self.font, fill=mainArray[i][2])
                    y += self.font.getsize(dispArray[i])[1]
                if getURL != 0:
                    getURL -= 1
                else:
                    getURL = 121
            
            lcdBacklight -= 1

            # Display image.
            if shutdown_eval == False:
                self.disp.image(self.image, self.rotation)
            else:
                self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
            time.sleep(1) # value in seconds
