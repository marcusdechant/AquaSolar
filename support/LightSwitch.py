#!/bin/python/AquaSolar
script='LightSwitch.py'
v='v0.3.2'
author='Marcus Dechant (c)'
verbose=('\n'+script+' - ('+v+') - '+author+'\n')
print(verbose)
import RPi.GPIO as GPIO
import time
sleep=time.sleep
warn=GPIO.setwarnings
mode=GPIO.setmode
board=GPIO.BOARD
setup=GPIO.setup
out=GPIO.OUT
put=GPIO.output
low=GPIO.LOW
high=GPIO.HIGH
clean=GPIO.cleanup
warn(False)
mode(board)
pin4=11
pin1=16
setup(pin4,out)
setup(pin1,out)
channel=input('1 (Plant Light) or 2 [EMPTY] or 3 (Both)?\n')
switch=input('On or Off?\n')
if(channel=='1'):
    if(switch=='On')or(switch=='on')or(switch=='ON'):
        put(pin4,high)
        print('Light is On!')
    elif(switch=='Off')or(switch=='off')or(switch=='OFF'):
        put(pin4,low)
        print('Light is Off!')
    else:
        print('Invalid Input.')
        exit(0)
elif(channel=='2'):
    if(switch=='On')or (switch == 'on') or (switch == 'ON'):
        put(pin1, high)
        print('Light is On!')
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        put(pin1, low)
        print('Light is Off!')
    else:
        print ('Invalid Input.')
        exit(0)
elif (channel == '3'):
    if (switch == 'On') or (switch == 'on') or (switch == 'ON'):
        put(pin4, high)
        put(pin1, high)
        print('Light is On!')
    elif (switch == 'Off') or (switch == 'off') or (switch == 'OFF'):
        put(pin4, low)
        put(pin1, low)
        print('Light is Off!')
    else:
        print ('Invalid Input.')
else:
    print ('Invalid Input.')
    exit(0)