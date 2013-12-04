import os
import dg.settings
from django.core.management import setup_environ
setup_environ(dg.settings)
import uuid
import codecs
from django.core.exceptions import ValidationError
from django.db.models import get_model
from write_xml_content import write_closing_meta, write_opening_meta, write_person_content
  
def write_full_case_list(person_list, filename, user_id, project_id): #for generating cases
    file = codecs.open(filename, "w",'utf-8')
    Person = get_model('dashboard','Person')
    PersonMeetingAttendance = get_model('dashboard','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('dashboard','PersonAdoptPractice')
    CommCareCase = get_model('dimagi','CommCareCase')
    CommCareUser = get_model('dimagi','CommCareUser')
    write_opening_meta(file, len(person_list))
    i = 0
    for person_id in person_list:
        owner_id = user_id
        person = Person.objects.get(id = person_id)
        case_id = uuid.uuid4()
        #Creating/populating CommCareCase table in DB
        try:
            commcarecase = CommCareCase(is_open = True,
                                    person_id = person_id,
                                    project_id = project_id,
                                    user_id = CommCareUser.objects.get(guid=owner_id).id,
                                    guid = case_id
                                    )
            if commcarecase.full_clean() == None:
                commcarecase.save()
        except ValidationError ,e:
            pass #what should be here????
            
        # Getting list of videos seen
        vids = PersonMeetingAttendance.objects.filter(person = person).values_list('screening__videoes_screened', flat = True).distinct('screening__videoes_screened')
        videos_seen = ''
        for vid in vids:
            videos_seen = videos_seen + unicode(vid) + ' '
        # Getting list of videos adopted
        adopts = PersonAdoptPractice.objects.filter(person = person).values_list('video', flat = True)
        videos_adopted = ''
        for vid in adopts:
            videos_adopted = videos_adopted + unicode(vid) + ' '
        # Putting all the info in xml tags
        write_person_content(file, i, case_id, owner_id, person, videos_seen, videos_adopted)
        i += 1

    write_closing_meta(file, owner_id, i)    
    file.close()

def make_upload_file(villages, filename, user_id, project_id):
    Person = get_model('dashboard','Person')
    person_ids = Person.objects.filter(village__in = villages).values_list('id',flat=True).exclude(group__isnull = True)    
    file = write_full_case_list(person_ids, filename, user_id, project_id)
    