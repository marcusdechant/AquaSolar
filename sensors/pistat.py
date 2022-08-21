#!/bin/python

#Raspberry Pi 4 CPU Temperature, Load, and Disk Usage
#Marcus Dechant (c)
#pistat.py
#v0.0.1

from gpiozero import CPUTemperature as CPUt
from gpiozero import LoadAverage as Load
from gpiozero import DiskUsage as Disk

#CPU Temperature
def cpu():
    CPU='{0:0.2f}'.format(CPUt().temperature)
    return(CPU)

#CPU Load Average
def load():
    LOAD='{0:0.2f}'.format(Load().load_average)
    return(LOAD)
    
#Disk Usage
def disk():
    DISK='{0:0.2f}'.format(Disk().usage)
    return(DISK)