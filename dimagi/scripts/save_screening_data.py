from django.core.management import setup_environ
import settings
setup_environ(settings)
from xml.dom import minidom
import time
from datetime import datetime,timedelta
from dashboard.models import *

xml_tree = minidom.parse('C:\Users\dg_systems\Documents\GitHub\dg\dimagi\submitted\sample1.xml')
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
            print person.getElementsByTagName('question_asked')
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


#print screening_data['start_time'],screening_data['end_time']


# save screening record
screening = Screening ( date = screening_data['date'],
                        start_time = screening_data['start_time'],
                        end_time = screening_data['end_time'],
                        location = 'Mobile',
                        village_id = screening_data['selected_village'],
                        animator_id = screening_data['selected_mediator'] )
screening.save()
print "Screening entry made"

# save targeted farmer groups
screening.farmer_groups_targeted = [screening_data['selected_group']]
screening.save()

# save person meeting attendance records 
for person in pma_record:
    pma = PersonMeetingAttendance ( screening_id = screening.id, 
                                    person_id = person['person_id'],
                                    interested = person['interested'],
                                    expressed_question = person['question'] )
    pma.save()
print str(len(pma_record)) + " pma entries made"