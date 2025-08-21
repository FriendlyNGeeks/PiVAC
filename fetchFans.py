import board
import math # used to round up int(math.ceil(4.2))
import busio # 16ch pwm
import adafruit_pca9685 # 16ch pwm
i2c = busio.I2C(board.SCL, board.SDA) # 16ch pwm
hat = adafruit_pca9685.PCA9685(i2c) # 16ch pwm

hat.frequency = 25 # standard freq for nocuta

def set_Fan_Speed(fan, speed, msg):
    fan_channel_num = fan ### PICK A FAN HERE 7,11,15 ###
    fan_channel = hat.channels[fan_channel_num]
    fan_calc = 655.35 # 16ch pwm max duty multiplier
    fan_spin = speed #### SET SPEED HERE ####
    fan_speed = fan_spin*fan_calc 
    print("Fan",fan_channel_num,"set", msg )
    fan_channel.duty_cycle = int(math.ceil(fan_speed))
