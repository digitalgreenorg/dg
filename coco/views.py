# python imports
import dg.settings
import json
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
from geographies.models import Village,District
from programs.models import Partner
from videos.models import Video,Language,Category,Practice,SubCategory
from activities.models import Screening
from activities.models import PersonAdoptPractice
from coco.prepare_data import *


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


def ap_video(request):
    video_list = APVideo.objects.filter(video__partner_id=50)
    data_list = []
    practice_list = []
    dg_practice_list = []
    tags = [{'id': '', 'tag_name': ''}]
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

        data_list.append({'id': video_iterable.video.id,
                         'video_title': video_iterable.video.title,
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

    return JsonResponse({'data': data_list}, safe=False)


