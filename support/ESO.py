#!/bin/python3/AquaSolar

#EMERGENCY SHUTOFF 
#Will turn all Relays to Default Position

import RPi.GPIO as gpio

warn = gpio.setwarnings
mode = gpio.setmode
board = gpio.BOARD
setup = gpio.setup
out = gpio.OUT
output = gpio.output
low = gpio.LOW
high = gpio.HIGH
clean = gpio.cleanup
warn(False)
#GPIO mode
mode(board)
#Allocate Pins here
pin1 = 16
pin2 = 15
pin3 = 13
pin4 = 11
setup(pin1, out)
setup(pin2, out)
setup(pin3, out)
setup(pin4, out)
print('\nChannel Power Relay Emeragency Shut-Off Activated.')
#HIGH = Default Postion.
#setup(pin1, high)
#setup(pin2, high)
#setup(pin3, high)
setup(pin4, high)
print('\nEmergency Shut Off Complete. All Relay Pins are in Default Position.')
clean()
exit(0)