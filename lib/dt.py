#!/bin/python

#Formatted DateTime
#(c) 2022 Marcus Dechant 
#dt.py
#v0.2

from datetime import datetime as dt

def time_():
    t_=dt.now().strftime('%H:%M:%S')
    return(t_)

def date_():
    d_=dt.now().strftime('%d/%m/%Y')
    return(d_)