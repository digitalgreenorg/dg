# -*- coding: utf-8 -*-
import os
import dg.settings
from django.core.management import setup_environ
setup_environ(dg.settings)
from userfile_functions import read_userfile, make_upload_file, upload_file

data = read_userfile(os.path.dirname(__file__)+'\cases.json')
for entry in data:
    print entry['username']
    villages = entry['villages']
    filename = entry['username'] + '.xml'
    file_to_upload = make_upload_file(villages, filename, entry['user_id'])
    break
    
    

