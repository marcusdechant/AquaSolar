#!/bin/python3/AquaSolar/Development

#Marcus Dechant (c)
#Project AquaSolar
#Light (Sun) and Watering (Rain) Control

#To-Do
#Add color to CLI output
#multi database troubleshooting

#Accidents
#Accident - v0.2.1 - 22/06/21 - Basin Spillage - Caused by Inccorect Pump Pinning - Fixed v0.2.2
#FATAL ERROR - 22/07/16 - v0.2.4 -  xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE) 
#                                   sqlite3.IntegrityError: UNIQUE constraint failed: EVENTS.ID
#Accident - v0.2.4 - 22/07/19 - Basin Spillage - Caused by unintended function call - Fixed v0.2.5

#Dev Event Log
#Conditionally operational - 22/06/20 - v0.2.1
#repaired database - 22/06/21 - v0.2.2
#repaired pin allocations - 22/06/21 - v0.2.2
#rearranged user input - 22/06/21 - v0.2.2
#file naming convention established. old, dev, live - 22/06/26 - v0.2.3
#added verbose print on dev version - 22/06/26 - v0.2.3
#added multi database for sun and rain records - 22/07/01 - v0.2.4
#repaired unintedted function call - 22/07/19 - v0.2.5


#Verbose
name = 'sunRain.2.py'
v = 'v0.2.5'
author = 'Marcus Dechant (c)'
verbose = (name + ' (' + v + ') ' + author)
print('\n' + verbose + '\n')

#Scheduler Docs 'https://schedule.readthedocs.io/en/stable/index.html'

#Import List.
import RPi.GPIO as gpio
import time
import schedule
import os
import sht30 as sht
from datetime import datetime
import sqlite3 as sql

#Constructors
#Force lowercase string, lower(string)
lower = str.lower
#Wait for time inside parenthesis, sleep(#)
sleep = time.sleep
#Path in local file system, pathE(/path)
pathE = os.path.exists
#'mkdir' (make directory), mkdir(/path)
mkdir = os.mkdir
#Scheduler Constructors
ON = schedule.Scheduler()
OFF = schedule.Scheduler()
REMD = schedule.Scheduler()
PUMP = schedule.Scheduler()
SUMP = schedule.Scheduler()
STOPJOB = schedule.CancelJob

#Create File System
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

#Relay
warn(False) #True for Relay Warnings
mode(bcm)
p4 = 17 #Plant Light
p3 = 27 #Main Pump
p2 = 22 #Sump Pump
p1 = 23 #None
setup(p4, out)
setup(p3, out)
setup(p2, out)
setup(p1, out)
oput(p3, high) #Force Pump off, percaution
oput(p2, high) #Force Sump off, percaution

#toggle for light at startup
oput(p4, high)

#Delays
generalDelay = 1
remDelay = 5

#Datetime
#time Constructors
readTime = datetime.strptime
tyme = datetime.strftime
#Datetime Variables
clock24 = '%H:%M'
clock12 = '%I:%M %p'
tyme24 =  '%H:%M:%S'
tyme12 = '%I:%M:%S %p'
date = '%d/%m/%y'

#User input questions
userSunON = ('Please Enter when the light will turn on.\n')
userSunOFF = ('Please Enter when the light will turn off.\n')
userRain = ('Please Enter when the Pump is activated.\n')
userPump = ('Please Enter how long Pump will run for.\n')
userWeek = ('Pease Enter Number of weekdays pump will run on.\n')
userDay = ('Day?\n')

#Startup and Input

#When will the light turns on?

#While loop will repeat until break
while(True):
    sunrise = input(userSunON)
    try:
        #if input is greater then 7 characters its implied its in HH:MM pp (pp = AM/PM) format (12 Hour)
        if(len(sunrise) >= 7):
            #convert 12 to 24 Hour
            inTime = readTime(sunrise, clock12)
            outTime = tyme(inTime, clock24)
            sunrise = outTime
            #break on good condition
            break
        #3 or greater its implied that its in HH:MM format (24 hour)
        elif(len(sunrise) >= 4):
            #leave 24 Hour as is
            break        
        else:
            print('error')
            #pass on bad condition
            pass
    except:
        print('error')
        pass
#convert to both 12 and 24 hour format
sunriseIn = readTime(sunrise, clock24)
sunrise12 = tyme(sunriseIn, clock12)
sunrise24 = sunrise

#Bugs
#If user inputs H:MM program will crash. must be HH:MM value

print()

#when light turns off
while(True):
    sunset = input(userSunOFF)
    try:
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
    except:
        print('error')
        pass
sunsetIn = readTime(sunset, clock24)
sunset12 = tyme(sunsetIn, clock12)
sunset24 = sunset

#Bugs
#If user inputs H:MM program will crash. must be HH:MM value

print()

#Watering Scheduling
print('If no Scheduled Watering enter 0.\n')

pump = int(input(userPump))
delayPump = pump
pumpDelay = str(delayPump)

print()

#If user enters 0, no watering schedule values
if(pump == 0):
    weekday = 0
    weekList = 'null'
    dayList = set('null')
    rain = '00:00'
    drain = rain
    rain12 = 'null'
    times = ('Sunrise at ' + sunrise12 + '. Sunset at ' + sunset12 + '. No Watering Scheduled.')

#If the user enters a value other than 0
else:
    #when water pump turns on
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
    
    #Bugs
    #If user inputs H:MM program will crash. must be HH:MM value

    print()
    
    day = 1
    while(True):
        #User inputs number of week days watering will occure on
        weekday = int(input(userWeek))
        
        print()
        
        #If User enters less than 1 or more than 7
        if(weekday < 1)or(weekday > 7):
            #Reiterate (pass) on bad conditions, number less than 1 or more than 7 
            pass
        else:
            #Break Loop on good conditions, number between 1 and 7
            break
            
    dayList = set()
    
    #Loops based on number of days User entered above
    while (day <= weekday):
        #User enters day
        dayWeek = input(userDay)
        #Day is added to dayList set, queried for Scheduler
        dayList.add(dayWeek)
        DAYWEEK = lower(dayWeek)
        day += 1
        #Print ready daylist = weeklist
        weekList = (', '.join(str(dai) for dai in dayList))
        
        print()
    
    #Drainage Basin Sump
    #Activates at 7:15 AM
    drain = '03:30'
    delaySump = (delayPump*1.8)
    sumpDelay = str(delaySump)
    
    #Used to display information to the user
    times = ('Sunrise at ' + sunrise12 + '. Sunset at ' + sunset12 + '. Watering every ' + weekList + ' at ' + rain12 + ' for ' + pumpDelay + ' Seconds.')

#test prints
print(sunrise12)
#print(sunrise24)
print(sunset12)
#print(sunset24)
print(weekList)
print(rain12)
#print(rain24)
print(pumpDelay)
print()

#Run ID, +1 if number is already taken by existing records
EID = 0 #Event ID
dbID = 0 #Database ID
sdID = 0 #Sun DAY ID
wdID = 0 #Water DAY ID
#Database ID Increment
while pathE(r'ASdb/SR/SR.%s.db' %dbID):
    dbID += 1

#Connect to SQL Database, cnct(/path) or cnct(variableOfPath)
cnct = sql.connect
#Database, uses Run ID to create a new database
database = (r'ASdb/SR/SR.%s.db' %dbID)
db = cnct(database)
xcte = db.execute
clse = db.close
comt = db.commit

#Database Creation
xcte('''
CREATE TABLE EVENTS(
ID          INT     NOT NULL    PRIMARY KEY,
EVENT       TEXT    NOT NULL,
INFO        TEXT    NULL,
TIME        TEXT    NOT NULL,
DATE        TEXT    NOT NULL);''')

xcte('''
CREATE TABLE SUN(
DAY         INT     NOT NULL    PRIMARY KEY,
SUNRISE     TEXT    NOT NULL,
SUNSET      TEXT    NOT NULL);''')

xcte('''
CREATE TABLE RAIN(
DAY     INT    NOT NULL    PRIMARY KEY,
WATER   INT    NULL,
PTIME   INT    NULL,
STIME   INT    NULL);''')

#FUNCTIONS
#Light On
def sunOn():
    global EID
    oput(p4, high)
    #Event ID Increment
    EID += 1
    #Port 1, 3 Prong interface, power cut
    #oput(p1, high)
    onTyme = datetime.now().strftime(tyme24)
    onDate = datetime.now().strftime(date)
    
    print()
    print('Light is off, ' + onTyme + ', ' + onDate + '.')
    print()
    
    xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'lightOn',null,?,?)''',
    (EID, onTyme, onDate))
    comt()
    
    print(times)
    
    return(onTyme)

#Light Off
def sunOff():
    global sunrise
    global sunset 
    global EID
    global sdID
    oput(p4, low)
    EID += 1
    sdID += 1
    #oput(p1, low)
    offTyme = datetime.now().strftime(tyme24)
    offDate = datetime.now().strftime(date)
    
    print()
    print('Light is off, ' + offTyme + ', ' + offDate + '.')
    print()
    
    xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'lightOff',null,?,?)''',
    (EID, offTyme, offDate))
    comt()
    
    xcte('''INSERT INTO SUN (DAY,SUNRISE,SUNSET)
            VALUES(?,?,?)''',
    (sdID, sunrise, sunset))
    comt()
    
    print(times)



#Display Times
#def remind():
#    print(times)

#Display Times when program is run
def remindOnce():   
    print(times)
    return STOPJOB

#Pump Controls
def pump():
    if(pump != 0):
        global EID
        print()
        pumpOn = datetime.now().strftime(tyme24)
        print('Pump is On. ' + str(pumpOn))
        
        oput(p3, low)
        sleep(delayPump)
        oput(p3, high)
        pumpOff = datetime.now().strftime(tyme24)
        
        print('Pump is Off. ' + str(pumpOff))
        print()
        
        EID += 1
        pTyme = datetime.now().strftime(tyme24)
        pDate = datetime.now().strftime(date)
        pumpInfo = (pumpDelay + ' seconds')
        
        xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'pumpRun',?,?,?)''',
        (EID, pumpInfo, pTyme, pDate))
        comt()
        
        print('On at ' + pumpOn + '. Off at ' + pumpOff + '. Ran for ' + pumpDelay + '.')
        print()
        print(times)
        
        return(pTyme, pDate)
        
#Drainage Pump Controls
def sump():
    if(sump != 0):
        global EID
        global wdID
        sumpOn = datetime.now().strftime(tyme24)
        print('Sump is On. ' + str(sumpOn))
        
        oput(p2, low)
        sleep(delaySump)
        oput(p2, high)
        sumpOff = datetime.now().strftime(tyme24)
        
        print('Sump is Off. ' + str(sumpOff))
        print()
        
        EID += 1
        wdID += 1
        sTyme = datetime.now().strftime(tyme24)
        sDate = datetime.now().strftime(date)
        sumpInfo = (sumpDelay + ' seconds')
        
        xcte('''INSERT INTO EVENTS (ID,EVENT,INFO,TIME,DATE)
            VALUES(?,'sumpRun',?,?,?)''',
        (EID, sumpInfo, sTyme, sDate))
        comt()
        
        #xcte('''INSERT INTO RAIN (DAY,
        print('On at ' + sumpOn + '. Off at ' + sumpOff + '. Ran for ' + sumpDelay + '.')
        print()
        print(times)
        
#SCHEDULER
#Build On, Off, and Reminder Schedules
ON.every().day.at(sunrise).do(sunOn)
OFF.every().day.at(sunset).do(sunOff)
#REMD.every(remDelay).hours.do(remind)
REMD.every().second.do(remindOnce)

#Build Watering Schedule
#Call User inputted days to build schedule
if('sunday' in dayList):
    #Pump Configuration
    PUMP.every().sunday.at(rain).do(pump)
    #Drainage runs at 3 AM but must run AFTER the pump
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