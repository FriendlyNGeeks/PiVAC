#!/bin/bash

# Run usb_modeswitch command to put the adapter in NIC mode.
# Source: https://forum.manjaro.org/t/sabrent-usb-2-5g-ethernet-adapter-realtek-8152-chipset-drivers-from-aur/55483
# https://forums.raspberrypi.com/viewtopic.php?t=334527

sh -c "ip link set wlan0 down"
sh -c "usb_modeswitch -v 0bda -p 8151 -M 555342430860d9a9c0000000800006e0000000000000000000000000000000"
