# Script to download and import database from S3
import django
import os, sys, glob, gzip, datetime, MySQLdb
from datetime import date

sys.path.append(os.path.abspath(os.path.realpath('..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
from dg.settings import DATABASES

user_name = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
host = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']

#script to download db from S3
execfile("download_from_s3.py")

dg_gz = sorted(glob.glob("*.gz"))[-1]
db_name = dg_gz.split('_')

# Unrar gz file
with gzip.open(dg_gz, 'rb') as infile:
	with open(dg_gz[:-3], 'wb') as outfile:
		for line in infile:
			outfile.write(line)

#read argument from cmd and set custom database name
list_argument =  sys.argv[1:]
custom_db_name = ''
if(list_argument) :
	custom_db_name = list_argument[0]
else :
	#create DB name according to date:
	prev_day =  db_name[2] + '_' + date(1900, int(db_name[1]), 1).strftime('%b')
	custom_db_name = 'dg_' + prev_day

# Mysql Connection
db = MySQLdb.connect(host=host, port=port, user=user_name, passwd=password)
cursor = db.cursor()
drop_database_sql = "DROP DATABASE IF EXISTS " + custom_db_name
cursor.execute(drop_database_sql)
sql = '''create schema ''' + custom_db_name
cursor.execute(sql)
db.close()

# To use current DB replace database = DATABASES['default']['NAME']
database = custom_db_name

print ("Import started : %s" %dg_gz[:-3])
#mysql command to import db
dumpcmd = 'mysql -u' + user_name + ' -p' + password + ' -h' + host + ' ' + database + '<' +  dg_gz[:-3]
os.system(dumpcmd)

# #set buffer size to remove previous sql and gz files
# buffer_size = 1
# file_types = ['*.gz','*.sql']
# [os.remove(i) for file in file_types for i in glob.glob(file)[:-buffer_size]]
