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
    
    person = Person.objects.get(id = person_id)
    owner_id = case_user_dict[person_id]
    case_id = case_person_dict[person_id]
    
    f = codecs.open(filename, "w",'utf-8')
    Person = get_model('dashboard','Person')
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    f.write('<?xml version="1.0" ?>\n')
    f.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    f.write('<num_people>' + unicode(1) + '</num_people>\n')
    i = 0
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
    f.write('<people>\n')
    f.write('<n'+unicode(i)+':case case_id="' + unicode(case_id)+ '" date_modified="'+ unicode(datetime.datetime.now().date()) + '" user_id="' + owner_id + '" xmlns:n'+unicode(i)+'="http://commcarehq.org/case/transaction/v2">\n')
    f.write('<n'+unicode(i)+':create>\n')
    f.write('<n'+unicode(i)+':case_type>person</n'+unicode(i)+':case_type>\n')
    f.write('<n'+unicode(i)+':owner_id>'  + owner_id + '</n'+unicode(i)+':owner_id>\n')
    f.write('<n'+unicode(i)+':case_name>' + unicode(person.person_name) + '</n'+unicode(i)+':case_name>\n')
    f.write('</n'+unicode(i)+':create>\n')
    f.write('<n'+unicode(i)+':update>\n')
    f.write('<n'+unicode(i)+':id>' + unicode(person.id) + '</n'+unicode(i)+':id>\n')
    f.write('<n'+unicode(i)+':group_id>' + unicode(person.group.id)+ '</n'+unicode(i)+':group_id>\n')
    f.write('<n'+unicode(i)+':videos_seen>' + videos_seen + '</n'+unicode(i)+':videos_seen>\n')
    f.write('<n'+unicode(i)+':videos_adopted>' + '' + '</n'+unicode(i)+':videos_adopted>\n')
    f.write('</n'+unicode(i)+':update>\n')
    f.write('</n'+unicode(i)+':case>\n')
    f.write('</people>\n')
    i+= 1
    # Writing closing meta info of the form        
    f.write('<n'+unicode(i) + ':meta xmlns:n' + unicode(i) + '="http://openrosa.org/jr/xforms">\n')
    f.write('<n'+unicode(i) + ':userID>2523fc995ccfd1d27c15111ec8987be6</n' + unicode(i) + ':userID>\n')
    f.write('<n'+unicode(i) + ':instanceID>2729386f-7fd2-42cc-807f-786bf2dc952b</n' + unicode(i) + ':instanceID>\n')
    f.write('</n' + unicode(i) + ':meta>\n')
    f.write('</data>')
    f.close()
    return f

def write_full_case_list(person_list, filename, user_id): #for generating cases
    f = codecs.open(filename, "w",'utf-8')
    Person = get_model('dashboard','Person')
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    f.write('<?xml version="1.0" ?>\n')
    f.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    f.write('<num_people>' + unicode(len(person_list)) + '</num_people>\n')
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
        f.write('<people>\n')
        f.write('<n'+unicode(i)+':case case_id="' + unicode(case_id)+ '" date_modified="'+ unicode(datetime.datetime.now().date()) + '" user_id="' + owner_id + '" xmlns:n'+unicode(i)+'="http://commcarehq.org/case/transaction/v2">\n')
        f.write('<n'+unicode(i)+':create>\n')
        f.write('<n'+unicode(i)+':case_type>person</n'+unicode(i)+':case_type>\n')
        f.write('<n'+unicode(i)+':owner_id>'  + owner_id + '</n'+unicode(i)+':owner_id>\n')
        f.write('<n'+unicode(i)+':case_name>' + unicode(person.person_name) + '</n'+unicode(i)+':case_name>\n')
        f.write('</n'+unicode(i)+':create>\n')
        f.write('<n'+unicode(i)+':update>\n')
        f.write('<n'+unicode(i)+':id>' + unicode(person.id) + '</n'+unicode(i)+':id>\n')
        f.write('<n'+unicode(i)+':group_id>' + unicode(person.group.id)+ '</n'+unicode(i)+':group_id>\n')
        f.write('<n'+unicode(i)+':videos_seen>' + videos_seen + '</n'+unicode(i)+':videos_seen>\n')
        f.write('<n'+unicode(i)+':videos_adopted>' + '' + '</n'+unicode(i)+':videos_adopted>\n')
        f.write('</n'+unicode(i)+':update>\n')
        f.write('</n'+unicode(i)+':case>\n')
        f.write('</people>\n')
        # Writing closing meta info of the form
        i += 1
        
    f.write('<n'+unicode(i) + ':meta xmlns:n' + unicode(i) + '="http://openrosa.org/jr/xforms">\n')
    f.write('<n'+unicode(i) + ':userID>' + owner_id  + '</n' + unicode(i) + ':userID>\n')
    f.write('<n'+unicode(i) + ':instanceID>2729386f-7fd2-42cc-807f-786bf2dc952b</n' + unicode(i) + ':instanceID>\n')
    f.write('</n' + unicode(i) + ':meta>\n')
    f.write('</data>')
    f.close()
    pickle.dump(case_user_dict, open('case_user','w')) #mapping of case with user
    pickle.dump(case_person_dict, open('case_person','w')) #mapping of case with person(farmer)
    return f

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
        

