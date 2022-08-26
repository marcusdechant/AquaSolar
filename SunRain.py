#!/bin/python3/AquaSolar

#AquaSolar
#Autonomous Gardening Project
#Marcus Dechant (c)
#SunRain.py
#v2.7.10

#Scheduler Docs 'https://schedule.readthedocs.io/en/stable/index.html'

name='SunRain.py'
v='v2.7.10'
cpyr=u'\u00A9'
year=' 2022'
author=' Marcus Dechant'
verbose=(name+' - '+v+' - '+cpyr+year+author)
print('\n'+verbose+'\n')

#import list and constructors
import RPi.GPIO as gpio
warn = gpio.setwarnings
mode = gpio.setmode
bcm = gpio.BCM
setup = gpio.setup
out = gpio.OUT
oput = gpio.output
high = gpio.HIGH
low =  gpio.LOW
clean = gpio.cleanup
import schedule
LIGHT=schedule.Scheduler()
PUMP=schedule.Scheduler()
SUMP=schedule.Scheduler()
SENS=schedule.Scheduler()
REMD=schedule.Scheduler()
from psycopg2 import connect as ct
database='aquasolar'
user='as_pi'
password='growIn3'
host='127.0.0.1'
port=5432
import os
pathE=os.path.exists
mkdir=os.mkdir
from datetime import datetime as dt
pTime=dt.strptime
fTime=dt.strftime
clock24='%H:%M'
clock12='%I:%M %p'
from time import sleep
from lib.sht import h
from lib.sht import t
from lib.pistat import cpu
from lib.pistat import load
from lib.pistat import disk
from lib.dt import time_
from lib.dt import date_

#Universal Variables
c=', '
d=180 #Sensor Delay
D=str(d)

#Relay
warn(False) #True for Relay Warnings
mode(bcm)
p4=17 #Plant Light
p3=27 #Main Pump
p2=22 #
p1=23 #OPEN
setup(p4, out) 
setup(p3, out) 
setup(p2, out) 
setup(p1, out) 
oput(p3, high) #Pump off
oput(p2, high) #Sump off
#ASR3 will require 2 more Relay Channels

#inputs and outputs (user)
skipUin='Active (1), Sensor (0):\n'
devUin='Day (1), Night (0):\n'
onUin='Please Enter when the light will turn on.\n'
offUin='Please Enter when the light will turn off.\n'
onUout='Light On\n'
offUout='Light Off\n'
rainUin='Please Enter when the Pump is activated.\n'
pumpUin='Please Enter how long Pump will run for.\n'
weekUin='Pease Enter Number of weekdays pump will run on.\n'
dayUin='Day?\n'
badUin='Error: Bad input! Please use 24 or 12 Hour time formats only.\n'
badUout='Error: Bad input!\n'

#determines if only sensors should be active
while(True):
    sk=input(skipUin)
    if(sk=='1'):
        skip=False
        act='deactivated'
        break
    elif(sk=='0'):
        skip=True
        act='activated'
        break
    else:
        print(badUout)
        continue
        
#startup light control DEV
if(skip is False):
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

if(skip is False):
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
else:
    sunrise12='00:00'
    sunrise24='00:00'
    sunset12='00:00'
    sunset24='00:00'
    sunrise=sunrise24
    sunset=sunset24

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
pump=0
if(skip is False):
    print('If no Scheduled Watering enter 0.')
    pump=int(input(pumpUin)) #Amount of time water pump will be active for
pumpRun=pump

if(pump!=0):
    while(True):
        try:
            rain=input(rainUin) #What time the water pump turns on
            if(len(rain)>=7):
                inTime=readTime(rain, clock12)
                outTime=time_(inTime, clock24)
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
    
    while(True):
        weekday=int(input(weekUin)) #How many day the water pump will turns on
        if(weekday>1)or(weekday<7):
            break
        else:
            print(badUin)
            continue
    
    day=1      
    dayList=set()
    setdayList=['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    while(day<=weekday):
        while(True):
            dayWeek=str.lower(input(dayUin)) #What days the water pump will turn on
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

# postgresql 
conn=ct(database=database,user=user,password=password,host=host,port=port)
conn.autocommit=True
cls=conn.close
save=conn.commit
helm=conn.cursor()
exe=helm.execute
rc=helm.rowcount
fa=helm.fetchall
ist='information_schema.tables'
ttn='tables.table_name'
a=True

exe('''SELECT * FROM %s WHERE %s='EVENT';''' %(ist,ttn))
vid_ch=bool(rc)
if(vid_ch is a):
    exe('''SELECT ID FROM EVENT;''')
    vid_last=fa()
    for row in vid_last:
        vid=int(row[0])
else: # events table
    tb_events='''
    CREATE TABLE IF NOT EXISTS EVENT(
    ID      INT     NOT NULL    PRIMARY KEY,
    EVENT   TEXT    NOT NULL,
    INFO1   TEXT    NULL,
    INFO2   TEXT    NULL,
    TIME    TEXT    NOT NULL,
    DATE    TEXT    NOT NULL);'''
    exe(tb_events)
    vid=0 # event id
    save()

exe('''SELECT * FROM %s WHERE %s='SUN';''' %(ist,ttn))
lid_ch=bool(rc)
if(lid_ch is a):
    exe('''SELECT ID FROM SUN;''')
    lid_last=fa()
    for row in lid_last:
        lid=int(row[0])
else: # light tracking table
    tb_sun='''
    CREATE TABLE IF NOT EXISTS SUN(
    ID          INT     NOT NULL    PRIMARY KEY,
    SUNRISE     TEXT    NOT NULL,
    SUNSET      TEXT    NOT NULL,
    DATE        TEXT    NOT NULL);'''
    exe(tb_sun)
    lid=0 # light id
    save()

exe('''SELECT * FROM %s WHERE %s='RAIN';''' %(ist,ttn))
wid_ch=bool(rc)
if(wid_ch is a):
    exe('''SELECT ID FROM RAIN;''')
    wid_last=fa()
    for row in wid_last:
        wid=int(row[0])
else: # water tracking table
    tb_rain='''
    CREATE TABLE IF NOT EXISTS RAIN(
    ID      INT     NOT NULL    PRIMARY KEY,
    PUMP    TEXT    NOT NULL,
    RUN     INT     NOT NULL,
    TIME    TEXT    NOT NULL,
    DATE    TEXT    NOT NULL);'''
    exe(tb_rain)
    wid=0 # water id
    save()

exe('''SELECT * FROM %s WHERE %s='SENSOR_PI';''' %(ist,ttn))
rid0_ch=bool(rc)
if(rid0_ch is a):
    exe('''SELECT ID FROM SENSOR_PI;''')
    rid0_last=fa()
    for row in rid0_last:
        rid0=int(row[0])
else: # rpi 4 stats table
    tb_pi=''' 
    CREATE TABLE IF NOT EXISTS SENSOR_PI(
    ID      INT     NOT NULL    PRIMARY KEY,
    DELAY   INT     NOT NULL,
    CPUT    REAL    NOT NULL,
    CPUL    REAL    NOT NULL,
    DISK    REAL    NULL,
    TIME    TEXT    NOT NULL,
    DATE    TEXT    NOT NULL);'''
    exe(tb_pi)
    rid0=0
    save()
    
exe('''SELECT * FROM %s WHERE %s='SENSOR_TH';''' %(ist,ttn))
rid1_ch=bool(rc)
if(rid1_ch is a):
    exe('''SELECT ID FROM SENSOR_TH;''')
    rid1_last=fa()
    for row in rid1_last:
        rid1=int(row[0])
else: # sensor 1 temp and humi reading table
    tb_sen1='''
    CREATE TABLE IF NOT EXISTS SENSOR_TH(
    ID      INT     NOT NULL    PRIMARY KEY,
    DELAY   INT     NOT NULL,
    TEMP    REAL    NOT NULL,
    HUMI    REAL    NOT NULL,
    TIME    TEXT    NOT NULL,
    DATE    TEXT    NOT NULL);'''
    exe(tb_sen1)
    rid1=0
    save()

exe('''SELECT * FROM %s WHERE %s='SENSOR_ER';''' %(ist,ttn))
eid_ch=bool(rc)
if(eid_ch is a):
    exe('''SELECT ID FROM SENSOR_ER;''')
    eid_last=fa()
    for row in eid_last:
        eid=int(row[0])
else: # sensor error table
    tb_err='''
    CREATE TABLE IF NOT EXISTS SENSOR_ER(
    ID      INT     NOT NULL    PRIMARY KEY,
    EID     INT     NOT NULL,
    DELAY   INT     NOT NULL,
    TIME    TEXT    NOT NULL,
    CODE    TEXT    NOT NULL,
    SENSOR  TEXT    NOT NULL,
    INFO    TEXT    NOT NULL,
    DATE    TEXT    NOT NULL);'''
    exe(tb_err)
    eid=0 # error id
    save()

sleep(1.5)
print('\nPostgreSQL: ready')
sleep(0.5)
print('readout: '+act+'\n')

#Light On
def sun_on():
    global vid
    oput(p4, high)
    vid+=1
    onTime=time_()
    onDate=date_()
    onInfo='LightOn'
    print('\nLight is On, '+onTime+', '+onDate+'.\n')
    para=(vid,onInfo,onTime,onDate)
    exe('''INSERT INTO EVENT (ID,EVENT,INFO1,INFO2,TIME,DATE)
            VALUES %s''', (para,))
    save()
    print(times)
LIGHT.every().day.at(sunrise).do(sun_on)

#Light Off
def sun_off():
    global vid
    global lid
    global sunrise
    global sunset 
    oput(p4, low)
    vid+=1
    lid+=1
    offTime=time_()
    offDate=date_()
    offInfo='LightOff'
    print('\nLight is off, '+offTime+', '+offDate+'.\n')
    para1=(vid,offInfo,offTime,offDate)
    para2=(lid,sunrise,sunset,offDate)
    exe('''INSERT INTO EVENT (ID,EVENT,INFO1,INFO2,TIME,DATE)
           VALUES %s''', (para1,))
    exe('''INSERT INTO SUN (DAY,SUNRISE,SUNSET,DATE)
           VALUES %s''', (para2,))
    save()
    print(times)
LIGHT.every().day.at(sunset).do(sun_off)

#Planning for more sensors with ASR3 

#rpi cpu temp
def sensor_pi():
    global rid0
    global skip
    rid0+=1
    cputemp=cpu()
    cpuload=load()
    diskuse=disk()
    pisTime=time_()
    pisDate=date_()
    para=(rid0,d,cputemp,cpuload,diskuse,pisTime,pisDate)
    exe('''INSERT INTO SENSOR_PI (ID,DELAY,CPUT,CPUL,DISK,TIME,DATE)
            VALUES %s''', (para,))
    if(skip is True):    
        print('PIS: '+str(rid0)+c+str(d)+c+cputemp+c+cpuload+c+diskuse+c+pisTime+c+pisDate)
    save()

#Temperature and Humidity Sensor
def sensor_th():
    global rid1
    global eid
    global skip
    rid1+=1
    try:
        temp=str(t())
        humi=str(h())
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
    thsTime=time_()
    thsDate=date_()
    if(fail is False):
        para=(rid1,d,temp,humi,thsTime,thsDate)
        exe('''INSERT INTO SENSOR_TH (ID,DELAY,TEMP,HUMI,TIME,DATE)
                VALUES %s''', (para,))
        if(skip is True):    
            print('THS: '+str(rid1)+c+str(d)+c+temp+c+humi+c+thsTime+c+thsDate)
    else:
        eid+=1
        para=(rid1,eid,d,thsTime,temp,humi,info,thsDate)
        exe('''INSERT INTO SENSOR_ER (ID,EID,DELAY,TIME,CODE,SENSOR,INFO,DATE)
                VALUES %s''', (para,))
        if(skip is True):
            print('ERS: '+str(rid1)+c+str(eid)+c+str(d)+c+temp+c+humi+c+info+c+thsTime+c+thsDate)
    save()
    
def sensor():
    sensor_pi()
    sensor_th()
    print()
SENS.every(d).seconds.do(sensor) 

#Pump Controls
def pump():
    if(pump!=0):
        global vid
        vid+=1
        pumpOn=time_()
        oput(p3, low)
        print('\nPump is On. '+str(pumpOn))
        sleep(pumpRun)
        pumpOff=time_()
        oput(p3, high)
        print('Pump is Off. '+str(pumpOff))
        pumpDate=date_()
        pumpInfo=str(pumpRun)+' seconds'
        pumpEvent='PumpRun'
        para=(vid,pumpEvent,pumpInfo,pumpOn,pumpOff,pumpDate)
        exe('''INSERT INTO EVENT (ID,EVENT,INFO1,INFO2,TIME,DATE)
                VALUES %s''', (para,))
        save()
        print('On at '+pumpOn+'. Off at '+pumpOff+'. Ran for '+pumpInfo+'.\n')
        print(times)
      
#ASR3 may require up to 4 sump pumps and possibly more than 1 water pump.
      
#Drainage Pump Controls
def sump():
    if(sump != 0):
        global vid
        vid+=1
        sumpOn=time_()
        oput(p2, low)
        print('\nSump is On. '+str(sumpOn))
        sleep(sumpRun)
        sumpOff=time_()
        oput(p2, high)
        print('Sump is Off. '+str(sumpOff))
        sumpDate=date_()
        sumpInfo=str(sumpRun)+' seconds'
        sumpEvent='SumpRun'
        para=(vid,sumpEvent,sumpInfo,sumpOn, sumpOff, sDate)
        exe('''INSERT INTO EVENT (ID,EVENT,INFO1,INFO2,TIME,DATE)
                VALUES %s''', (para,))
        save()
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
    if(skip is False):
        print(times)
    sensor()
    return(STOPJOB)
REMD.every().second.do(remind_once)

#MAIN
while(True):
    try:
        REMD.run_pending()
        SENS.run_pending()
        if(skip is False):
            LIGHT.run_pending()
        if(pump!=0):
            PUMP.run_pending()
        sleep(1)
    except KeyboardInterrupt:
        oput(p3, high)
        oput(p2, high)
        cls()
        clean()
        break
exit(0)