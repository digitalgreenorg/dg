import base64
import csv
import datetime
import json
import os
import pickle
import urllib2
import uuid

from django.db.models import get_model
from userfile_functions import upload_file, write_person_detail

def get_case_person_list():
    BASE_URL = 'https://www.commcarehq.org/a/biharpilot/api/v0.3/case/?limit=1000'  #taking 500 as upper limit for now
    Realm = 'DJANGO'
    Username = 'nandinibhardwaj@gmail.com'
    Password = 'digitalgreen'
    URL = BASE_URL
    authhandler = urllib2.HTTPDigestAuthHandler()
    authhandler.add_password(Realm, URL, Username, Password)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    page_content = urllib2.urlopen(URL)
    data = json.loads(page_content.read())
    case_ids = {}
    person_caseid_dict = {}
    for case in data['objects']:
        case_id = case['case_id']
        if case['properties'].has_key('id'):
            person_id = case['properties']['id']
            Person_caseid_dict[Person_id] = Case_id
    fp = open('person_case','wb')
    pickle.dump({
                 'person_caseid_dict': person_caseid_dict,
                 },fp)
    fp.close()
    
def get_case_id(person_id):
    dir = os.path.dirname(__file__)
    filepath = os.path.join(dir,'person_case')
    fp = open(filepath,'rb')
    loaded = pickle.load(fp)
    fp.close()
    person_caseid_dict = loaded['person_caseid_dict']
    case_id = person_caseid_dict[person_id]
    return case_id


def get_user_data(user_id):
    BASE_URL = 'https://www.commcarehq.org/a/biharpilot/api/v0.3/case/?limit=1000'  #taking 500 as upper limit for now
    Realm = 'DJANGO'
    Username = 'nandinibhardwaj@gmail.com'
    Password = 'digitalgreen'
    URL = BASE_URL + '&user_id=' + user_id
    
    authhandler = urllib2.HTTPDigestAuthHandler()
    authhandler.add_password(Realm, URL, Username, Password)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    page_content = urllib2.urlopen(URL)
    data = json.loads(page_content.read())
    case_ids = []
    return data['objects']

def get_case_user_list(user_ids):
    for user_id in user_ids:
        case_user_dict = {}
        data = get_user_data(user_id)
        for case in data:
            case_id = case['case_id']
            user_id = case['user_id']
            case_user_dict[case_id] = user_id
    dir = os.path.dirname(__file__)
    filepath = os.path.join(dir,'case_user')
    fp = open(filepath,'wb')
    pickle.dump({
                 'case_user_dict': case_user_dict,
                 },fp)
    fp.close()
    

def check_person_id(data, person_id):
    exists = False
    for case in data:
        if case['properties'].has_key('id'):
            if case['properties']['id'] == person_id and case['closed']==False:
                exists = True
                return exists
    return exists

def close_case(case_id, filename):
    dir = os.path.dirname(__file__)
    filepath = os.path.join(dir,'case_user')
    fp = open(filepath,'rb')
    loaded = pickle.load(fp)
    fp.close()
    case_user_dict = loaded['case_user_dict']
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

