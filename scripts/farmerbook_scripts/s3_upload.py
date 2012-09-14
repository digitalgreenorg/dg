import glob, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
ACCESS_KEY = '01GE4NJEXRFQTBCFG782'
SECRET_KEY = 'bK8gt4siHBryH/cRagSMtcDPwNbfB0l2E/KXVhYy'
BUCKET_NAME = 'dg_farmerbook'
# Get already created bucket dg_farmerbook
con = S3Connection(ACCESS_KEY, SECRET_KEY)
bucket = con.get_bucket(BUCKET_NAME)
i=0
# uploading thumbnails of all images in current directory
for root, dirs, files in os.walk(r'C:\Users\Yash\Desktop\DG\scripts\village_wise\to_upload'):
    for file_name in files:
		file_extension = os.path.splitext(file_name)
		if(file_extension[1].upper() in [".JPG", ".JPEG", ".PNG", ".BMP"]):
			if not bucket.get_key('2/' + file_name):
				k = Key(bucket)
				#1/for original image and 2/for thumbnail and /test for testing
				k.key = '2/' + file_name
				k.set_contents_from_filename(os.path.join(root, file_name))
				k.make_public()
				i = i + 1
				print "uploading done : " + str(i)
			else:
				# What to do if it already exists- Overwrite or Replace 
				k = Key(bucket)
				#1/for original image and 2/for thumbnail and /test for testing
				k.key = '2/' + file_name
				k.set_contents_from_filename(os.path.join(root, file_name))
				k.make_public()
				i = i + 1
				print "replacing done : " + str(i)
				