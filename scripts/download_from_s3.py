from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import datetime
import os, sys
import django

sys.path.append(os.path.abspath(os.path.realpath('..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
import dg.settings

def show_status(received, total):
    percent = (float(received)/total) * 100
    sys.stdout.write("\r%f%%" % percent)
    sys.stdout.flush()

ACCESS_KEY = dg.settings.ACCESS_KEY
SECRET_KEY = dg.settings.SECRET_KEY
BUCKET_NAME = 'dgbackups'
DOWNLOAD_FOLDER = os.path.abspath(os.getcwd()) + '/'

con = S3Connection(ACCESS_KEY, SECRET_KEY)
dg_bk = con.get_bucket(BUCKET_NAME)
ks = dg_bk.get_all_keys()

ks = filter(lambda x: x.name[:2] == "db", ks)
def cmp_key(x,y):
    return cmp(datetime.strptime(x.name[3:-7], "%Y_%m_%d_%H_%M"), datetime.strptime(y.name[3:-7], "%Y_%m_%d_%H_%M"))

ks.sort(cmp=cmp_key, reverse=True)

if ks[0].name in os.listdir(DOWNLOAD_FOLDER):
	print ks[0].name, "already exists"
else:
	print "Downloading", ks[0].name, "\n"
	ks[0].get_contents_to_filename(filename=DOWNLOAD_FOLDER + ks[0].name, cb=show_status, num_cb=200)
	print "Download Finished"
