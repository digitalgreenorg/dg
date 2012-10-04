import settings
from django.core.management import setup_environ
setup_environ(settings)
from dashboard.models import *
import video_schedule
import xlrd
import xlwt


def truncate_id(id):
    return id

def find_exact_villages(cluster_dict):
    village_info = []
    village_not_found = 0 
    for cluster in cluster_dict:
        for counter,vill in enumerate(cluster['villages']):
            village_info = Village.objects.filter(village_name = vill).values_list('id','village_name')
            if village_info:
                cluster["villages"][counter] = village_info[0][1]
            else:
                village_info = Village.objects.filter(village_name__icontains = vill).values_list('id','village_name')
                cluster["villages"][counter] = village_info[0][1]
            if not village_info:
                village_not_found +=1
    return cluster_dict
    
    
def write_person_info(cluster_dict, workbook):
    person_info = []
    sheet = workbook.add_sheet('person')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: group_id")
    sheet.write(row, 3, "group 1")
    row += 1
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_person_info = Person.objects.filter(village__village_name = vill).values_list('id','person_name','group')
            person_info.append(village_person_info)
            for person in village_person_info:
                person_id = truncate_id(person[0])
                group_id = truncate_id(person[2])
                sheet.write(row, 0, str(person_id))
                sheet.write(row, 1, person[1])
                sheet.write(row, 2, str(group_id))
                watched = PersonMeetingAttendance.objects.filter(person = person[0]).count()
                if(watched > 0 ):
                    sheet.write(row, 3, '1')
                else:
                    sheet.write(row, 3, '0')
                sheet.write(row, 4, cluster['cluster'])
                row += 1
        if len(village_person_info) < 1:
            print " No person found in " + cluster['cluster'] 
    return sheet

def write_group_info(cluster_dict, workbook):
    group_info = []
    sheet = workbook.add_sheet('group')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: village_id")
    sheet.write(row, 3, "group 1")
    row += 1
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_persongroup_info = PersonGroups.objects.filter(village__village_name = vill).values_list('id','group_name','village')
            group_info.append(village_persongroup_info)
            for group in village_persongroup_info:
                group_id = truncate_id(group[0])
                vill_id = truncate_id(group[2])
                sheet.write(row, 0, str(group_id))
                sheet.write(row, 1, group[1])
                sheet.write(row, 2, str(vill_id))
                sheet.write(row, 3, cluster['cluster'])
                row += 1
    return sheet

def write_village_info(cluster_dict, workbook):
    village_info = []
    sheet = workbook.add_sheet('village')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "group 1")
    row += 1
    village_not_found = 0 
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_info = Village.objects.filter(village_name = vill).values_list('id','village_name')
            if village_info:
                village_id = truncate_id(village_info[0][0])
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
        mediator_info = Animator.objects.filter(assigned_villages__village_name = mediator['village']).values_list('id','name','village__id')
        if len(mediator_info)<1:
            mediator_info = Animator.objects.filter(village__village_name__icontains = mediator['village']).values_list('id','name',
                                                                                                                        'village__id')
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
    print str(mediator_not_found) + " mediators not found"
    return sheet

def write_person_watched_video_info(cluster_dict, workbook):
    person_info = []
    sheet = workbook.add_sheet('videoseen')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: video_id")
    sheet.write(row, 3, "group 1")
    row += 1
    for cluster in cluster_dict:
        for vill in cluster['villages']:
            village_person_info = Person.objects.filter(village__village_name = vill).values_list('id','person_name','group')
#            person_info.append(village_person_info)
            for person in village_person_info:
                vid_id_list = PersonMeetingAttendance.objects.filter(person = person[0]).values_list('screening__videoes_screened', flat = True).distinct()
                for vid_id in vid_id_list:
                    vid_name = Video.objects.filter(id = vid_id).values_list('title')
                    person_id = truncate_id(person[0])
                    group_id = truncate_id(person[2])
                    sheet.write(row, 0, str(person_id))
                    sheet.write(row, 1, vid_name[0])
                    sheet.write(row, 2, str(vid_id))
                    sheet.write(row, 3, cluster['cluster'])
                    row += 1
        if len(village_person_info) < 1:
            print " No person found in " + cluster['cluster'] 
    return sheet

def write_video_schedule_info(vid_dict, workbook):
    sheet = workbook.add_sheet('video')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name")
    sheet.write(row, 2, "field: low")
    sheet.write(row, 3, "field: high")
    sheet.write(row, 4, 'group 1')
    row += 1
    for record in vid_dict:
        vid_name = Video.objects.filter(id = record['id']).values_list('title')
        if vid_name:
            sheet.write(row, 0, str(record['id']))
            sheet.write(row, 1, vid_name[0][0])
            sheet.write(row, 2, record['low_val'])
            sheet.write(row, 3, record['high_val'])
            sheet.write(row, 4, 'JADCHERLA')  # for testing 
            row += 1
        else:
            print str(record['id']) + " not found"
    return sheet
        

wb = xlrd.open_workbook('..\mahabubnagar1_cluster.xls')
wb.sheet_names()
sh = wb.sheet_by_index(0)
clusters_to_take = [1]
index=0

permission_group = []
cluster_village_dict = []
mediator_village_dict = []
 
while index < len(clusters_to_take):
    i=clusters_to_take[index]
    name = sh.cell(rowx=i,colx=0).value
    print "Processing values of cluster " + name
    cluster_village_dict.append({'cluster':name , 'villages': [sh.cell(rowx=i+vill,colx=1).value for vill in range(0,2)]})
    for village in range(0,2):
        mediator_village_dict.append({'mediator': sh.cell(rowx=i+village,colx=1).value,
                                      'village': sh.cell(rowx=i+village,colx=1).value,
                                      'cluster': name})
    
    index += 1 

workbook = xlwt.Workbook()
cluster_village_dict = find_exact_villages(cluster_village_dict)

person_sheet = write_person_info(cluster_village_dict, workbook)
group_sheet = write_group_info(cluster_village_dict, workbook)
village_sheet = write_village_info(cluster_village_dict, workbook)
mediator_sheet = write_mediator_info(mediator_village_dict, workbook)
video_sheet = write_person_watched_video_info(cluster_village_dict, workbook)
video_schedule_dict = video_schedule.get_video_schedule()
video_schedule_sheet = write_video_schedule_info(video_schedule_dict,workbook)
workbook.save('trial-2-Fixture.xls')
print "Done"





    
