import json

from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.http import HttpResponse

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

    if sender in ['VideoQualityReview']:
        block_id = instance.video.village.block_id
    elif sender in ['DisseminationQuality', 'AdoptionVerification']:
        block_id = instance.village.block_id
    else:
        block_id = None

    if sender in ['VideoQualityReview']:
        partner_id = instance.video.partner_id
    elif sender in ['DisseminationQuality', 'AdoptionVerification']:
        partner_id = instance.mediator.partner_id
    else:
        partner_id = None

    ServerLog = get_model('qacoco', 'ServerLog')
    log = ServerLog(block=block_id, user=user, action=action, entry_table=sender,
                    model_id=model_id, partner=partner_id)
    log.save()
    ###Raise an exception if timestamp of latest entry is less than the previously saved data timestamp
#     if previous_time_stamp:
#         if previous_time_stamp.timestamp > log.timestamp:
#             raise TimestampException('timestamp error: Latest entry data time created is less than previous data timecreated')
# #    
def delete_log(sender, **kwargs ):
    instance = kwargs["instance"]
    sender = sender.__name__    # get the name of the table which sent the request
    user = None
    if instance.user_created_id:
        if instance.user_modified_id:
            user = User.objects.get(id = instance.user_modified_id) 
        else:
            user = User.objects.get(id = instance.user_created_id)
    # Adding PersonMeetingAttendance records to the ServerLog. This is required for Mobile COCO, since we need to update a person record, whenever a pma is edited or deleted. We are adding the instance.person.id since the corresponding person record needs to be updated whenever an attendance record is changed.
    model_id = instance.id
    ServerLog = get_model('qacoco', 'ServerLog')
    try:
        log = ServerLog(block = instance.block.id, user = user, action = -1, entry_table = sender, model_id = instance.id, partner = instance.partner.id)
        log.save()
    except Exception as ex:
        pass

def qa_send_updated_log(request):
    timestamp = request.GET.get('timestamp', None)
    if timestamp:
        QACocoUser = get_model('qacoco','QACocoUser')
        CocoUserBlocks = get_model('qacoco','QACocoUser_blocks')
        try:
            coco_user = QACocoUser.objects.get(user_id=request.user.id)
        except Exception as e:
            raise UserDoesNotExist('User with id: '+str(request.user.id) + 'does not exist')
        partner_id = coco_user.partner_id
        blocks = CocoUserBlocks.objects.filter(qacocouser_id = coco_user.id).values_list('block_id', flat = True)
        ServerLog = get_model('qacoco', 'ServerLog')
        #based on same block
        rows = ServerLog.objects.filter(timestamp__gte = timestamp,block__in = blocks)
        #based on same user
        rows = rows | ServerLog.objects.filter(timestamp__gte = timestamp,user_id = request.user.id)
        if partner_id:
            rows = rows | ServerLog.objects.filter(timestamp__gte = timestamp, block__in = blocks, partner = partner_id )
        else:
            rows = rows | ServerLog.objects.filter(timestamp__gte = timestamp, block__in = blocks)
        if rows:
            data = serializers.serialize('json', rows, fields=('action','entry_table','model_id', 'timestamp'))
            return HttpResponse(data, content_type="application/json")
    return HttpResponse("0")

def get_latest_timestamp():
    ServerLog = get_model('qacoco', 'ServerLog')
    try:
        timestamp = ServerLog.objects.latest('id')
    except Exception as e:
        timestamp = None
    return timestamp
