from django.shortcuts import render_to_response
from django.template import RequestContext

from videokheti.models import ActionType, Crop, Method, Video, TimeYear


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
                           'link': ''.join(['/videokheti/video/?crop=', crop_id, '&time=', str(time_id), '&video=', str(obj.id)])
                       }
                list_dict.append(dic_obj)
            context = {
                      'crop': list_dict,
                      'video': 1,
                      'title': 'Choose the Video',
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
                           'link': ''.join(['/videokheti/video/?crop=', crop_id, '&time=', str(time_id), '&action=', action_id, '&video=', str(obj.id)])
                       }
                list_dict.append(dic_obj)
            context = {
                      'crop': list_dict,
                      'video': 1,
                      'title': 'Choose the Video',
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
                        'link': ''.join(['/videokheti/video/?crop=', crop_id, '&time=', str(time_id), '&action=', action_id, '&method=', method_id, '&video=', str(obj.id)])
                       }
            list_dict.append(dic_obj)
        context = {
                   'crop': list_dict,
                    'video': 1,
                    'title': 'Choose the Video',
                    'breadcrumb': breadcrumb_list,
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))


def play_video(request):
    crop_id = request.GET.get('crop', None)
    time_id = request.GET.get('time', None)
    action_id = request.GET.get('action', None)
    method_id = request.GET.get('method', None)
    video_id = request.GET.get('video', None)
    breadcrumb_list = []
    if(crop_id):
        crop = Crop.objects.get(id=crop_id)
        breadcrumb_obj = {'image': crop.image_file,
                           'link': '/videokheti'
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(time_id):
        time = TimeYear.objects.get(id=time_id)
        breadcrumb_obj = {'image': time.image_file,
                           'link': ''.join(['/videokheti/kheti/?crop=', crop_id, '&level=1'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(action_id):
        action = ActionType.objects.get(id=action_id)
        breadcrumb_obj = {'image': action.image_file,
                           'link': ''.join(['/videokheti/kheti/?crop=', crop_id, '&time=', str(time_id), '&level=2'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    if(method_id):
        method = Method.objects.get(id=method_id)
        breadcrumb_obj = {'image': method.image_file,
                           'link': ''.join(['/videokheti/video/?crop=', crop_id, '&time=', str(time_id), '&action=', str(action_id), '&level=3'])
                         }
        breadcrumb_list.append(breadcrumb_obj)
    video = Video.objects.get(id=video_id)
    context = {
                'title': video.coco_video.title,
                'youtube': video.coco_video.youtubeid,
                'breadcrumb': breadcrumb_list,
              }
    return render_to_response('video_play.html', context, context_instance=RequestContext(request))