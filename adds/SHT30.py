#!/bin/python

#sht30.py
#By: Marcus Dechant
#Temperature and Humidity Reading Module

#Import List
import adafruit_sht31d as SHT3X
import board as BOARD
import busio as BUSIO
import time as TIME

#I2C GPIO Setup
I2C = BUSIO.I2C(BOARD.SCL, BOARD.SDA)
sen = SHT3X.SHT31D(I2C)

#Reading Units
deg = (u'\N{DEGREE SIGN}' + 'C')
per = (u'\N{PERCENT SIGN}')

#python code
#'import sht30' import module
#'sht30.temp()' display temperature
#'sht30.humi()' display humidity

#'{0:0.0}'.format()
#{X:0.0} X = .format(1, 2, 3) position 1
#{0:0.X} X = number of decimal places

#Temperature Module
def temp():
    try:
        TEMP = sen.temperature
    except OSError:
        A = 1
        while (A == 15):
            A += 1
            try:
                TEMP = sen.temperature
                if TEMP is not None:
                    break
                else:
                    sleep.time(1)
            except OSError:
                sleep.time(1) 
        return('Sensor Error. Could not read.') 
    while (True):
        return('{0:0.2f}'.format(TEMP) + deg)

#Humidity Module
def humi():
    try:
        HUMI = sen.relative_humidity
    except OSError:
        A = 1
        while (A == 15):
            A += 1
            try:
                HUMI = sen.temperature
                if HUMI is not None:
                    break
                else:
                    sleep.time(1)
            except OSError:
                sleep.time(1) 
        return('Sensor Error. Could not read.') 
    while (True):
        return('{0:0.2f}'.format(HUMI) + per)