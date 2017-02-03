# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import xlsxwriter

import requests
from requests.auth import HTTPDigestAuth

from activities.models import PersonMeetingAttendance, Screening
from geographies.models import Village, State
from people.models import Animator, Person, PersonGroup
from videos.models import Video
from dg.settings import MEDIA_ROOT, DIMAGI_USERNAME, DIMAGI_PASSWORD

from dimagi.models import CommCareUser


def write_type_info(workbook):
    sheet = workbook.add_worksheet('types')
    row = 0
    #header row
    sheet.write(row, 0, "name")
    sheet.write(row, 1, "tag")
    sheet.write(row, 2, "field 1")
    sheet.write(row, 3, "field 2")
    sheet.write(row, 4, "field 3")
    sheet.write(row, 5, "field 4")
    row = 1
    #Define village relation below
    sheet.write(row, 0, "Village")
    sheet.write(row, 1, "village")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "")
    sheet.write(row, 5, "")
    row = 2
    #Define mediator relation below
    sheet.write(row, 0, "Mediator")
    sheet.write(row, 1, "mediator")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "village_id")
    sheet.write(row, 5, "")
    row = 3
    #Define group relation below
    sheet.write(row, 0, "Group")
    sheet.write(row, 1, "group")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "village_id")
    sheet.write(row, 5, "")


def write_village_info(village_dict_list, workbook):
    sheet = workbook.add_worksheet('village')
    row = 0
    #header row
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "user 1")
    sheet.write(row, 3, "user 2")
    sheet.write(row, 4, "group 1")
    row += 1
    for village_dict in village_dict_list:
        sheet.write(row, 0, str(village_dict['village_id']))
        sheet.write(row, 1, unicode(village_dict['village_name']))
        sheet.write(row, 2, str(village_dict['username']))
        row += 1


def write_mediator_info(mediator_dict_list, workbook):
    sheet = workbook.add_worksheet('mediator')
    row = 0
    #header row
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: village_id")
    sheet.write(row, 3, "user 1")
    sheet.write(row, 4, "user 2")
    sheet.write(row, 5, "group 1")
    row += 1
    for mediator_dict in mediator_dict_list:
        sheet.write(row, 0, str(mediator_dict['mediator_id']))
        #print str(mediator_dict['mediator_id'])
        #print mediator_dict['mediator_id']
        sheet.write(row, 1, unicode(mediator_dict['mediator_name']))
        sheet.write(row, 2, str(mediator_dict['village_id']))
        sheet.write(row, 3, str(mediator_dict['username']))
        row += 1


def write_group_info(group_dict_list, workbook):
    sheet = workbook.add_worksheet('group')
    row = 0
    #header row
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name ")
    sheet.write(row, 2, "field: village_id")
    sheet.write(row, 3, "user 1")
    sheet.write(row, 4, "user 2")
    sheet.write(row, 5, "group 1")
    row += 1
    for group_dict in group_dict_list:
        sheet.write(row, 0, str(group_dict['group_id']))
        sheet.write(row, 1, unicode(group_dict['group_name']))
        sheet.write(row, 2, str(group_dict['village_id']))
        sheet.write(row, 3, str(group_dict['username']))
        row += 1


def write_distinct_video(vid_list, workbook, group_name):
    sheet = workbook.add_worksheet('unique_video')
    row = 0
    #header row
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: name")
    sheet.write(row, 2, 'group 1')
    row += 1
    print vid_list
    for id in vid_list:
        vid = Video.objects.get(id=id)
        if vid.title:
            sheet.write(row, 0, str(id))
            sheet.write(row, 1, unicode(vid.title))
            sheet.write(row, 2, str(group_name))
            row += 1


def write_latest_video_info(vid_dict, workbook, group_name):
    sheet = workbook.add_worksheet('video')
    row = 0
    sheet.write(row, 0, "field: id")
    sheet.write(row, 1, "field: low")
    sheet.write(row, 2, "field: high")
    sheet.write(row, 3, 'group 1')
    row += 1
    for record in vid_dict:
        sheet.write(row, 0, str(record['id']))
        sheet.write(row, 1, record['low_val'])
        sheet.write(row, 2, record['high_val'])
        sheet.write(row, 3, str(group_name))
        row += 1
    sheet.write(row, 0, "0")
    sheet.write(row, 1, "2013-01-01")
    sheet.write(row, 2, "2100-12-31")
    sheet.write(row, 3, str(group_name))
    return sheet


def create_fixture(users, project_name, list_group, list_village, list_mediator, Update):
    # getting user information in list of dictionaries; dictionary contains ursrname, uder_id and villages assigned
    data = []
    for user in users:
        filename = os.path.join(MEDIA_ROOT, "dimagi", "%s_%s_fixtures.xlsx" % (project_name, user.username))
        workbook = xlsxwriter.Workbook(filename)
        write_type_info(workbook)
        username = user.username
        user_id = user.guid
        
        village_dict_list = []
        mediator_dict_list = []
        group_dict_list = []
        
        villages = user.coco_user.villages.all()
        if villages:
            for vil in villages:
                if str(vil.id) not in list_village:
                    village_dict = {}
                    village_dict['village_id'] = vil.id
                    village_dict['village_name'] = vil.village_name
                    village_dict['username'] = username
                    village_dict['user_id'] = user_id
                    village_dict_list.append(village_dict)

                for animator in Animator.objects.filter(assigned_villages=vil):
                    if (str(animator.id), str(vil.id)) not in list_mediator:
                        mediator_dict = {}
                        mediator_dict['mediator_id'] = animator.id
                        mediator_dict['mediator_name'] = animator.name
                        mediator_dict['village_id'] = vil.id
                        mediator_dict['username'] = username
                        mediator_dict_list.append(mediator_dict)
                for group in PersonGroup.objects.filter(village=vil):
                    if (str(group.id) not in list_group):
                        group_dict = {}
                        group_dict['group_id'] = group.id
                        group_dict['group_name'] = group.group_name
                        group_dict['village_id'] = vil.id
                        group_dict['username'] = username
                        group_dict_list.append(group_dict)
            write_village_info(village_dict_list, workbook)
            write_mediator_info(mediator_dict_list, workbook)
            write_group_info(group_dict_list, workbook)
            workbook.close()
            # Uploading Fixtures to Commcare
            url = "".join(["https://www.commcarehq.org/a/", project_name, "/fixtures/fixapi/"])
            payload = {'replace': 'false'}
            files = {'file-to-upload': open(filename, 'rb')}
            print "Upload start" + filename
            r = requests.post(url, data=payload, files=files, auth=HTTPDigestAuth(DIMAGI_USERNAME, DIMAGI_PASSWORD))
            r.content
            print "Uploaded: "+filename
        else:
            print 'No villages assigned to %s' % user.username


def create_fixture_video(project_name, users, group_name):
    filename = os.path.join(MEDIA_ROOT, "dimagi", "%s_fixtures_video.xlsx" % (project_name))
    workbook = xlsxwriter.Workbook(filename)

    #Adding Video and Unique Video Information
    sheet = workbook.add_worksheet('types')
    row = 0
    sheet.write(row, 0, "name")
    sheet.write(row, 1, "tag")
    sheet.write(row, 2, "field 1")
    sheet.write(row, 3, "field 2")
    sheet.write(row, 4, "field 3")
    sheet.write(row, 5, "field 4")

    row = 1
    #Define unique video relation below
    sheet.write(row, 0, "Unique_video")
    sheet.write(row, 1, "unique_video")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "name")
    sheet.write(row, 4, "")
    sheet.write(row, 5, "")

    row = 2
    #Define video relation below
    sheet.write(row, 0, "Video")
    sheet.write(row, 1, "video")
    sheet.write(row, 2, "id")
    sheet.write(row, 3, "low")
    sheet.write(row, 4, "high")
    sheet.write(row, 5, "")

    village_list = []
    partner_list = []
    
    for user in users:
        village_list.append(list(user.coco_user.villages.all().values_list('id', flat=True)))
        if user.coco_user.partner_id not in partner_list:
            partner_list.append(user.coco_user.partner_id)
    villages = reduce(lambda x, y: x + y, village_list)
    user_states = State.objects.filter(district__block__village__id__in=villages).distinct().values_list('id', flat=True)
    
    #Video List from Videos Screened
    #video_list = Screening.objects.filter(village__block__district__state__id__in=user_states, partner_id__in=partner_list).values_list('videoes_screened', flat=True).order_by('-date')
    #video_list = [i for i in video_list if i is not None]
    #video_list = set(video_list)

    #Video List from Video Table
    videos_list = Video.objects.filter(village__block__district__state__id__in=user_states, partner_id__in=partner_list).values_list('id', flat=True)
    videos_list = [i for i in videos_list if i is not None]

    write_distinct_video(videos_list, workbook, group_name)
    video_schedule_list_of_dict = []
    for id in list(videos_list):
        video_schedule_list_of_dict.append({'id': id,
                                        'low_val': '2013-01-01',
                                        'high_val': '2020-01-01'})
    write_latest_video_info(video_schedule_list_of_dict, workbook, group_name)
    workbook.close()

    # Uploading Fixtures to Commcare
    url = "".join(["https://www.commcarehq.org/a/", project_name, "/fixtures/fixapi/"])
    payload = {'replace': 'True'}
    files = {'file-to-upload': open(filename, 'rb')}

    r = requests.post(url, data=payload, files=files, auth=HTTPDigestAuth(DIMAGI_USERNAME, DIMAGI_PASSWORD))

