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
    elif log_obj.entry_table == 'Language':
        app = 'videos'
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

    if action == -1:
        DeleteLog = apps.get_model('training','DeleteLog')
        obj = model_to_dict(instance)
        deletedObject = DeleteLog(entry_table=sender,table_object=obj)
        deletedObject.save()


@csrf_exempt
def send_updated_log(request):
    if request.method == 'POST':
        apiKey = request.POST['ApiKey']
        request_timestamp = request.POST['timestamp']
        if request_timestamp:
            try:
                apikey_object = ApiKey.objects.get(key=apiKey)
                user = apikey_object.user
                TrainingUser = apps.get_model('training', 'TrainingUser')
                requesting_training_user = TrainingUser.objects.get(user_id=user.id)
            except Exception, e:
                return HttpResponse("-1", status=401)

            LogData = apps.get_model('training','LogData')
            District = apps.get_model('geographies','District')
            Animator = apps.get_model('people','Animator')
            Training = apps.get_model('training','Training')
            Score = apps.get_model('training','Score')

            rows = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table__in=['Partner','Trainer','Assessment','Question', 'Language'])
            district_animator_training_list = []

            if requesting_training_user:
                requesting_user_states = requesting_training_user.get_states()

                filtered_districts = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table='District')
                for district in filtered_districts:
                    try:
                        if district.action != -1 and District.objects.get(id=district.model_id).state in requesting_user_states:
                            district_animator_training_list.append(district)
                        elif district.action == -1:
                            district_animator_training_list.append(district)
                    except Exception: #Incase object edited and then deleted
                        district_animator_training_list.append(district)

                filtered_animators = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table='Animator')
                for animator in filtered_animators:
                    try:
                        if animator.action != -1 and Animator.objects.get(id=animator.model_id).district.state in requesting_user_states:
                            district_animator_training_list.append(animator)
                        elif animator.action == -1:
                            district_animator_training_list.append(animator)
                    except Exception: #Incase object edited and then deleted
                        district_animator_training_list.append(animator)

                # TO SEND TRAINING AND SCORE OBJECTS IN THE LOG REQUEST
                # filtered_trainings = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table='Training')
                # for training in filtered_trainings:
                #     try:
                #         if training.action != -1 and Training.objects.get(id=training.model_id).user_created_id == requesting_training_user.user_id:
                #             district_animator_training_list.append(training)
                #         elif training.action == -1:
                #             district_animator_training_list.append(training)
                #     except Exception: #Incase training edited and then deleted by admin
                #         district_animator_training_list.append(training)
                #
                # filtered_scores = LogData.objects.filter(timestamp__gt=request_timestamp,entry_table='Score')
                # for score in filtered_scores:
                #     try:
                #         if score.action != -1 and Score.objects.get(id=score.model_id).training.user_created_id == requesting_training_user.user_id:
                #             district_animator_training_list.append(score)
                #         elif score.action == -1:
                #             district_animator_training_list.append(score)
                #     except Exception:
                #         district_animator_training_list.append(score)


                # TO SEND DISTRICTS AND ANIMATORS INCASE TRAINING USER IS ASSIGNED/UNASSIGNED SOME STATE
                # user_modified = LogData.objects.filter(timestamp__gt=request_timestamp, entry_table="TrainingUser")
                # if user_modified:
                #     new_assigned_districts = District.objects.filter(state__id__in=requesting_user_states)
                #     for n_a_d in new_assigned_districts:
                #         obj = LogData(action=1,entry_table="District",model_id=n_a_d.id)
                #         district_animator_training_list.append(obj)
                #     new_mediators = Animator.objects.filter(district__state__id__in=requesting_user_states)
                #     for n_m in new_mediators:
                #         obj = LogData(action=1,entry_table="Animator",model_id=n_m.id)
                #         district_animator_training_list.append(obj)

            log_list = []
            for row in rows:
                log_list.append(get_log_object(row))
            for row in district_animator_training_list:
                log_list.append(get_log_object(row))

            if log_list:
                data = json.dumps(log_list, cls=DjangoJSONEncoder)
                return HttpResponse(data, content_type="application/json")
    return HttpResponse(json.dumps({'message': 'No Data to send'}), status=200)
