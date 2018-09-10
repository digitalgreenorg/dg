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
from django.db.models import Q, get_model, F, Value, CharField
from django.db.models.functions import Concat
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message
# app imports
from forms import DataUploadForm, GeographyMappingForm
from models import CocoUser
from videos.models import APVideo
from coco.models import FullDownloadStats, CocoUser
from people.models import Person,Animator,AnimatorAssignedVillage
from people.models import PersonGroup
from geographies.models import Village,District, Block, AP_District, AP_Mandal, AP_Village, AP_COCO_Mapping
from programs.models import Partner
from videos.models import Video,Language,Category,Practice,SubCategory
from activities.models import Screening
from activities.models import PersonAdoptPractice
from coco.prepare_data import *
from django.views.generic import View
from tastypie.models import ApiKey
from django.db import IntegrityError
import traceback


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
def ap_geography_mapping(request):
    if request.method == 'GET':
        form_data = GeographyMappingForm()
    else:
        form_data = GeographyMappingForm(request.POST)
        if form_data.is_valid():
            #import pdb;pdb.set_trace()
            cd = form_data.cleaned_data
            geo_type = cd.get('geographytype')
            apgeo = cd.get('apgeo')
            cocogeo = cd.get('cocogeo')
            # obj = CocoUser.objects.filter(villages__in=[apgeo])
            # print geo_type, apgeo, cocogeo, request.user.id
            try:
                mapping_obj, created = AP_COCO_Mapping.objects.get_or_create(geo_type=geo_type, ap_geo_id=apgeo, coco_geo_id=cocogeo)
                if created:
                    mapping_obj.user_created_id=request.user.id
                    mapping_obj.time_created=datetime.now()
                    mapping_obj.save()
                else:
                    mapping_obj.user_modified_id=request.user.id
                    mapping_obj.time_modified=datetime.now()
                    mapping_obj.save()

            except Exception as e:
                print e
    context = {'form': form_data}
    template = "coco/geo_mapping.html"
    return render(request, template, context)


class GetGeography(View):

    def get(self, request, *args, **kwargs):
        selected_geography = kwargs.get('selected_geography')
        if selected_geography == 'District':
            ap_districts = AP_District.objects.values_list('district_id',flat=True).distinct()
            results_coco = list(District.objects.filter(state_id=6).exclude(id__in=ap_districts).annotate(value=F('id'), text=Concat(F('district_name'), Value('( '), F('id'), Value(' )'), output_field=CharField())).values('id','value','text'))
            results_ap = list(District.objects.filter(id__in=ap_districts).annotate(value=F('id'), text=Concat(F('district_name'), Value('( '), F('id'), Value(' )'), output_field=CharField())).values('id','value','text'))

        elif selected_geography == 'Block':
            ap_blocks = AP_Mandal.objects.values_list('block_id',flat=True).distinct()
            results_coco = list(Block.objects.filter(district__state_id=6).exclude(id__in=ap_blocks).annotate(value=F('id'), text=Concat(F('block_name'), Value('( '), F('district__district_name'), Value(' )'), Value('( '), F('id'), Value(' )'), output_field=CharField())).values('id','value','text'))
            results_ap = list(Block.objects.filter(id__in=ap_blocks).annotate(value=F('id'), text=Concat(F('block_name'), Value('( '), F('district__district_name'), Value(' )'), Value('( '), F('id'), Value(' )'), output_field=CharField())).values('id','value','text'))

        else:
            # import pdb;pdb.set_trace()
            ap_villages = AP_Village.objects.values_list('village_id',flat=True).distinct()
            results_coco = list(Village.objects.filter(block__district__state_id=6).exclude(id__in=ap_villages).annotate(value=F('id'), text=Concat(F('village_name'), Value('( '), F('block__block_name'), Value(' )'), Value('( '), F('block__district__district_name'), Value(' )'), Value('( '), F('id'), Value(' )'), output_field=CharField())).values('id','text','value'))
            results_ap = list(Village.objects.filter(id__in=ap_villages).annotate(value=F('id'), text=Concat(F('village_name'), Value('( '), F('block__block_name'), Value(' )'), Value('( '), F('block__district__district_name'), Value(' )'), Value('( '), F('id'), Value(' )') ,output_field=CharField())).values('id','text','value'))

        results_list = [results_ap, results_coco]
        data = {'results': results_list}
        #import pdb;pdb.set_trace()
        return JsonResponse(data)

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
                #Checking file header format    
                if header == columns:
                    lines = file_data.split('\n')[1:]
                    filter_lines = [x.strip() for x in lines if x.strip()] 
                    for row in filter_lines:
                        try:
                            row = row.split(',')
                            block_obj, created = Block.objects.get_or_create(block_name=row[2].strip(),\
                                                                            district_id=int(row[1]), \
                                                                            defaults={'block_name': row[2].strip(), \
                                                                                     'district_id':int(row[1].strip())})
                            if block_obj or created:
                                village_obj, created = \
                                Village.objects.get_or_create(village_name=row[3].strip(),block_id=block_obj.id,\
                                                                defaults={'village_name':row[3].strip(), \
                                                                        'block_id':block_obj.id})
                                if village_obj or created:
                                    person_group, created = \
                                    PersonGroup.objects.get_or_create(group_name=row[4].strip(),\
                                                                    village_id=village_obj.id, \
                                                                    partner_id=int(row[0]),\
                                                                    defaults={'group_name': row[4].strip(),\
                                                                    'village_id':village_obj.id, \
                                                                    'partner_id':int(row[0].strip())},)
                                    if person_group or created:
                                        if row[8] != '' and row[8] != '\r':
                                            row[8] = row[8].strip('\r')
                                            person_obj, created = \
                                            Person.objects.get_or_create(person_name__iexact=row[5].strip(),\
                                             village_id=village_obj.id,group_id=person_group.id, \
                                             partner_id=int(row[0].strip()), defaults={'person_name':row[5].strip(), \
                                             'gender':row[6].strip(),'village_id':village_obj.id,'group_id':person_group.id, \
                                             'partner_id':int(row[0].strip()), 'age':int(row[8].strip()), 'phone_no': row[7].strip()})
                                            person_obj.gender = row[6].strip()
                                            person_obj.phone_no = row[7].strip()
                                            person_obj.age = int(row[8].strip())
                                            person_obj.save()
                                        else:
                                            row[8] = row[8].strip('\r')
                                            person_obj, created = \
                                            Person.objects.get_or_create(person_name__iexact=row[5].strip(),\
                                             village_id=village_obj.id,group_id=person_group.id, \
                                             partner_id=int(row[0].strip()), defaults={'person_name':row[5].strip(), \
                                             'gender':row[6].strip(),'village_id':village_obj.id,'group_id':person_group.id, \
                                             'partner_id':int(row[0]), 'phone_no': row[7].strip()})
                                            person_obj.gender = row[6].strip()
                                            person_obj.phone_no = row[7].strip()
                                            person_obj.save()
                        #Handle Duplicate KeyError
                        except IntegrityError as e:
                            print e
                            pass
                    add_message(request, 25, 'Your data has been successfully uploaded. Please login in COCO to view this data.')
                else:
                    add_message(request,40, "File Header is not in correct format")
            except Exception as e:
                print e
                add_message(request, 40, 'Unable to upload data, please contact system@digitalgreen.org for any issues')
            return redirect(".")
        else:
            add_message(request, 40, "Please correct the errors below.")
    else:
        form_data = DataUploadForm()
    context = {'form': form_data}
    template = "coco/uploaddata.html"
    return render(request, template, context)


@login_required
def getFileHeader(request):
    if request.method == 'GET':
        columns = 'Partner ID,District ID,Block Name,Village Name,Person Group,Member Name,Gender,Phone Number,Age'
        output = StringIO.StringIO()
        try:
            output.write(columns)
            response = HttpResponse(output.getvalue().encode('utf-8'), content_type='text/csv', charset='utf-8')
            response['Content-Disposition'] = 'attachment; filename=header_format.csv'
            return response
        except Exception as e:
            add_message(request, 40, 'Unable to download header format, contact system@digitalgreen.org for further information')




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
                    errors_videos = []
                    for video_iterable in video_list:
                        try:
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
                        except Exception as e:
                            pass

                    return JsonResponse({'data': data_list})
            except Exception:
                return HttpResponse("You are not authorized.Wrong Key", status=401)
        else:
            return HttpResponse("You are not authorized", status=401)

