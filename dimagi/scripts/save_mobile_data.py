from datetime import datetime, timedelta
import time

from django.core.exceptions import ValidationError

from activities.models import PersonAdoptPractice, PersonMeetingAttendance, Screening
from people.models import PersonGroup
from dimagi.models import CommCareUser, error_list
from dimagi.scripts.exception_email import sendmail


def save_screening_data(xml_tree):
    status = {}
    error_msg = ''
    try:
        xml_data = xml_tree.getElementsByTagName('data')
        commcare_user = CommCareUser.objects.get(guid = str(xml_tree.getElementsByTagName('n0:userID')[0].childNodes[0].nodeValue))
        cocouser = commcare_user.coco_user
        for record in xml_data:
            try:
                screening_data = {}
                screening_data['date'] = record.getElementsByTagName('date')[0].firstChild.data
                screening_data['time'] = record.getElementsByTagName('time')[0].firstChild.data
                screening_data['selected_village'] = record.getElementsByTagName('selected_village')[0].firstChild.data
                screening_data['selected_group'] = record.getElementsByTagName('selected_group')[0].firstChild.data
                screening_data['selected_mediator'] = record.getElementsByTagName('selected_mediator')[0].firstChild.data
                screening_data['selected_video'] = record.getElementsByTagName('selected_video')[0].firstChild.data
                if  screening_data['selected_video'] == '0' :
                    screening_data['selected_video'] = record.getElementsByTagName('additional_selected_video')[0].firstChild.data
                screening_data['attendance_record'] = record.getElementsByTagName('attendance_record')
                pma_record = []
                for person in screening_data['attendance_record']:
                    if int(person.getElementsByTagName('attended')[0].firstChild.data) == 1:
                        pma = {}
                        pma['person_id'] = person.getElementsByTagName('attendee_id')[0].firstChild.data
                        if person.getElementsByTagName('interested')[0].firstChild:
                            pma['interested'] = person.getElementsByTagName('interested')[0].firstChild.data
                        else:
                            pma['interested'] = 0
                        
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
    
                try:
                    ScreeningObject = Screening.objects.get(animator_id=screening_data['selected_mediator'], date=screening_data['date'], start_time=screening_data['start_time'], end_time=screening_data['end_time'], village_id=screening_data['selected_village'])
                    status['screening'] = 1
                    # add only if group doesn't exist
                    for group in screening_data['selected_group'].split(" "):
                        GroupExisting = Screening.objects.filter(farmer_groups_targeted=group, id=ScreeningObject.id)
                        if not(len(GroupExisting)):                                
                            GroupObject = PersonGroup.objects.get(id=group)                     
                            ScreeningObject.farmer_groups_targeted.add(GroupObject)
                            ScreeningObject.save()
                            status['screening'] = 1
                            error_msg = 'Successful'
                        else:
                            status['screening'] = error_list['DUPLICATE_SCREENING']
                            error_msg = 'Duplicate Screening'
                    
                    status['pma'] = save_pma(pma_record, ScreeningObject.id, status['screening'])
                    if status['pma'] == -6:
                        status['screening'] = error_list['PMA_SAVE_ERROR']
                        error_msg = 'pma_save_error'
                
                except Screening.DoesNotExist as e:            
                    screening = Screening ( date = screening_data['date'],
                                            start_time = screening_data['start_time'],
                                            end_time = screening_data['end_time'],
                                            location = 'Mobile',
                                            village_id = screening_data['selected_village'],
                                            animator_id = screening_data['selected_mediator'],
                                            partner = cocouser.partner,
                                            user_created = cocouser.user )                    
                    try:
                        screening.full_clean()
                        screening.save()
                        status['screening'] = 1
                        try:
                            screening.farmer_groups_targeted = screening_data['selected_group'].split(" ") 
                            screening.videoes_screened = screening_data['selected_video'].split(" ")
                            screening.save()
                        except Exception as e:
                            error = "Error in Saving Groups and Videos : " + str(e)
                            status['screening'] = error_list['SCREENING_SAVE_ERROR'] 
                            error_msg = 'screening_save_error'
                            sendmail("Exception in Mobile COCO. Error in saving groups and videos (Line 91)", error)
    
                        status['pma'] = save_pma(pma_record, screening.id, status['screening'])
                        if status['pma'] == -6:
                            status['screening'] = error_list['PMA_SAVE_ERROR']
                            error_msg = 'pma_save_error'
                                                    
                    except ValidationError as err:
                        status['screening'] = error_list['SCREENING_SAVE_ERROR'] 
                        error_msg = 'screening_save_error'
                        error = "Error in Saving Screening : " + str(err)
                        sendmail("Exception in Mobile COCO. Screening save error (Line 87)", error)
    
            except Exception as ex:
                status['screening'] = error_list['SCREENING_READ_ERROR']
                error_msg = 'screening_read_error'
                error = "Error in Reading Screening : " + str(ex)
                sendmail("Exception in Mobile COCO. Screening read error (Line 22)", error)
                
    except Exception as e:
        status['screening'] = error_list['USER_NOT_FOUND']
        error_msg = 'user_read_error'
        error = "Error in Reading User : " + str(e)
        sendmail("Exception in Mobile COCO. User not found (Line 17)", error)
            
    return status['screening'],error_msg

def save_pma(pma_record, Sid, status):
    for person in pma_record:
        try:
            PersonExisting = PersonMeetingAttendance.objects.filter(screening_id=Sid, person_id=person['person_id'])
            if not(len(PersonExisting)):              
                pma = PersonMeetingAttendance ( screening_id = Sid, 
                                                person_id = person['person_id'],
                                                interested = person['interested'],
                                                expressed_question = person['question'] )
                pma.full_clean()
                pma.save()
                status = 1
        except ValidationError, e:
            status = error_list['PMA_SAVE_ERROR'] 
            error = "Error in Saving PMA : " + str(e)
            sendmail("Exception in Mobile COCO. Error in Saving PMA {Line 134)", error)
    return status

def save_adoption_data(xml_tree):
    error_msg = ''
    try:
        xml_data = xml_tree.getElementsByTagName('data')
        commcare_user = CommCareUser.objects.get(guid = str(xml_tree.getElementsByTagName('n0:userID')[0].childNodes[0].nodeValue))
        cocouser = commcare_user.coco_user
        for record in xml_data:
            try:
                adoption_data = {}
                adoption_data['date'] = record.getElementsByTagName('selected_date')[0].firstChild.data
                adoption_data['selected_person'] = record.getElementsByTagName('selected_person')[0].firstChild.data
                adoption_data['selected_video'] = record.getElementsByTagName('selected_video')[0].firstChild.data
                
                try:
                    AdoptionExisting = PersonAdoptPractice.objects.filter(person_id = adoption_data['selected_person'], video_id = adoption_data['selected_video'], date_of_adoption =  adoption_data['date'])
                    status = error_list['DUPLICATE_ADOPTION']
                    error_msg = 'Duplicate Adoption'
                    if not(len(AdoptionExisting)):
                        pap = PersonAdoptPractice(person_id = adoption_data['selected_person'],
                                                  date_of_adoption = adoption_data['date'],
                                                  video_id = adoption_data['selected_video'],
                                                  partner = cocouser.partner,
                                                  user_created = cocouser.user
                                                  )
            
                        pap.full_clean()
                        pap.save()
                        status = 1
                        error_msg = 'Successful'
                                                
                except ValidationError ,e:
                    status = error_list['ADOPTION_SAVE_ERROR']
                    error_msg = 'adoption_save_error'
                    error = "Error in Saving Adoption : " + str(e)
                    sendmail("Exception in Mobile COCO. Adoption save error (Line 168)", error)
                
            except Exception as ex:
                status = error_list['ADOPTION_READ_ERROR']
                error_msg = 'adoption_read_error'
                error = "Error in Reading Adoption : " + str(ex) 
                sendmail("Exception in Mobile COCO. Adoption read error (Line 152)", error) 

    except Exception as e:
        status = error_list['USER_NOT_FOUND']
        error_msg = 'user_read_error'
        error = "Error in Reading User : " + str(e)
        sendmail("Exception in Mobile COCO. User read error (Line 147)", error)
         
    return status, error_msg
