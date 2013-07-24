import json
from datetime import datetime
from django.core import serializers
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.http import HttpResponse
from models import User

class TimestampException(Exception):
    pass

def save_log(sender, **kwargs ):
    pass
#    instance = kwargs["instance"]
#    action  = kwargs["created"]
#    sender = sender.__name__    # get the name of the table which sent the request
#    model_dict = model_to_dict(instance)
#    previous_time_stamp = get_latest_timestamp()
#    try:
#        user = User.objects.get(id = instance.user_modified_id) if instance.user_modified_id else User.objects.get(id = instance.user_created_id)
#    except Exception, ex:
#        user = None
#    try:
#        instance.get_village()
#    except Exception as e:
#        print type(e), e
#    ServerLog = get_model('dashboard','ServerLog')
#    log = ServerLog(village = instance.get_village(), user = user, action = action, entry_table = sender, 
#                    model_id = instance.id, partner = instance.get_partner())
#    log.save()
#    ###Raise an exception if timestamp of latest entry is less than the previously saved data timestamp
#    if previous_time_stamp > log.timestamp:
#        raise TimestampException('timestamp error: Latest entry data time created is less than previous data timecreated')
#    
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
    timestamp = request.GET.get('timestamp', None)
    if not timestamp:
        #for testing purpose
        timestamp = '2012-03-10 12:06:04'
    CocoUser = get_model('dashboard','CocoUser')
    CocoUserVillages = get_model('dashboard','CocoUser_villages')
    ServerLog = get_model('dashboard','ServerLog')
    Village = get_model('dashboard', 'village')
    if request.user.id == 1:
        #admin account
        partner_id = None
        villages = Village.objects.all().values_list('id', flat=True)
    else:
        coco_user = CocoUser.objects.get(user_id=request.user.id)
        partner_id = coco_user.partner_id
        villages = CocoUserVillages.objects.filter(cocouser_id = coco_user.id).values_list('village_id', flat = True)
    if timestamp:
        if partner_id:  
            rows = ServerLog.objects.filter(timestamp__gte = timestamp, village__in = villages, partner = partner_id )
        else:
            rows = ServerLog.objects.filter(timestamp__gte = timestamp, village__in = villages)
    ####Not necessary..need to remove it..####
    else:
        if partner_id:
            rows = ServerLog.objects.filter(village__in = villages, partner = partner_id )
        else:
            rows = ServerLog.objects.filter(village__in = villages)
            
    print len(rows)
    if rows:
        from django.core import serializers
        data = serializers.serialize('json', rows, fields=('action','entry_table','model_id', 'timestamp'))
        return HttpResponse(data, mimetype="application/json")
    else:
        return HttpResponse("0")

def get_latest_timestamp():
    from models import ServerLog
    timestamp = ServerLog.objects.latest('id')
    return timestamp.timestamp
