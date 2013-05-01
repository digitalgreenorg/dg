# -*- coding: utf-8 -*-
import settings
from django.core.management import setup_environ
setup_environ(settings)
from dashboard.models import *
import video_schedule
import xlrd
import xlwt
import sys
import time
from datetime import datetime,timedelta

three_months = datetime.now() - timedelta(days = 365)

def truncate_id(id):
    return id

def find_exact_villages(cluster_dict):
    
    village_not_found = 0 
    mediator_dict= []
    for cluster in cluster_dict:
        counter = 0
        for vill in cluster['villages']:
            if vill == '':
                print "blank"
            else:
                village_info = []
                village_info = Village.objects.filter(village_name = vill).values_list('id','village_name')
                if village_info:
                    cluster['villages'][counter] = village_info[0][1]
                    counter += 1
                    mediator_dict.append(({'mediator': '',
                                      'village': village_info[0][1],
                                      'cluster': cluster['cluster']}))
                else:
                    village_info = Village.objects.filter(village_name__icontains = vill).values_list('id','village_name')
                    cluster['villages'][counter] = village_info[0][1]
                    counter += 1
                    mediator_dict.append(({'mediator': '',
                                      'village': village_info[0][1],
                                      'cluster': cluster['cluster']}))
                if not village_info:
                    village_not_found +=1
    return cluster_dict, mediator_dict
    
    
def write_person_info(cluster_dict, workbook):
    person_info = []
    sheet = workbook.add_sheet('person')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: group_id")
    sheet.write(row, 3, "field: seen")
    sheet.write(row, 4, "group 1")
    row += 1
    vid_list = []
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_person_info = Person.objects.filter(village__village_name = vill).values_list('id','person_name','group')
            person_info.append(village_person_info)
            for person in village_person_info:
                person_id = truncate_id(person[0])
                group_id = truncate_id(person[2])
                sheet.write(row, 0, unicode(person_id))
                sheet.write(row, 1, person[1])
                sheet.write(row, 2, unicode(group_id))
                vid_id_list = PersonMeetingAttendance.objects.filter(person = person[0], screening__date__gt = three_months).values_list('screening__videoes_screened', flat = True)
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
                    watched = PersonMeetingAttendance.objects.filter(person = person, screening__date__gt = three_months).values_list('screening__videoes_screened').distinct().count()
                    if watched > 0:
                        sheet.write(row, 3, '1')
                    else:
                        sheet.write(row, 3, '0')
                    row += 1
        if len(village_person_info) < 1:
            print " No person found in " + cluster['cluster'] 
    
    sheet = workbook.add_sheet('all_videos')
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
    sheet = workbook.add_sheet('group')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: village_id")
    sheet.write(row, 3, "field: seen")
    sheet.write(row, 4, "group 1")
    row += 1
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_persongroup_info = PersonGroups.objects.filter(village = vill).values_list('id','group_name','village')
            group_info.append(village_persongroup_info)
            for group in village_persongroup_info:
                watched = PersonMeetingAttendance.objects.filter(person__group = group[0], screening__date__gt = three_months).values_list('screening__videoes_screened').distinct().count() 
                group_id = truncate_id(group[0])
                vill_id = truncate_id(group[2])
                sheet.write(row, 0, str(group_id))
                sheet.write(row, 1, group[1])
                sheet.write(row, 2, str(vill_id))
                if watched > 0:
                    sheet.write(row, 3, '1')
                else:
                    sheet.write(row, 3, '0')
                sheet.write(row, 4, cluster['cluster'])
                row += 1
            if Person.objects.filter(village = vill, group = None).count() > 0:
                sheet.write(row, 0, str(vill_id))
                sheet.write(row, 1, 'Without Group')
                sheet.write(row, 2, str(vill_id))
                watched = PersonMeetingAttendance.objects.filter(person__village = vill_id, person__group = None, screening__date__gt = three_months).values_list('screening__videoes_screened').distinct().count()
                if watched > 0:
                    sheet.write(row, 3, '1')
                else:
                    sheet.write(row, 3, '0')
                row += 1
            
    return sheet

def write_village_info(cluster_dict, workbook):
    village_info = []
    sheet = workbook.add_sheet('village')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: seen ")
    sheet.write(row, 3, "group 1")
    row += 1
    village_not_found = 0 
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            
            village_info = Village.objects.filter(id = vill).values_list('id','village_name')
            if village_info:
                watched = PersonMeetingAttendance.objects.filter(person__village = village_info[0][0], screening__date__gt = three_months).values_list('screening__videoes_screened').distinct().count()
                village_id = truncate_id(village_info[0][0])
                sheet.write(row, 0, str(village_id))
                sheet.write(row, 1, village_info[0][1])
                if watched > 0:
                    sheet.write(row, 2, '1')
                else:
                    sheet.write(row, 2, '0')
                 
                sheet.write(row, 3, cluster['cluster'])
                row += 1
            else:
                village_not_found +=1
                print vill + " not found"
    print str(village_not_found) + " villages not found "
    return sheet

def write_mediator_info(mediator_dict, workbook):
    mediator_info = []
    sheet = workbook.add_sheet('mediator')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: village_id")
    sheet.write(row, 3, "group 1")
    row += 1
    mediator_not_found = 0
    for mediator in mediator_dict:
        mediator_info = AnimatorAssignedVillage.objects.filter(village__village_name = mediator['village']).values_list('animator_id','animator__name','village_id')
        if len(mediator_info)<1:
            mediator_info = AnimatorAssignedVillage.objects.filter(village__village_name__icontains = mediator['village']).values_list('animator__id','animator__name','village_id')
        if(mediator_info):
            mediator_id = truncate_id(mediator_info[0][0])
            vill_id = truncate_id(mediator_info[0][2])
            sheet.write(row, 0, str(mediator_id))
            sheet.write(row, 1, mediator_info[0][1])
            sheet.write(row, 2, str(vill_id))
            sheet.write(row, 3, mediator['cluster'])
            row += 1
        else:
            mediator_not_found += 1
            print "no mediator for "  + mediator['village']
    print str(mediator_not_found) + " mediators not found"
    return sheet

def write_distinct(vid_list, workbook):
    sheet = workbook.add_sheet('unique_video')
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
            sheet.write(row, 2, 'KURNOOL')  # for testing 
            row += 1
    return sheet
    

def write_person_watched_video_info(cluster_dict, workbook):
    person_info = []
    sheet = workbook.add_sheet('videoseen')
    row = 0
    sheet.write(row, 0, "field: id")
#    sheet.write(row, 1, "field: name ")
    sheet.write(row, 1, "field: video_id")
    sheet.write(row, 2, "group 1")
    row += 1
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_person_info = Person.objects.filter(village__village_name = vill).values_list('id','person_name','group')
#            person_info.append(village_person_info)
            for person in village_person_info:
                vid_id_list = PersonMeetingAttendance.objects.filter(person = person[0], screening__date__gt = three_months).values_list('screening__videoes_screened', flat = True)
                for vid_id in vid_id_list:
                    if (vid_id):
                        vid_name = Video.objects.filter(id = vid_id).values_list('title')
                        person_id = truncate_id(person[0])
                        group_id = truncate_id(person[2])
                        sheet.write(row, 0, str(person_id))
#                        sheet.write(row, 1, vid_name[0])
                        sheet.write(row, 1, str(vid_id))
                        sheet.write(row, 2, cluster['cluster'])
                        row += 1
                    else:
                        print "not found"
                        
        if len(village_person_info) < 1:
            print " No person found in " + cluster['cluster'] 
    return sheet

def write_video_schedule_info(vid_dict, workbook):
    sheet = workbook.add_sheet('video')
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
            sheet.write(row, 3, 'KURNOOL')  # for testing 
            row += 1
        else:
            print str(record['id']) + " not found"
    return sheet
        
from userfile_functions import read_userfile
data = read_userfile('userfileappilot.json')
cluster_village_dict = []
mediator_dict = []
for entry in data:
    print entry['username']
    villages = entry['villages']
    cluster_village_dict.append({'cluster': entry['username'],
                                 'villages': entry['villages']})
    for v in villages:
        village = Village.objects.get(id = v).village_name
        mediator = Animator.objects.filter(assigned_villages = v)[0]
        mediator_dict.append({'mediator':mediator,
                              'village': village,
                              'cluster' : entry['username']})
workbook = xlwt.Workbook(encoding = 'utf-8')
group_sheet = write_group_info(cluster_village_dict, workbook)
village_sheet = write_village_info(cluster_village_dict, workbook)
mediator_sheet = write_mediator_info(mediator_dict, workbook)
video_schedule_dict, video_list = video_schedule.get_video_schedule()
print video_list
video_list = Screening.objects.filter(village__block__district__state__state_name = 'Andhra Pradesh').values_list('videoes_screened', flat=True)
video_list = set(video_list)
print video_list
video_distinct_sheet = write_distinct(video_list,workbook)
video_schedule_sheet = write_video_schedule_info(video_schedule_dict,workbook)
workbook.save('trial-2-Fixtures_02_25.xls')







    
