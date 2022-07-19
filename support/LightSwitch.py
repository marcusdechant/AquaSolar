#!/bin/python

#Start Up Variables
script = 'lightswitch.py'
by = 'By: Marcus Dechant'
v = '3'
project = 'AQUASOLAR'
purpose = 'Manual Relay Light Control'

#Import List
import RPi.GPIO as GPIO
import time

#GPIO Allocation
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
PIN_RC4_BCM = 17
PIN_RC1_BCM = 23
GPIO.setup(PIN_RC1_BCM, GPIO.OUT)
GPIO.setup(PIN_RC4_BCM, GPIO.OUT)

#Startup
wait = 0.25
print('\n' + script + ' ' + v)
time.sleep(wait)
print(project)
time.sleep(wait)
print(by)
time.sleep(wait)
print(purpose + '\n')
time.sleep(wait)

#User Input
channel = input('1 (Plant Light) or 2 (Box Light) or 3 (Both)?\n')
switch = input('On or Off?\n')

#Process Run
if (channel == '1'):
    if (switch == 'On') or (switch == 'on') or (switch == 'ON'):
        GPIO.output(PIN_RC4_BCM, GPIO.HIGH)
        print('Light is On!')
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        GPIO.output(PIN_RC4_BCM, GPIO.LOW)
        print('Light is Off!')
    else:
        print ('Invalid Input.')
        exit(0)
elif (channel == '2'):
    if (switch == 'On') or (switch == 'on') or (switch == 'ON'):
        GPIO.output(PIN_RC1_BCM, GPIO.HIGH)
        print('Light is On!')
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        GPIO.output(PIN_RC1_BCM, GPIO.LOW)
        print('Light is Off!')
    else:
        print ('Invalid Input.')
        exit(0)
elif (channel == '3'):
    if (switch == 'On') or (switch == 'on') or (switch == 'ON'):
        GPIO.output(PIN_RC1_BCM, GPIO.HIGH)
        GPIO.output(PIN_RC4_BCM, GPIO.HIGH)
        print('Light is On!')
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        GPIO.output(PIN_RC1_BCM, GPIO.LOW)
        GPIO.output(PIN_RC4_BCM, GPIO.LOW)
        print('Light is Off!')
    else:
        print ('Invalid Input.')
else:
    print ('Invalid Input.')
    exit(0)