#!/bin/python3/AquaSolar

#AquaSolar
#Autonomous Gardening Project
#Marcus Dechant (c)
#SunRain.py
#v2.7.7

#Scheduler Docs 'https://schedule.readthedocs.io/en/stable/index.html'

name='SunRain.py'
v='v2.7.7'
cpyr=u'\u00A9'
year=' 2022'
author=' Marcus Dechant'
verbose=(name+' - '+v+' - '+cpyr+year+author)
print('\n'+verbose+'\n')

import RPi.GPIO as gpio
import sqlite3 as sql
import schedule
import os

from time import sleep

from lib.sht import h
from lib.sht import t

from lib.pistat import cpu
from lib.pistat import load

from lib.dt import tyme
from lib.dt import dayte
from datetime import datetime as dt

#Constructors
lower=str.lower
pathE=os.path.exists
mkdir=os.mkdir

#Universal Variables
c=','
sensorDelay=300

#Datetime
pTime=dt.strptime
fTime=dt.strftime
#Datetime Variables
clock24='%H:%M'
clock12='%I:%M %p'
tyme24='%H:%M:%S'
tyme12='%I:%M:%S %p'
date='%d/%m/%y'

#Scheduler Initalization
LIGHT=schedule.Scheduler()
PUMP=schedule.Scheduler()
SUMP=schedule.Scheduler()
SENS=schedule.Scheduler()
REMD=schedule.Scheduler()

#Relay Constructors
warn = gpio.setwarnings
mode = gpio.setmode
bcm = gpio.BCM
setup = gpio.setup
out = gpio.OUT
oput = gpio.output
high = gpio.HIGH
low =  gpio.LOW
clean = gpio.cleanup

#ASR3 will require 2 more Relay Channels

#Relay
warn(False) #True for Relay Warnings
mode(bcm)
p4=17 #Plant Light
p3=27 #Main Pump
p2=22 #Sump Pump
p1=23 #Free
setup(p4, out)
setup(p3, out)
setup(p2, out)
setup(p1, out)
oput(p3, high) #Pump off
oput(p2, high) #Sump off

devUin='Day (1), Night (0):\n'
badUout='Error: Bad input!\n'
onUout='Light On\n'
offUout='Light Off\n'

while(True):
    dn=input(devUin)
    if(dn=='1'):
        oput(p4, high)
        print(onUout)
        break
    elif(dn=='0'):
        oput(p4, low)
        print(offUout)
        break
    else:
        print(badUout)
        continue

#Light Scheduling
"""
While loop will repeat until break
Enter time in either 12 or 24 hour format

if input is greater then 7 characters it will be in 12 hour format
    Convert 12 to 24 Hour
    sunrise is passed in 24 hour format

if 3 or greater it will be in 24 hour format
    No conversion needed
    sunrise is passed in 24 hour format

else:
    Bad input
    Repeats loop
    
try/except:
    Bad input
    Repeats Loop
    
Returns a sunrise value in 12 and 24 hour format

Known Issues:
If user inputs H:MM program will crash. must be HH:MM value. same issue with watering timing.
"""

#Specific Variables
onUin=('Please Enter when the light will turn on.\n')
offUin=('Please Enter when the light will turn off.\n')
badUin='Error: Bad input! Please use 24 or 12 Hour time formats only.\n'

#when the light turns on
while(True):
    sunrise=input(onUin)
    try:
        if(len(sunrise)>=7):
            inTime=pTime(sunrise,clock12)
            outTime=fTime(inTime,clock24)
            sunrise=outTime
            break
        elif(len(sunrise)>=4):
            break        
        else:
            print(badUin)
            continue
    except:
        print(badUin)
        continue
sunriseIn=pTime(sunrise, clock24)
sunrise12=fTime(sunriseIn, clock12)
sunrise24=sunrise

#when light turns off
while(True):
    sunset=input(offUin)
    try:
        if(len(sunset)>=7):
            inTime=pTime(sunset,clock12)
            outTime=fTime(inTime,clock24)
            sunset=outTime
            break
        elif(len(sunrise)>=4):
            break
        else:
            print(badUin)
            pass
    except:
        print(badUin)
        pass
sunsetIn=pTime(sunset,clock24)
sunset12=fTime(sunsetIn,clock12)
sunset24=sunset

#Watering Scheduling
"""
Inital pump setup and timing
Enter 0 if user only wants Light Scheduling
Enter how long the pump will run for in seconds

if user does not enter 0
    
    What time of day the pump will run?
    While loop to repeat until break
    Enter when pump will turn on
    
    if input is greater then 7 characters it will be in 12 hour format
        Convert 12 to 24 Hour
        rain is passed in 24 hour format
        
    if 3 or greater it will be in 24 hour format
        No conversion needed
        rain is passed in 24 hour format
        
    else
        Bad input
        Repeats loop
    
    try/except
        Bad input
        Repeats loop
    
    Returns a rain value in 12 and 24 hour format
    
    How many days of the week the pump will run?
    While loop to repeat until break
    Enter number of days pump will run
    
    if number is greater than 1 or lower 7
        break 
    
    else
        Bad Input
        Repeat loop
    
    What days of the wek the pump will run?
    While loop is to repeat for the number of days the water pump will run
        
        While loop (nested) is to repeat until break
        Enter days pump will run
        
        if word entered matches name of day 
            break
        
        else
            Bad Input
            Repeat (nested) loop
        
        Add day to dayList
        Using dayList, weekList adds a comma between entries
    
    Set sump pump run time
        
if user does enter 0
    all relavent variables are set to 0 or nullified
"""
#Specific Variables
rainUin=('Please Enter when the Pump is activated.\n')
pumpUin=('Please Enter how long Pump will run for.\n')
weekUin=('Pease Enter Number of weekdays pump will run on.\n')
userDay=('Day?\n')
#Amount of time water pump willbe active for
print('If no Scheduled Watering enter 0.')
pump=int(input(pumpUin))
pumpRun=pump

if(pump!=0):
    #What time the water pump turns on
    while(True):
        try:
            rain=input(rainUin)
            if(len(rain)>=7):
                inTime=readTime(rain, clock12)
                outTime=tyme(inTime, clock24)
                rain=outTime
                break
            elif(len(rain)>=4):
                break
            else:
                print(badUin)
                continue
        except:
            print(badUin)
            continue
    rainIn=pTime(rain, clock24)
    rain12=fTime(rainIn, clock12)
    rain24=rain
    
    #How many day the water pump will turns on
    while(True):
        weekday=int(input(weekUin))
        if(weekday>1)or(weekday<7):
            break
        else:
            print(badUin)
            continue
    
    #What days the water pump will turn on
    day=1      
    dayList=set()
    setdayList=['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    while(day<=weekday):
        while(True):
            dayWeek=lower(input(dayUin))
            if(dayWeek in setdayList):
                break
            else:
                print(badUin)
                continue
        dayList.add(dayWeek)
        day+=1
        weekList=(', '.join(str(jour) for jour in dayList))
    drain='07:00'
    sumpRun=(pumpRun*1.5)
    times=('Sunrise at '+sunrise12+'. Sunset at '+sunset12+'. Watering every '+weekList+' at '+rain12+' for '+str(pumpRun)+' Seconds.')

else:
    weekday=0
    weekList='null'
    dayList=set('null')
    rain='00:00'
    drain=rain
    rain12='null'
    times=('Sunrise at '+sunrise12+'. Sunset at '+sunset12+'. No Watering Scheduled.')

#SQLite3 Database
"""
Tracking databases

EVENTS
ID = EID, Event ID, (interger variable)
EVENT = Event Description
INFO1 = Additional event information
INFO2 = Additional event information
TIME = Time of event
DATE = Date of event

DAY = sdID, sun day ID (integer variable)
SUNRISE = Time light turned on
SUNSET = Time light turned off

DAY = wdID, water day ID (integer variable)
WATER = Water pump run time
DRAIN = Sump pump run time
WINFO = Water pump run addional info
DINFO = Sump pump run addional info


"""

#File System for output
if not pathE(r'ASdb'):
    mkdir('ASdb')
    print('\n\ASdb : Good')

#Database variables
EID=0 #Event ID
sdID=0 #Sun day ID
wdID=0 #Water day ID
thsID=0 #Sensor 1 ID
pisID=0 #Pi Onboard Sensor ID
errID=0 #Error ID
cnct=sql.connect
database=(r'ASdb/aquasolar.db')
db=cnct(database)
xcte=db.execute
clse=db.close
comt=db.commit

#Database Creation
xcte('''CREATE TABLE IF NOT EXISTS EVENTS(
        ID          INT     NOT NULL    PRIMARY KEY,
        EVENT       TEXT    NOT NULL,
        INFO1       TEXT    NULL,
        INFO2       TEXT    NULL,
        TIME        TEXT    NOT NULL,
        DATE        TEXT    NOT NULL);''')

xcte('''CREATE TABLE IF NOT EXISTS SUN(
        DAY         INT     NOT NULL    PRIMARY KEY,
        SUNRISE     TEXT    NOT NULL,
        SUNSET      TEXT    NOT NULL,
        DATE        TEXT    NOT NULL);''')

#WIP   
xcte('''CREATE TABLE IF NOT EXISTS RAIN(
        DAY     INT     NOT NULL    PRIMARY KEY,
        WATER   INT     NOT NULL,
        DRAIN   INT     NOT NULL,
        WINFO   TEXT    NOT NULL,
        DINFO   TEXT    NOT NULL,
        DATE    TEXT    NOT NULL);''')
        
xcte('''CREATE TABLE IF NOT EXISTS SENSOR1(
        ID      INT     NOT NULL    PRIMARY KEY,
        DELAY   INT     NOT NULL,
        TEMP    TEXT    NOT NULL,
        HUMI    TEXT    NOT NULL,
        TIME    TEXT    NOT NULL,
        DATE    TEXT    NOT NULL);''')
        
xcte('''CREATE TABLE IF NOT EXISTS PI_STATS(
        ID          INT     NOT NULL    PRIMARY KEY,
        DELAY       INT     NOT NULL,
        CPUTEMP     REAL    NOT NULL,
        AVELOAD     REAL    NOT NULL,
        TIME        TEXT    NOT NULL,
        DATE        TEXT    NOT NULL);''')

#WIP    
xcte('''CREATE TABLE IF NOT EXISTS SENSOR_ERRORS(
        ID      INT     NOT NULL    PRIMARY KEY,
        LID     INT     NOT NULL,
        DELAY   INT     NOT NULL,
        CODE    TEXT    NOT NULL,
        SENSOR  TEXT    NOT NULL,
        TIME    TEXT    NOT NULL,
        DATE    TEXT    NOT NULL,
        INFO    TEXT    NOT NULL);''')
        
#Get last ID
if(pathE(database)):
    IDlast=xcte('''SELECT ID FROM EVENTS''')
    for row in IDlast:
        EID=int(row[0])
    sdIDlast=xcte('''SELECT DAY FROM SUN''')
    for row in sdIDlast:
        sdID=int(row[0])
    wdIDlast=xcte('''SELECT DAY FROM RAIN''')
    for row in wdIDlast:
        wdID=int(row[0])
    thsIDlast=xcte('''SELECT ID FROM SENSOR1''')
    for row in thsIDlast:
        thsID=int(row[0])
    pisIDlast=xcte('''SELECT ID FROM PI_STATS''')
    for row in pisIDlast:
       pisID=int(row[0])
    errIDlast=xcte('''SELECT ID FROM SENSOR_ERRORS''')
    for row in errIDlast:
       errID=int(row[0])
       
print('\nASdb/aquasolar.db: Ready\n')

#Light On
def sun_on():
    global EID
    oput(p4, high)
    EID+=1
    onTime=tyme()
    onDate=dayte()
    onInfo='LightOn'
    print('\nLight is On, '+onTime+', '+onDate+'.\n')
    xcte('''INSERT INTO EVENTS (ID,EVENT,INFO1,INFO2,TIME,DATE)
            VALUES(?,?,null,null,?,?)''',
                  (EID, onInfo, onTime, onDate))
    comt()
    print(times)
LIGHT.every().day.at(sunrise).do(sun_on)

#Light Off
def sun_off():
    global EID
    global sdID
    global sunrise
    global sunset 
    oput(p4, low)
    EID+=1
    sdID+=1
    offTime=tyme()
    offDate=dayte()
    offInfo='LightOff'
    print('\nLight is off, '+offTime+', '+offDate+'.\n')
    xcte('''INSERT INTO EVENTS (ID,EVENT,INFO1,INFO2,TIME,DATE)
            VALUES(?,?,null,null,?,?)''',
                  (EID, offInfo, offTime, offDate))
    xcte('''INSERT INTO SUN (DAY,SUNRISE,SUNSET,DATE)
            VALUES(?,?,?,?)''',
                  (sdID, sunrise, sunset, offDate))
    comt()
    print(times)
LIGHT.every().day.at(sunset).do(sun_off)

#Planning for more sensors with ASR3 

#Temperature and Humidity Sensor
def sensor_ths():
    global thsID
    global errID
    try:
        temp=t()
        humi=h()
        if(temp is None)or(humi is None):
            temp='err1'
            humi='ths'
            info='Null Reading'
            fail=True
        else:
            fail=False
    except(OSError):
        temp='err2'
        humi='ths'
        info='OSError'
        fail=True
    except(RuntimeError):
        temp='err3'
        humi='ths'
        info='RuntimeError'
        fail=True
    thsTime=tyme()
    thsDate=dayte()
    thsID+=1
    if(fail is False):
        xcte('''INSERT INTO SENSOR1 (ID,DELAY,TEMP,HUMI,TIME,DATE)
                VALUES(?,?,?,?,?,?)''',
                      (thsID, sensorDelay, temp, humi, thsTime, thsDate))
    else:
        errID+=1
        xcte('''INSERT INTO SENSOR_ERRORS (ID,LID,DELAY,CODE,SENSOR,TIME,DATE,INFO)
                VALUES(?,?,?,?,?,?,?,?)''',
                      (thsID, errID, sensorDelay, temp, humi, thsTime, thsDate, info))
    comt()
    #print(str(thsID)+c+temp+c+humi+c+thsTime+c+thsDate)
SENS.every(sensorDelay).seconds.do(sensor_ths)

#rpi cpu temp
def sensor_pi():
    global pisID
    cputemp=cpu()
    loadave=load()
    pisID+=1
    pisTime=tyme()
    pisDate=dayte()
    xcte('''INSERT INTO PI_STATS (ID,DELAY,CPUTEMP,AVELOAD,TIME,DATE)
            VALUES(?,?,?,?,?,?)''',
                  (pisID, sensorDelay, cputemp, loadave, pisTime, pisDate))
    comt()
    #print(str(pisID)+c+cputemp+c+loadave+c+pisTime+c+pisDate)
SENS.every(sensorDelay).seconds.do(sensor_pi)

#Pump Controls
def pump():
    if(pump!=0):
        global EID
        pumpOn=tyme()
        oput(p3, low)
        print('\nPump is On. '+str(pumpOn))
        sleep(pumpRun)
        pumpOff=tyme()
        oput(p3, high)
        print('Pump is Off. '+str(pumpOff))
        EID+=1
        pumpDate=dayte()
        pumpInfo=str(pumpRun)+' seconds'
        pumpEvent='PumpRun'
        xcte('''INSERT INTO EVENTS (ID,EVENT,INFO1,INFO2,TIME,DATE)
                VALUES(?,?,?,?,?,?)''',
                      (EID, pumpEvent, pumpInfo, pumpOn, pumpOff, pumpDate))
        comt()
        print('On at '+pumpOn+'. Off at '+pumpOff+'. Ran for '+pumpInfo+'.\n')
        print(times)
      
#ASR3 may require up to 4 sump pumps and possibly more than 1 water pump.
      
#Drainage Pump Controls
def sump():
    if(sump != 0):
        global EID
        sumpOn=tyme()
        oput(p2, low)
        print('\nSump is On. '+str(sumpOn))
        sleep(sumpRun)
        sumpOff=tyme()
        oput(p2, high)
        print('Sump is Off. '+str(sumpOff))
        EID += 1
        sumpDate=dayte()
        sumpInfo=str(sumpRun)+' seconds'
        sumpEvent='SumpRun'
        xcte('''INSERT INTO EVENTS (ID,EVENT,INFO1,INFO2,TIME,DATE)
                VALUES(?,?,?,?,?,?)''',
                      (EID, sumpEvent, sumpInfo, sumpOn, sumpOff, sDate))
        comt()
        print('On at '+sumpOn+'. Off at '+sumpOff+'. Ran for '+sumpInfo+'.\n')
        print(times)
        
if('sunday' in dayList):
    PUMP.every().sunday.at(rain).do(pump)
    PUMP.every().monday.at(drain).do(sump)
if('monday' in dayList):
    PUMP.every().monday.at(rain).do(pump)
    PUMP.every().tuesday.at(drain).do(sump)
if('tuesday' in dayList):
    PUMP.every().tuesday.at(rain).do(pump)
    PUMP.every().wednesday.at(drain).do(sump)
if('wednesday' in dayList):
    PUMP.every().wednesday.at(rain).do(pump)
    PUMP.every().thursday.at(drain).do(sump)
if('thursday' in dayList):
    PUMP.every().thursday.at(rain).do(pump)
    PUMP.every().friday.at(drain).do(sump)
if('friday' in dayList):
    PUMP.every().friday.at(rain).do(pump)
    PUMP.every().saturday.at(drain).do(sump)
if('saturday' in dayList):
    PUMP.every().saturday.at(rain).do(pump)
    PUMP.every().sunday.at(drain).do(sump)

def remind_once():
    STOPJOB=schedule.CancelJob
    print(times)
    sensor_ths()
    sensor_pi()
    return(STOPJOB)
REMD.every().second.do(remind_once)

#MAIN
while(True):
    try:
        REMD.run_pending()
        SENS.run_pending()
        LIGHT.run_pending()
        if(pump!=0):
            PUMP.run_pending()
        sleep(1)
    except KeyboardInterrupt:
        oput(p3, high)
        oput(p2, high)
        clse()
        clean()
        break
exit(0)