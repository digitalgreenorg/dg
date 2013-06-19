from boto.s3.connection import S3Connection
import os
from boto.s3.key import Key


ACCESS_KEY = '01GE4NJEXRFQTBCFG782'
SECRET_KEY = 'bK8gt4siHBryH/cRagSMtcDPwNbfB0l2E/KXVhYy'
BUCKET_NAME = 'video_thumbnail'

con = S3Connection(ACCESS_KEY, SECRET_KEY)

bucket = con.get_bucket(BUCKET_NAME)
bucket.set_acl('public-read')

files_list = os.listdir(r'C:\Users\Aadish\Desktop\image_upload_video_id')
 
for file in files_list:
     if not bucket.get_key(file):
         print file
         print type(file)
         k = Key(bucket)
         k.key = file
         k.set_contents_from_filename(file)
         k.make_public()
 

  

