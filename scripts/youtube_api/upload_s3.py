from boto.s3.connection import S3Connection
import os
from boto.s3.key import Key


ACCESS_KEY = 'AKIAIKTVJKVVHA7Y4HNA'
SECRET_KEY = '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'
BUCKET_NAME = 'video_thumbnail'
 
con = S3Connection(ACCESS_KEY, SECRET_KEY)
 
bucket = con.create_bucket(BUCKET_NAME)
bucket.set_acl('public-read')

files_list = os.listdir(r'C:\Users\Aadish\Desktop\image_upload_video_id')
for root, dirs, files in os.walk(r'C:\Users\Aadish\Desktop\image_upload_video_id'):
    print (len(files))
    for file in files:
        print (file)
        key = file
        if (root[-1] == 'd'):
            key = 'raw/' + file
        if (root[-1] == '6'):
            key = '16by9/' + file
        if (root[-1] == '4'):
            key = '4by3/' + file
        if not bucket.get_key(key):
            print root
            print file
            k = Key(bucket)
            k.key = key
            k.set_contents_from_filename(root+'\\'+file)
            k.make_public()

 

  

