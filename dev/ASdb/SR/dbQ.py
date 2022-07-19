#!/bin/python3

import sqlite3 as sql

dbNum = input('Run ID? ')
db = ('SR.%s.db' %dbNum)
database = sql.connect(db)
cur = database.execute('''SELECT * FROM EVENTS''')
print()
print('ID,EVENT,INFO,TIME,DATE')

for row in cur:
    r0 = str(row[0])
    r1 = str(row[1])
    r2 = str(row[2])
    r3 = str(row[3])
    r4 = str(row[4])
    s = ', '
    print(r0 + s + r1 + s + r2 + s + r3 + s + r4)

print('End of Database')
cur.close()
database.close()
exit(0)
