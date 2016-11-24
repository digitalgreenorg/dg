import gzip
import os, sys
import MySQLdb
import datetime
import django
import glob


sys.path.append(os.path.abspath(os.path.realpath('..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
django.setup()
from dg.settings import DATABASES

#script to download db from S3
execfile("download_from_s3.py")

dbName = glob.glob("*.gz")
# delete previous db 
for i in range(len(dbName) - 1) :
	os.remove(dbName[i])

db_name = dbName[len(dbName) - 1].split('_')
# Unrar gz file
with gzip.open(dbName[len(dbName) - 1], 'rb') as infile:
	print infile
	with open(dbName[len(dbName) - 1][:-3], 'wb') as outfile:
		for line in infile:
			outfile.write(line)

dbName = glob.glob("*.sql")

# delete previous sql
for i in range(len(dbName) - 1) :
	os.remove(dbName[i])

user_name = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
database = DATABASES['default']['NAME']

dumpcmd = 'mysql -u' + user_name + ' -p' + password + ' ' + database + '<' +  dbName[0]
os.system(dumpcmd)