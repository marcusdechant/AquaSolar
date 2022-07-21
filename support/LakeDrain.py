#!/bin/python3/AquaSolar
script = 'LakeDrain.py'
v = 'v1.0.1'
author = 'Marcus Dechant (c)'
verbose =('\n'+script+' - ('+v+') - '+author+'\n')
print(verbose)
import RPi.GPIO as gpio
import time
sleep = time.sleep
warn = gpio.setwarnings
mode = gpio.setmode
board = gpio.BOARD
setup = gpio.setup
out = gpio.OUT
put = gpio.output
low = gpio.LOW
high = gpio.HIGH
clean = gpio.cleanup
warn(False)
pin3 = 13
mode(board)
setup(pin3, out)
delay = 1
while True:
    user1 = input('Minutes or Seconds (M or S)?\n')
    user1 = user1.lower()
    if (user1 == 'm') or (user1 == 's'):
        break
    else:
        print('\nError. Please Enter M or S.')
user2 = int(input('\nDuration?\n'))
try:
    put(pin3, low)
    count = 0
    print('\nPump On.\n')
    if user1 == 'm':
        left = (user2 * 60)
        unit = ' Minutes. '
    else:
        left = user2
        unit = ' Seconds. '
    while (count < left):
        count += 1 
        diff = (left - count)
        print('Running for '+str(count)+unit+str(diff)+' remaining.')
        sleep(delay)
except KeyboardInterrupt:
        print()
        pass
put(pin3, high)
print('\nPump Off.\n')
clean()
exit(0)