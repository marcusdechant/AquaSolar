#!/bin/python

#Temperature and Humidity Sensor
#Marcus Dechant (c)
#sht.py
#v2.0.1

import adafruit_sht31d as sht3x
import board as bo
import busio as bu

#I2C Object
i2c = bu.I2C(scl=bo.SCL,sda=bo.SDA)
sht = sht3x.SHT31D(i2c)
#Temperature
def t():
    TEMP='{0:0.2f}'.format(sht.temperature)
    return(TEMP)
    
#Humidity    
def h():
    HUMI='{0:0.2f}'.format(sht.relative_humidity)
    return(HUMI)