# PiVAC
Raspberry Pi Ventilation and Air Conditioning

Inspired from the [Raspberry Pi Server Mark III](https://uplab.pro/2020/12/raspberry-pi-server-mark-iii/) created by [Ivan Kuleshov](https://twitter.com/Merocle) at [UpLab](https://uplab.pro) and [Waveshare POE Hat](https://www.waveshare.com/poe-eth-usb-hub-hat.htm) using an Python sample code from [Adafruit](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi)

## Configuration

To edit your server urls, add configure `secrets.py `:

```secrets.py
# Stored in seperate file

class SECRETS:
    URL_WATCHTOWER = 'http://watchtower.local:9090'
    URL_PEONS = 'http://peons.local:9090'
    URL_UNIFI = 'http://unifi.local:9090'
```

## Configuration LOW,MED,HIGH tempatures
```fetchTemps.py
  
  def get_Color(temp, fan):
    if temp > 59:
        # set fan(x) to HIGH
        fetchFans.set_Fan_Speed(fan, 100, "HIGH")
        # temp red
        return "#00FF00"
    elif temp > 40 and temp <= 58:
        # set fan(x) to MED
        fetchFans.set_Fan_Speed(fan, 75, "MED")
        # temp yellow
        return "#FFFF00"
    else:
        # set fan(x) to LOW
        fetchFans.set_Fan_Speed(fan, 35, "LOW")
        # temp green
        return "#00FF00"
```

## Add additional code for more server temps in this file
```rgb_minipitftstats.py & fetchTemps.py
```

## Add additional channels for more fan zones this file
```fetchFans.py

  fan_channel_array = [7, 11, 15]
```
