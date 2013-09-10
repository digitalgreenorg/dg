import base64
import csv
import datetime
import json
import os
import urllib2
import uuid

from dashboard.models import PersonMeetingAttendance
from dimagi.models import CommCareCase
from django.db.models import get_model
from userfile_functions import upload_file, write_person_detail

def get_case_person_list():
    person_caseid_dict = {}
    cases = CommCareCase.objects.all()
    for case in cases:
        person_caseid_dict[case.person.id]=case.guid
    return person_caseid_dict
    
def get_case_id(person_id):
    return CommCareCase.objects.get(person__id=person_id).guid


def get_case_user_list():
    case_user_dict = {}
    cases = CommCareCase.objects.all()
    for case in cases:
        case_user_dict[case.guid]=case.user.guid
    return case_user_dict

def check_person_id(person_id):
    exists = False
    case = CommCareCase.objects.get(person__id=person_id) 
    if case.is_open==True:
        exists = True
    return exists

def close_case(case_id, filename):
    case_user_dict = get_case_user_list
    owner_id = case_user_dict[case_id]
    # Putting all the info in xml tags
    f = open(filename,'w')
    f.write('<?xml version="1.0" ?>\n')
    f.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    f.write('<num_people>1</num_people>\n')
    f.write('<people>\n')
    i = 0
    f.write('<n'+str(i)+':case case_id="'+str(case_id)+ '" date_modified="'+ str(datetime.datetime.now().date()) + '" user_id="' + owner_id +'" xmlns:n'+str(i)+'="http://commcarehq.org/case/transaction/v2">\n')
    f.write('<n'+str(i)+':create>\n')
    f.write('<n'+str(i)+':case_type>person</n'+str(i)+':case_type>\n')
    f.write('<n'+str(i)+':owner_id>' + owner_id + '</n'+str(i)+':owner_id>\n')
    f.write('</n'+str(i)+':create>\n')
    f.write('<n'+str(i)+':update>\n')
    f.write('</n'+str(i)+':update>\n')
    f.write('<n'+str(i)+':close>' + '1' + '</n'+str(i)+':videos_adopted>\n')
    f.write('</n'+str(i)+':case>\n')
    f.write('</people>\n')
    # Writing closing meta info of the form
    i += 1
    f.write('<n'+str(i) + ':meta xmlns:n' + str(i) + '="http://openrosa.org/jr/xforms">\n')
    f.write('<n'+str(i) + ':userID>' + owner_id + '</n' + str(i) + ':userID>\n')
    f.write('<n'+str(i) + ':instanceID>2729386f-7fd2-42cc-807f-786bf2dc952b</n' + str(i) + ':instanceID>\n')
    f.write('</n' + str(i) + ':meta>\n')
    f.write('</data>')
    f.close()
    return f

def get_person_id_from_pma(instance):
    PersonMeetingAttendance = get_model('dashboard',instance.entry_table)
    person_id = PersonMeetingAttendance.objects.get(id = instance.model_id).person.id
    return person_id
    
def update_case(sender, **kwargs):
    instance = kwargs["instance"]
    action  = instance.action
    if instance.entry_table == 'Person' or instance.entry_table == 'PersonMeetingAttendance' or instance.entry_table == 'PersonAdoptPractice':
        if instance.entry_table == 'Person':
            person_id = instance.model_id
        else:
            person_id = get_person_id_from_pma(instance)
        case_id = get_case_id(str(person_id))
        scripts_dir = os.path.dirname(__file__)
        dir = scripts_dir + "\case_update"
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = 'person' + str(person_id) + '.xml'
        filename = os.path.join(dir,filename)
        if action == 0 or action == 1:
            write_person_detail(person_id,filename,0, case_id )
        else:
            close_case(case_id, filename)
#        Uncomment the line below if cron job is not active/ or to have real time changes in pma
#        response = upload_file(filename)
#        print response

def write_dict(dict, filename):
    f = open(filename,'w')
    data = json.dumps(dict)
    f.write(data)

def read_dict(filename):
    json_data=open(filename).read()
    data = json.loads(json_data)
    return data

#
#user_ids = ['8a7cc079078e17fd20e068eb4bd05729', #Joshin
#            '8a7cc079078e17fd20e068eb4bb0f056'] #Disha
#get_case_user_list(user_ids)
#get_case_person_list()

