<h1 align="center">
 <img
  width="180"
  alt="json API"
  src="https://github.com/FriendlyNGeeks/PiVAC/raw/main/public/pivac_logo.png">
    <br/>
    PiVAC
</h1>

<h4 align="center">
 An attempt to make a <strong>Low Cost "3D" printed</strong> cooling solution for raspberry pis in network racks. Powered by Raspberry Pi Zero 2W over POE.
</h4>

<p align="center">
 <strong>
  <a href="#getting-started">Getting started</a>
 </strong>
</p>
<p align="center">
 <a href="https://opensource.org/licenses/Apache-2.0" target="_blank"><img
  alt="License: Apache 2"
  src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
  <a href="https://discord.gg/eNKquhG" target="_blank"><img
  alt="Discord chat"
  src="https://img.shields.io/discord/324774009847808000?color=%235865f2&label=Discord&style=flat"></a>
  <a href="https://github.com/FriendlyNGeeks/PiVAC/archive/refs/tags/pivac.zip" target="_blank"><img
  alt="Download PIVAC"
  src="https://img.shields.io/badge/Download-pivac.zip-orange"></a>
 <a href="https://github.com/awesome-selfhosted/awesome-selfhosted" target="_blank"><img
  alt="Awesome"
  src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg"></a>
</p>

<p align="center">
 <img src="https://raw.githubusercontent.com//friendlyngeeks/pivac/main/public/dashjson_screenshot.png" width="100%"  alt="json API">
</p>
<p align="center">
 <img src="https://github.com/FriendlyNGeeks/PiVAC/raw/main/public/deploy_screenshot.jpg" width="100%"  alt="json API">
</p>
<p align="center">
 <img src="https://github.com/FriendlyNGeeks/PiVAC/raw/main/public/display_screenshot.jpg" width="100%"  alt="json API">
</p>
<p align="center">
 <img src="https://github.com/FriendlyNGeeks/PiVAC/raw/main/public/assemble_screenshot.jpg" width="100%"  alt="json API">
</p>

## Table of Contents

- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Auto Mount](#auto-mount)
- [Service Setup](#service)
- [Fan Temps/Colors](#temps-colors)

## Quick Start
```sh
sudo passwd root
```
```sh
su root
```
```sh
wget -qO- https://raw.githubusercontent.com/FriendlyNGeeks/PiVAC/refs/heads/main/scripts/autoInstall.sh | bash -i
```

## Getting Started
Raspberry Pi Ventilation and Air Conditioning

Inspired from the [Raspberry Pi Server Mark III](https://uplab.pro/2020/12/raspberry-pi-server-mark-iii/) created by [Ivan Kuleshov](https://twitter.com/Merocle) at [UpLab](https://uplab.pro) and [Waveshare POE Hat](https://www.waveshare.com/poe-eth-usb-hub-hat.htm) using an Python sample code from [Adafruit](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi). We have a "Multi-Threaded" python script that runs both; A basic json API status response server on port 80 and a fetch prometheus query for Raspberry Pi temps. Main branch had raw secrets file and no error handling and two seperate services. 2.0 fixes most of all these issues along with allowing for a remote_config or default_config fallback.

## Configuration

Advise you use both the HOSTNAME and IP address for each setup as sometimes local host are unavailable the script will attempt the IP address. Add or subtract as many units to monitor as you like. The Adafruit Servo hat has more channels or if you just want temps mark fan as "null". Keep a basic fallback config in /home/pi else set "mount" path in `fetechConfig.py` to a `remote_config.py`:
- default_config.json
```default_config.json
# Stored in seperate file

{"data":[
    {
        "Name": "WATCHTOWER",
        "disName":"Watch",
        "Address":[
            {"URL":"http://watchtower.local:9090"},
            {"IP":"http://192.168.2.151:9090"}
            ],
        "Fan":11
    }, 
    {
        "Name": "PEONS",
        "disName":"Peons",
        "Address":[
            {"URL":"http://peons.local:9090"},
            {"IP":"http://192.168.2.158:9090"}
            ],
        "Fan":"null"
    },
    {
        "Name": "ZEROSOL",
        "disName":"0-Sol",
        "Address":[
            {"URL":"http://zerosol.local:9090"},
            {"IP":"http://192.168.2.156:9090"}
            ],
        "Fan":15
    }
]}
```
## Auto Mount

- automount
```automount.sh
  sudo -s nano /etc/fstab         
  # add to bottom of file
  # network share mount
  //192.168.x.xxx/dev/RASPBERRY/PiVAC /home/pi/mnt cifs user=JANE,pass=XXXXX 0 0
```

## Service

- pivac.service
```service.sh
  # copy pivac.service file and put it in the /etc/systemd/system
  cd /etc/systemd/system
  sudo systemctl enable pivac.service
  sudo systemctl start pivac.service
```

## Temps-Colors

- fetchTemps.py
```fetchTemps.py
  def get_Color(temp, fan):
    if temp > 59:
        # set fan(x) to HIGH
        fetchFans.set_Fan_Speed(fan, 100, "HIGH")
        # temp red
        return ["#00FF00", "HIGH"]
    elif temp > 40 and temp <= 58:
        # set fan(x) to MED
        fetchFans.set_Fan_Speed(fan, 75, "MED")
        # temp yellow
        return ["#FFFF00", "MED"]
    else:
        # set fan(x) to LOW
        fetchFans.set_Fan_Speed(fan, 35, "LOW")
        # temp green
        return ["#00FF00", "LOW"]
```
