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


def upload_entries(sender, **kwargs ):
    from coco.models import CocoUser
    instance = kwargs["instance"]
    if kwargs["created"]:
        a = instance.upload_file.read()
        d= json.loads(a)
        user_object = User.objects.get(username=d['user']['username'])
        instance.user = user_object
        instance.save()
        partner = CocoUser.objects.get(user=user_object).partner
        upload_entries = d['uploads']
        for entry in upload_entries:
            if str(entry['action']) == 'A':
                #str(entry['entity_name'])()
                globals()[str(entry['entity_name']) + '_add'](entry['data'], user_object.id, partner.id, d)
            if str(entry['action']) == 'E':
                #str(entry['entity_name'])()
                globals()[str(entry['entity_name']) + '_edit'](entry['data'], user_object.id, partner.id, d['mediator'])

def mediator_add(data, user_id, partner_id, d):
    from people.models import Animator, AnimatorAssignedVillage
    print data['phone_no']
    obj = Animator(user_created_id=user_id, user_modified_id=user_id, name=data['name'],
                   gender=data['gender'], 
                   phone_no=data['phone_no'] if data['phone_no'] != None else "",
                   partner_id=partner_id,
                   district_id=data['district']['id'])
    obj.save()
    for vil in data["assigned_villages"]:
        obj_vil = AnimatorAssignedVillage(animator_id=obj.id, village_id=vil['id'])
        obj_vil.save()


def mediator_edit(data, user_id, parter_id, district_data):
    from people.models import Animator
    if data['online_id']:
        mediator_obj = Animator.objects.get(id=data['online_id'])


def group_add(data, user_id, partner_id, d):
    from people.models import PersonGroup
    obj = PersonGroup(user_created_id=user_id, user_modified_id=user_id,
                      group_name=data['group_name'],
                      partner_id=partner_id,
                      village_id=data['village']['id'])
    obj.save()


def person_add(data, user_id, partner_id, d):
    from people.models import Person, PersonGroup
    group_id = None
    if data['group']['id'] is not None:
        for entry in d['group']:
            if entry['id'] == data['group']['id']:
                if 'online_id' in entry:
                    group_id = entry['online_id']
                else:
                    group_object = PersonGroup.objects.get(group_name=entry['group_name'], village_id=entry['village']['id'])
                    group_id = group_object.id
                break
    obj = Person(user_created_id=user_id, user_modified_id=user_id, 
                 person_name=data['person_name'],
                 father_name=data['father_name'],
                 village_id=data['village']['id'],
                 gender=data['gender'],
                 age=data['age'],
                 phone_no=data['phone_no'] if data['phone_no'] != None else "",
                 group_id=group_id,
                 partner_id=partner_id)

    obj.save()

def video_add(data, user_id, partner_id, d):
    from people.models import Animator, Person, PersonGroup
    from videos.models import Video
    
    facilitator_id = None
    cameraoperator_id = None
    for entry in d['mediator']:
        if entry['id'] == data['facilitator']['id']:
            if 'online_id' in entry:
                facilitator_id = entry['online_id']
            else:
                facilitator_object = Animator.objects.get(name=entry['name'],
                                                          gender=entry['gender'],
                                                          district_id=entry['district']['id'],
                                                          partner_id=entry['partner']['id'])
                facilitator_id = facilitator_object.id
        if entry['id'] == data['cameraoperator']['id']:
            if 'online_id' in entry:
                cameraoperator_id = entry['online_id']
            else:
                cameraoperator_object = Animator.objects.get(name=entry['name'],
                                                             gender=entry['gender'],
                                                             district_id=entry['district']['id'],
                                                             partner_id=entry['partner']['id'])
                cameraoperator_id = cameraoperator_object.id
    obj = Video(user_created_id=user_id, user_modified_id=user_id,
                title=data['title'], 
                video_type=data['video_type'],
                language_id=data['language']['id'],
                summary=data['summary'],
                video_production_start_date=data['video_production_start_date'],
                video_production_end_date=data['video_production_end_date'],
                village_id=data['village']['id'],
                facilitator_id=facilitator_id,
                cameraoperator_id=cameraoperator_id,
                video_suitable_for=data['video_suitable_for'],
                actors=data['actors'],
                youtubeid=data['youtubeid'],
                partner_id=partner_id)
 
    obj.save()

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
    
    # Adding PersonMeetingAttendance records to the ServerLog. This is required for Mobile COCO, since we need to update a person record, whenever a pma is edited or deleted. We are adding the instance.person.id since the corresponding person record needs to be updated whenever an attendance record is changed.
    model_id = instance.person.id if sender is "PersonMeetingAttendance" else instance.id
    if sender == "Village":
        village_id = instance.id
    elif sender == "Animator" or sender == 'Language' or sender == 'NonNegotiable':
        village_id = None
    elif sender == "PersonAdoptPractice":
        village_id = instance.person.village.id
    else:
        village_id = instance.village.id
    partner_id = None if sender is "Village" or 'Language' or 'NonNegotiable' else instance.partner.id
    ServerLog = get_model('coco', 'ServerLog')
    log = ServerLog(village=village_id, user=user, action=action, entry_table=sender,
                    model_id=model_id, partner=partner_id)
    log.save()
    ###Raise an exception if timestamp of latest entry is less than the previously saved data timestamp
    if previous_time_stamp:
        if previous_time_stamp.timestamp > log.timestamp:
            raise TimestampException('timestamp error: Latest entry data time created is less than previous data timecreated')
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
    # Adding PersonMeetingAttendance records to the ServerLog. This is required for Mobile COCO, since we need to update a person record, whenever a pma is edited or deleted. We are adding the instance.person.id since the corresponding person record needs to be updated whenever an attendance record is changed.
    model_id = instance.person.id if sender is "PersonMeetingAttendance" else instance.id
    ServerLog = get_model('coco', 'ServerLog')
    try:
        log = ServerLog(village = instance.village.id, user = user, action = -1, entry_table = sender, model_id = instance.id, partner = instance.partner.id)
        log.save()
    except Exception as ex:
        pass

def send_updated_log(request):
    timestamp = request.GET.get('timestamp', None)
    if timestamp:
        CocoUser = get_model('coco','CocoUser')
        CocoUserVillages = get_model('coco','CocoUser_villages')
        try:
            coco_user = CocoUser.objects.get(user_id=request.user.id)
        except Exception as e:
            raise UserDoesNotExist('User with id: '+str(request.user.id) + 'does not exist')
        partner_id = coco_user.partner_id
        villages = CocoUserVillages.objects.filter(cocouser_id = coco_user.id).values_list('village_id', flat = True)
        ServerLog = get_model('coco', 'ServerLog')
        rows = ServerLog.objects.filter(timestamp__gte = timestamp, entry_table__in = ['Animator', 'Video', 'NonNegotiable'])
        if partner_id:
            rows = rows | ServerLog.objects.filter(timestamp__gte = timestamp, village__in = villages, partner = partner_id )
        else:
            rows = rows | ServerLog.objects.filter(timestamp__gte = timestamp, village__in = villages)
        if rows:
            data = serializers.serialize('json', rows, fields=('action','entry_table','model_id', 'timestamp'))
            return HttpResponse(data, mimetype="application/json")
    return HttpResponse("0")

def get_latest_timestamp():
    ServerLog = get_model('coco', 'ServerLog')
    try:
        timestamp = ServerLog.objects.latest('id')
    except Exception as e:
        timestamp = None
    return timestamp
