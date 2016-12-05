# Script to download and import database from S3
import gzip
import os, sys
import MySQLdb
import datetime
import django
import glob

sys.path.append(os.path.abspath(os.path.realpath('..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
from dg.settings import DATABASES

user_name = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']

#script to download db from S3
execfile("download_from_s3.py")

dbName = glob.glob("*.gz")

# buffer size showing delete all except one.
# buffer_size = 1
# for i in range(len(dbName) - buffer_size) :
# 	os.remove(dbName[i])

db_name = dbName[len(dbName) - 1].split('_')
# Unrar gz file
with gzip.open(dbName[len(dbName) - 1], 'rb') as infile:
	print infile
	with open(dbName[len(dbName) - 1][:-3], 'wb') as outfile:
		for line in infile:
			outfile.write(line)


list_argument =  sys.argv[1:]
custom_db_name = ''
if(len(list_argument) >  0) :
	custom_db_name = list_argument[0]
else :
	# To create DB name according to date:
	month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	prev_day =  db_name[2] + '_' + month_list[int(db_name[1]) - 1]
	custom_db_name = 'dg_' + prev_day

# Mysql Connection
db = MySQLdb.connect("localhost", user_name, password)
cursor = db.cursor()
drop_database_sql = "DROP DATABASE IF EXISTS " + custom_db_name
cursor.execute(drop_database_sql)
sql = '''create schema ''' + custom_db_name
cursor.execute(sql)
db.close()

dbName = glob.glob("*.sql")

# delete previous sql leaving one
# for i in range(len(dbName) - buffer_size) :
# 	os.remove(dbName[i])

# To use current DB replace database = DATABASES['default']['NAME']
database = custom_db_name

dumpcmd = 'mysql -u' + user_name + ' -p' + password + ' ' + database + '<' +  dbName[0]
os.system(dumpcmd)
