# python imports
import dg.settings
import json, StringIO
import re
from os.path import join, dirname, abspath
# django imports
from datetime import datetime
from django.contrib import auth
from django.core import urlresolvers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message
# app imports
from forms import DataUploadForm
from models import CocoUser
from videos.models import APVideo
from coco.models import FullDownloadStats
from people.models import Person,Animator,AnimatorAssignedVillage
from people.models import PersonGroup
from geographies.models import Village,District, Block
from programs.models import Partner
from videos.models import Video,Language,Category,Practice,SubCategory
from activities.models import Screening
from activities.models import PersonAdoptPractice
from coco.prepare_data import *
from django.views.generic import View
from tastypie.models import ApiKey
import pandas as pd,os


def coco_v2(request):
    return render(request,'dashboard.html')
    
def login(request):
    partner_name = None
    type_of_cocouser = None
    partner_id = None
    user_id = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            coco_user_obj = CocoUser.objects.filter(user_id=request.user.id)
            if len(coco_user_obj):
                partner_name = coco_user_obj[0].partner.partner_name.lower()
                type_of_cocouser = coco_user_obj[0].type_of_cocouser
                partner_id = coco_user_obj[0].partner.id
                user_id = coco_user_obj[0].user.id
    else:
        return HttpResponse("0")
    return JsonResponse({'success': '1', 'partner_name': partner_name,
                         'type_of_cocouser': type_of_cocouser,
                         'partner_id': partner_id,
                         'type_of_cocouser': type_of_cocouser,
                         'user_id': user_id})

    
def logout(request):
    auth.logout(request)    
    return HttpResponse("1")
   
def record_full_download_time(request):
    if not(request.user and request.POST["start_time"] and request.POST["end_time"]):
        return HttpResponse("0")
    stat = FullDownloadStats(user = request.user, start_time = request.POST["start_time"], end_time = request.POST["end_time"])
    stat.save()
    return HttpResponse("1")
       
def reset_database_check(request):
    if not request.user.is_authenticated():
        return HttpResponse("0")
    cocouser = CocoUser.objects.get(user = request.user)
    if not(cocouser and cocouser.time_modified):
        return HttpResponse("0")
    lastdownloadtime = request.GET["lastdownloadtimestamp"]
    lastdownloadtimestamp = datetime.strptime(lastdownloadtime, '%Y-%m-%dT%H:%M:%S.%f')
    if lastdownloadtimestamp <= cocouser.time_modified:
        return HttpResponse("1")
    return HttpResponse("0")
    
               
def html_decorator(func):
    """
    This decorator wraps the output in html.
    (From http://stackoverflow.com/a/14647943)
    """
 
    def _decorated(*args, **kwargs):
        response = func(*args, **kwargs)
 
        wrapped = ("<html><body>",
                   response.content,
                   "</body></html>")
 
        return HttpResponse(wrapped)
 
    return _decorated
 
@html_decorator
def debug(request):
    """
    Debug endpoint that uses the html_decorator,
    """
    path = request.META.get("PATH_INFO")
    api_url = path.replace("debug/", "")
 
    view = urlresolvers.resolve(api_url)
 
    accept = request.META.get("HTTP_ACCEPT")
    accept += ",application/json"
    request.META["HTTP_ACCEPT"] = accept
 
    res = view.func(request, **view.kwargs)
    return HttpResponse(res._container)


def format_data(request, data_from_uploadqueue, user_data):
    data_list = data_from_uploadqueue
    user_id = user_data[0].get('user_id')
    partner_id = user_data[0].get('partner_id')
    action = None
    for item in data_list:
        if item.get('entity_name') == "group":
            # formatting for group
            format_data_or_saving_in_group(request, item.get('data'), user_id, partner_id)
        if item.get('entity_name') == "person":
            print item
            # formatting for group
            format_data_or_saving_in_person(request, item.get('data'), user_id, partner_id)
        if item.get('entity_name') == "mediator":
            # formatting for mediator
            format_data_or_saving_in_mediator(request, item.get('data'), user_id, partner_id)
        if item.get('entity_name') == "video":
            # formatting for video
            format_data_or_saving_in_video(request, item.get('data'), user_id, partner_id)
        if item.get('entity_name') == "nonnegotiable":
            format_data_or_saving_in_nonnegotiable(request, item.get('data'), user_id, partner_id)
        if item.get('entity_name') == "screening":
            # formatting for screening
            format_data_or_saving_in_screening(request, item.get('data'), user_id, partner_id)
        if item.get('entity_name') == "adoption":
            # formatting for screening
            format_data_or_saving_in_adoption(request, item.get('data'), user_id, partner_id)
    add_message(request, 25, "Data has been uploaded Successfully")
    return redirect(".")


@login_required
def upload_data(request):
    if request.method == 'POST':
        form_data = DataUploadForm(request.POST, request.FILES)
        if form_data.is_valid():
            cd = form_data.cleaned_data
            handle = request.FILES.get('datafile').read()
            try:
                data = json.loads(handle)
                data_from_uploadqueue = json.loads(data.get('uploadqueue'))
                user_data = json.loads(data.get('user'))
                format_data(request, data_from_uploadqueue, user_data)
            except:
                add_message(request, 25, "Data has been tampered")
                pass
            return redirect(".")
        else:
            add_message(request, 25, "Please correct the errors below.")
    else:
        form_data = DataUploadForm()
    context = {'form': form_data}
    template = "coco/data_upload.html"
    return render(request, template, context)

@login_required
def upload_csv_data(request):
    if request.method == 'POST':
        columns = 'Partner ID,District ID,Block Name,Village Name,Person Group,Member Name,Gender,Phone Number,Age'
        form_data = DataUploadForm(request.POST, request.FILES)
        if form_data.is_valid():
            cd = form_data.cleaned_data
            csv_file = request.FILES.get('datafile').read()
            try:
                file_data = csv_file.decode('utf-8')
                header = str(file_data.split('\n')[0])
                if '\r' in header:
                    header = header.strip('\r')
                if header == columns:
                    lines = file_data.split('\n')[1:]
                    for row in lines:
                        row = row.split(',')
                        block_obj, created = Block.objects.get_or_create(block_name__iexact=row[2].strip(),\
                                                                        district_id=int(row[1]), \
                                                                        defaults={'block_name': row[2].strip(), \
                                                                                 'district_id':int(row[1])})
                        if block_obj or created:
                            village_obj, created = \
                            Village.objects.get_or_create(village_name__iexact=row[3].strip(),block_id=block_obj.id,\
                                                            defaults={'village_name':row[3].strip(), \
                                                                    'block_id':block_obj.id})
                            if village_obj or created:
                                person_group, created = \
                                PersonGroup.objects.get_or_create(group_name__iexact=row[4].strip(),\
                                                                village_id=village_obj.id, \
                                                                partner_id=int(row[0]),\
                                                                defaults={'group_name': row[4].strip(),\
                                                                'village_id':village_obj.id, \
                                                                'partner_id':int(row[0])},)
                                if person_group or created:
                                    if row[8] != '' and row[8] != '\r':
                                        person_obj, created = \
                                        Person.objects.get_or_create(person_name=row[5], gender=row[6],\
                                         village_id=village_obj.id,group_id=person_group.id, \
                                         partner_id=int(row[0]), age=int(row[8]))
                                    else:
                                        person_obj, created = \
                                        Person.objects.get_or_create(person_name=row[5], gender=row[6], \
                                            village_id=village_obj.id, group_id=person_group.id, partner_id=int(row[0]))
                    add_message(request, 25, 'Data Successfully uploaded')
                else:
                    add_message(request,40, "File Header is not in correct format")
            except Exception as e:
                print e
                pass
            return redirect(".")
        else:
            add_message(request, 40, "Please correct the errors below.")
    else:
        form_data = DataUploadForm()
    context = {'form': form_data}
    template = "coco/data_upload.html"
    return render(request, template, context)


@login_required
def getFileHeader(request):
    if request.method == 'GET':
        columns = 'Partner ID,District ID,Block Name,Village Name,Person Group,Member Name,Gender,Phone Number,Age'
        output = StringIO.StringIO()
        try:
            output.write(columns)
            response = HttpResponse(output.getvalue().encode('utf-8-sig'), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=header_format.csv'
            return response
        except Exception as e:
            print e




class APVideoGenerator(View):

    def get(self, request, *args, **kwargs):
        meta_auth_container = request.META.get('HTTP_AUTHORIZATION')
        if meta_auth_container and len(meta_auth_container):
            apikey = meta_auth_container.split('ApiKey')[-1].split(':')[-1]
            try:
                apikey_object = ApiKey.objects.get(key=apikey)
                if apikey_object:
                    video_list = APVideo.objects.filter(video__partner_id=50)
                    data_list = []
                    practice_list = []
                    dg_practice_list = []
                    tags = []
                    for video_iterable in video_list:
                        dg_practice = video_iterable.video.videopractice.all()
                        for item in dg_practice:
                            dg_practice_list.append({'id': item.id,
                                                     'practice_name': item.videopractice_name,
                                                     })
                        practice_q = video_iterable.practice.all()
                        for item in practice_q:
                            practice_list.append({'id': item.id,
                                                  'practice_name': item.pest_name,
                                                  'practice_code': item.pest_code,
                                                  'practice_name_telgu': item.pest_name_telgu})
                        tags_q = video_iterable.video.tags.all()
                        for tag_item in tags_q:
                            tags.append({'id': tag_item.id,
                                         'tag_name': tag_item.tag_name,
                                         'tag_code': tag_item.tag_code,
                                         'tag_regional_name': tag_item.tag_regional_name})

                        data_list.append({'id': video_iterable.video.id,
                                         'video_title': video_iterable.video.title,
                                         'district_name': video_iterable.video.village.block.district.district_name,
                                         'video_short_name_english': video_iterable.video_short_name,
                                         'video_short_regionalname': video_iterable.video_short_regionalname,
                                         'category': {'id': video_iterable.video.category.id,
                                                      'category_name': video_iterable.video.category.category_name},
                                         'subcategory': {'id': video_iterable.video.subcategory.id,
                                                         'subcategory_name': video_iterable.video.subcategory.subcategory_name},
                                         'practice': practice_list,
                                         'dg_practice': dg_practice_list,
                                         'tags': tags,
                                         'producton_date': video_iterable.video.production_date,
                                         'youtube': video_iterable.video.youtubeid,
                                         'updation_date': video_iterable.video.approval_date,
                                         'version': 2,
                                         'video_type': video_iterable.video.video_type
                                         })

                    return JsonResponse({'data': data_list})
            except Exception:
                return HttpResponse("You are not authorized.Wrong Key", status=401)
        else:
            return HttpResponse("You are not authorized", status=401)

