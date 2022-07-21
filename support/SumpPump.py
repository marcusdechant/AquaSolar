#!/bin/python3/AquaSolar
script='SumpPump.py'
v='v2.0.1'
author='Marcus Dechant (c)'
verbose=('\n'+script+' - ('+v+') - '+author+'\n')
print(verbose)
import RPi.GPIO as gpio
import time
sleep=time.sleep
warn=gpio.setwarnings
mode=gpio.setmode
board=gpio.BOARD
setup=gpio.setup
out=gpio.OUT
output=gpio.output
low=gpio.LOW
high=gpio.HIGH
clean=gpio.cleanup
user=('Seconds Sump will Run?\n')
delay=1
pin2=15
warn(False)
mode(board)
setup(pin2, out)
run=int(input(user))
try:
    print('\nSump Pump Active.\nRunning for '+str(run)+' Seconds\nPlease Wait...\n')
    output(pin2,low)
    a=0
    while(a<run):
        a+=1
        b=str(a)
        print(b+' seconds lapsed.')
        sleep(delay)
except KeyboardInterrupt as ki:
    print()
    pass
output(pin2,high)
print('\nSump Pump Deactivated.\n')
clean()
exit(0)