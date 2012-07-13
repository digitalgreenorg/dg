import glob, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.core.management import setup_environ
import settings


setup_environ(settings)

from dashboard.models import *
ACCESS_KEY = '01GE4NJEXRFQTBCFG782'
SECRET_KEY = 'bK8gt4siHBryH/cRagSMtcDPwNbfB0l2E/KXVhYy'
BUCKET_NAME = 'dg_farmerbook'
# Get already created bucket dg_farmerbook
con = S3Connection(ACCESS_KEY, SECRET_KEY)
bucket = con.get_bucket(BUCKET_NAME)
i=0
rs = bucket.list("2/")
# Creating thumbnails for all images in current directory
for key in rs:
	key_name = key.name
	file_extension = os.path.splitext(key_name)
	print key_name
	farmer_id1 = file_extension[0][2:]
	print farmer_id1
	try:
		farmer_id = int(farmer_id1)
	except ValueError:
		print "Value error "+ farmer_id1 	
		farmer_id = 0		
	if Person.objects.filter(id = farmer_id).exists():
		p = Person.objects.filter(id = farmer_id).update(image_exists = True)
		print i
		i= i+1
	else:
		print 'id does not exist'+str(farmer_id)	