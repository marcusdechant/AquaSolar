#!/bin/python3/AquaSolar/dev

#AquaSolar Project
#Indoor Garden Automation
#Marcus Dechant (c)
#LakeDrain.dev.py
#Manual Pump Activation
#v1.0.1

#verbose
script = 'LakeDrain.dev.py'
v = 'v1.0.1'
author = 'Marcus Dechant (c)'
verbose =('\n'+script+' - ('+v+') - '+author+'\n')
print(verbose)

#Import List
import RPi.GPIO as gpio
import time
sleep = time.sleep

#GPIO Constructors
warn = gpio.setwarnings
mode = gpio.setmode
board = gpio.BOARD
setup = gpio.setup
out = gpio.OUT
put = gpio.output
low = gpio.LOW
high = gpio.HIGH
clean = gpio.cleanup

#Relay Setup
warn(False)
pin3 = 13
mode(board)
setup(pin3, out)

#Main Process
delay = 1
while True:
    #Minute or Second
    user1 = input('Minutes or Seconds (M or S)?\n')
    #Script will accept any case input
    user1 = user1.lower()
    #move on if user inputs eith m or s
    if (user1 == 'm') or (user1 == 's'):
        break
    #Input Error
    else:
        print('\nError. Please Enter M or S.')

#Amount of Time
user2 = int(input('\nDuration?\n'))

try:
    #Activate Pump
    put(pin3, low)
    count = 0
    print('\nPump On.\n')
    #If user selects minutes
    if user1 == 'm':
        left = (user2 * 60)
        unit = ' Minutes. '
    #If user selects seconds
    else:
        left = user2
        unit = ' Seconds. '
    #Running Loop
    while (count < left):
        count += 1 
        diff = (left - count)
        print('Running for '+str(count)+unit+str(diff)+' remaining.')
        sleep(delay)
        
except KeyboardInterrupt:
        print()
        pass
#Pump is off
put(pin3, high)
print('\nPump Off.\n')
clean()
exit(0)