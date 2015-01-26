import json

from django.contrib.auth.decorators import login_required
import django.core.serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from social_website.models import Comment, Partner, Video as social_video
from videokheti.models import ActionType, Crop, Method, Video, VideoComment, TimeYear


def home(request):
    crop_objects = Crop.objects.all()
    list_dict = []
    for obj in crop_objects:
        dic_obj = {'name': obj.name.replace('_', ' '),
                   'image': obj.image_file,
                   'audio': obj.sound_file,
                   'id': obj.id,
                   'link': ''.join(['kheti/?crop=', str(obj.id), '&level=1']),
                   }
        list_dict.append(dic_obj)
        context = {
                  'crop': list_dict,
                  'title': 'Choose the Crop',
                  'title_audio': 'you-can-name-crop-prompt-graphics.wav'
                  }
    return render_to_response('videokheti.html', context, context_instance=RequestContext(request))


def level(request):
    level = request.GET.get('level', None)
    if level == '1':
        crop_id = request.GET.get('crop', None)
        time_objects = TimeYear.objects.all()
        list_dict = []
        for obj in time_objects:
            dic_obj = {'name': obj.name.replace('_', ' '),
                       'image': obj.image_file,
                       'audio': obj.sound_file,
                       'id': obj.id,
                       'link': ''.join(['?crop=', crop_id, '&time=', str(obj.id), '&level=2'])
                   }
            list_dict.append(dic_obj)
        breadcrumb_list = []
        crop = Crop.objects.get(id=crop_id)
        breadcrumb_obj = {'image': crop.image_file,
                          'link': '/videokheti'
                          }
        breadcrumb_list.append(breadcrumb_obj)

        context = {
                  'crop': list_dict,
                  'title': 'Choose the Time of Year',
                  'title_audio': 'you-can-select-an-option-prompt-graphics.wav',
                  'breadcrumb': breadcrumb_list,
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
    if level == '2':
        crop_id = request.GET.get('crop', None)
        time_id = request.GET.get('time', None)
        breadcrumb_list = []
        crop = Crop.objects.get(id=crop_id)
        time = TimeYear.objects.get(id=time_id)
        breadcrumb_obj = {'image': crop.image_file,
                          'link': '/videokheti'
                          }
        breadcrumb_list.append(breadcrumb_obj)
        breadcrumb_obj = {'image': time.image_file,
                          'link': ''.join(['?crop=', crop_id, '&level=1'])
                          }
        breadcrumb_list.append(breadcrumb_obj)
        if time_id == '2':
            # Success stories
            video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id)
            list_dict = []
            for obj in video_objects:
                dic_obj = {'name': obj.coco_video.title.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['/videokheti/video/?video=', str(obj.id)])
                       }
                list_dict.append(dic_obj)
            context = {
                      'crop': list_dict,
                      'video': 1,
                      'title': 'Choose the Video',
                      'title_audio': 'you-can-select-an-option-prompt-graphics.wav',
                      'breadcrumb': breadcrumb_list,
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
        else:
            action_objects = ActionType.objects.filter(time_year_id=time_id)
            list_dict = []
            for obj in action_objects:
                dic_obj = {'name': obj.name.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&action=', str(obj.id), '&level=3'])
                       }
                list_dict.append(dic_obj)
            context = {
                      'crop': list_dict,
                      'title': 'Choose the Action',
                      'title_audio': 'you-can-select-an-option-prompt-graphics.wav',
                      'breadcrumb': breadcrumb_list,
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
                          'link': '/videokheti'
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
            method_objects = Method.objects.all()[:3]
            list_dict = []
            for obj in method_objects:
                dic_obj = {'name': obj.name.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&action=', action_id, '&method=', str(obj.id), '&level=4'])
                           }
                list_dict.append(dic_obj)
            context = {
                        'crop': list_dict,
                        'title': 'Choose the Method',
                        'title_audio': 'you-can-select-an-option-prompt-graphics.wav',
                        'breadcrumb': breadcrumb_list,
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
        elif action_object.name == 'interculture':
            method_objects = Method.objects.all()[3:]
            list_dict = []
            for obj in method_objects:
                dic_obj = {'name': obj.name.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['?crop=', crop_id, '&time=', str(time_id), '&action=', action_id, '&method=', str(obj.id), '&level=4'])
                           }
                list_dict.append(dic_obj)
            context = {
                        'crop': list_dict,
                        'title': 'Choose the Method',
                        'title_audio': 'you-can-select-an-option-prompt-graphics.wav',
                        'breadcrumb': breadcrumb_list,
                      }
            return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
        else:
            video_objects = Video.objects.filter(crop_id=crop_id, time_year_id=time_id, action_type_id=action_id)
            list_dict = []
            for obj in video_objects:
                dic_obj = {'name': obj.coco_video.title.replace('_', ' '),
                           'image': obj.image_file,
                           'audio': obj.sound_file,
                           'id': obj.id,
                           'link': ''.join(['/videokheti/video/?video=', str(obj.id)])
                       }
                list_dict.append(dic_obj)
            context = {
                      'crop': list_dict,
                      'video': 1,
                      'title': 'Choose the Video',
                      'title_audio': 'you-can-select-an-option-prompt-graphics.wav',
                      'breadcrumb': breadcrumb_list,
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
                          'link': '/videokheti'
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
            dic_obj = {'name': obj.coco_video.title.replace('_', ' '),
                        'image': obj.image_file,
                        'audio': obj.sound_file,
                        'id': obj.id,
                        'link': ''.join(['/videokheti/video/?video=', str(obj.id)])
                       }
            list_dict.append(dic_obj)
        context = {
                   'crop': list_dict,
                    'video': 1,
                    'title': 'Choose the Video',
                    'title_audio': 'you-can-select-an-option-prompt-graphics.wav',
                    'breadcrumb': breadcrumb_list,
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))


def play_video(request):
    video_id = request.GET.get('video', None)
    video = Video.objects.get(id=video_id)
    crop = video.crop if video.crop is not None else None
    time = video.time_year if video.time_year is not None else None
    action = video.action_type if video.action_type is not None else None
    method = video.method if video.method is not None else None
    breadcrumb_list = []
    if(crop):
        breadcrumb_obj = {'image': crop.image_file,
                           'link': '/videokheti'
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(time):
        breadcrumb_obj = {'image': time.image_file,
                           'link': ''.join(['/videokheti/kheti/?crop=', str(crop.id), '&level=1'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(action):
        breadcrumb_obj = {'image': action.image_file,
                           'link': ''.join(['/videokheti/kheti/?crop=', str(crop.id), '&time=', str(time.id), '&level=2'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    else:
        breadcrumb_obj = {'image': video.image_file,
                          'video': 1,
                           'link': ''.join(['/videokheti/kheti/?crop=', str(crop.id), '&time=', str(time.id), '&level=2'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(method):
        breadcrumb_obj = {'image': method.image_file,
                           'link': ''.join(['/videokheti/kheti/?crop=', str(crop.id), '&time=', str(time.id), '&action=', str(action.id), '&level=3'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    elif(action):
        breadcrumb_obj = {'image': video.image_file,
                          'video': 1,
                           'link': ''.join(['/videokheti/kheti/?crop=', str(crop.id), '&time=', str(time.id), '&action=', str(action.id), '&level=3'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(crop and time and action and method):
        breadcrumb_obj = {'image': video.image_file,
                          'video': 1,
                           'link': ''.join(['/videokheti/kheti/?crop=', str(crop.id), '&time=', str(time.id), '&action=', str(action.id), '&method=', str(method.id),'&level=4'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    partner = Partner.objects.get(coco_id=video.coco_video.partner_id)
    svideo = social_video.objects.get(uid=video.website_id)
    comments = Comment.objects.filter(video_id=svideo.uid)
    video_carousel = ['brinjal.jpg', 'chilli.jpg', 'coriander.jpg', 'garlic.jpg']
    context = {
                'title': video.coco_video.title,
                'partner': video.coco_video.partner.partner_name,
                'partner_image': partner.logoURL,
                'youtube': video.coco_video.youtubeid,
                'breadcrumb': breadcrumb_list,
                'adoptions': svideo.adoptions,
                'views': svideo.offlineViews,
                'language': svideo.language,
                'state': svideo.state,
                'date_pro': svideo.date,
                'facillitator': video.coco_video.facilitator.name,
                'cameraoperator': video.coco_video.cameraoperator.name,
                'comments': comments,
                'id': video_id,
                'video_carousel': video_carousel,
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
                   'imageURL': obj.person.thumbnailURL,
                   'personName': obj.person.name,
                   }
        list_comments.append(obj_dic)
    resp = json.dumps(list_comments)
    return HttpResponse(resp)