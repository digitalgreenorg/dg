from os import listdir

import json

from django.contrib.auth.decorators import login_required
import django.core.serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from dg.settings import MEDIA_ROOT
from social_website.models import Comment, Partner, Video as social_video
from videokheti.models import ActionType, Crop, Method, Video, VideoComment, TimeYear, Title


def home(request):
    if 'videokheti_cookie' in request.COOKIES:
        video_objects = Video.objects.all()
        if "videokheti_language" in request.COOKIES:
            language = request.COOKIES["videokheti_language"]
        else:
            language = "Hindi"
        crop_list = video_objects.values_list('crop', flat=True).distinct()
        crop_objects = Crop.objects.filter(id__in=crop_list)
        list_dict = []
        for obj in crop_objects:
            dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.name.replace('_', ' '),
                        'image': obj.image_file,
                        'audio': obj.sound_file,
                        'id': obj.id,
                        'link': ''.join(['opt/?crop=', str(obj.id), '&level=1']),
                      }
            list_dict.append(dic_obj)
        title = Title.objects.get(table='Crop')
        context = {
                    'language': language,
                    'crop': list_dict,
                    'title': title.hindi_text if language == "Hindi" else title.title,
                    'title_audio': 'you-can-name-crop-prompt-graphics.mp3'
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
    else:
        language = "Hindi"
        title = Title.objects.get(table='Home')
        context = {
                    'cookies': 1,
                    'language': language,
                    'title': title.hindi_text if language == "Hindi" else title.title,
                   }
        response = render_to_response('videokheti_home.html', context, context_instance=RequestContext(request))
        response.set_cookie("videokheti_cookie", 1)
        response.set_cookie("videokheti_language", language)
        return response


def home_static(request):
    if "videokheti_language" in request.COOKIES:
        language = request.COOKIES["videokheti_language"]
    else:
        language = "Hindi"
    title = Title.objects.get(table='Home')
    context = {
                'language': language,
                'title': title.hindi_text if language == "Hindi" else title.title,
              }
    response = render_to_response('videokheti_home.html', context, context_instance=RequestContext(request))
    return response


def level(request):
    if "videokheti_language" in request.COOKIES:
        language = request.COOKIES["videokheti_language"]
    else:
        language = "Hindi"
    level = request.GET.get('level', None)
    if level == '1':
        crop_id = request.GET.get('crop', None)
        video_objects = Video.objects.filter(crop_id=crop_id)
        time_list = video_objects.values_list('time_year', flat=True).distinct()
        time_objects = TimeYear.objects.filter(id__in=time_list)
        list_dict = []
        for obj in time_objects:
            dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.name.replace('_', ' '),
                       'image': obj.image_file,
                       'audio': obj.sound_file,
                       'id': obj.id,
                       'link': ''.join(['?crop=', crop_id, '&time=', str(obj.id), '&level=2'])
                   }
            list_dict.append(dic_obj)
        breadcrumb_list = []
        crop = Crop.objects.get(id=crop_id)
        breadcrumb_obj = {'image': crop.image_file,
                          'link': '/videos/videokheti/'
                          }
        breadcrumb_list.append(breadcrumb_obj)
        title = Title.objects.get(table='TimeYear')
        context = {
                  'crop': list_dict,
                  'title': title.hindi_text if language == "Hindi" else title.title,
                  'title_audio': 'you-can-select-an-option-prompt-graphics.mp3',
                  'breadcrumb': breadcrumb_list,
                  'language': language,
                  'videos': video_objects
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
    if level == '2':
        crop_id = request.GET.get('crop', None)
        time_id = request.GET.get('time', None)
        breadcrumb_list = []
        crop = Crop.objects.get(id=crop_id)
        time = TimeYear.objects.get(id=time_id)
        breadcrumb_obj = {'image': crop.image_file,
                          'link': '/videos/videokheti/'
                          }
        breadcrumb_list.append(breadcrumb_obj)
        breadcrumb_obj = {'image': time.image_file,
                          'link': ''.join(['?crop=', crop_id, '&level=1'])
                          }
        breadcrumb_list.append(breadcrumb_obj)
        if time_id == '4':
            # Success stories
            video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id)
            list_dict = []
            for obj in video_objects:
                dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.coco_video.title.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['/videos/videokheti/video/?video=', str(obj.id)])
                       }
                list_dict.append(dic_obj)
            title = Title.objects.get(table='Video')
            error_message = Title.objects.get(table='Error')
            context = {
                      'crop': list_dict,
                      'video': 1,
                      'title': title.hindi_text if language == "Hindi" else title.title,
                      'title_audio': 'you-can-select-an-option-prompt-graphics.mp3',
                      'breadcrumb': breadcrumb_list,
                      'language': language,
                      'error_message': error_message.hindi_text if language == "Hindi" else error_message.title
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
        else:
            video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id)
            action_list = video_objects.values_list('action_type', flat=True).distinct()
            action_objects = ActionType.objects.filter(time_year_id=time_id, id__in=action_list)
            list_dict = []
            for obj in action_objects:
                dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.name.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&action=', str(obj.id), '&level=3'])
                       }
                list_dict.append(dic_obj)
            title = Title.objects.get(table='Action')
            context = {
                      'crop': list_dict,
                      'title': title.hindi_text if language == "Hindi" else title.title,
                      'title_audio': 'you-can-select-an-option-prompt-graphics.mp3',
                      'breadcrumb': breadcrumb_list,
                      'language': language,
                      'videos': video_objects,
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
    if level == '3':
        crop_id = request.GET.get('crop', None)
        time_id = request.GET.get('time', None)
        action_id = request.GET.get('action', None)

        breadcrumb_list = []
        crop = Crop.objects.get(id=crop_id)
        time = TimeYear.objects.get(id=time_id)
        action = ActionType.objects.get(id=action_id)
        breadcrumb_obj = {'image': crop.image_file,
                          'link': '/videos/videokheti'
                          }
        breadcrumb_list.append(breadcrumb_obj)
        breadcrumb_obj = {'image': time.image_file,
                          'link': ''.join(['?crop=', crop_id, '&level=1'])
                          }
        breadcrumb_list.append(breadcrumb_obj)
        breadcrumb_obj = {'image': action.image_file,
                          'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&level=2'])
                          }
        breadcrumb_list.append(breadcrumb_obj)

        action_object = ActionType.objects.get(id=action_id)
        if action_object.name in ('seed_treatment', 'nutrient_management', 'disease_and_pest_control'):
            video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id, action_type_id=action_id)
            method_list = video_objects.values_list('method', flat=True).distinct()
            method_objects = Method.objects.filter(id__in=method_list)
            list_dict = []
            for obj in method_objects:
                dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.name.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&action=', action_id, '&method=', str(obj.id), '&level=4'])
                           }
                list_dict.append(dic_obj)
            title = Title.objects.get(table='Method')
            context = {
                        'crop': list_dict,
                        'title': title.hindi_text if language == "Hindi" else title.title,
                        'title_audio': 'you-can-select-an-option-prompt-graphics.mp3',
                        'breadcrumb': breadcrumb_list,
                        'language': language,
                        'videos': video_objects,
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
        elif action_object.name == 'interculture':
            video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id, action_type_id=action_id)
            method_list = video_objects.values_list('method', flat=True).distinct()
            method_objects = Method.objects.filter(id__in=method_list)
            list_dict = []
            for obj in method_objects:
                dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.name.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&action=', action_id, '&method=', str(obj.id), '&level=4'])
                           }
                list_dict.append(dic_obj)
            title = Title.objects.get(table='Method')
            context = {
                        'crop': list_dict,
                        'title': title.hindi_text if language == "Hindi" else title.title,
                        'title_audio': 'you-can-select-an-option-prompt-graphics.mp3',
                        'breadcrumb': breadcrumb_list,
                        'language': language,
                        'videos': video_objects,
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
        else:
            video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id, action_type_id=action_id)
            list_dict = []
            for obj in video_objects:
                dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.coco_video.title.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['/videos/videokheti/video/?video=', str(obj.id)])
                       }
                list_dict.append(dic_obj)
            title = Title.objects.get(table='Video')
            error_message = Title.objects.get(table='Error')
            context = {
                      'crop': list_dict,
                      'video': 1,
                      'title': title.hindi_text if language == "Hindi" else title.title,
                      'title_audio': 'you-can-select-an-option-prompt-graphics.mp3',
                      'breadcrumb': breadcrumb_list,
                      'language': language,
                      'error_message': error_message.hindi_text if language == "Hindi" else error_message.title
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
    if level == '4':
        crop_id = request.GET.get('crop', None)
        time_id = request.GET.get('time', None)
        action_id = request.GET.get('action', None)
        method_id = request.GET.get('method', None)
        breadcrumb_list = []
        crop = Crop.objects.get(id=crop_id)
        time = TimeYear.objects.get(id=time_id)
        action = ActionType.objects.get(id=action_id)
        method = Method.objects.get(id=method_id)
        breadcrumb_obj = {'image': crop.image_file,
                          'link': '/videos/videokheti/'
                          }
        breadcrumb_list.append(breadcrumb_obj)
        breadcrumb_obj = {'image': time.image_file,
                          'link': ''.join(['?crop=', crop_id, '&level=1'])
                          }
        breadcrumb_list.append(breadcrumb_obj)
        breadcrumb_obj = {'image': action.image_file,
                          'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&level=2'])
                          }
        breadcrumb_list.append(breadcrumb_obj)
        breadcrumb_obj = {'image': method.image_file,
                          'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&action=', str(action_id), '&level=3'])
                          }
        breadcrumb_list.append(breadcrumb_obj)
        video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id, action_type_id=action_id, method_id=method_id)
        list_dict = []
        for obj in video_objects:
            dic_obj = {'name': obj.hindi_text if language == "Hindi" else obj.coco_video.title.replace('_', ' '),
                       'image': obj.image_file,
                       'audio': obj.sound_file,
                       'id': obj.id,
                       'link': ''.join(['/videos/videokheti/video/?video=', str(obj.id)])
                       }
            list_dict.append(dic_obj)
        title = Title.objects.get(table='Video')
        error_message = Title.objects.get(table='Error')
        context = {
                   'crop': list_dict,
                   'video': 1,
                   'title': title.hindi_text if language == "Hindi" else title.title,
                   'title_audio': 'you-can-select-an-option-prompt-graphics.mp3',
                   'breadcrumb': breadcrumb_list,
                   'language': language,
                   'error_message': error_message.hindi_text if language == "Hindi" else error_message.title
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))


def play_video(request):
    if "videokheti_language" in request.COOKIES:
        language = request.COOKIES["videokheti_language"]
    else:
        language = "Hindi"
    video_id = request.GET.get('video', None)
    video = Video.objects.get(id=video_id)
    crop = video.crop if video.crop is not None else None
    time = video.time_year if video.time_year is not None else None
    action = video.action_type if video.action_type is not None else None
    method = video.method if video.method is not None else None
    breadcrumb_list = []
    if(crop):
        breadcrumb_obj = {'image': crop.image_file,
                           'link': '/videos/videokheti/'
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(time):
        breadcrumb_obj = {'image': time.image_file,
                           'link': ''.join(['/videos/videokheti/opt/?crop=', str(crop.id), '&level=1'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(action):
        breadcrumb_obj = {'image': action.image_file,
                           'link': ''.join(['/videos/videokheti/opt/?crop=', str(crop.id), '&time=', str(time.id), '&level=2'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    else:
        breadcrumb_obj = {'image': video.image_file,
                          'video': 1,
                           'link': ''.join(['/videos/videokheti/opt/?crop=', str(crop.id), '&time=', str(time.id), '&level=2'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(method):
        breadcrumb_obj = {'image': method.image_file,
                           'link': ''.join(['/videos/videokheti/opt/?crop=', str(crop.id), '&time=', str(time.id), '&action=', str(action.id), '&level=3'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    elif(action):
        breadcrumb_obj = {'image': video.image_file,
                          'video': 1,
                           'link': ''.join(['/videos/videokheti/opt/?crop=', str(crop.id), '&time=', str(time.id), '&action=', str(action.id), '&level=3'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(crop and time and action and method):
        breadcrumb_obj = {'image': video.image_file,
                          'video': 1,
                           'link': ''.join(['/videos/videokheti/opt/?crop=', str(crop.id), '&time=', str(time.id), '&action=', str(action.id), '&method=', str(method.id),'&level=4'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    partner = Partner.objects.get(coco_id=video.coco_video.partner_id)
    svideo = social_video.objects.get(uid=video.website_id)
    comments = Comment.objects.filter(video_id=svideo.uid)
    video_carousel = []
    for f in listdir(''.join([MEDIA_ROOT, '/img/', str(video.coco_video.id), '/'])):
        print f
        if f.split('.')[-1] == 'jpg':
            video_carousel.append(f)
    video_carousel.sort()
    context = {
                'title': video.hindi_text if language == "Hindi" else video.coco_video.title,
                'coco_id': video.coco_video.id,
                'partner': video.coco_video.partner.partner_name,
                'partner_image': partner.logoURL,
                'youtube': video.coco_video.youtubeid,
                'breadcrumb': breadcrumb_list,
                'adoptions': svideo.adoptions,
                'views': svideo.offlineViews,
                'language': svideo.language,
                'state': svideo.state,
                'date_pro': svideo.date,
                'comments': comments,
                'id': video_id,
                'video_carousel': video_carousel,
                'language': language,
              }
    return render_to_response('video_play.html', context, context_instance=RequestContext(request))


@login_required()
@csrf_exempt
def comment(request):
    #resp = json.dumps({"mapping_dropdown": practice_dictionary})
    video_id = request.POST.get('video', None)
    text = request.POST.get('comment', None)
    try:
        provider = request.user.social_auth.all()[0].provider
        if provider == 'google-oauth2':
            url = '%s?sz=75' % request.user.social_auth.all()[0].extra_data['picture']
        elif provider == 'facebook':
            url = 'https://graph.facebook.com/%s/picture?type=large' % request.user.social_auth.all()[0].uid
    except Exception as e:
        print e
        url = "/media/social_website/content/default.png"

    video = VideoComment(text=text, video_id=video_id, user=request.user, imageURL=url, personName=request.user.username)
    video.save()
    resp = django.core.serializers.serialize('json', [video])
    resp = resp.strip("[]")
    return HttpResponse(resp)


def get_comments(request):
    #resp = json.dumps({"mapping_dropdown": practice_dictionary})
    video_id = request.GET.get('video', None)
    video = Video.objects.get(id=video_id)
    comments_screenings = Comment.objects.filter(video_id=video.website_id, isOnline=False)
    comments_online = VideoComment.objects.filter(video_id=video.id).order_by('-id')
    list_comments = []
    for obj in comments_online:
        obj_dic = {'text': obj.text,
                   'imageURL': obj.imageURL,
                   'personName': obj.personName,
                   }
        list_comments.append(obj_dic)
    for obj in comments_screenings:
        obj_dic = {'text': obj.text,
                   'imageURL': obj.animator.thumbnailURL,
                   'personName': obj.animator.name,
                   }
        list_comments.append(obj_dic)
    resp = json.dumps(list_comments)
    return HttpResponse(resp)


def language(request):
    #resp = json.dumps({"mapping_dropdown": practice_dictionary})
    language = request.GET.get('language', None)
    if "videokheti_language" in request.COOKIES:
        if request.COOKIES["videokheti_language"] == language:
            return HttpResponse('0')
        else:
            response = HttpResponse('1')
            response.set_cookie("videokheti_language", language)
            return response
    else:
        response = HttpResponse('1')
        response.set_cookie("videokheti_language", language)
        return response
