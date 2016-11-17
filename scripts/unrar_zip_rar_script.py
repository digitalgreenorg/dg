
import gzip

import os, sys
import MySQLdb
import datetime

import glob



dbName = glob.glob("*.gz")
# delete db before 3 days ago
for i in range(len(dbName) - 3) :
	os.remove(dbName[i])

db_name = dbName[len(dbName) - 1].split('_')
with gzip.open(dbName[len(dbName) - 1], 'rb') as infile:
    with open(dbName[len(dbName) - 1][:-3], 'wb') as outfile:
        for line in infile:
            outfile.write(line)


now = datetime.datetime.now()
month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
db = MySQLdb.connect("localhost","root","root")
cursor = db.cursor()
month = month_list[now.month - 1]
day = str(now.day)

prev_day =  db_name[2] + '_' + month_list[int(db_name[1]) - 1]
cdate = 'dg_' + prev_day
 
sql = '''create schema ''' + cdate
cursor.execute(sql)
db.close()



file = open("sql_dump.bat", "w")

dbName = glob.glob("*.sql")

# delete previous sql
for i in range(len(dbName) - 1) :
	os.remove(dbName[i])


line1 = "mysql -u root -proot " + cdate + ' < ' + dbName[len(dbName) - 1]  + '\n'
line2 = "PAUSE"

file.write(line1)
file.write(line2)

file.close()
