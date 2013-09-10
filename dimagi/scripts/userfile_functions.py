import os
import dg.settings
from django.core.management import setup_environ
setup_environ(dg.settings)
import csv,datetime, json, urllib2, uuid
from django.db.models import get_model
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import codecs

def write_opening_meta(file, num_people):
    file.write('<?xml version="1.0" ?>\n')
    file.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    file.write('<num_people> %s </num_people>\n' % (unicode(num_people)))
    
def write_person_content(file, i, case_id, owner_id, person, videos_seen):
    file.write('<people>\n')
    file.write('<n'+unicode(i)+':case case_id="' + unicode(case_id)+ '" date_modified="'+ unicode(datetime.datetime.now().date()) + '" user_id="' + owner_id + '" xmlns:n'+unicode(i)+'="http://commcarehq.org/case/transaction/v2">\n')
    file.write('<n'+unicode(i)+':create>\n')
    file.write('<n'+unicode(i)+':case_type>person</n'+unicode(i)+':case_type>\n')
    file.write('<n'+unicode(i)+':owner_id>'  + owner_id + '</n'+unicode(i)+':owner_id>\n')
    file.write('<n'+unicode(i)+':case_name>' + unicode(person.person_name) + '</n'+unicode(i)+':case_name>\n')
    file.write('</n'+unicode(i)+':create>\n')
    file.write('<n'+unicode(i)+':update>\n')
    file.write('<n'+unicode(i)+':id>' + unicode(person.id) + '</n'+unicode(i)+':id>\n')
    file.write('<n'+unicode(i)+':group_id>' + unicode(person.group.id)+ '</n'+unicode(i)+':group_id>\n')
    file.write('<n'+unicode(i)+':videos_seen>' + videos_seen + '</n'+unicode(i)+':videos_seen>\n')
    file.write('<n'+unicode(i)+':videos_adopted>' + '' + '</n'+unicode(i)+':videos_adopted>\n')
    file.write('</n'+unicode(i)+':update>\n')
    file.write('</n'+unicode(i)+':case>\n')
    file.write('</people>\n')
    
def write_closing_meta(file, owner_id, i):
    file.write('<n'+unicode(i) + ':meta xmlns:n' + unicode(i) + '="http://openrosa.org/jr/xforms">\n')
    file.write('<n'+unicode(i) + ':userID>'+unicode(owner_id) + '</n' + unicode(i) + ':userID>\n')
    file.write('<n'+unicode(i) + ':instanceID>' + unicode(uuid.uuid4()) + '</n' + unicode(i) + ':instanceID>\n')
    file.write('</n' + unicode(i) + ':meta>\n')
    file.write('</data>')
   
   
def write_person_detail(person_id, filename): #used for updating case..
    
    Person = get_model('dashboard','Person')
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    person = Person.objects.get(id = person_id)
    
    owner_id = case_user_dict[person_id]
    case_id = case_person_dict[person_id]
    
    # Getting list of videos seen
    vids = PersonMeetingAttendance.objects.filter(person = person).values_list('screening__videoes_screened', flat = True)
    videos_seen = ''
    for vid in vids:
        videos_seen = videos_seen + unicode(vid) + ' '
    # Getting list of videos adopted
    adopts = PersonAdoptPractice.objects.filter(person = person).values_list('video', flat = True)
    videos_adopted = ''
    for vid in adopts:
        videos_adopted = videos_adopted + unicode(vid) + ' '
    # Write xml for a particular person
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, 1)
    i = 0
    write_person_content(file, i, case_id, owner_id, person, videos_seen)
    i+= 1
    write_closing_meta(file, owner_id, i)    
    file.close()

def write_full_case_list(person_list, filename, user_id, case_user_dict, case_person_dict): #for generating cases
    file = codecs.open(filename, "w",'utf-8')
    Person = get_model('dashboard','Person')
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    write_opening_meta(file, len(person_list))
    i = 0
    for person_id in person_list:
        owner_id = user_id
        person = Person.objects.get(id = person_id)
        case_id = uuid.uuid4()
        case_user_dict[person.id] = user_id
        case_person_dict[person.id] = unicode(case_id)
        # Getting list of videos seen
        vids = PersonMeetingAttendance.objects.filter(person = person).values_list('screening__videoes_screened', flat = True)
        videos_seen = ''
        for vid in vids:
            videos_seen = videos_seen + unicode(vid) + ' '
        # Getting list of videos adopted
        adopts = PersonAdoptPractice.objects.filter(person = person).values_list('video', flat = True)
        videos_adopted = ''
        for vid in adopts:
            videos_adopted = videos_adopted + unicode(vid) + ' '
        # Putting all the info in xml tags
        write_person_content(file, i, case_id, owner_id, person, videos_seen)
        i += 1
    
    write_closing_meta(file, owner_id, i)    
    file.close()

def make_upload_file(villages, filename, user_id, case_user_dict, case_person_dict):
    Person = get_model('dashboard','Person')
    person_ids = Person.objects.filter(village__in = villages).values_list('id',flat=True)    
    file = write_full_case_list(person_ids, filename, user_id, case_user_dict, case_person_dict)
    #response = upload_file(filename)
    #   print response
    
#TODO: Can we change all calls to upload file?
def upload_file(file, commcare_project):
    register_openers()
    print 'uploading ' + file + 'to the' + project_name
    datagen, headers = multipart_encode({"xml_submission_file": open(file, "r")})
    request = urllib2.Request(commcare_project.receiver_url , datagen, headers)
    response = urllib2.urlopen(request)
    return response.getcode()
