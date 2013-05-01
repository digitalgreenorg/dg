import settings
from django.core.management import setup_environ
setup_environ(settings)
import csv,datetime, json, urllib2, uuid
from django.db.models import get_model
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def write_userfile(file, data):
    f = open(file,'w')
    f.write(data)
        
def read_userfile(file):
    json_data=open(file).read()
    data = json.loads(json_data)
    return data

def rm_bom(filename):
    print filename
    out = r'C:\Users\Yash\Documents\GitHub\dg\dimagi\scripts\try2.xml'
    with open(filename, 'rb') as source_file:
        with open(out, 'w+b') as dest_file:
            contents = source_file.read()
            dest_file.write(contents.decode('utf-8').encode('utf-8-sig'))
    return out

def write_person_detail(person_ids, filename, i=0, case_id=None):
    import codecs
    f = open(filename, "w")
    Person = get_model('dashboard','Person')
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    f.write('<?xml version="1.0" ?>\n')
    f.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    f.write('<num_people>' + str(len(person_ids)) + '</num_people>\n')
    for person_id in person_ids:
        person = Person.objects.get(id = person_id)
    #    f = open(filename,'w')
        case_id = uuid.uuid4()
    #    owner_id = 'f097d1d213ad3a08fee6643133465660'
        # Getting list of videos seen
        vids = PersonMeetingAttendance.objects.filter(person = person).values_list('screening__videoes_screened', flat = True)
        videos_seen = ''
        for vid in vids:
            videos_seen = videos_seen + str(vid) + ' '
        # Getting list of videos adopted
        adopts = PersonAdoptPractice.objects.filter(person = person).values_list('video', flat = True)
        videos_adopted = ''
        for vid in adopts:
            videos_adopted = videos_adopted + str(vid) + ' '
        # Putting all the info in xml tags
        f.write('<people>\n')
        f.write('<n'+str(i)+':case case_id="'+str(case_id)+ '" date_modified="'+ str(datetime.datetime.now().date()) + '" user_id="2523fc995ccfd1d27c15111ec8987be6" xmlns:n'+str(i)+'="http://commcarehq.org/case/transaction/v2">\n')
        f.write('<n'+str(i)+':create>\n')
        f.write('<n'+str(i)+':case_type>person</n'+str(i)+':case_type>\n')
        f.write('<n'+str(i)+':owner_id>' + '2523fc995ccfd1d27c15111ec8987be6' + '</n'+str(i)+':owner_id>\n')
        f.write('<n'+str(i)+':case_name>' + unicode(person.person_name) + '</n'+str(i)+':case_name>\n')
        f.write('</n'+str(i)+':create>\n')
        f.write('<n'+str(i)+':update>\n')
        f.write('<n'+str(i)+':id>' + str(person.id) + '</n'+str(i)+':id>\n')
        f.write('<n'+str(i)+':group_id>' + str(person.group.id)+ '</n'+str(i)+':group_id>\n')
        f.write('<n'+str(i)+':videos_seen>' + videos_seen + '</n'+str(i)+':videos_seen>\n')
        f.write('<n'+str(i)+':videos_adopted>' + '' + '</n'+str(i)+':videos_adopted>\n')
        f.write('</n'+str(i)+':update>\n')
        f.write('</n'+str(i)+':case>\n')
        f.write('</people>\n')
        # Writing closing meta info of the form
        i += 1
        
    f.write('<n'+str(i) + ':meta xmlns:n' + str(i) + '="http://openrosa.org/jr/xforms">\n')
    f.write('<n'+str(i) + ':userID>2523fc995ccfd1d27c15111ec8987be6</n' + str(i) + ':userID>\n')
    f.write('<n'+str(i) + ':instanceID>2729386f-7fd2-42cc-807f-786bf2dc952b</n' + str(i) + ':instanceID>\n')
    f.write('</n' + str(i) + ':meta>\n')
    f.write('</data>')
    f.close()
#    f = rm_bom(filename)
    return f

def make_upload_file(villages, filename):
    Person = get_model('dashboard','Person')
    person_ids = Person.objects.filter(village__in = villages).values_list('id',flat=True)
    f = write_person_detail(person_ids, filename)
#    response = upload_file(filename)
#    print response
    
        
def upload_file(file):
    register_openers()
#    print 'uploading ' + file
    datagen, headers = multipart_encode({"xml_submission_file": open(file, "r")})
    request = urllib2.Request("https://www.commcarehq.org/a/dgappilot/receiver", datagen, headers)
    response = urllib2.urlopen(request).read()
    return response
    

if __name__ == '__main__':
    file = 'userfileappilot.json'
#    user_villages = []
#    json_data = json.dumps([{'user_id': '53d48b7a60a11661405244b98581d3ea',
#                          'username': 'krishna',
#                          'villages' : [10000000020940,10000000020936,10000000020938,10000000021295]},
##                            {'user_id': 'f097d1d213ad3a08fee6643133465660',
##                          'username': 'y2',
##                          'villages' : [10000000020974,10000000020975,10000000021293,
##                                        10000000020958,10000000020960,10000000020956]}
#                            ])
#    data = json.loads(json_data)
#    write_userfile(file,json_data)
    data = read_userfile(file)
    print data
    villages = data[0]['villages']
    make_upload_file(villages, r'C:\Users\Yash\Documents\GitHub\dg\dimagi\scripts\try.xml')
