import uuid
import codecs
from django.db.models import get_model
from django.core.exceptions import ValidationError
from write_xml_content import write_close_person_content, write_closing_meta, write_opening_meta, write_person_content, write_person_update_content 


def close_case(cases, filename):
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, len(cases))

    i = 0
    for i, case in enumerate(cases):
        case_id = case.guid
        owner_id = case.user.guid
        write_close_person_content(file, i, case_id, owner_id)

    write_closing_meta(file, owner_id, i + 1)
    file.close()


def update_case(cases, filename):
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, len(cases))
    PersonMeetingAttendance = get_model('activities','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('activities','PersonAdoptPractice')
    Person = get_model('people','Person')
    for i, case in enumerate(cases):
        case_id = case.guid
        owner_id = case.user.guid
        person = Person.objects.get(id=case.person_id)
        vids = PersonMeetingAttendance.objects.filter(person=person).values_list('screening__videoes_screened', flat = True)
        videos_seen = " ".join([unicode(v) for v in vids])

        # Getting list of videos adopted
        adopts = PersonAdoptPractice.objects.filter(person=person).values_list('video', flat = True)
        videos_adopted = " ".join([unicode(a) for a in adopts])

        # Write xml for a particular person
        write_person_update_content(file, i, case_id, owner_id, person, videos_seen, videos_adopted)
    write_closing_meta(file, owner_id, i + 1)
    file.close()


def write_new_case(persons, filename): #this creates new cases both in our and commcare database
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, len(persons))
    Person = get_model('people', 'Person')
    PersonMeetingAttendance = get_model('activities','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('activities','PersonAdoptPractice')
    CommCareUserVillage=get_model('dimagi','CommCareUserVillage')
    CommCareUser = get_model('dimagi','CommCareUser')
    CommCareCase = get_model('dimagi','CommCareCase')

    for i, person_id in enumerate(persons):
        person = Person.objects.get(id=person_id) 
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

        vids = PersonMeetingAttendance.objects.filter(person=person).values_list('screening__videoes_screened', flat=True)
        videos_seen = " ".join([unicode(v) for v in vids])

        # Getting list of videos adopted
        adopts = PersonAdoptPractice.objects.filter(person=person).values_list('video', flat = True)
        videos_adopted = " ".join([unicode(a) for a in adopts])

        # Write xml for a particular person
        write_person_content(file, i, case_id, owner_id, person, videos_seen, videos_adopted)

    write_closing_meta(file, owner_id, i + 1)
    file.close()
