import os

from boto.s3.connection import S3Connection

from dg.settings import S3_ACCESS_KEY, S3_SECRET_KEY, MEDIA_ROOT
from dg.settings import ACCESS_KEY, SECRET_KEY

from libs.s3_utils import add_to_s3

#old S3 Account
bucket_name = 'dg_farmerbook'
conn = S3Connection(S3_ACCESS_KEY, S3_SECRET_KEY)
bucket = conn.get_bucket(bucket_name)

#new S3 Account
bucket_name_new = 'dg-farmerbook'
bucket_new = S3Connection(ACCESS_KEY, SECRET_KEY).create_bucket(bucket_name_new)
bucket_new.set_acl('public-read')

folder_path = MEDIA_ROOT + 'farmerbook/'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

buck_list = bucket.list()

for key in buck_list:
    if key.name.find('.') != -1:
        print key.name
        if not bucket_new.get_key(key.name.replace("JPG", "jpg")):
            key.get_contents_to_filename(folder_path + key.name)
            add_to_s3(bucket_new, key.name.replace("JPG", "jpg"), folder_path + key.name)
    else:
        if not os.path.exists(folder_path + key.name):
            os.makedirs(folder_path + key.name)
