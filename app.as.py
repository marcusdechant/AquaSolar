#!/bin/python3/AquaSolar

#Project AquaSolar
#Autonomous Gradening Project
#Marcus Dechant (c)
#app.as.py
#v0.0.3

import sqlite3 as sql
import os

from flask import Flask
from flask import render_template as template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for as url4

from werkzeug.utils import secure_filename

conn=sql.connect
database=r'./ASdb/aquasolar.db'
    
app=Flask(__name__)

def pi_stats_single():
    db=conn(database)
    xcte=db.execute
    clse=db.close
    curs=xcte('''SELECT ID,DELAY,CPUTEMP,AVELOAD,TIME,DATE FROM PI_STATS''')
    data=curs.fetchall()
    for row in data:
        rid=str(row[0])
        delay=str(row[1])
        cpuTemp=str(row[2])
        loadAve=str(row[3])
        time=str(row[4])
        date=str(row[5])
    clse()
    return(rid,delay,cpuTemp,loadAve,time,date)

def sensor_one_single():
    db=conn(database)
    xcte=db.execute
    clse=db.close
    curs=xcte('''SELECT TEMP,HUMI FROM SENSOR1''')
    data=curs.fetchall()
    for row in data:
        temp=str(row[0])
        humi=str(row[1])
    clse()
    return(temp,humi)

def pi_stats_all():
    db=conn(database)
    xcte=db.execute
    clse=db.close
    xaxis=request.args.get('x')
    try:
        curs=xcte('''SELECT ID,CPUTEMP,AVELOAD FROM PI_STATS PI_STATS ORDER BY LID DESC LIMIT %s''' %xaxis)
    except:
        xaxis=(-1)
        curs=xcte('''SELECT ID,CPUTEMP,AVELOAD FROM PI_STATS FROM PI_STATS ORDER BY LID DESC LIMIT %s''' %xaxis)
    data=reversed(curs.fetchall())
    ridAll=[]
    cpuTempAll=[]
    loadAveAll=[]
    for row in data:
        ridAll.append(row[0])
        cpuTempAll.append(row[1])
        loadAveAll.append(row[2])
    clse()
    return(ridAll,cpuTempAll,loadAveAll,xaxis)

def sensor_one_all():
    db=conn(database)
    xcte=db.execute
    clse=db.close
    xaxis=request.args.get('x')
    try:
        curs=xcte('''SELECT ID,TEMP,HUMI FROM PI_STATS SENSOR1 ORDER BY LID DESC LIMIT %s''' %xaxis)
    except:
        xaxis=(-1)
        curs=xcte('''SELECT ID,TEMP,HUMI FROM SENSOR1 FROM PI_STATS ORDER BY LID DESC LIMIT %s''' %xaxis)
    data=reversed(curs.fetchall())
    ridAll=[]
    tempAll=[]
    humiAll=[]
    for row in data:
        ridAll.append(row[0])
        tempAll.append(row[1])
        humiAll.append(row[2])
    clse()
    (ridAll,tempAll,humiAll,xaxis)

#/
@app.route('/', methods=['GET'])
def gauge():
    (rid,delay,cpuTemp,loadAve,time,date)=pi_stats_single()
    (temp,humi)=sensor_one_single()
    rV=(int(delay)*1000)
    base=delay*12
    x1=(int(base)/int(delay))
    x24=int(x1*24)
    gaugeData={'ID':rid, 'DELAY':delay, 'TIME':time, 'DATE':date,
               'CPUTEMP':cpuTemp, 'CPULOAD':loadAve, 'TEMP':temp,
               'HUMI':humi, 'refreshValue':rV, 'x1':x1, 'x24':x24, 'ex':None}
    return(template('gauge.html', **gaugeData)), 200
    
#/graph
@app.route('/graph', methods=['GET'])
def graph():
    (rid,delay,cpuTemp,loadAve,time,date)=pi_stats_single()
    (temp,humi)=sensor_one_single()
    (ridAll1,cpuTempAll,loadAveAll)=pi_stats_single()
    (ridAll2,tempAll,humiAll)=sensor_one_single()
    rV=delay*1000
    base=delay*12
    xH=int((int(xaxis)/base)*delay)
    if(xH==0):
        xH='ALL'
    x1=int(base/delay)
    x3=int(x1*3) #x1*3 = 3 hours
    x6=int(x1*6) #x1*6 = 6 hours
    x12=int(x1*12) #x1*12 = 12 hours
    x24=int(x1*24) #x1*24 = 24 hours
    xW=int(x24*7) #x24*7 = 7 days
    x4W=int(xW*4) #x7*4 = 4 weeks
    graphData={'ID1':ridAll1, 'ID2':ridAll2, 'ID':rid, 'CPUTEMPGR':cpuTempAll,
               'CPULOADGR':loadAveAll, 'TEMPGR':tempAll, 'HUMIGR':humiAll,
               'CPUTEMP':cpuTemp, 'CPULOAD':loadAve, 'TEMP':temp, 'HUMI':humi,
               'refreshValue':rV, 'xH':xH, 'x1':x1, 'x3':x3, 'x6':x6, 
               'x12':x12, 'x24':x24, 'xW':xW,  'x4W':x4W, 'ex':None}
    return(template('graph.html', **graphData)), 200

@app.route('/graph', methods=['POST','GET'])
def graph_input():
    if(request.method=='POST'):
        xID=request.form['x']
        inputData={'x':xID}
        return(redirect(url4('graph_input', **inputData))), 302
    return(template('graph.html')), 201

if(__name__=='__main__'):
    app.run(host='192.168.1.12', port=5002, debug=True)