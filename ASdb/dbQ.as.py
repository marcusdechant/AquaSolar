#!/bin/python3

import sqlite3 as sql

s=', '
db=('aquasolar.db')

while(True):
    try:
        table=str.lower(input('\nEvents, Sun, Rain, THS, or Pi Stats?\n'))
        
        database=sql.connect(db)
        
        if(table=='events'):
            cur=database.execute('''SELECT * FROM EVENTS''')
            print('\nID, EVENT, INFO, TIME, DATE')
            for row in cur:
                r0=str(row[0])
                r1=str(row[1])
                r2=str(row[2])
                r3=str(row[3])
                r4=str(row[4])
                print(r0+s+r1+s+r2+s+r3+s+r4)
            break
            
        elif(table=='sun'):
            cur=database.execute('''SELECT * FROM SUN''')
            print('\nDay, Sunrise, Sunset')
            for row in cur:
                r0=str(row[0])
                r1=str(row[1])
                r2=str(row[2])
                print(r0+s+r1+s+r2)
            break
            
        elif(table=='rain'):
            cur=database.execute('''SELECT * FROM RAIN''')
            print('\nDay, Sunrise, Sunset')
            for row in cur:
                r0=str(row[0])
                r1=str(row[1])
                r2=str(row[2])
                r3=str(row[3])
                print(r0+s+r1+s+r2+r3)
            break
            
        elif(table=='ths'):
            cur=database.execute('''SELECT * FROM SENSOR1''')
            print('\nID, Delay, Temp, Humi, Time, Date')
            for row in cur:
                r0=str(row[0])
                r1=str(row[1])
                r2=str(row[2])
                r3=str(row[3])
                r4=str(row[4])
                r5=str(row[5])
                print(r0+s+r1+s+r2+s+r3+s+r4+s+r5)
            break
            
        elif(table=='pi_stats'):
            cur=database.execute('''SELECT * FROM PI_STATS''')
            print('\nID, Delay, CPUTemp, CPULoad, Time, Date')
            for row in cur:
                r0=str(row[0])
                r1=str(row[1])
                r2=str(row[2])
                r3=str(row[3])
                r4=str(row[4])
                r5=str(row[5])
                print(r0+s+r1+s+r2+s+r3+s+r4+s+r5)
            break
        
        else:
            print('error')
            pass
            
    except KeyboardInterrupt:
        print('\n')
        exit(0)
print('End of Database\n')
cur.close()
database.close()
exit(0)
