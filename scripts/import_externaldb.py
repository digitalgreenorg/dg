# Script to download and import database from S3
import django
import os, sys, glob, gzip, datetime, MySQLdb
from datetime import date
from download_externaldb import *

sys.path.append(os.path.abspath(os.path.realpath('..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
from dg.settings import DATABASES

user_name = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
hostname = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']

#script to download db from S3
# execfile("download_externaldb.py")

dg_gz = 'production.sql.gz'

# Unrar gz file
with gzip.open(dg_gz, 'rb') as infile:
	with open(dg_gz[:-3], 'wb') as outfile:
		for line in infile:
			outfile.write(line)

mysql_query = 'mysql -u' + user_name + ' -p'+ password + ' -h' +  hostname + ' -P'+ str(port) + ' < ' + dg_gz[:-3]
# print mysql_query
os.system(mysql_query)
