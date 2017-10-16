import os, sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError

sys.path.append(os.path.abspath(os.path.realpath('..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
from dg.settings import ACCESS_KEY, SECRET_KEY, DATABASES

user_name = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
hostname = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']
bucket_name = 'externaldb_backups'
bucket = None
con = S3Connection(ACCESS_KEY, SECRET_KEY)

# preparing backup for external DB
production = 'production.sql'
external = 'external_db.sql'
sql_query_prod = 'mysqldump -u' + user_name + ' -p' + password + ' --databases digitalgreen > ' +  production
sql_query_ext = 'mysqldump -u' + user_name + ' -p' + password + ' --databases nrlm game sps > ' +  external
os.system(sql_query_prod)
os.system(sql_query_ext)
os.system('gzip ' + production)
os.system('gzip ' + external)

try :
	bucket = con.get_bucket(bucket_name)

	# delete all key
	#for obj in bucket.get_all_keys():
	#	bucket.delete_key(obj.key)

	# filepath
	upload_file_prod = production + '.gz'
	upload_file_ext = external + '.gz'
	key_prod = bucket.new_key(upload_file_prod)
	key_ext = bucket.new_key(upload_file_ext)

	print 'Uploading to Amazon S3 bucket %s' %(bucket.name)
	
	def percent_cb(complete, total):
		percent = (float(received)/total) * 100
		sys.stdout.write("\r%f%%" % percent)
		sys.stdout.flush()

	# To insert data into created key
	key_prod.set_contents_from_filename(upload_file_prod, cb = percent_cb, num_cb=200)
	key_ext.set_contents_from_filename(upload_file_ext, cb = percent_cb, num_cb=200)

	for obj in bucket.get_all_keys():
		print(obj.key)
	
except S3ResponseError as e:
	print str(e)
	print 'its okay, let\'s create one'
	bucket = con.create_bucket(bucket_name)
	print bucket
	
