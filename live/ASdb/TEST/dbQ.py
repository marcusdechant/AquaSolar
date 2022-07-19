#!/bin/python3

import sqlite3 as sql

#db_num = input('Run ID? ')
db = ('t8.db')
database = sql.connect(db)
cur = database.execute('''
SELECT * FROM TEST
''')
print()
print('ID, NUM')

for row in cur:
    r0 = str(row[0])
    r1 = str(row[1])
    #r2 = str(row[2])
    #r3 = str(row[3])
    #r4 = str(row[4])
    s = ', '
    print(r0 + s + r1)

print('End of Database')
cur.close()
database.close()
exit(0)
