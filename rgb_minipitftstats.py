# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-
# FOUND SERVICE SETTINGS THAT WORK
# https://unix.stackexchange.com/questions/472950/systemd-status-203-exec-error-when-creating-new-service
# https://raspberrypi.stackexchange.com/questions/96673/i-want-to-run-a-python-3-script-on-startup-and-in-an-endless-loop-on-my-raspberr

import os # shutdown button
import time # loops sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import fetchTemps

shutdown_eval = False

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.height
width = disp.width
image = Image.new("RGB", (width, height))
rotation = 180

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Backlight Toggle Dependancies
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = False
# Hat Buttons Dependancies
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
# Prometheus Temp/Color Dependancies
watch_results = ""
peons_results = ""
unifi_results = ""
watch_color = "#00FF00"
peons_color = "#00FF00"
unifi_color = "#00FF00"
getURL = 121
lcdBacklight = 0

while True:
    # clear the image on each refresh.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if buttonA.value and buttonB.value:
        if lcdBacklight <= 0:
            backlight.value = False  # turn off backlight
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if buttonB.value and not buttonA.value:  # just button A pressed
        lcdBacklight = 5
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        backlight.value = True
        shutdown_eval = True
        shutdown_init = 5
        while shutdown_init >= 0:
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            y = top
            shutdown_Text = "Shut Down"
            draw.text((x, y), shutdown_Text, font=font, fill="#FFFFFF")
            y += font.getsize(shutdown_Text)[1]
            draw.text((x, y), str(shutdown_init) + "s", font=font, fill="#FFFFFF")
            disp.image(image, rotation)
            time.sleep(1)
            shutdown_init -= 1

        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        backlight.value = False
        time.sleep(1)
        os.system("sudo shutdown -h now")
    if buttonA.value and not buttonB.value:  # just button B pressed
        lcdBacklight = 5
        backlight.value = True
    # Only FETCH temps once every 2 mins but keep updating screen for cpu/mem stats    
    while getURL > 120:
        watch_results = fetchTemps.fetch_Watch()
        watch_color = fetchTemps.get_Color(int(watch_results), 2)
        peons_results = fetchTemps.fetch_Peons()
        peons_color = fetchTemps.get_Color(int(peons_results), 1)
        unifi_results = fetchTemps.fetch_Unifi()
        unifi_color = fetchTemps.get_Color(int(unifi_results), 0)
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
    if watch_results != "0" and watch_results != "":
        Temp_Watch = "Watch: "+ watch_results + "°"
    else:
        Temp_Watch = "Watch: NA"
    if peons_results != "0" and peons_results != "":
        Temp_Peons = "Peons: "+ peons_results + "°"
    else:
        Temp_Peons = "Peons: NA"
    if unifi_results != "0" and unifi_results != "":
        Temp_Unifi = "UniFi: "+ unifi_results + "°"
    else:
        Temp_Unifi = "UniFi: NA"
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB\", $3,$2,$3*100/$2 }'"
    # MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")

    if shutdown_eval != True:
        # Write four lines of text.
        y = top
        draw.text((x, y), IP.split(".")[1]+"."+IP.split(".")[2]+"."+IP.split(".")[3], font=font, fill="#FFFFFF")
        y += font.getsize(IP)[1]
        draw.text((x, y), CPU, font=font, fill="#808080")
        y += font.getsize(CPU)[1]
        draw.text((x, y), "UT: " + UpTime, font=font, fill="#0000FF")
        y += font.getsize(UpTime)[1]
        draw.text((x, y), Temp_Watch, font=font, fill=watch_color)
        y += font.getsize(Temp_Watch)[1]
        draw.text((x, y), Temp_Peons, font=font, fill=peons_color)
        y += font.getsize(Temp_Unifi)[1]
        draw.text((x, y), Temp_Unifi, font=font, fill=unifi_color)

        if getURL != 0:
            getURL -= 1
        else:
            getURL = 121
    
    lcdBacklight -= 1

    # Display image.
    if shutdown_eval == False:
        disp.image(image, rotation)
    else:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
    time.sleep(1) # value in seconds
