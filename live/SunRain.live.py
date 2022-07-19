#!/bin/python3/AquaSolar/Live
#sunRain.2.py
#v0.2.3
#Marcus Dechant (c)
import RPi.GPIO as gpio
import time
import schedule
import os
import sht30 as sht
from datetime import datetime
import sqlite3 as sql
lower = str.lower
sleep = time.sleep
pathE = os.path.exists
mkdir = os.mkdir
readTime = datetime.strptime
tyme = datetime.strftime
now = datetime.now().strftime
ON = schedule.Scheduler()
OFF = schedule.Scheduler()
REMD = schedule.Scheduler()
PUMP = schedule.Scheduler()
SUMP = schedule.Scheduler()
STOPJOB = schedule.CancelJob
if not pathE(r'ASdb'):
    mkdir('ASdb')
    print('\n\ASdb : Good')
if not pathE(r'ASdb/SR'):
    mkdir('ASdb/SR')
    print('\n\ASdb\SR : Good\n')
warn = gpio.setwarnings
mode = gpio.setmode
bcm = gpio.BCM
setup = gpio.setup
out = gpio.OUT
oput = gpio.output
high = gpio.HIGH
low =  gpio.LOW
warn(False)
mode(bcm)
p4 = 17 
p3 = 27 
p2 = 22 
p1 = 23 
setup(p4, out)
setup(p3, out)
setup(p2, out)
setup(p1, out)
oput(p3, high)
oput(p2, high)
#oput(p4, high)
generalDelay = 1
remDelay = 5
readTime = datetime.strptime
tyme = datetime.strftime
now = datetime.now().strftime
clock24 = '%H:%M'
clock12 = '%I:%M %p'
tyme24 =  '%H:%M:%S'
tyme12 = '%I:%M:%S %p'
date = '%d/%m/%y'
userSunON = ('Please Enter when the light will turn on.\n')
userSunOFF = ('Please Enter when the light will turn off.\n')
userRain = ('Please Enter when the Pump is activated.\n')
userPump = ('Please Enter how long Pump will run for.\n')
userWeek = ('Pease Enter Number of weekdays pump will run on.\n')
userDay = ('Day?\n')
while(True):
    sunrise = input(userSunON)
    if(len(sunrise) >= 7):
        inTime = readTime(sunrise, clock12)
        outTime = tyme(inTime, clock24)
        sunrise = outTime
        break
    elif(len(sunrise) >= 4):
        break        
    else:
        print('error')
        pass 
sunriseIn = readTime(sunrise, clock24)
sunrise12 = tyme(sunriseIn, clock12)
sunrise24 = sunrise
print()
while(True):
    sunset = input(userSunOFF)
    if(len(sunset) >= 7):
        inTime = readTime(sunset, clock12)
        outTime = tyme(inTime, clock24)
        sunset = outTime
        break
    elif(len(sunrise) >= 4):
        break
    else:
        print('error')
        pass
sunsetIn = readTime(sunset, clock24)
sunset12 = tyme(sunsetIn, clock12)
sunset24 = sunset
print()
print('If no Scheduled Watering enter 0.\n')
pump = int(input(userPump))
delayPump = pump
pumpDelay = str(delayPump)
print()
if(pump == 0):
    weekday = 0
    weekList = 'null'
    dayList = set('null')
    rain = '00:00'
    drain = rain
    times = ('Sunrise at ' + sunrise12 + '. Sunset at ' + sunset12 + '. No Watering Scheduled.')
else:
    while(True):
        rain = input(userRain)
        if(len(rain) >= 7):
            inTime = readTime(rain, clock12)
            outTime = tyme(inTime, clock24)
            rain = outTime
            break
        elif(len(rain) >= 4):
            break
        else:
            print('error')
            pass
    rainIn = readTime(rain, clock24)
    rain12 = tyme(rainIn, clock12)
    rain24 = rain
    print()
    day = 1
    while(True):
        weekday = int(input(userWeek))
        print()
        if(weekday < 1)or(weekday > 7):
            pass
        else:
            break
    dayList = set()
    while (day <= weekday):
        dayWeek = input(userDay)
        dayList.add(dayWeek)
        DAYWEEK = lower(dayWeek)
        day += 1
        weekList = (', '.join(str(dai) for dai in dayList))
        print()
    drain = '03:30'
    delaySump = (delayPump*1.8)
    sumpDelay = str(delaySump)
    times = ('Sunrise at ' + sunrise12 + '. Sunset at ' + sunset12 + '. Watering every ' + weekList + ' at ' + rain12 + ' for ' + pumpDelay + ' Seconds.')
print(sunrise12)
print(sunset12)
print(weekList)
print(rain12)
print(pumpDelay)
print()
EID = 0
dbID = 0
while pathE(r'ASdb/SR/SR.%s.db' %dbID):
    dbID += 1
cnct = sql.connect
database = (r'ASdb/SR/SR.%s.db' %dbID)
db = cnct(database)
xcte = db.execute
clse = db.close
comt = db.commit
xcte('''
CREATE TABLE EVENTS(
ID          INT     NOT NULL    PRIMARY KEY,
EVENT       TEXT    NOT NULL,
INFO        TEXT    NULL,
TIME        TEXT    NOT NULL,
DATE        TEXT    NOT NULL
);''')
def sunOn():
    global EID
    oput(p4, high)
    EID += 1
    #oput(p1, high)
    onTyme = now(tyme24)
    onDate = now(date)
    print()
    print('Light is off, ' + onTyme + ', ' + onDate + ', ' + str(EID))
    print()
    xcte('''INSERT INTO EVENTS(ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'lightOn',null,?,?)''',
    (EID, onTyme, onDate))
    comt()
    print(times)
def sunOff():
    global EID
    oput(p4, low)
    EID += 1
    #oput(p1, low)
    offTyme = now(tyme24)
    offDate = now(date)
    print()
    print('Light is off, ' + offTyme + ', ' + offDate + ', ' + str(EID))
    print()
    xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'lightOff',null,?,?)''',
    (EID, offTyme, offDate))
    comt()
    print(times)
def remindOnce():   
    print(times)
    return STOPJOB
def pump():
    if(pump != 0):
        global EID
        print()
        pumpOn = now(tyme24)
        print('Pump is On. ' + str(pumpOn))
        oput(p3, low)
        sleep(delayPump)
        oput(p3, high)
        pumpOff = now(tyme24)
        print('Pump is Off. ' + str(pumpOff))
        print()
        EID += 1
        onTyme = now(tyme24)
        dayte = now(date)
        pumpInfo = (pumpDelay + 's')
        xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'pumpRun',?,?,?)''',
        (EID, pumpInfo, onTyme, dayte))
        comt()
        print('On at ' + pumpOn + '. Off at ' + pumpOff + '. Ran for ' + pumpDelay + '.')
        print()
        print(times)
def sump():
    if(sump != 0):
        global EID
        sumpOn = now(tyme24)
        print('Sump is On. ' + str(sumpOn))
        oput(p2, low)
        sleep(delaySump)
        oput(p2, high)
        sumpOff = now(tyme24)
        print('Sump is Off. ' + str(sumpOff))
        print()
        EID += 1
        onTyme = now(tyme24)
        dayte = now(date)
        sumpInfo = (sumpDelay + ' seconds')
        xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'sumpRun',?,?,?)''',
        (EID, sumpInfo, onTyme, dayte))
        comt()
        print('On at ' + sumpOn + '. Off at ' + sumpOff + '. Ran for ' + sumpDelay + '.')
        print()
        print(times)
ON.every().day.at(sunrise).do(sunOn)
OFF.every().day.at(sunset).do(sunOff)
REMD.every().second.do(remindOnce)
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
while(True):
    try:
        ON.run_pending()
        OFF.run_pending()
        REMD.run_pending()
        if(delayPump != 0):
            PUMP.run_pending()
            SUMP.run_pending()
        sleep(generalDelay)
    except KeyboardInterrupt:
        oput(p3, high)
        oput(p2, high)
        clse()
        clean = gpio.cleanup
        clean()
        break
exit(0)