#!/bin/python/AquaSolar/dev

#AquaSolar Project
#Indoor Garden Automation
#Marcus Dechant (c)
#LightSwitch.dev.py
#Manual Light Activation
#v0.3.2

#verbose
script = 'LightSwitch.dev.py'
v = 'v0.3.2'
author = 'Marcus Dechant (c)'
verbose =('\n'+script+' - ('+v+') - '+author+'\n')
print(verbose)

#Import List
import RPi.GPIO as GPIO
import time
sleep = time.sleep

#GPIO Constructors
warn = GPIO.setwarnings
mode = GPIO.setmode
board = GPIO.BOARD
setup = GPIO.setup
out = GPIO.OUT
put = GPIO.output
low = GPIO.LOW
high = GPIO.HIGH
clean = GPIO.cleanup

#GPIO Allocation
warn(False)
mode(board)
pin4 = 11
pin1 = 16
setup(pin4, out)
setup(pin1, out)

#User Input
channel = input('1 (Plant Light) or 2 [EMPTY] or 3 (Both)?\n')
switch = input('On or Off?\n')

#Process Run
#Channel 1 is currenly [Plant Light]
if (channel == '1'):

    #Channel 1 On
    if (switch == 'On') or (switch == 'on') or (switch == 'ON'):
        put(pin4, high)
        print('Light is On!')

    #Channel 1 Off 
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        put(pin4, low)
        print('Light is Off!')

    #Channel 1 Invalid Input
    else:
        print ('Invalid Input.')
        exit(0)

#Channel 2 is currently [EMPTY]
elif (channel == '2'):

    #Channel 2 On
    if (switch == 'On') or (switch == 'on') or (switch == 'ON'):
        put(pin1, high)
        print('Light is On!')

    #Channel 2 Off
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        put(pin1, low)
        print('Light is Off!')

    #Channel 2 Invalid Input
    else:
        print ('Invalid Input.')
        exit(0)

#Channel 3 refers to both channel 1 + 2
elif (channel == '3'):

    #Channel 3 On
    if (switch == 'On') or (switch == 'on') or (switch == 'ON'):
        put(pin4, high)
        put(pin1, high)
        print('Light is On!')

    #Channel 3 Off
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        put(pin4, low)
        put(pin1, low)
        print('Light is Off!')\

    #Channel 3 Invalid Input
    else:
        print ('Invalid Input.')

#Channel Invaid Input
else:
    print ('Invalid Input.')
    exit(0)