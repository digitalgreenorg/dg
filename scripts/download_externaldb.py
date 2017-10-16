from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import datetime
import os, sys
import django
# from copy_db_from_rds import upload_file_prod, upload_file_ext

sys.path.append(os.path.abspath(os.path.realpath('..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
import dg.settings

def show_status(received, total):
    percent = (float(received)/total) * 100
    sys.stdout.write("\r%f%%" % percent)
    sys.stdout.flush()

ACCESS_KEY = dg.settings.ACCESS_KEY
SECRET_KEY = dg.settings.SECRET_KEY
BUCKET_NAME = 'externaldb_backups'
DOWNLOAD_FOLDER = os.path.abspath(os.getcwd()) + '/'

con = S3Connection(ACCESS_KEY, SECRET_KEY)
bucket = con.get_bucket(BUCKET_NAME)
key_prod = bucket.get_key('production.sql.gz')
# key_ext = bucket.get_key('external.sql.gz')

print "Downloading", key_prod.name, "\n"
key_prod.get_contents_to_filename(filename=DOWNLOAD_FOLDER + key_prod.name, cb=show_status, num_cb=200)
print "Download Finished"
