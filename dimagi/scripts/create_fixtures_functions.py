# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
import os
import sys
import time
import xlrd
import xlsxwriter

from activities.models import PersonMeetingAttendance, Screening
from geographies.models import Village
from people.models import Animator, Person, PersonGroup
from videos.models import Video
from dg.settings import MEDIA_ROOT

from dimagi.models import CommCareUser, CommCareUserVillage

one_year = datetime.now() - timedelta(days = 365)

def write_type_info(workbook):
    sheet = workbook.add_worksheet('types')
    row = 0
    sheet.write(row, 0, "name")
    sheet.write(row, 1, "tag")
    sheet.write(row, 2, "field 1")
    sheet.write(row, 3, "field 2")
    sheet.write(row, 4, "field 3")
    sheet.write(row, 5, "field 4")
    row = 1
    #Define group relation below
    sheet.write(row, 0, "Group")
    sheet.write(row, 1, "group")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "village_id")
    sheet.write(row, 5, "")
    row = 2
    #Define village relation below
    sheet.write(row, 0, "Village")
    sheet.write(row, 1, "village")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "")
    sheet.write(row, 5, "")
    row = 3
    #Define mediator relation below
    sheet.write(row, 0, "Mediator")
    sheet.write(row, 1, "mediator")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "village_id")
    sheet.write(row, 5, "")
    row = 4
    #Define unique video relation below
    sheet.write(row, 0, "Unique_video")
    sheet.write(row, 1, "unique_video")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "")
    sheet.write(row, 5, "")
    row = 5
    #Define video relation below
    sheet.write(row, 0, "Video")
    sheet.write(row, 1, "video")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "low")
    sheet.write(row, 4, "high")
    sheet.write(row, 5, "")
    return sheet

def write_person_info(cluster_dict, workbook):
    person_info = []
    sheet = workbook.add_worksheet('person')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: group_id")
    sheet.write(row, 3, "")
    sheet.write(row, 4, "group 1")
    row += 1
    vid_list = []
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_person_info = Person.objects.filter(village__village_name = vill).values_list('id','person_name','group')
            person_info.append(village_person_info)
            for person in village_person_info:
                person_id = person[0]
                group_id = person[2]
                sheet.write(row, 0, unicode(person_id))
                sheet.write(row, 1, person[1])
                sheet.write(row, 2, unicode(group_id))
                vid_id_list = PersonMeetingAttendance.objects.filter(person = person[0], screening__date__gt = one_year).values_list('screening__videoes_screened', flat = True)
                if len(vid_id_list) > 0:
                    arr = ''
                    for vid in vid_id_list:
                        vid_list.append(vid)
                        arr = arr + str(vid) + ' '
                    sheet.write(row, 3, arr)
                else:
                    sheet.write(row, 3, '0')
                sheet.write(row, 4, cluster['cluster'])
                row += 1
            if Person.objects.filter(village__village_name= vill, group = None).count() > 0:
                p = Person.objects.filter(village__village_name= vill, group = None).values_list('id', 'person_name','village')
                for person, name, vill_id in p:
                    sheet.write(row, 0, str(person))
                    sheet.write(row, 1, unicode(name))
                    sheet.write(row, 2, str(vill_id))                    
                    row += 1
        if len(village_person_info) < 1:
            print " No person found in " + cluster['cluster'] 
    
    sheet = workbook.add_worksheet('all_videos')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    vid_list = set(vid_list)
    row += 1
    for id in vid_list:
        vid_obj = Video.objects.get(id = id)
        title = vid_obj.title
        sheet.write(row, 0, str(id))
        sheet.write(row, 1, unicode(title))
        row += 1
    return sheet

def write_group_info(cluster_dict, workbook):
    group_info = []
    sheet = workbook.add_worksheet('group')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: village_id")
    sheet.write(row, 3, "user 1")
    sheet.write(row, 4, "user 2")
    sheet.write(row, 5, "group 1")
    row += 1
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_persongroup_info = PersonGroup.objects.filter(village = vill).values_list('id','group_name','village')
            group_info.append(village_persongroup_info)
            for group in village_persongroup_info:         
                group_id = group[0]
                print 'in write group info '+ str(group[0])
                vill_id = group[2]
                print 'in write group info '+ str(vill_id)
                sheet.write(row, 0, str(group_id))
                sheet.write(row, 1, group[1])
                sheet.write(row, 2, str(vill_id))
                sheet.write(row, 3, cluster['cluster'])
                row += 1
            if Person.objects.filter(village = vill, group = None).count() > 0:
                sheet.write(row, 0, str(vill_id))
                sheet.write(row, 1, 'Without Group')
                sheet.write(row, 2, str(vill_id))
                row += 1
            
    return sheet

def write_village_info(cluster_dict, workbook):
    village_info = []
    sheet = workbook.add_worksheet('village')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "user 1")
    sheet.write(row, 3, "user 2")
    sheet.write(row, 4, "group 1")
    row += 1
    village_not_found = 0 
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            
            village_info = Village.objects.filter(id = vill).values_list('id','village_name')
            if village_info:
                village_id = village_info[0][0]
                sheet.write(row, 0, str(village_id))
                sheet.write(row, 1, village_info[0][1])
                sheet.write(row, 2, cluster['cluster'])
                row += 1
            else:
                village_not_found +=1
                print vill + " not found"
    print str(village_not_found) + " villages not found "
    return sheet

def write_mediator_info(mediator_dict, workbook):
    sheet = workbook.add_worksheet('mediator')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: village_id")
    sheet.write(row, 3, "user 1")
    sheet.write(row, 4, "user 2")
    sheet.write(row, 5, "group 1")
    row += 1
    mediator_not_found = 0
    for mediator in mediator_dict:
        mediator_id = mediator['mediator']
        vill_id = mediator['village']
        print 'in write mediator info '+vill_id
        user_name = mediator['cluster']
        mediator_name = mediator['mediator_name']
        if(mediator):
            sheet.write(row, 0, str(mediator_id))
            sheet.write(row, 1, mediator_name)
            sheet.write(row, 2, str(vill_id))
            sheet.write(row, 3, user_name)
            row += 1
        else:
            mediator_not_found += 1
            print "no mediator for "  + str(mediator['village'])
    print str(mediator_not_found) + " mediators not found"
    return sheet

def write_distinct(vid_list, workbook):
    sheet = workbook.add_worksheet('unique_video')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name")
    sheet.write(row, 2, 'group 1')
    row += 1
    for id in vid_list:
        vid_name = Video.objects.filter(id = id).values_list('title')
        if vid_name:
            sheet.write(row, 0, str(id))
            sheet.write(row, 1, unicode(vid_name[0][0]))
            sheet.write(row, 2, 'warangal')  # for testing 
            row += 1
    sheet.write(row,0,"0")
    sheet.write(row,1,"More Videos")
    sheet.write(row,2,'warangal')
    return sheet

def write_video_schedule_info(vid_dict, workbook):
    sheet = workbook.add_worksheet('video')
    row = 0
    sheet.write(row, 0, "field: id")
#    sheet.write(row, 1, "field: name")
    sheet.write(row, 1, "field: low")
    sheet.write(row, 2, "field: high")
    sheet.write(row, 3, 'group 1')
    row += 1
    for record in vid_dict:
        vid_name = Video.objects.filter(id = record['id']).values_list('title')
        if vid_name:
            sheet.write(row, 0, str(record['id']))
#            sheet.write(row, 1, vid_name[0][0])
            sheet.write(row, 1, record['low_val'])
            sheet.write(row, 2, record['high_val'])
            sheet.write(row, 3, 'warangal')  # for testing 
            row += 1
        else:
            print str(record['id']) + " not found"
    sheet.write(row,0,"0")
    sheet.write(row,1,"2013-01-01")
    sheet.write(row,2,"2100-12-31")
    sheet.write(row,3,'warangal')
    return sheet
        
#getting user getting from the database and storing it in list of dictionaries

def create_fixture(users, project_name, want_seasonal_behavior):
    # getting user information in list of dictionaries; dictionary contains ursrname, uder_id and villages assigned
    data = []    
    for user in users:
        dict = {}
        villages = CommCareUserVillage.objects.filter(user = user.id)
        if villages:
            dict['villages']=[]
            for vil in villages:
                dict['villages'].append(vil.village.id)
            dict['username'] = user.username
            dict['user_id'] = user.guid
            data.append(dict)
        else:
            print 'No villages assigned to %s'% user.username
        
    cluster_village_dict = []
    mediator_dict = []
    for entry in data:
        print entry['username']
        villages = entry['villages']
        cluster_village_dict.append({'cluster': entry['username'],
                                     'villages': entry['villages']})
        for v in villages:
            mediator = ''
            try:
                mediator_list = Animator.objects.filter(assigned_villages = v)
            except Exception ,ex:
                pass
            for mediator in mediator_list:
                mediator_dict.append({'mediator':mediator.id,
                                      'mediator_name':mediator.name,
                                      'village': v,
                                      'cluster' : entry['username']})
    if want_seasonal_behavior.lower() =="yes":
        filename = os.path.join(MEDIA_ROOT, "dimagi", "%s_fixtures.xlsx" % (project_name))
    else:
        filename = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_fixtures_update.xlsx" % (project_name))
        
    workbook = xlsxwriter.Workbook(filename)
    type_sheet = write_type_info(workbook)
    group_sheet = write_group_info(cluster_village_dict, workbook)
    village_sheet = write_village_info(cluster_village_dict, workbook)
    mediator_sheet = write_mediator_info(mediator_dict, workbook)
    video_list = Screening.objects.filter(village__block__district__state__state_name = 'Andhra Pradesh').values_list('videoes_screened', flat=True)
    video_list = set(video_list)
    video_distinct_sheet = write_distinct(video_list,workbook)
    if want_seasonal_behavior.lower() =="yes":
        video_schedule_list = []
        for id in video_list:
            video_schedule_list.append(id)
        video_schedule_list_of_dict = []
        ##Get videos screened in Chittor for this project
        video_list_screened_in_villages = Screening.objects.filter(village__block__district__id = 47).values_list('videoes_screened', flat=True) 
        for id in video_list_screened_in_villages[:5]: #when we create a project, we should atleast see some data. That can serve as example. And seasonal data must be added and deleted as and when they needed.
            video_schedule_list_of_dict.append({'id': id,
                                        'low_val': '2013-01-01', 
                                        'high_val': '2020-01-01' })
        video_schedule_sheet = write_video_schedule_info(video_schedule_list_of_dict,workbook)
        