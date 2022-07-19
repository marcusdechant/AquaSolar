#!/bin/python3/Test

import sqlite3 as sql
import os

conn = sql.connect

database = (r't8.db')

db = conn(database)

ex = db.execute
close = db.close
save = db.commit

ex('''
CREATE TABLE IF NOT EXISTS TEST(
ID      INT     NOT NULL     PRIMARY KEY,
NUM     INT    NOT NULL);
''')

ID = 0

if os.path.exists(database):
    num = ex('''SELECT ID FROM TEST''')
    for row in num:
        ID = int(row[0])

a = 0

while(a != 100):
    a += 1
    ID += 1
    ex('''
    INSERT INTO TEST (ID,NUM)
    VALUES(?,?)''',
    (ID,a))
    save()
    last = ex('''SELECT ID FROM TEST''')
    for row in last:
        nID = int(row[0])
print(nID)    
close()

"""
def test1():
    ID = 1
    ex('''
    INSERT INTO TEST1 (ID,EVENT)
    VALUES (?,?)''',
    (ID, 'test1'))
    save()
    return(ID)
    close()

def test2():
    ID = test1()
    print(ID)
    
test2()
"""



exit(0)