import uuid
import codecs
from django.db.models import get_model
from write_xml_content import write_close_person_content, write_closing_meta, write_opening_meta, write_person_content 
   
def close_case(persons, filename):
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, len(persons))
    i = 0
    CommCareCase = get_model('dimagi', 'CommCareCase')
    for person in persons:
        case_id = CommCareCase.objects.get(person=person).guid
        owner_id = CommCareCase.objects.get(person=person).user.guid
        write_close_person_content(file, i, case_id, owner_id)
        i+= 1
    write_closing_meta(file, owner_id, i)
    file.close()                

def update_case(persons, filename): #this will just update cases that are already on our and commcare database  
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, len(persons))
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    i = 0
    CommCareCase = get_model('dimagi', 'CommCareCase')
    Person = get_model('dashboard','Person')
    for person in persons:
        case_id = CommCareCase.objects.get(person=person).guid
        owner_id = CommCareCase.objects.get(person=person).user.guid
        person = Person.objects.get(id = person)
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
        write_person_content(file, i, case_id, owner_id, person, videos_seen, videos_adopted)
        i+= 1
    write_closing_meta(file, owner_id, i)    
    file.close()                

def write_new_case(persons, filename): #this creates new cases both in our and commcare database
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, len(persons))
    CommCareUserVillage=get_model('dimagi','CommCareUserVillage')
    CommCareUser = get_model('dimagi','CommCareUser')
    CommCareCase = get_model('dimagi','CommCareCase')
    i = 0
    for person in persons:
        person = Person.objects.get(id = person_id) 
        owner_id = CommCareUserVillage.objects.get(village=person.village_id).user.id
        project_id = CommCareUser.objects.get(id=owner_id).project_id
        case_id = uuid.uuid4()
        #Creating/populating CommCareCase table in DB
        try:
            commcarecase = CommCareCase(is_open = True,
                                    person_id = person_id,
                                    project_id = project_id,
                                    user_id = owner_id,
                                    guid = case_id
                                    )
            if commcarecase.full_clean() == None:
                commcarecase.save()
        except ValidationError ,e:
            pass #what should be here????
        
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
        
        write_person_content(file, i, case_id, owner_id, person, videos_seen, videos_adopted)
        i+= 1
    write_closing_meta(file, owner_id, i)    
    file.close()
    