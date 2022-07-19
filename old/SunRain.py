#!/bin/python

# sunrain.py
#By: Marcus Dechant

v = 'v.2.9'

#Project AQUASOLAR
#Light Control (SUN)
#Watering Control (RAIN1)

#Sources
#Scheduler Docs 'https://schedule.readthedocs.io/en/stable/index.html'

#Import List
import RPi.GPIO as GPIO
import time as TIME
import schedule as SCHEDULE
import os as OS
import sht30 as ENV
import threading as THREADING
from datetime import datetime as DATETIME
import sqlite3 as SQL

#create database file


#RPi GPIO Declaration and Setup
PIN_RC4 = 11
PIN_RC4_BCM = 17
PIN_RC3 = 13
PIN_RC3_BCM = 27
PIN_RC2 = 15
PIN_RC2_BCM = 22
PIN_RC1 = 16
PIN_RC1_BCM = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_RC4_BCM, GPIO.OUT)
GPIO.setup(PIN_RC3_BCM, GPIO.OUT)
GPIO.setup(PIN_RC2_BCM, GPIO.OUT)
GPIO.setup(PIN_RC1_BCM, GPIO.OUT)
GPIO.output(PIN_RC3_BCM, GPIO.HIGH)
GPIO.output(PIN_RC2_BCM, GPIO.HIGH)

#Delay Variable
DELAY = 1 #General script delay (startup, input, etc.).

#Text Formating (Color)
R = '\u001b[0;31;40m'
RW = '\u001b[0;37;41m'
RY = '\u001b[1;31;43m'
G = '\u001b[0;32;40m'
GB = '\u001b[0;30;42m'
C = '\u001b[0;36;40m'
Y = '\u001b[0;33;40m'
P = '\u001b[0;35;40m'
WB = '\u001b[0;34;47m'
BW = '\u001b[0;37;44m'
CK = '\u001b[0;30;46m'
WK = '\u001b[0;37;40m'

#Formatted Text
DOES_NOT_EXIST = (R + 'Does Not Exist.' + WK)
NOTE = (R + 'Please Note!' + WK)
R3MINDER = (R + 'Reminder:' + WK)
BAD_TIME = ('\n' + R + 'Invalid Time Entry' + WK + '\n')
BAD_INP = ('\n' + RW + 'Invaild Input' + WK + '\n')
EXISTS = (G + 'Exists.' + WK)
LIGHT_OFF = (G + 'Off! ' + WK)
PLS_ENT = (G + 'Please Enter' + WK)
INP_VAL = (GB + 'Inputed Values' + WK)
PUMP_ONE = (C + 'Pump One' + WK)
WATERING = (C + 'watering' + WK)
PUMP_ON = (C + 'on!' + WK)
PUMP_OFF = (C + 'off!' + WK)
SUMP_ONE = (RY + 'Sump One' + WK)
SUMP_ON = (RY + 'on!' + WK)
SUMP_OFF = (RY + 'off!' + WK)
LIGHT_ON = (Y + 'On! ' + WK)

#User Inputed Formatted
userPumpONE = (PLS_ENT + ' (in seconds) ' + PUMP_ONE + ' Run-time: ') 
userSched = (PLS_ENT + ' days between ' + WATERING + ': ')
userSunON = (PLS_ENT + ' Time Light will turn on: ')  
userSunOFF = (PLS_ENT + ' Time Light will turn off: ')
userRainONE = (PLS_ENT + ' Time of ' + WATERING + ': ')
userWeekday = (PLS_ENT + ' Number of weekdays ' + WATERING + ' will occur on: ')
userDayweek = (PLS_ENT + ' Days of the week ' + WATERING + ' will occur on: ')

#Clock Variations
CLOCK_24H = '%H:%M:%S %d/%m/%y'
TIME_24H = '%H:%M:%S'
CLOCK_12H = '%I:%M:%S %p %d/%m/%y'

#Start-up, displays versions, name, author, and purpose
print('\nsunrain.py. ' + v)
TIME.sleep(DELAY)
print('Project AQUASOLAR')
TIME.sleep(DELAY)
print('By: Marcus Dechant')
TIME.sleep(DELAY)
print('Light Control')
TIME.sleep(DELAY)
print('Watering Control')
TIME.sleep(DELAY)
print('Startime: ' + DATETIME.now().strftime(CLOCK_12H) + '.\n')
TIME.sleep(DELAY)

#User Input
print('\nPlease use 24H time format (HH:MM)')
TIME.sleep(DELAY)
SUNRISE = input(userSunON)
#SUNRISE Time Converter
try:
    A1 = SUNRISE
    B1 = (A1[0] + A1[1] + A1[3] + A1[4])
    SUNRISE_TIME = int(B1)
    if (B1 >= '0000' and B1 < '1159'):
        B1 = (A1[0] + A1[1] + ':' + A1[3] + A1[4] + ' AM')
        C1 = (A1[0] + A1[1])
        D1 = (A1[3] + A1[4])
        E1 = A1[0]
        if (E1 == '0'):
            B1 = B1[1:]
        if (C1 == '00'):
            B1 = ('12:' + C1 + ' AM')
        if (D1 > '59'):
            print(BAD_TIME)
            exit(0)
    elif (B1 >= '1200' and B1 < '2359'):
        C1 = (A1[0] + A1[1])
        D1 = (A1[3] + A1[4])
        if (D1 > '59'):
            print(BAD_TIME)
            exit(0)
        if (C1 == '12'):
            B1 = (C1 + ':' + D1 + ' PM')
        elif (C1 == '13'):
            E1 = '1'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '14'):
            E1 = '2'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '15'):
            E1 = '3'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '16'):
            E1 = '4'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '17'):
            E1 = '5'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '18'):
            E1 = '6'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '19'):
            E1 = '7'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '20'):
            E1 = '8'
            B1 = (E1 + ':' + D1 + ' PM') 
        elif (C1 == '21'):
            E1 = '9'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '22'):
            E1 = '10'
            B1 = (E1 + ':' + D1 + ' PM')
        elif (C1 == '23'):
            E1 = '11'
            B1 = (E1 + ':' + D1 + ' PM')
        else:
            print(BAD_TIME)
            exit(0)
    else:
        print(BAD_TIME)
        exit(0)
    SUNRISE_12H = B1
except IndexError:
    print(BAD_TIME)
    exit(0)
TIME.sleep(DELAY)
#SUNSET Time Converter
SUNSET = input(userSunOFF)
try:
    A2 = SUNSET
    B2 = (A2[0] + A2[1] + A2[3] + A2[4])
    SUNSET_TIME = int(B2)
    if (B2 >= '0000' and B2 < '1200'):
        B2 = (A2[0] + A2[1] + ':' + A2[3] + A2[4] + ' AM')
        C2 = (A2[0] + A2[1])
        D2 = (A2[3] + A2[4])
        E2 = A2[0]
        if (E2 == '0'):
            B2 = B2[1:]
        if (C2 == '00'):
            B2 = ('12:' + C2 + ' AM')
        if (D2 > '59'):
            print(BAD_TIME)
            exit(0)
    elif (B2 >= '1200' and B2 < '2359'):
        C2 = (A2[0] + A2[1])
        D2 = (A2[3] + A2[4])
        if (D2 > '59'):
            print(BAD_TIME)
            exit(0)
        if (C2 == '12'):
            B2 = (C2 + ':' + D2 + ' PM')
        elif (C2 == '13'):
            E2 = '1'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '14'):
            E2 = '2'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '15'):
            E2 = '3'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '16'):
            E2 = '4'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '17'):
            E2 = '5'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '18'):
            E2 = '6'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '19'):
            E2 = '7'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '20'):
            E2 = '8'
            B2 = (E2 + ':' + D2 + ' PM') 
        elif (C2 == '21'):
            E2 = '9'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '22'):
            E2 = '10'
            B2 = (E2 + ':' + D2 + ' PM')
        elif (C2 == '23'):
            E2 = '11'
            B2 = (E2 + ':' + D2 + ' PM')
        else:
            print(BAD_TIME)
            exit(0)    
    else:
        print(BAD_TIME)
        exit(0)
    SUNSET_12H = B2
except IndexError:
    print(BAD_TIME)
    exit(0)
TIME.sleep(DELAY)
print(NOTE + ' If no watering needed enter 0.')
TIME.sleep(DELAY)
DELAYPUMP = int(input(userPumpONE))
PUMPDELAY = str(DELAYPUMP)
TIME.sleep(DELAY)
if (DELAYPUMP != 0):
    DAE = 1
    WEEKDAY = int(input(userWeekday))
    if (WEEKDAY < 1) or (WEEKDAY > 7):
        print(BAD_INP)
        exit(0)
    DAYLIST = set()
    print(NOTE + ' enter only lowercase.')
    while (DAE <= WEEKDAY):
        DAYWEEK = input(userDayweek)
        DAE += 1
        DAYLIST.add(DAYWEEK)
        WEEKLIST = (', '.join(str(a) for a in DAYLIST))
        TIME.sleep(DELAY)
    #RAIN1 Time Converter
    RAIN1 = input(userRainONE)
    try:    
        A3 = RAIN1
        B3 = (A3[0] + A3[1] + A3[3] + A3[4])
        if (B3 >= '0000' and B3 < '1200'):
            B3 = (A3[0] + A3[1] + ':' + A3[3] + A3[4] + ' AM')
            C3 = (A3[0] + A3[1])
            D3 = (A3[3] + A3[4])
            E3 = A3[0]
            if (E3 == '0'):
                B3 = B3[1:]
            if (C3 == '00'):
                B3 = ('12:' + C3 + ' AM')
            if (D3 > '59'):
                print(BAD_TIME)
                exit(0)
        elif (B3 >= '1200' and B3 < '2359'):
            C3 = (A3[0] + A3[1])
            D3 = (A3[3] + A3[4])
            if (D3 > '59'):
                print(BAD_TIME)
                exit(0)
            if (C3 >= '12'):
                B3 = (C3 + ':' + D3 + ' PM')
            elif (C3 >= '13'):
                E3 = '1'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '14'):
                E3 = '2'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '15'):
                E3 = '3'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '16'):
                E3 = '4'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '17'):
                E3 = '5'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '18'):
                E3 = '6'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '19'):
                E3 = '7'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '20'):
                E3 = '8'
                B3 = (E3 + ':' + D3 + ' PM') 
            elif (C3 >= '21'):
                E3 = '9'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '22'):
                E3 = '10'
                B3 = (E3 + ':' + D3 + ' PM')
            elif (C3 >= '23'):
                E3 = '11'
                B3 = (E3 + ':' + D3 + ' PM')
            else:
                print(BAD_TIME)
                exit(0)
        else:
            print(BAD_TIME)
            exit(0)
        RAIN1_12H = B3
    except IndexError:
        print(BAD_TIME)
        exit(0)
    DRAIN1 = '20:00'
    DELAYSUMP = (DELAYPUMP / 2)
    SUMPDELAY = str(DELAYSUMP)
    TIME.sleep(DELAY)
else:  
    WEEKDAY = 0
    WEEKLIST = 'Null'
    DAYLIST = set('null')
    RAIN1 = '00:00'
    DRAIN1 = RAIN1
    RAIN1_12H = RAIN1


#Inputed Values printed back to user
print('\n' + INP_VAL)
TIME.sleep(DELAY)
print('Sunrise (Light On) at: ' + SUNRISE + '.')
TIME.sleep(DELAY)
print('Sunset (Light Off) at: ' + SUNSET + '.')
TIME.sleep(DELAY)
DAYLIGHT = str(SUNSET_TIME - SUNRISE_TIME)
DAYLIGHT = (DAYLIGHT[0] + DAYLIGHT[1] + '.' + DAYLIGHT[2] + DAYLIGHT[3])
print(DAYLIGHT + ' hours of sunlight.')
TIME.sleep(DELAY)
if (DELAYPUMP != 0):
    print('Watering (Pump Running) for ' + PUMPDELAY + ' seconds.')
    TIME.sleep(DELAY)
    print('Watering Days: ' + WEEKLIST + '.')
    TIME.sleep(DELAY)
    print('Watering (Pump Run) at ' + RAIN1 + '.\n')
    TIME.sleep(DELAY)
else:
    print('No Watering is Scheduled.\n')
    TIME.sleep(DELAY)

#User Input Formatted Text
SUNRISE_12H_C = (Y + SUNRISE_12H + WK)
SUNSET_12H_C = (G + SUNSET_12H + WK)
DELAYPUMP_C = (C + PUMPDELAY + WK)
RAIN1_12H_C = (C + RAIN1_12H + WK)
WEEKLIST_C = (C + WEEKLIST + WK)
DAYLIGHT_C = (P + DAYLIGHT + WK)

#Times Message Formating
if (DELAYPUMP != 0):
    TIMES = (R3MINDER +  ' Sunrise at ' + SUNRISE_12H_C + ', Sunset at ' + SUNSET_12H_C + ', ' + DAYLIGHT_C + ' hours of sunlight. Watering every ' + WEEKLIST_C + ' at: ' + RAIN1_12H_C + ' for ' + DELAYPUMP_C + ' Seconds.')
else:
    TIMES =(R3MINDER + ' Sunrise at ' + SUNRISE_12H_C + '.  Sunset at ' + SUNSET_12H_C + ', ' + DAYLIGHT_C + ' hours of sunlight. Watering every ' + '. No Watering Scheduled.')

#Light On Function
def SUNON():
    GPIO.output(PIN_RC4_BCM, GPIO.HIGH)
    GPIO.output(PIN_RC1_BCM, GPIO.HIGH)
    Light_On_Clock = DATETIME.now().strftime(CLOCK_24H)
    with open(r'_sunrain.log', 'a') as LOG:
        LOG.write('Light has turned on at: ' + Light_On_Clock + '.\n')
    print('Light has turned ' + LIGHT_ON + Light_On_Clock + '.\n')
    TIME.sleep(DELAY)
    print(TIMES)
    TIME.sleep(DELAY)
    print(WB + 'Current Temperature: ' + (ENV.temp()) + '.' + ' Current Humidity: ' + (ENV.humi()) + '.' + ' Current Time: ' + DATETIME.now().strftime(TIME_24H) + '.' + WK + '\n')
#Light Off Function
def SUNOFF():
    GPIO.output(PIN_RC4_BCM, GPIO.LOW)
    GPIO.output(PIN_RC1_BCM, GPIO.LOW)
    Light_Off_Clock = DATETIME.now().strftime(CLOCK_24H)
    with open(r'_sunrain.log', 'a') as LOG:
        LOG.write('Light has turned off at: ' + Light_Off_Clock + '.\n')
    print('Light has turned ' + LIGHT_OFF + Light_Off_Clock + '.\n')
    TIME.sleep(DELAY)
    print(TIMES)
    TIME.sleep(DELAY)
    print(WB + 'Current Temperature: ' + (ENV.temp()) + '.' + ' Current Humidity: ' + (ENV.humi()) + '.' + ' Current Time: ' + DATETIME.now().strftime(TIME_24H) + '.' + WK + '\n')
   
#Reminder of On, Off, and Watering Times
def REMIND():
    print(TIMES)
    TIME.sleep(DELAY)
    print(WB + 'Current Temperature: ' + (ENV.temp()) + '.' + ' Current Humidity: ' + (ENV.humi()) + '.' + ' Current Time: ' + DATETIME.now().strftime(TIME_24H) + '.' + WK + '\n')

#Displays REMIND() once when script is  started
def REMIND_ONCE():
    print(TIMES)
    TIME.sleep(DELAY)
    print(WB + 'Current Temperature: ' + (ENV.temp()) + '.' + ' Current Humidity: ' + (ENV.humi()) + '.' + ' Current Time: ' + DATETIME.now().strftime(TIME_24H) + '.' + WK + '\n')
    TIME.sleep(DELAY)
    return SCHEDULE.CancelJob

#Water Pump Function
def PUMPONE():
    if (DELAYPUMP != 0):
        print(PUMP_ONE + ' is ' + PUMP_ON + ' Timestamp: ' + DATETIME.now().strftime(CLOCK_12H) + '.')
        START_P1 = DATETIME.now().strftime(CLOCK_24H)
        db_START_P1 = DATETIME.now().strftime(TIME_24H)
        GPIO.output(PIN_RC3_BCM, GPIO.LOW) #pull pin low to turn pump on
        TIME.sleep(DELAYPUMP) #duration pump is on
        GPIO.output(PIN_RC3_BCM, GPIO.HIGH) #pull pin high to turn pump off
        STOP_P1 = DATETIME.now().strftime(CLOCK_24H)
        db_STOP_P1 = DATETIME.now().strftime(TIME_24H)
        with open (r'_sunrain.log', 'a') as LOG:
            LOG.write('Pump One was actiavted at ' + START_P1 + ' ran for ' + PUMPDELAY + 's. Was deactivated at ' + STOP_P1 + '\n')
        print(PUMP_ONE + ' is ' + PUMP_OFF + ' Ran for ' + PUMPDELAY + 's. Timestamp: ' + DATETIME.now().strftime(CLOCK_12H) + '.\n')
        TIME.sleep(DELAY)
        print(TIMES)
        TIME.sleep(DELAY)
        print(WB + 'Current Temperature: ' + (ENV.temp()) + '.' + ' Current Humidity: ' + (ENV.humi()) + '.' + ' Current Time: ' + DATETIME.now().strftime(TIME_24H) + '.' + WK + '\n')

def SUMPONE():
    if (DELAYPUMP != 0):
        print(SUMP_ONE + ' is ' + SUMP_ON + ' Timestamp: ' + DATETIME.now().strftime(CLOCK_12H) + '.')
        START_S1 = DATETIME.now().strftime(CLOCK_24H)
        db_START_S1 = DATETIME.now().strftime(TIME_24H)
        GPIO.output(PIN_RC2_BCM, GPIO.LOW)
        TIME.sleep(DELAYSUMP)
        GPIO.output(PIN_RC2_BCM, GPIO.HIGH)
        STOP_S1 = DATETIME.now().strftime(CLOCK_24H)
        db_STOP_S1 = DATETIME.now().strftime(TIME_24H)
        with open (r'_sunrain.log', 'a') as LOG:
            LOG.write('Sump was actiavted at ' + START_S1 + ' ran for ' + SUMPDELAY + 's. Was deactivated at ' + STOP_S1 + '\n')
        print(SUMP_ONE + ' is ' + SUMP_OFF + ' Ran for ' + PUMPDELAY + 's. Timestamp: ' + DATETIME.now().strftime(CLOCK_12H) + '.\n')
        TIME.sleep(DELAY)
        print(TIMES)
        TIME.sleep(DELAY)
        print(WB + 'Current Temperature: ' + (ENV.temp()) + '.' + ' Current Humidity: ' + (ENV.humi()) + '.' + ' Current Time: ' + DATETIME.now().strftime(TIME_24H) + '.' + WK + '\n')

#Scheduler
ON = SCHEDULE.Scheduler()
OFF = SCHEDULE.Scheduler()
REMINDER = SCHEDULE.Scheduler()
PUMPS = SCHEDULE.Scheduler()
SUMP = SCHEDULE.Scheduler()
try: 
    try:
        #Light Control Schedules
        ON.every().day.at(SUNRISE).do(SUNON)
        OFF.every().day.at(SUNSET).do(SUNOFF)
        #Sunrise/Sunset Reminder Schedules
        DELAYREM = 5
        REMINDER.every(DELAYREM).hours.do(REMIND)
        REMINDER.every().second.do(REMIND_ONCE)
        #Pump One Control Schedules
        if 'monday' in DAYLIST:
            PUMPS.every().monday.at(RAIN1).do(PUMPONE)
            SUMP.every().monday.at(DRAIN1).do(SUMPONE)
        if 'tuesday' in DAYLIST:
            PUMPS.every().tuesday.at(RAIN1).do(PUMPONE)
            SUMP.every().tuesday.at(DRAIN1).do(SUMPONE)
        if 'wednesday' in DAYLIST:
            PUMPS.every().wednesday.at(RAIN1).do(PUMPONE)
            SUMP.every().wednesday.at(DRAIN1).do(SUMPONE)
        if 'thursday' in DAYLIST:
            PUMPS.every().thursday.at(RAIN1).do(PUMPONE)
            SUMP.every().thursday.at(DRAIN1).do(SUMPONE)
        if 'friday' in DAYLIST:
            PUMPS.every().friday.at(RAIN1).do(PUMPONE)
            SUMP.every().friday.at(DRAIN1).do(SUMPONE)
        if 'saturday' in DAYLIST:
            PUMPS.every().saturday.at(RAIN1).do(PUMPONE)
            SUMP.every().saturday.at(DRAIN1).do(SUMPONE)
        if 'sunday' in DAYLIST:
            PUMPS.every().sunday.at(RAIN1).do(PUMPONE)
            SUMP.every().sunday.at(DRAIN1).do(SUMPONE)
    except ScheduleValueError:
        pass
except NameError:
    print(BAD_TIME)
    exit(0)  

#Background Thread Function (https://schedule.readthedocs.io/en/stable/background-execution.html)
BACK_RUN = SCHEDULE.Scheduler()
DELAYBACK = 1 #Function specific delay variable
def RUN_ALWAYS(DELAYBACK):
    STOP_RUN = THREADING.Event()
    class SCHEDULE_THREAD(THREADING.Thread):
        @classmethod
        def run(cls):
            while not STOP_RUN.is_set():
                BACK_RUN.run_pending()
                TIME.sleep(DELAYBACK)
    ALWAYS_THREAD = SCHEDULE_THREAD()
    ALWAYS_THREAD.start()
    return STOP_RUN
def BACKGROUND():
    return SCHEDULE.CancelJob
TIME.sleep(DELAYBACK)
STOP_RUN = RUN_ALWAYS(DELAYBACK)
BACK_RUN.every().second.do(BACKGROUND)

#Log file check
if not OS.path.exists(r'./sunrain_files/_sunrain.log'):
    print('\n_sunrain.log ' + DOES_NOT_EXIST + ' Creating File...')
    TIME.sleep(DELAY)
    with open(r'_sunrain.log', 'w') as LOG:
        if (DELAYPUMP != 0):
            LOG.write('Script started at: ' + DATETIME.now().strftime(CLOCK_24H) + '.\n')
            LOG.write('Light is On at ' + SUNRISE + '. Light is Off at ' + SUNSET + '. Weekdays pump is active on ' + WEEKLIST + ' for ' + PUMPDELAY + ' seconds.\n')
            
        else:
            LOG.write('Script started at: ' + DATETIME.now().strftime(CLOCK_24H) + '.\n')
            LOG.write('Light is On at ' + SUNRISE + '. Light is Off at ' + SUNSET + '.\n')
    print('File Created.\n\n')
    TIME.sleep(DELAY)
else:
    print('\n_sunrain.log ' + EXISTS + ' Apending.')
    TIME.sleep(DELAY)
    with open(r'_sunrain.log', 'a') as LOG:
        if (DELAYPUMP != 0):
            LOG.write('Script started at: ' + DATETIME.now().strftime(CLOCK_24H) + '.\n')
            LOG.write('Light is On at ' + SUNRISE + '. Light is Off at ' + SUNSET + '. Weekdays pump is active on ' + WEEKLIST + ' for ' + PUMPDELAY + ' seconds.\n')
        else:
            LOG.write('Script started at: ' + DATETIME.now().strftime(CLOCK_24H) + '.\n')
            LOG.write('Light is On at ' + SUNRISE + '. Light is Off at ' + SUNSET + '.\n')
    print('File Appended.\n\n')
    TIME.sleep(DELAY)

#Script Primary Loop Function
while True:
    try:
        try:
            #Runs Schedulers with Schedules
            DELAYMAIN = 1
            ON.run_pending()
            OFF.run_pending()
            REMINDER.run_pending()
            if (DELAYPUMP != 0):
                PUMPS.run_pending()
                SUMP.run_pending()
            TIME.sleep(DELAYMAIN)
        except OSError as OSE:
            print(OSE + '. Trying SHT30 Again...')
            TIME.sleep(DELAYMAIN)
            print(WB + ' Current Temperature: ' + (ENV.temp()) + '.' + WK + BW + ' Current Humidity: ' + (ENV.humi()) + '.' + WK + CK + ' Current Time: ' + DATETIME.now().strftime(TIME_24H) + '.' + WK + '\n')
    #Keyboard Interupt (Ctrl+C) will end Main Loop
    except KeyboardInterrupt:
        STOP_RUN.set()
        GPIO.output(PIN_RC3_BCM, GPIO.HIGH)
        GPIO.output(PIN_RC2_BCM, GPIO.HIGH)
        GPIO.cleanup()
        with open(r'./sunrain_files/_sunrain.log', 'a') as LOG:
            LOG.write('Script Terminated at: ' + DATETIME.now().strftime(CLOCK_24H) + '.\n\n')
        print('\nNo longer running in background thread!\n')
        break
exit(0)