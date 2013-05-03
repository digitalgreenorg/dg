import site, sys
sys.path.append('/home/ubuntu/code/dg_test')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')
from django.core.management import setup_environ
import settings
setup_environ(settings)
from xml.dom import minidom
import time
from datetime import datetime,timedelta
from dashboard.models import Screening, PersonMeetingAttendance, PersonAdoptPractice
from dimagi.models import XMLSubmission
from dimagi.models import error_list
from django.core.exceptions import ValidationError


def save_screening_data(xml_tree):
    status = {}
    error_msg = ''
    xml_data = xml_tree.getElementsByTagName('data')
    for record in xml_data:
        try:
            screening_data = {}
            screening_data['date'] = record.getElementsByTagName('date')[0].firstChild.data
            screening_data['time'] = record.getElementsByTagName('time')[0].firstChild.data
            screening_data['selected_village'] = record.getElementsByTagName('selected_village')[0].firstChild.data
            screening_data['selected_group'] = record.getElementsByTagName('selected_group')[0].firstChild.data
            screening_data['selected_mediator'] = record.getElementsByTagName('selected_mediator')[0].firstChild.data
            screening_data['selected_video'] = record.getElementsByTagName('selected_video')[0].firstChild.data
            if  screening_data['selected_video'] == 0 :
                screening_data['selected_video'] = record.getElementsByTagName('additional_selected_video')[0].firstChild.data
                 
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
            error_msg = 'Successful'
        
                
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
              
                if screening.full_clean() == None: # change to full_clean() 
                    screening.save()
                    status['screening'] = 1
                    screening.farmer_groups_targeted = [screening_data['selected_group']] 
                    screening.videoes_screened = [screening_data['selected_video']]
                    screening.save()
                    status['pma'] = 1
                    try :
                        for person in pma_record:
                            pma = PersonMeetingAttendance ( screening_id = screening.id, 
                                                            person_id = person['person_id'],
                                                            interested = person['interested'],
                                                            expressed_question = person['question'] )
                            if pma.full_clean() == None:
                                pma.save()
                            else:
                                status['pma'] = error_list['PMA_SAVE_ERROR'] 
                                error_msg = 'Not valid' 
                    except ValidationError, e:
                        status['pma'] = error_list['PMA_SAVE_ERROR'] 
                        error_msg = unicode(e)
                else:
                    status['screening'] = error_list['SCREENING_SAVE_ERROR'] 
                    error_msg = 'Not valid' 
                        
            except Exception as ex:
                status['screening'] = error_list['SCREENING_SAVE_ERROR'] 
                error_msg = unicode(ex)
           
        except Exception as ex:
            status['screening'] = error_list['SCREENING_READ_ERROR'] 
            error_msg = unicode(ex)
            
    return status['screening'],error_msg


def save_adoption_data(xml_tree):
    xml_data=xml_tree.getElementsByTagName('data')
    error_msg = ''
    for record in xml_data:
        try:
            screening_data = {}
            screening_data['date'] = record.getElementsByTagName('selected_date')[0].firstChild.data
            screening_data['selected_person'] = record.getElementsByTagName('selected_person')[0].firstChild.data
            screening_data['selected_video'] = record.getElementsByTagName('selected_video')[0].firstChild.data
            
            try:
                pap = PersonAdoptPractice( person_id = screening_data['selected_person'],
                                     date_of_adoption = screening_data['date'],
                                     video_id = screening_data['selected_video'],
                                     )
            
                if pap.full_clean() == None:
                    pap.save()
                    status = 1
                    error_msg = 'Sucessful'
            except ValidationError ,e:
                status = error_list['ADOPTION_SAVE_ERROR'] 
                error_msg = unicode(e)
            
        except Exception as ex:
            status = error_list['ADOPTION_READ_ERROR'] 
            error_msg = unicode(ex)

    return status, error_msg



if __name__ == "__main__":
    xml_file = r'C:\Users\Yash\Desktop\trial.xml'
    xml_parse = minidom.parse(xml_file)
    data = xml_parse.getElementsByTagName('data')
    if data[0].attributes["name"].value.lower() == 'screening' :
        status,msg = save_screening_data(xml_parse)
    elif data[0].attributes["name"].value.lower() == 'adoption' :
        status,msg = save_adoption_data(xml_parse)
    else :
        status = -1
    print status 
    print msg