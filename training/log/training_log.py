from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey
from django.apps import apps
import json
from django.core.serializers.json import DjangoJSONEncoder

def get_log_object(log_obj):
    if log_obj.entry_table == 'Partner':
        app = 'programs'
    elif log_obj.entry_table == 'People':
        app = 'people'
    elif log_obj.entry_table == 'District':
        app = 'geographies'
    else:
        app = 'training'
    model = apps.get_model(app, log_obj.entry_table)
    try:
        obj = model.objects.get(id=log_obj.model_id)
        data = {'log' : model_to_dict(log_obj, exclude=['user','id']), 'data' : model_to_dict(obj), 'online_id' : obj.id}
    except Exception:
        data = {'log' : model_to_dict(log_obj, exclude=['user','id']), 'data' : None, 'online_id' : log_obj.model_id}
    return data

def enter_to_log(sender,**kwargs):
    instance = kwargs["instance"]
    # 1 : Add, 0 : Edit, -1 : Delete
    try:
        action = kwargs["created"]
    except Exception:
        action = -1
    sender = sender.__name__
    model_id = instance.id
    try:
        user = User.object.get(id=instance.user_modified_id) if instance.user_modified_id else User.objects.get(id=instance.user_created_id)
    except Exception:
        user = None

    LogData = apps.get_model('training','LogData')
    log = LogData(user=user, entry_table=sender, model_id=model_id, action=action)
    log.save()


@csrf_exempt
def send_updated_log(request):
    if request.method == 'POST':
        apiKey = request.POST['ApiKey']
        request_timestamp = request.POST['timestamp']
        if request_timestamp:
            # try:
            #     apikey_object = ApiKey.objects.get(key=apikey)
            #     user = apikey_object.user
            #     TrainingUser = apps.get_model('training', 'TrainingUser')
            #     requesting_training_user = TrainingUser.objects.get(user_id=user.id)
            # except Exception, e:
            #     return HttpResponse("-1", status=401)

            LogData = apps.get_model('training','LogData')
            District = apps.get_model('geographies','District')
            Animator = apps.get_model('people','Animator')

            # rows = []
            rows = LogData.objects.filter(timestamp__gt=timestamp ,entry_table__in=['Partner','Trainer','Assessment','Question'])

            # if requesting_training_user:
                # requesting_user_states = requesting_training_user.get_states()

            log_list = []
            for row in rows:
                log_list.append(get_log_object(row))

            if rows:
                data = json.dumps(log_list, cls=DjangoJSONEncoder)
                return HttpResponse(data, content_type="application/json")
    return HttpResponse("0")
