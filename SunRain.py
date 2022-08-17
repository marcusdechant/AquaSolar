#!/bin/python3/AquaSolar/Development

#AquaSolar
#Autonomous Gardening Project
#Marcus Dechant (c)
#SunRain.dev.py
#v2.7.2

#Scheduler Docs 'https://schedule.readthedocs.io/en/stable/index.html'

#Verbose
name='sunRain.dev.py'
v='v2.7.2'
author='Marcus Dechant (c)'
verbose=(name+' ('+v+') '+author)
print('\n'+verbose+'\n')

#Import List.
import RPi.GPIO as gpio
import sqlite3 as sql
import time
import schedule
import os

from datetime import datetime
def tyme():
    tyme=datetime.now().strftime('%d/%m/%Y')
    return(tyme)
def dayte():
    dayte=datetime.now().strftime('%H:%M:%S')
    return(dayte)

#Constructors
lower=str.lower
sleep=time.sleep
pathE=os.path.exists
mkdir=os.mkdir

#Datetime
pTime=datetime.strptime
fTime=datetime.strftime
#Datetime Variables
clock24='%H:%M'
clock12='%I:%M %p'
tyme24='%H:%M:%S'
tyme12='%I:%M:%S %p'
date='%d/%m/%y'

#Scheduler Initalization
ON=schedule.Scheduler()
OFF=schedule.Scheduler()
REMD=schedule.Scheduler()
PUMP=schedule.Scheduler()
SUMP=schedule.Scheduler()

#File System for output
if not pathE(r'ASdb'):
    mkdir('ASdb')
    print('\n\ASdb : Good')
if not pathE(r'ASdb/SR'):
    mkdir('ASdb/SR')
    print('\n\ASdb\SR : Good\n')

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
#make auto configuring
oput(p4, high) #high = Light on, low = Light off

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
    
#Print verification
print(sunrise12)
print(sunset12)
print(weekList)
print(rain12)
print(str(pumpRun))

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

#Database variables
EID=0 #Event ID
sdID=0 #Sun day ID
wdID=0 #Water day ID
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
        TIME        TEXT    NOT NULL,
        DATE        TEXT    NOT NULL);''')

#WIP
xcte('''CREATE TABLE IF NOT EXISTS RAIN(
        DAY     INT     NOT NULL    PRIMARY KEY,
        WATER   INT     NOT NULL,
        DRAIN   INT     NOT NULL,
        WINFO   TEXT    NOT NULL,
        DINFO   TEXT    NOT NULL,
        DATE    TEXT    NOT NULL);''')
        
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
print('\nASdb/aquasolar.db: Ready\nEID: '+str(EID))

def remindOnce():
    STOPJOB=schedule.CancelJob
    print(times)
    return(STOPJOB)
REMD.every().second.do(remindOnce)

#Light On
def sunOn():
    global EID
    oput(p4, high)
    EID+=1
    onTime=tyme()
    onDate=dayte()
    onInfo='LightOn'
    print('\nLight is On, '+onTime+', '+onDate+'.\n')
    xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,?,null,?,?)''',
                  (EID, onInfo, onTime, onDate))
    comt()
    print(times)
ON.every().day.at(sunrise).do(sunOn)

#Light Off
def sunOff():
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
    xcte('''INSERT INTO SUN (DAY,SUNRISE,SUNSET,TIME,DATE)
            VALUES(?,?,?,?,?)''',
                  (sdID, sunrise, sunset, offTime, offDate))
    comt()
    print(times)
OFF.every().day.at(sunset).do(sunOff)

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
    SUMP.every().monday.at(drain).do(sump)
if('monday' in dayList):
    PUMP.every().monday.at(rain).do(pump)
    SUMP.every().tuesday.at(drain).do(sump)
if('tuesday' in dayList):
    PUMP.every().tuesday.at(rain).do(pump)
    SUMP.every().wednesday.at(drain).do(sump)
if('wednesday' in dayList):
    PUMP.every().wednesday.at(rain).do(pump)
    SUMP.every().thursday.at(drain).do(sump)
if('thursday' in dayList):
    PUMP.every().thursday.at(rain).do(pump)
    SUMP.every().friday.at(drain).do(sump)
if('friday' in dayList):
    PUMP.every().friday.at(rain).do(pump)
    SUMP.every().saturday.at(drain).do(sump)
if('saturday' in dayList):
    PUMP.every().saturday.at(rain).do(pump)
    SUMP.every().sunday.at(drain).do(sump)

#MAIN
while(True):
    try:
        REMD.run_pending()
        ON.run_pending()
        OFF.run_pending()
        if(pump!=0):
            PUMP.run_pending()
            SUMP.run_pending()
        sleep(1)
    except KeyboardInterrupt:
        oput(p3, high)
        oput(p2, high)
        clse()
        clean()
        break
exit(0)