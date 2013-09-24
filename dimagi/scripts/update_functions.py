import base64
import csv
import datetime
import json
import os
import urllib2
import uuid
import datetime
import codecs

from dg.settings import MEDIA_ROOT
from django.db.models import get_model
from userfile_functions import write_closing_meta, write_person_content, write_opening_meta 

def get_case_person_list():
    person_caseid_dict = {}
    CommCareCase = get_model('dimagi','CommCareCase')
    cases = CommCareCase.objects.all()
    for case in cases:
        person_caseid_dict[case.person.id]=case.guid
    return person_caseid_dict
    
def get_case_id(person_id):
    CommCareCase= get_model('dimagi','CommCareCase')
    return CommCareCase.objects.get(person__id=person_id).guid


def get_case_user_list():
    case_user_dict = {}
    CommCareCase= get_model('dimagi','CommCareCase')
    cases = CommCareCase.objects.all()
    for case in cases:
        case_user_dict[case.guid]=case.user.guid
    return case_user_dict

def check_person_id(person_id):
    CommCareCase= get_model('dimagi','CommCareCase')
    exists = False
    case = CommCareCase.objects.get(person__id=person_id) 
    if case.is_open==True:
        exists = True
    return exists

def close_case(person_id, filename):
    CommCareCase = get_model('dimagi', 'CommCareCase')
    case_id = CommCareCase.objects.get(person = person_id).guid
    owner_id = CommCareCase.objects.get(person = person_id).user.guid
    # Putting all the info in xml tags
    f = open(filename,'w')
    f.write('<?xml version="1.0" ?>\n')
    f.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    f.write('<num_people>1</num_people>\n')
    f.write('<people>\n')
    i = 0
    f.write('<n'+unicode(i)+':case case_id="'+unicode(case_id)+ '" date_modified="'+ unicode(datetime.datetime.now().date()) + '" user_id="' + owner_id +'" xmlns:n'+unicode(i)+'="http://commcarehq.org/case/transaction/v2">\n')
    f.write('<n'+unicode(i)+':create>\n')
    f.write('<n'+unicode(i)+':case_type>person</n'+unicode(i)+':case_type>\n')
    f.write('<n'+unicode(i)+':owner_id>' + owner_id + '</n'+unicode(i)+':owner_id>\n')
    f.write('</n'+unicode(i)+':create>\n')
    f.write('<n'+unicode(i)+':update>\n')
    f.write('</n'+unicode(i)+':update>\n')
    f.write('<n'+unicode(i)+':close>' + '1' + '</n'+unicode(i)+':close>\n')
    f.write('</n'+unicode(i)+':case>\n')
    f.write('</people>\n')
    # Writing closing meta info of the form
    i += 1
    f.write('<n'+unicode(i) + ':meta xmlns:n' + unicode(i) + '="http://openrosa.org/jr/xforms">\n')
    f.write('<n'+unicode(i) + ':userID>' + owner_id + '</n' + unicode(i) + ':userID>\n')
    f.write('<n'+unicode(i) + ':instanceID>' + unicode(uuid.uuid4()) + '</n' + unicode(i) + ':instanceID>\n')
    f.write('</n' + unicode(i) + ':meta>\n')
    f.write('</data>')
    f.close()
    

def get_person_id_from_pma(instance):
    PersonMeetingAttendance = get_model('dashboard',instance.entry_table)
    person_id = PersonMeetingAttendance.objects.get(id = instance.model_id).person.id
    return person_id
    
def update_case(persons, filename):
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, 1)
    i = 0
    CommCareCase = get_model('dimagi', 'CommCareCase')
    for person in persons:
        case_id = CommCareCase.objects.get(person=person).guid
        owner_id = CommCareCase.objects.get(person=person).user.guid
        Person = get_model('dashboard','Person')
        person = Person.objects.get(id = person)
        PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
        vids = PersonMeetingAttendance.objects.filter(person = person).values_list('screening__videoes_screened', flat = True)
        videos_seen = ''
        for vid in vids:
            videos_seen = videos_seen + unicode(vid) + ' '
        # Getting list of videos adopted
        PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
        adopts = PersonAdoptPractice.objects.filter(person = person).values_list('video', flat = True)
        videos_adopted = ''
        for vid in adopts:
            videos_adopted = videos_adopted + unicode(vid) + ' '
        # Write xml for a particular person
        write_person_content(file, i, case_id, owner_id, person, videos_seen)
        i+= 1
    write_closing_meta(file, owner_id, i)    
    file.close()                
