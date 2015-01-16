from django.shortcuts import render_to_response
from django.template import RequestContext

from videokheti.models import ActionType, Crop, TimeYear


def home(request):
    crop_objects = Crop.objects.all()
    list_dict = []
    for obj in crop_objects:
        dic_obj = {'name': obj.name.replace('_', ' '),
                   'image': obj.image_file,
                   'audio': obj.sound_file,
                   'id': obj.id,
                   'link': ''.join(['kheti/?crop=', str(obj.id), '&level=1'])
                   }
        list_dict.append(dic_obj)
        context = {
                  'crop': list_dict,
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
        context = {
                  'crop': list_dict,
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))
    if level == '2':
        crop_id = request.GET.get('crop', None)
        time_id = request.GET.get('time', None)
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
                  }
        return render_to_response('videokheti.html', context, context_instance=RequestContext(request))