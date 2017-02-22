from datetime import datetime

from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey
from django.apps import apps


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

    Log = apps.get_model('training','LogData')
    log = Log(user=user, entry_table=sender, model_id=model_id, action=action)
    log.save()
