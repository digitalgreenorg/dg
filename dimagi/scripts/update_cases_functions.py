import uuid
import codecs
from django.db.models import get_model
from django.core.exceptions import ValidationError
import json
import requests
from requests.auth import HTTPDigestAuth

from dg.settings import DIMAGI_USERNAME, DIMAGI_PASSWORD
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


def update_case(cases, filename, project_name):
    file = codecs.open(filename, "w",'utf-8')
    PersonMeetingAttendance = get_model('activities','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('activities','PersonAdoptPractice')
    Person = get_model('people','Person')
    count = 0
    content_array = []
    for case in cases:
        case_id = case.guid
        owner_id = case.user.guid

        url = "".join(["https://www.commcarehq.org/a/", project_name, "/api/v0.5/case/", case_id, "/?type=json"])
        person = Person.objects.get(id=case.person_id)
        vids = PersonMeetingAttendance.objects.filter(person=person).values_list('screening__videoes_screened', flat = True).distinct()

        videos_seen = " ".join([unicode(v) for v in vids])

        # Getting list of videos adopted
        adopts = PersonAdoptPractice.objects.filter(person=person).values_list('video', flat = True).distinct()
        videos_adopted = " ".join([unicode(a) for a in adopts])

        #check for changes in the cases in dimagi

        r = requests.get(url, auth=HTTPDigestAuth(DIMAGI_USERNAME, DIMAGI_PASSWORD))
        data = json.loads(r.content)
        video_seen_in_case = sorted(data['properties']['videos_seen'].split())
        video_seen_in_db = sorted(videos_seen.split())
        print cmp(video_seen_in_case, video_seen_in_db)
        video_adopt_in_case = sorted(data['properties']['videos_adopted'].split())
        video_adopt_in_db = sorted(videos_adopted.split())
        print cmp(video_adopt_in_case, video_adopt_in_db)

        # Write xml for a particular person
        if (cmp(video_seen_in_case, video_seen_in_db) != 0 or cmp(video_adopt_in_case, video_adopt_in_db) != 0):
            write_person_update_content(content_array, count, case_id, owner_id, person, videos_seen, videos_adopted)
            count += 1
    write_opening_meta(file, count)
    for content in content_array:
        file.write(content)
    write_closing_meta(file, owner_id, count)
    file.close()


def write_new_cases(case_new_list, filename, commcare_project): #this creates new cases both in our and commcare database
    file = codecs.open(filename, "w",'utf-8')
    write_opening_meta(file, len(case_new_list))
    PersonMeetingAttendance = get_model('activities','PersonMeetingAttendance')
    PersonAdoptPractice = get_model('activities','PersonAdoptPractice')
    CommCareCase = get_model('dimagi','CommCareCase')
    for i, case in enumerate(case_new_list):
        person = case['person']
        owner_id = case['user'].guid
        case_id = uuid.uuid4()
        #Creating/populating CommCareCase table in DB
        try:
            commcarecase = CommCareCase(is_open = True,
                                    person = person,
                                    project = commcare_project,
                                    user = case['user'],
                                    guid = case_id
                                    )
            if commcarecase.full_clean() == None:
                commcarecase.save()
        except ValidationError ,e:
            print 'in write new case'+str(e)
            pass #what should be here????

        vids = PersonMeetingAttendance.objects.filter(person=person).values_list('screening__videoes_screened', flat=True).distinct()
        videos_seen = " ".join([unicode(v) for v in vids])

        # Getting list of videos adopted
        adopts = PersonAdoptPractice.objects.filter(person=person).values_list('video', flat = True).distinct()
        videos_adopted = " ".join([unicode(a) for a in adopts])
        print 'videos_adopted '+str(videos_adopted)
        # Write xml for a particular person
        write_person_content(file, i, case_id, owner_id, person, videos_seen, videos_adopted)

    write_closing_meta(file, owner_id, i + 1)
    file.close()
