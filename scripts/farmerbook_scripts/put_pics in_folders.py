# SCRIPT TO PUT FARMER PICS FROM A SOURCE DIR INTO A DST DIR MAKING NEW FOLDERS 
# WITH FOLDER NAME AS THE VILLAGE_ID AND COPYING PHOTOS IN THEM

from django.core.management import setup_environ
import dg.settings
import shutil
setup_environ(dg.settings)
import sys, os, glob , string

from activities.models import *
from coco.models import *
from geographies.models import *
from programs.models import *
from people.models import *
from videos.models import *

source_dir = r'\dg\scripts\to_be_uploaded'
dst_dir = r'\dg\scripts\village_wise'

image_list=[]
for root, dirs, files in os.walk(source_dir):
    for name in files:
        image_list.append(name)

folder_count = image_count = not_found = 0
for name in image_list:
    person = name.split('.')[0]
    village = Person.objects.filter(id = person).values_list('village')
    if not village:
        not_found += 1
    else:
        directory = os.path.join(dst_dir,str(village[0][0]))
        if not os.path.exists(directory):
            os.makedirs(directory)
            folder_count += 1
        src = os.path.join(source_dir,name)
        dst = os.path.join(directory,name)
        shutil.copy2(src, dst)
        image_count += 1

print str(folder_count) + " folders made"
print str(image_count) + " images put in them"
print str(not_found) + " ids did not match any record in DB"
