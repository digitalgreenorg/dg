from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey
from django.apps import apps
import json
from django.core.serializers.json import DjangoJSONEncoder

def get_latest_timestamp():
    LogData = apps.get_model('training','LogData')
    try:
        obj = LogData.objects.latest('id')
    except Exception:
        obj = None
    return obj

def get_log_object(log_obj):
    if log_obj.entry_table == 'Partner':
        app = 'programs'
    elif log_obj.entry_table == 'Animator':
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
            try:
                apikey_object = ApiKey.objects.get(key=apikey)
                user = apikey_object.user
                TrainingUser = apps.get_model('training', 'TrainingUser')
                requesting_training_user = TrainingUser.objects.get(user_id=user.id)
                requesting_training_user = TrainingUser.objects.get(id=15)
            except Exception, e:
                return HttpResponse("-1", status=401)

            LogData = apps.get_model('training','LogData')
            District = apps.get_model('geographies','District')
            Animator = apps.get_model('people','Animator')

            # rows = []
            rows = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table__in=['Partner','Trainer','Assessment','Question'])
            distrcit_animator_list = []

            if requesting_training_user:
                requesting_user_states = requesting_training_user.get_states()
                requesting_user_districts = []

                filtered_districts = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table='District')
                for district in filtered_districts:
                    if district.action != -1 and District.objects.get(id=district.model_id).state in requesting_user_states:
                        distrcit_animator_list.append(district)
                        requesting_user_districts.append(district.model_id)

                filtered_animators = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table='Animator')
                for animator in filtered_animators:
                    if animator.action != -1 and Animator.objects.get(id=animator.model_id).district.state in requesting_user_states:
                        distrcit_animator_list.append(animator)

            log_list = []
            for row in rows:
                log_list.append(get_log_object(row))
            for row in distrcit_animator_list:
                log_list.append(get_log_object(row))

            if rows:
                data = json.dumps(log_list, cls=DjangoJSONEncoder)
                return HttpResponse(data, content_type="application/json")
    return HttpResponse("0")
