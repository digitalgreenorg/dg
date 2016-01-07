import json

from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from tastypie.models import ApiKey

class TimestampException(Exception):
    pass
class UserDoesNotExist(Exception):
    pass

def save_log(sender, **kwargs ):
    instance = kwargs["instance"]
    action  = kwargs["created"]
    sender = sender.__name__    # get the name of the table which sent the request
    model_dict = model_to_dict(instance)
    previous_time_stamp = get_latest_timestamp()
    try:
        user = User.objects.get(id = instance.user_modified_id) if instance.user_modified_id else User.objects.get(id = instance.user_created_id)
    except Exception, ex:
        user = None

    model_id = instance.id
    if sender == "Village":
        village_id = instance.id
        user = None
    elif sender == "Crop":
        village_id = None
        user = None
    else:
        village_id = instance.village.id # farmer add
    Log = get_model('loop', 'Log')
    log = Log(village=village_id, user=user, action=action, entry_table=sender,
                    model_id=model_id)
    log.save()
    ###Raise an exception if timestamp of latest entry is less than the previously saved data timestamp
    if previous_time_stamp:
        if previous_time_stamp.timestamp > log.timestamp:
            raise TimestampException('timestamp error: Latest entry data time created is less than previous data timecreated')

def delete_log(sender, **kwargs ):
    instance = kwargs["instance"]
    sender = sender.__name__    # get the name of the table which sent the request
    try:
        user = User.objects.get(id = instance.user_modified_id) if instance.user_modified_id else User.objects.get(id = instance.user_created_id)
    except Exception, ex:
        user = None
    if sender == "Village":
        village_id = instance.id
        user = None
    elif sender == "Crop":
        village_id = None
        user = None
    else:
        village_id = instance.village.id # farmer add
    Log = get_model('loop', 'Log')
    try:
        log = Log(village = village_id, user = user, action = -1, entry_table = sender, model_id = instance.id)
        log.save()
    except Exception as ex:
        pass

def get_latest_timestamp():
    Log = get_model('loop', 'Log')
    try:
        timestamp = Log.objects.latest('id')
    except Exception as e:
        timestamp = None
    return timestamp

@csrf_exempt
def send_updated_log(request):
    if request.method == 'POST':
        apikey = request.POST['apikey']
        timestamp = request.POST['timestamp']
        if timestamp:
            try:
                apikey_object = ApiKey.objects.get(key = apikey)
                user = apikey_object.user
            except Exception, e:
                return HttpResponse("-1", status=401)
            LoopUser = get_model('loop','LoopUser')
            try:
                loop_user = LoopUser.objects.get(user_id=user.id)
            except Exception as e:
                raise UserDoesNotExist('User with id: '+str(user.id) + 'does not exist')
            villages = loop_user.get_villages()
            Log = get_model('loop', 'Log')
            rows = Log.objects.filter(timestamp__gte = timestamp, entry_table__in = ['Crop'])
            rows = rows | Log.objects.filter(timestamp__gte = timestamp, village__in = villages, entry_table__in = ['Farmer'])
            rows = rows | Log.objects.filter(timestamp__gte = timestamp, user = user, entry_table__in = ['CombinedTransaction'])
            if rows:
                data = serializers.serialize('json', rows, fields=('action','entry_table','model_id', 'timestamp'))
                return HttpResponse(data, mimetype="application/json")
    return HttpResponse("0")
