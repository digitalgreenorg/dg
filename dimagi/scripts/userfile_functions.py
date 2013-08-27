import dg.settings
from django.core.management import setup_environ
setup_environ(dg.settings)
import csv,datetime, json, urllib2, uuid, pickle,os
from django.db.models import get_model
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import codecs

def write_userfile(file, data):
    f = open(file,'w')
    f.write(data)
        
def read_userfile(file):
    json_data=open(file).read()
    print json_data
    data = json.loads(json_data)
    return data

def write_opening_meta(file, num_people):
    file.write('<?xml version="1.0" ?>\n')
    file.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    file.write('<num_people>' + unicode(num_people) + '</num_people>\n')
    
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
    # Retrieving the mapping from pickle files
    dir = os.path.dirname(__file__)
    filepath = os.path.join(dir,'case_user')
    fp = open(filepath,'rb')
    case_user_dict = pickle.load(fp)
    fp.close()
    filepath = os.path.join(dir,'case_person')
    fp = open(filepath,'rb')
    case_person_dict = pickle.load(fp)
    fp.close()
    
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
    write_person_content(file, 0, case_id, owner_id, person, videos_seen)
    write_closing_meta(file, owner_id, 1)    
    file.close()
    return file

def write_full_case_list(person_list, filename, user_id): #for generating cases
    file = codecs.open(filename, "w",'utf-8')
    Person = get_model('dashboard','Person')
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    write_opening_meta(file, len(person_list))
    i = 0
    case_user_dict = {}
    case_person_dict = {}
    for person_id in person_list:
        owner_id = user_id
        person = Person.objects.get(id = person_id)
        case_id = uuid.uuid4()
        case_person_dict[person.id] = case_id
        case_user_dict[person.id] = user_id
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
    pickle.dump(case_user_dict, open('case_user','w')) #mapping of case with user
    pickle.dump(case_person_dict, open('case_person','w')) #mapping of case with person(farmer)
    return file

def make_upload_file(villages, filename, user_id):
    Person = get_model('dashboard','Person')
    person_ids = Person.objects.filter(village__in = villages).values_list('id',flat=True)
    f = write_full_case_list(person_ids, filename, user_id)
#    response = upload_file(filename)
#    print response
    
        
def upload_file(file):
    register_openers()
#    print 'uploading ' + file
    datagen, headers = multipart_encode({"xml_submission_file": open(file, "r")})
    request = urllib2.Request("https://www.commcarehq.org/a/capilot/receiver", datagen, headers)
    response = urllib2.urlopen(request)
    return response.getcode()

if __name__ == '__main__':
    Person = get_model('dashboard','Person')
    data = read_userfile('apca.json')
    for row in data:
        username = row['username']
        print "creating xml for " + str(username)
        filename = username + '.xml'
        person_list = Person.objects.filter(village__in = row['villages']).values_list('id', flat=True)
        write_full_case_list(person_list,filename,row['user_id'])
        
#        upload_file(filename)
        

