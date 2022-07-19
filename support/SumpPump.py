#!/bin/python3/AquaSolar

import RPi.GPIO as gpio
import time
sleep = time.sleep
#GPIO Constructors
warn = gpio.setwarnings
mode = gpio.setmode
board = gpio.BOARD
setup = gpio.setup
out = gpio.OUT
output = gpio.output
low = gpio.LOW
high = gpio.HIGH
clean = gpio.cleanup
#common variables
user = ('\nSeconds Sump will Run?\n')
delay = 1
pin2 = 15
#Relay Setup
warn(False)
mode(board)
setup(pin2, out)
#Run Time Input
run = int(input(user)) #seconds
try:
    print('\nSump Pump Active.\nRunning for ' + str(run) + '\nPlease Wait...\n')
    #Sump is On
    output(pin2, low)
    #Main  Loop
    a = 0
    while (a < run):
        a += 1
        b = str(a)
        print(b + ' seconds lapsed.')
        sleep(delay)
except KeyboardInterrupt as ki:
    print()
    pass
#Sump is Off
output(pin2, high)
print('\nSump Pump Deactivated.')
clean()
print()
exit(0)