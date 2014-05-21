import json

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render_to_response

from dg.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from path.models import *
from people.models import Person
import gdata.spreadsheet.service

def page(request):
    return render_to_response("path/pathpage.html")

def update(request):
    if not PathLog.objects.all():
        first_elem = PathLog( person_offline_id = MIN_OFFLINE_PRB, 
                              person_online_id = MIN_ONLINE)
        try:
            first_elem.save()
        except Exception as ex:
            return graceful_exit("Technical error: could not save initial values.")
    
    try:
        last_log = PathLog.objects.get(read = False);
    except MultipleObjectsReturned:
        return graceful_exit("Database in inconsistent state.")
    except ObjectDoesNotExist:
        return graceful_exit("Error in previous iteration.")
    
    last_log.read = True
    last_log.save()
    current_ids = {
                   'offline' : last_log.person_offline_id, 
                   'online' : last_log.person_online_id,
                   }
    
    person = Person.objects.filter(village__block__district__id=DISTRICT_ID)
    persons_online = person.filter(id__gt=current_ids['online']).values_list('village__block__district__district_name',
                                                                         'village__block__block_name',
                                                                         'village__village_name',
                                                                         'group__group_name',
                                                                         'person_name',
                                                                         'father_name',
                                                                         'age',
                                                                         'gender',
                                                                         'id')
    
    persons_offline = person.filter(id__gt=current_ids['offline'], id__lt =  MAX_OFFLINE_PRB).values_list('village__block__district__district_name',
                                                                      'village__block__block_name',
                                                                      'village__village_name',
                                                                      'group__group_name',
                                                                      'person_name',
                                                                      'father_name',
                                                                      'age',
                                                                      'gender',
                                                                      'id')
    list_person = []
    for p in persons_online:
        list_p = list(p)
        for i in range(len(list_p)-1):
            if not list_p[i]:
                list_p[i]= " "
            else:
                list_p[i] = unicode(list_p[i])
        list_person.append({'id':p[8],'dic':{'district':list_p[0],'block':list_p[1],'village':list_p[2],'group':list_p[3],'personname':list_p[4],'fathernameorspousename':list_p[5],'age':list_p[6],'gender':list_p[7]}})
        
         
    for p in persons_offline:
        list_p=list(p)
        for i in range(len(p)-1):
            if not list_p[i]:
                list_p[i]= " "
            else:
                list_p[i] = unicode(list_p[i])            
        list_person.append({'id':p[8],'dic':{'district':list_p[0],'block':list_p[1],'village':list_p[2],'group':list_p[3],'personname':list_p[4],'fathernameorspousename':list_p[5],'age':list_p[6],'gender':list_p[7]}})
    
    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.email = EMAIL_HOST_USER
    spr_client.password = EMAIL_HOST_PASSWORD
    spr_client.source = 'DG Path App'
    spr_client.ProgrammaticLogin()
    
    for elem in list_person:
        ex_flag = 0
        while(ex_flag < 3):
            try:
                entry = spr_client.InsertRow(elem['dic'], spreadsheet_key, worksheet_id)
                # Check whether insert was successful.
                if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
                    if(elem['id'] > MIN_ONLINE):
                        current_ids['online'] = elem['id']
                    else:
                        current_ids['offline'] = elem['id']
                    break
                else:
                    return graceful_exit('Instance not saved.', ids=current_ids)
            except Exception as ex:
                ex_flag = ex_flag + 1
        if(ex_flag == 3):
            return graceful_exit('Network problem. Please try later.', ids=current_ids)
    return graceful_exit('Spreadsheet updated successfully.', ids=current_ids)

def graceful_exit(message, ids=None):
    if ids is not None:
        try:
            curr_elem = PathLog(person_offline_id = ids['offline'], person_online_id = ids['online'])
            curr_elem.save()
        except Exception:
            return HttpResponse({'message': 'Technical Error: Saving in PathLog not working. Contact Sytems.'})
    if message=='':
        message = "No message"
    return HttpResponse(json.dumps({'message': message}))
