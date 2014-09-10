import os

from boto.s3.connection import S3Connection

from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from dg.settings import S3_ACCESS_KEY, S3_SECRET_KEY, MEDIA_ROOT
from dg.settings import ACCESS_KEY, SECRET_KEY

from libs.s3_utils import add_to_s3

from geographies.models import Village
from people.models import Animator, Person, PersonGroup


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
    print key.name
    new_key_name = ""
    l = (key.name).split('/')
    dir_name = l[0]
    file_name = l[-1]
    if(dir_name == '1' or dir_name == '2'):
        if(file_name.find('.') != -1):
            person_id = file_name.split('.')[0]
            if person_id.isdigit():
                try:
                    obj = Person.objects.get(old_coco_id=person_id)
                    new_key_name = "".join([dir_name, '/', str(obj.id), '.jpg'])
                except Person.DoesNotExist:
                    print "Person Does Not Exist"
    elif(dir_name == 'group'):
        if(file_name.find('.') != -1):
            group_id = file_name.split('.')[0]
            if group_id.isdigit():
                try:
                    obj = PersonGroup.objects.get(old_coco_id=group_id)
                    new_key_name = "".join([dir_name, '/', str(obj.id), '.jpg'])
                except PersonGroup.DoesNotExist:
                    print "Person Group Does Not Exist"
    elif(dir_name == 'csp'):
        if(file_name.find('.') != -1):
            animator_id = file_name.split('.')[0]
            if animator_id.isdigit():
                try:
                    obj = Animator.objects.get(old_coco_id=animator_id)
                    new_key_name = "".join([dir_name, '/', str(obj.id), '.jpg'])
                except Animator.DoesNotExist:
                    print "Animator Does Not Exist"
    elif(dir_name == 'village'):
        if(file_name.find('.') != -1):
            village_id = file_name.split('.')[0]
            if village_id.isdigit():
                try:
                    obj = Village.objects.get(old_coco_id=village_id)
                    new_key_name = "".join([dir_name, '/', str(obj.id), '.jpg'])
                except Village.DoesNotExist:
                    print "Village Does Not Exist"
    if(len(dir_name) == 11 or len(dir_name) == 14):
        try:
            obj = Person.objects.get(old_coco_id=dir_name)
            new_key_name = "".join([str(obj.id), '/', file_name.replace('JPG', 'jpg')])
        except Person.DoesNotExist:
            print "Person Does Not Exist"

    if new_key_name != '':
        if not bucket_new.get_key(new_key_name):
            print new_key_name
            save_name = key.name.replace('/', '_')
            key.get_contents_to_filename(folder_path + save_name)
            add_to_s3(bucket_new, new_key_name, folder_path + save_name)
        else:
            if not os.path.exists(folder_path + key.name):
                os.makedirs(folder_path + key.name)
