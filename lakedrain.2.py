#!/bin/python3/AquaSolar

import RPi.GPIO as gpio
import time
sleep = time.sleep

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

pin3 = 13
mode(board)
setup(pin3, out)

delay = 1
while True:
    user1 = input('\nMinutes or Seconds (M or S)?\n')
    if user1 == 'M' or user1 == 'S':
        break
    else:
        print('\nError. Please Enter M or S.')
user2 = int(input('\nDuration?\n'))
try:
    output(pin3, low)
    a = 0
    print('\nPump On.\n')
    if user1 == 'M':
        b = (user2 * 60)
        c = ' Minutes. '
    else:
        b = user2
        c = ' Seconds. '
    while (a < b):
        a += 1 
        d = (b - a)
        print('Running for ' + str(a) + c + str(d) + ' left.')
        sleep(delay)
except KeyboardInterrupt:
        print()
        pass
output(pin3, high)
print('\nPump Off.\n')
clean()
print()
exit(0)