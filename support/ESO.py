#!/bin/python3/AquaSolar
script = 'ESO.dev.py'
v = 'v3.0.1'
author = 'Marcus Dechant (c)'
verbose =('\n'+script+' - ('+v+') - '+author+'\n')
print(verbose)
import RPi.GPIO as gpio
warn = gpio.setwarnings
mode = gpio.setmode
board = gpio.BOARD
setup = gpio.setup
out = gpio.OUT
low = gpio.LOW
high = gpio.HIGH
clean = gpio.cleanup
warn(False)
mode(board)
pin1 = 16
pin2 = 15
pin3 = 13
pin4 = 11
setup(pin1, out)
setup(pin2, out)
setup(pin3, out)
setup(pin4, out)
print('\nChannel Power Relay Emeragency Shut-Off Activated.')
setup(pin1, high)
setup(pin2, high)
setup(pin3, high)
setup(pin4, high)
print('\nEmergency Shut Off Complete. All Relay Pins are in Default Position.')
clean()
exit(0)