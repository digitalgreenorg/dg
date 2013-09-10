# -*- coding: utf-8 -*-
import os
import dg.settings
from django.core.management import setup_environ
setup_environ(dg.settings)
from userfile_functions import read_userfile, make_upload_file, upload_file
from dimagi.models import CommCareUser, CommCareUserVillage

case_user_dict = {}
case_person_dict = {}
#getting user data from database
users = CommCareUser.objects.all()
data = []
dict = {}
for user in users:
    dict['username'] = user.username
    dict['user_id'] = user.guid 
    villages = CommCareUserVillage.objects.filter(user = user.id)
    dict['villages']=[]
    for vil in villages:
        dict['villages'].append(vil.village.id)
    data.append(dict)
    
for entry in data:
    print entry['username']
    villages = entry['villages']
    filename = entry['username'] + '.xml'
    make_upload_file(villages, filename, entry['user_id'], case_user_dict, case_person_dict)
    response = upload_file(filename)
    if response == 201 or response == 200:
       print "Successfully uploaded cases for " +entry['username']
       