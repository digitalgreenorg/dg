from datetime import datetime, timedelta
import time

from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned

from activities.models import PersonAdoptPractice, PersonMeetingAttendance, Screening
from people.models import PersonGroup
from dimagi.models import CommCareUser, error_list
from dimagi.scripts.exception_email import sendmail


def save_screening_data(xml_tree):
    status = {}
    error_msg = ''
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
                    #print "Person Entered : "+str(pma['person_id'])
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
            # save screening record
            try:
                screening = Screening ( date = screening_data['date'],
                                        start_time = screening_data['start_time'],
                                        end_time = screening_data['end_time'],
                                        location = 'Mobile',
                                        village_id = screening_data['selected_village'],
                                        animator_id = screening_data['selected_mediator'],
                                        partner = cocouser.partner,
                                        user_created = cocouser.user )
                
                #print str(screening_data['selected_mediator']) + str(screening_data['date']) + str(screening_data['start_time']) + str(screening_data['end_time']) + str(screening_data['selected_village'])
                
                ScreeningObject = Screening.objects.get(animator_id=screening_data['selected_mediator'], date=screening_data['date'], start_time=screening_data['start_time'], end_time=screening_data['end_time'], village_id=screening_data['selected_village'])

                if ScreeningObject:
                    #Append group and save PMA
                    status['screening'] = 1
                    flag=0
                    # add only if group doesn't exist
                    for group in screening_data['selected_group'].split(" "):
                        try:
                            GroupExisting = Screening.objects.get(farmer_groups_targeted=group, id=ScreeningObject.id)
                            print "Duplicate Entry!"
                            #print GroupExisting
                        except ObjectDoesNotExist as e:
                            #print e
                            GroupObject = PersonGroup.objects.get(id=group)                     
                            ScreeningObject.farmer_groups_targeted.add(GroupObject)
                            ScreeningObject.save()
                            status['pma'] = 1
                            flag=1
                        except MultipleObjectsReturned as ex:
                            print ex   
                    
                    if flag==1:
                        try :
                            for person in pma_record:
                                #check if person in PMA already for that screening
                                try:
                                    PersonExisting = PersonMeetingAttendance.objects.get(screening_id=ScreeningObject.id, person_id=person['person_id'])
                                    print "Attendance Marked"
                                except ObjectDoesNotExist as ex:
                                    #print ex                                
                               
                                    pma = PersonMeetingAttendance ( screening_id = ScreeningObject.id, 
                                                                    person_id = person['person_id'],
                                                                    interested = person['interested'],
                                                                    expressed_question = person['question'] )
                                    
                                    if pma.full_clean() == None:
                                            pma.save()
                                            #print "PMA Record Saved"
                                    else:
                                            status['pma'] = error_list['PMA_SAVE_ERROR'] 
                                            error_msg = 'Not valid' 
                                            
                                except MultipleObjectsReturned as e:
                                    print e
                                            
                        except ValidationError, e:
                            status['pma'] = error_list['PMA_SAVE_ERROR'] 
                            error = "Error in saving Pma line 85" + str(e)
                            sendmail("Exception in Mobile COCO", error)
                        
                else:
                    print "Save Screening"
                    if screening.full_clean() == None: # change to full_clean()
                        screening.save()
                        print "Screening Saved :O"
                        
                        status['screening'] = 1
                        try:
                            screening.farmer_groups_targeted = screening_data['selected_group'].split(" ") 
                            screening.videoes_screened = screening_data['selected_video'].split(" ")
                            screening.save()

                        except Exception as e:
                            error = "Error in saving groups and videos" + str(e)
                            sendmail("Exception in Mobile COCO line 74", error)
                        status['pma'] = 1
                        
                        try :
                            for person in pma_record:
                                pma = PersonMeetingAttendance ( screening_id = screening.id, 
                                                                person_id = person['person_id'],
                                                                interested = person['interested'],
                                                                expressed_question = person['question'] )
                                
                                if pma.full_clean() == None:
                                    pma.save()
                                    #print "PMA Record Saved"
                                else:
                                    status['pma'] = error_list['PMA_SAVE_ERROR'] 
                                    error_msg = 'Not valid' 
                        except ValidationError, e:
                            status['pma'] = error_list['PMA_SAVE_ERROR'] 
                            error = "Error in saving Pma line 85" + str(e)
                            sendmail("Exception in Mobile COCO", error)
                            
                    else:
                        status['screening'] = error_list['SCREENING_SAVE_ERROR'] 
                        error_msg = 'Not valid'
                    
            except Exception as ex:
                #print str(ex)
                status['screening'] = error_list['SCREENING_SAVE_ERROR'] 
                error = "Error in saving Screening " + str(ex)
                sendmail("Exception in Mobile COCO Screening save error line 97", error)
       
        except Exception as ex:
            #print str(ex)
            status['screening'] = error_list['SCREENING_READ_ERROR'] 
            error = "Error in Reading Screening " + str(ex)
            sendmail("Exception in Mobile COCO screening read error line 103", error)
            
    return status['screening'],error_msg


def save_adoption_data(xml_tree):
    xml_data=xml_tree.getElementsByTagName('data')
    commcare_user = CommCareUser.objects.get(guid = str(xml_tree.getElementsByTagName('n0:userID')[0].childNodes[0].nodeValue))
    cocouser = commcare_user.coco_user
    error_msg = ''
    for record in xml_data:
        try:
            adoption_data = {}
            adoption_data['date'] = record.getElementsByTagName('selected_date')[0].firstChild.data
            adoption_data['selected_person'] = record.getElementsByTagName('selected_person')[0].firstChild.data
            adoption_data['selected_video'] = record.getElementsByTagName('selected_video')[0].firstChild.data
            
            try:
                pap = PersonAdoptPractice(person_id = adoption_data['selected_person'],
                                     date_of_adoption = adoption_data['date'],
                                     video_id = adoption_data['selected_video'],
                                     partner = cocouser.partner,
                                     user_created = cocouser.user
                                     )
            
                if pap.full_clean() == None:
                    pap.save()
                    status = 1
                    error_msg = 'Successful'
            except ValidationError ,e:
                status = error_list['ADOPTION_SAVE_ERROR']
                error = "Error in saving Adoption " + str(e)
                sendmail("Exception in Mobile COCO adoption save line 136", error)
            
        except Exception as ex:
            status = error_list['ADOPTION_READ_ERROR']
            error = "Error in reading Adoption " + str(ex)
            sendmail("Exception in Mobile COCO adoption read line 142", error) 

    return status, error_msg
