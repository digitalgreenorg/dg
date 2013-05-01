import settings
from django.core.management import setup_environ
setup_environ(settings)
import csv,datetime, json, urllib2, uuid, base64
from userfile_functions import upload_file, write_person_detail
from django.db.models import get_model

def get_case_id(person_id):
    return 'c80ac8cb-58d9-4533-a928-e5e7cc9607a3' # dummy case id

def get_user_data(user_id):
    BASE_URL = 'https://www.commcarehq.org/a/dgappilot/api/v0.3/case/?limit=500'  #taking 500 as upper limit for now
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

def check_person_id(data, person_id):
    exists = False
    for case in data:
        if case['properties'].has_key('id'):
            if case['properties']['id'] == person_id and case['closed']==False:
                exists = True
                return exists
    return exists

def close_case(case_id, filename):
    owner_id = '2523fc995ccfd1d27c15111ec8987be6'
    # Putting all the info in xml tags
    f = open(filename,'w')
    f.write('<?xml version="1.0" ?>\n')
    f.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    f.write('<num_people>1</num_people>\n')
    f.write('<people>\n')
    i = 0
    f.write('<n'+str(i)+':case case_id="'+str(case_id)+ '" date_modified="'+ str(datetime.datetime.now().date()) + '" user_id="2523fc995ccfd1d27c15111ec8987be6" xmlns:n'+str(i)+'="http://commcarehq.org/case/transaction/v2">\n')
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
    f.write('<n'+str(i) + ':userID>2523fc995ccfd1d27c15111ec8987be6</n' + str(i) + ':userID>\n')
    f.write('<n'+str(i) + ':instanceID>2729386f-7fd2-42cc-807f-786bf2dc952b</n' + str(i) + ':instanceID>\n')
    f.write('</n' + str(i) + ':meta>\n')
    f.write('</data>')
    f.close()
    return f

def get_person_id_from_pma(instance):
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    person_id = PersonMeetingAttendance.objects.get(id = instance.model_id).person.id
    return person_id
    
def update_case(sender, **kwargs):
    instance = kwargs["instance"]
    action  = instance.action
    print instance.entry_table
    if instance.entry_table == 'Person' or instance.entry_table == 'PersonMeetingAttendance':
        if instance.entry_table == 'Person':
            person_id = instance.model_id
        elif instance.entry_table == 'PersonMeetingAttendance': 
            person_id = get_person_id_from_pma(instance)
        case_id = get_case_id(person_id)
        filename = 'person' + str(person_id) + '.xml'
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

def update_case_person_dict(user_id):
    case_person_dict = {}
    data = get_user_data(user_id)
    for case in data:
        if case['properties'].has_key('id'):
            person_id = case['properties']['id']
            case_person_dict[person_id] = case['case_id']
    write_dict(case_person_dict, 'user.csv')
    return case_person_dict
    
if __name__ == '__main__':
    user_id = 'krishna'
    person_id = 5000001002
#    data = get_user_data(user_id)
#    already_exists = check_person_id(data, person_id)
#    if not already_exists:
#        write_person_detail(person_id,'person.xml' )
#        response = upload_file('person.xml')
#        print response
#    close_case('cbb7d038-4905-4776-a798-e0c9f1ddcf98','close.xml')
    dict = update_case_person_dict(user_id)
    print dict
    print len(dict)
    dd = read_dict('user.csv')
    print dd