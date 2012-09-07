from django.core.management import setup_environ
import settings
setup_environ(settings)
from xml.dom import minidom
import time
from datetime import datetime,timedelta
from dashboard.models import Screening, PersonMeetingAttendance, PersonAdoptPractice
from dimagi.models import XMLSubmission

def save_screening_data(xml_tree):
    status = {}
    xml_data=xml_tree.getElementsByTagName('data')
    for record in xml_data:
        screening_data = {}
        screening_data['date'] = record.getElementsByTagName('date')[0].firstChild.data
        screening_data['time'] = record.getElementsByTagName('time')[0].firstChild.data
        screening_data['selected_village'] = record.getElementsByTagName('selected_village')[0].firstChild.data
        screening_data['selected_group'] = record.getElementsByTagName('selected_group')[0].firstChild.data
        screening_data['selected_mediator'] = record.getElementsByTagName('selected_mediator')[0].firstChild.data
        screening_data['num_people'] = record.getElementsByTagName('num_people')[0].firstChild.data
        screening_data['attendance_record'] = record.getElementsByTagName('attendance_record')
        
        pma_record = []
        for person in screening_data['attendance_record']:
            if int(person.getElementsByTagName('attended')[0].firstChild.data) == 1:
                pma = {}
                pma['person_id'] = person.getElementsByTagName('attendee_id')[0].firstChild.data
                pma['interested'] = person.getElementsByTagName('interested')[0].firstChild.data
                if person.getElementsByTagName('question_asked')[0].firstChild:
                    pma['question'] = person.getElementsByTagName('question_asked')[0].firstChild.data
                else:
                    pma['question'] = ""
                pma_record.append(pma)
                
    # time is returned as string, doing funky things to retrieve it in time format  
    temp_time = screening_data['time'].split('.')
    temp_time = time.strptime(temp_time[0], "%H:%M:%S")
    temp_time = datetime(*temp_time[:6])
    screening_data['start_time'] = temp_time.time()
    screening_data['end_time'] = temp_time + timedelta(minutes = 45)
    screening_data['end_time'] = screening_data['end_time'].time() 
    
    # save screening record
    try:
        screening = Screening ( date = screening_data['date'],
                                start_time = screening_data['start_time'],
                                end_time = screening_data['end_time'],
                                location = 'Mobile',
                                village_id = screening_data['selected_village'],
                                animator_id = screening_data['selected_mediator'] )
    
        screening.save()
        status['screening'] = screening.id
    except Exception as Ex:
        status['screening'] = -1

    # save targeted farmer groups
    screening.farmer_groups_targeted = [screening_data['selected_group']]
    screening.save()
    
    # save person meeting attendance records 
    status['pma'] = 0
    try :
        for person in pma_record:
            pma = PersonMeetingAttendance ( screening_id = screening.id, 
                                            person_id = person['person_id'],
                                            interested = person['interested'],
                                            expressed_question = person['question'] )
            pma.save()
            status['pma'] += 1
    except Exception as Ex:
        status['pma'] = -1
    
    return status


def save_adoption_data(xml_tree):
    xml_data=xml_tree.getElementsByTagName('data')
    for record in xml_data:
        screening_data = {}
        screening_data['date'] = record.getElementsByTagName('date')[0].firstChild.data
        screening_data['selected_village'] = record.getElementsByTagName('selected_village')[0].firstChild.data
        screening_data['selected_group'] = record.getElementsByTagName('selected_group')[0].firstChild.data
        screening_data['selected_mediator'] = record.getElementsByTagName('selected_mediator')[0].firstChild.data
        screening_data['selected_person'] = record.getElementsByTagName('selected_person')[0].firstChild.data
        screening_data['selected_video'] = record.getElementsByTagName('selected_video')[0].firstChild.data
    
    
    # saving the person_adopt_practice record    
    pap = PersonAdoptPractice( person_id = screening_data['selected_person'],
                                 date_of_adoption = screening_data['date'],
                                 video_id = screening_data['selected_video'])
    try:
        pap.save()
        status = pap.id
    except Exception as exception:
        status = -1                             # -1 correspoding to error
        
    return status

if __name__ == "__main__":
    xml_string = XMLSubmission.objects.all()[0].xml_data
    xml_parse = minidom.parseString(xml_string)
    data = xml_parse.getElementsByTagName('data')
    if data[0].attributes["name"].value.lower() == 'screening' :
        status = save_screening_data(xml_parse)
    elif data[0].attributes["name"].value.lower() == 'adoption' :
        status = save_adoption_data(xml_parse)
    else :
        status = -1
