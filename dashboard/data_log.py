from dashboard.models import User
from datetime import datetime
from django.db.models import get_model
import json
from django.http import HttpResponse

def save_log(sender, **kwargs ):
    instance = kwargs["instance"]
    action  = kwargs["created"]
    sender = sender.__name__    # get the name of the table which sent the request
    user = User.objects.get(id = instance.user_modified_id) if instance.user_modified_id else User.objects.get(id = instance.user_created_id)
    try:
        ServerLog = get_model('dashboard','ServerLog')
        log = ServerLog(village = instance.get_village(), user = user, action = action, entry_table = sender, model_id = instance.id, partner = instance.get_partner())
        log.save()
    except Exception as ex:
        print ex
    
def delete_log(sender, **kwargs ):
    instance = kwargs["instance"]
    sender = sender.__name__    # get the name of the table which sent the request
    user = None
    if instance.user_created_id:
        if instance.user_modified_id:
            user = User.objects.get(id = instance.user_modified_id) 
        else:
            user = User.objects.get(id = instance.user_created_id)
    try:
        ServerLog = get_model('dashboard','ServerLog')
        log = ServerLog(village = instance.get_village(), user = user, action = -1, entry_table = sender, model_id = instance.id, partner = instance.get_partner())
        log.save()
    except Exception as ex:
        pass

def send_updated_log(request):
    timestamp = request.GET['timestamp']
    user = User.objects.get(id = request.GET['user'])
    CocoUser = get_model('dashboard','CocoUser')
    CocoUserVillages = get_model('dashboard','CocoUser_villages')
    ServerLog = get_model('dashboard','ServerLog')
    coco_user = CocoUser.objects.get(user_id=user)
    partner_id = coco_user.partner_id
    villages = CocoUserVillages.objects.filter(cocouser_id = coco_user.id).values_list('village_id', flat = True)
    if timestamp:  
        rows = ServerLog.objects.filter(timestamp__gte = timestamp, village__in = villages, partner = partner_id )
    else:
        rows = ServerLog.objects.filter(village__in = villages, partner = partner_id )
    if rows:
        from django.core import serializers
        data = serializers.serialize('json', rows, fields=('action','entry_table','model_id'))
        return HttpResponse(data, mimetype="application/json")
    else:
        return HttpResponse("0")
    
    
    