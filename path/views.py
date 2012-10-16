import cjson
import datetime
import operator
import re
import time
import gdata.spreadsheet.service

from django.conf.urls.defaults import *
from django.contrib import auth
from django.core import serializers
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.db.models import Q,Max
from django.db.models.query import QuerySet
from django.forms.models import inlineformset_factory, modelformset_factory
from django.http import Http404, HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import *
from django.template import Context, Template
from django.template.loader import get_template
from dashboard.models import *
from path.models import *
from settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD

def page(request):
    return render_to_response("path/pathpage.html")

def update(request):
    
    if not PathLog.objects.all():
        first_elem = PathLog( person_offline_id = 68000000000, 
                              person_online_id = MIN_ONLINE)
        try:
            first_elem.save()
        except Exception as ex:
            print ex
            
    last_read_online = PathLog.objects.all().aggregate(Max('person_online_id'))['person_online_id__max']
    last_read_offline = PathLog.objects.all().aggregate(Max('person_offline_id'))['person_offline_id__max']
    #person = Person.objects.all()
    person = Person.objects.filter(village__block__district__id=10000000000041)
    persons_online = person.filter(id__gt= last_read_online).values_list('village__block__district__district_name',
                                                                         'village__block__block_name',
                                                                         'village__village_name',
                                                                         'group__group_name',
                                                                         'person_name',
                                                                         'father_name',
                                                                         'age',
                                                                         'gender',
                                                                         'id')
        
    persons_offline = person.filter(id__gt = last_read_offline, id__lt =  69000000000 ).values_list('village__block__district__district_name',
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
        list_p=list(p)
        for i in range(len(list_p)-1):
            if not list_p[i]:
                list_p[i]= " "
            else:
                list_p[i]=str(list_p[i])
        list_person.append({'id':p[8],'dic':{'district':list_p[0],'block':list_p[1],'village':list_p[2],'group':list_p[3],'personname':list_p[4],'fathernameorspousename':list_p[5],'age':list_p[6],'gender':list_p[7]}})
        
         
    for p in persons_offline:
        list_p=list(p)
        for i in range(len(p)-1):
            if not list_p[i]:
                list_p[i]= " "
            else:
                list_p[i]=str(list_p[i])            
        list_person.append({'id':p[8],'dic':{'district':list_p[0],'block':list_p[1],'village':list_p[2],'group':list_p[3],'personname':list_p[4],'fathernameorspousename':list_p[5],'age':list_p[6],'gender':list_p[7]}})
        
    # Find this value in the url with 'key=XXX' and copy XXX below
    spreadsheet_key = '0AsotIQD30kd_dGZXZEZiVE9nYlhvNURPSXNSdFM2RGc'
    # All spreadsheets have worksheets. I think worksheet #1 by default always
    # has a value of 'od6'
    worksheet_id = 'od6'
    
    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.email = EMAIL_HOST_USER
    spr_client.password = EMAIL_HOST_PASSWORD
    spr_client.source = 'DG Path App'
    spr_client.ProgrammaticLogin()
    curr_offline=PathLog.objects.aggregate(Max('person_offline_id'))['person_offline_id__max']
    curr_online=PathLog.objects.aggregate(Max('person_online_id'))['person_online_id__max']
    for elem in list_person:
        ex_flag=0
        while(ex_flag<3):
            try:
                entry = spr_client.InsertRow(elem['dic'], spreadsheet_key, worksheet_id)
            except Exception as ex:
                ex_flag=ex_flag+1
            if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
                if(elem['id']>MIN_ONLINE):
                    curr_online=elem['id']
                else:
                    curr_offline=elem['id']
                break    
        if(ex_flag==3):
            try:
                PathLog.objects.filter(id =PathLog.objects.aggregate(Max('id'))['id__max']).update(read=True)
            except Exception as ex:
                print ex
            curr_elem = PathLog( person_offline_id = curr_offline, 
                          person_online_id = curr_online)
            try:
                curr_elem.save()
            except Exception as ex:
                print ex
            return HttpResponse("Aborted")
    

    try:
        PathLog.objects.filter(id =PathLog.objects.aggregate(Max('id'))['id__max']).update(read=True)
    except Exception as ex:
        print ex
    curr_elem = PathLog( person_offline_id = person.filter(id__gt= 68000000000,id__lt= 69000000000).aggregate(Max('id'))['id__max'], 
                          person_online_id = person.aggregate(Max('id'))['id__max'])
    try:
        curr_elem.save()
    except Exception as ex:
        print ex
    
    return HttpResponse("Success")
        
     
 
