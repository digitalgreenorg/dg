import json

import datetime
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


class DatetimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def save_log(sender, **kwargs):
    LoopUser = get_model('loop', 'LoopUser')
    instance = kwargs["instance"]
    action = kwargs["created"]
    sender = sender.__name__  # get the name of the table which sent the request
    model_dict = model_to_dict(instance)
    previous_time_stamp = get_latest_timestamp()
    try:
        user = User.objects.get(id=instance.user_modified_id) if instance.user_modified_id else User.objects.get(
            id=instance.user_created_id)
    except Exception, ex:
        user = None

    model_id = instance.id
    if sender == "Village":
        village_id = instance.id
        user = None
        loop_user = None
    elif sender == "Crop":
        village_id = None
        user = None
        loop_user = None
    elif sender == "CropLanguage":
        village_id = None
        user = None
        loop_user = None
    elif sender == "CombinedTransaction":
        village_id = instance.farmer.village.id
        user = instance.user_created
        loop_user = LoopUser.objects.get(user=instance.user_created)
    elif sender == "Transporter":
        village_id = None
        user = instance.user_created
        if instance.user_created is not None:
            loop_user = LoopUser.objects.get(user=instance.user_created)
        else:
            loop_user = None

    elif sender == "Vehicle":
        village_id = None
        user = None
        loop_user = None
    elif sender == "VehicleLanguage":
        village_id = None
        user = None
        loop_user = None
    elif sender == "TransportationVehicle":
        village_id = None
        user = instance.user_created
        if instance.user_created is not None:
            loop_user = LoopUser.objects.get(user=instance.user_created)
        else:
            loop_user = None
    elif sender == "DayTransportation":
        village_id = None
        user = instance.user_created
        loop_user = LoopUser.objects.get(user=instance.user_created)
    elif sender == "Gaddidar":
        village_id = None
        user = None
        # Loop user not required
        loop_user = None
    elif sender == "Mandi":
        village_id = None
        user = instance.user_created
        # loop user not required
        loop_user = None
    elif sender == "LoopUserAssignedMandi":
        model_id = instance.mandi.id
        village_id = None
        user = instance.user_created
        loop_user = instance.loop_user
        sender = "Mandi"
    elif sender == "LoopUserAssignedVillage":
        model_id = instance.village.id
        village_id = instance.village.id
        user = instance.user_created
        loop_user = instance.loop_user
        sender = "Village"
    elif sender == "GaddidarCommission":
        village_id = None
        user = instance.user_created
        loop_user=None
    elif sender == "State":
        village_id=None
        user = instance.user_created
        loop_user = None
    elif sender == "LoopUser":
        village_id=None
        user = instance.user_created
        loop_user = None
    else:           # farmer add
        village_id = instance.village.id
        loop_user = None
    Log = get_model('loop', 'Log')
    log = Log(village=village_id, user=user, action=action, entry_table=sender,
              model_id=model_id, loop_user=loop_user)
    log.save()
    # Raise an exception if timestamp of latest entry is less than the
    # previously saved data timestamp
    # if previous_time_stamp:
    #     if previous_time_stamp.timestamp >= log.timestamp:
    #         raise TimestampException(
    #             {"previous": previous_time_stamp.timestamp,"current":log.timestamp,'timestamp error': 'Latest entry data time created is less than previous data timecreated'})


def delete_log(sender, **kwargs):
    LoopUser = get_model('loop', 'LoopUser')
    instance = kwargs["instance"]
    sender = sender.__name__  # get the name of the table which sent the request
    try:
        user = User.objects.get(id=instance.user_modified_id) if instance.user_modified_id else User.objects.get(
            id=instance.user_created_id)
    except Exception, ex:
        user = None

    model_id = instance.id
    if sender == "Village":
        village_id = instance.id
        user = None
        loop_user = None
    elif sender == "Crop":
        village_id = None
        user = None
        loop_user = None
    elif sender == "CropLanguage":
        village_id = None
        user = None
        loop_user = None
    elif sender == "CombinedTransaction":
        village_id = instance.farmer.village.id
        user = instance.user_created
        loop_user = LoopUser.objects.get(user=instance.user_created)
    elif sender == "Transporter":
        village_id = None
        user = instance.user_created
        if instance.user_created is not None:
            loop_user = LoopUser.objects.get(user=instance.user_created)
        else:
            loop_user = None
    elif sender == "Vehicle":
        village_id = None
        user = None
        loop_user = None
    elif sender == "VehicleLanguage":
        village_id = None
        user = None
        loop_user = None
    elif sender == "TransportationVehicle":
        village_id = None
        user = instance.user_created
        if instance.user_created is not None:
            loop_user = LoopUser.objects.get(user=instance.user_created)
        else:
            loop_user = None
    elif sender == "DayTransportation":
        village_id = None
        user = instance.user_created
        loop_user = LoopUser.objects.get(user=instance.user_created)
    elif sender == "Gaddidar":
        village_id = None
        user = None
        # Loop user not required
        loop_user = None
    elif sender == "Mandi":
        village_id = None
        user = None
        # Loop user not required
        loop_user = None
    elif sender == "GaddidarCommission":
        village_id=None
        user = instance.user_created
        loop_user = None
    elif sender == "LoopUserAssignedMandi":
        village_id = None
        user = None
        loop_user = instance.loop_user
        sender = "Mandi"
        model_id = instance.mandi.id
    elif sender == "LoopUserAssignedVillage":
        village_id = instance.village.id
        user = instance.user_created
        loop_user = instance.loop_user
        sender = "Village"
        model_id = instance.village.id
    elif sender == "State":
        village_id = None
        user = instance.user_created
        loop_user = None
    elif sender == "LoopUser":
        village_id = None
        user = instance.user_created
        loop_user = None
    else:               # farmer add
        village_id = instance.village.id
        loop_user = None
    Log = get_model('loop', 'Log')
    try:
        log = Log(village=village_id, user=user, action=-1,
                  entry_table=sender, model_id=model_id, loop_user=loop_user)
        log.save()
    except Exception as ex:
        pass


def get_log_crop_vehicle_object(log_object, preferred_language):
    Obj_model = get_model('loop', log_object.entry_table)
    if log_object.entry_table == 'CropLanguage':
        table = 'Crop'
        attr = 'crop_name'
    else:
        table = 'Vehicle'
        attr = 'vehicle_name'

    obj=Obj_model.objects.get(id=log_object.model_id,language__notation=preferred_language)
    obj = model_to_dict(obj)
    Obj_model = get_model('loop',table)
    attr_value = obj[attr]
    obj = Obj_model.objects.get(id = obj[table.lower()])
    obj = model_to_dict(obj)
    obj[attr] = attr_value
    log_object.entry_table = table
    log_object.model_id = obj['id']
    return obj,log_object



def get_log_object(log_object, preferred_language):
    Obj_model = get_model('loop', log_object.entry_table)
    try:
        obj = Obj_model.objects.get(id=log_object.model_id)
        if Obj_model.__name__=='CropLanguage' or Obj_model.__name__=='VehicleLanguage':
            if obj.language.notation == preferred_language:
                obj,log_object = get_log_crop_vehicle_object(log_object,preferred_language)
            else:
                return
        else:
            obj = model_to_dict(obj)
        data = {'log': model_to_dict(log_object, exclude=['loop_user', 'user', 'village', 'id']), 'data':obj, 'online_id': obj['id']}
    except Exception, e:
        data = {'log': model_to_dict(
            log_object, exclude=['loop_user', 'user', 'village', 'id']), 'data': None, 'online_id': log_object.model_id}
    return data

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
        apikey = request.POST['ApiKey']
        timestamp = request.POST['timestamp']
        if timestamp:
            try:
                apikey_object = ApiKey.objects.get(key=apikey)
                user = apikey_object.user
            except Exception, e:
                return HttpResponse("-1", status=401)
            LoopUser = get_model('loop', 'LoopUser')
            try:
                requesting_loop_user = LoopUser.objects.get(user_id=user.id)
                preferred_language = requesting_loop_user.preferred_language.notation
                user_list = LoopUser.objects.filter(
                    village__block_id=requesting_loop_user.village.block.id).values_list('user__id', flat=True)
            except Exception as e:
                raise UserDoesNotExist(
                    'User with id: ' + str(user.id) + 'does not exist')
            villages = requesting_loop_user.get_villages()
            mandis = requesting_loop_user.get_mandis()
            Log = get_model('loop', 'Log')
            Farmer = get_model('loop', 'Farmer')
            Mandi = get_model('loop', 'Mandi')
            Gaddidar = get_model('loop', 'Gaddidar')
            GaddidarCommission = get_model('loop','GaddidarCommission')
            Transporter = get_model('loop', 'Transporter')
            TransportationVehicle = get_model('loop', 'TransportationVehicle')
            State = get_model('loop','State')
            list_rows = []
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_loop_user.id,entry_table__in=['LoopUser']))
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_loop_user.village.block.district.state.id,entry_table__in=['State']))
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, entry_table__in=['CropLanguage','VehicleLanguage']))
            village_list_queryset = Log.objects.filter(
                timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['Village'])
            list_rows.append(village_list_queryset)

            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, village__in=villages, entry_table__in=['Farmer']))

            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,
                                                loop_user__village__block_id=requesting_loop_user.village.block.id,
                                                entry_table__in=[
                                                    'Transporter']))

            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,
                                                loop_user__village__block_id=requesting_loop_user.village.block.id,
                                                entry_table__in=[
                                                    'TransportationVehicle']))

            transporter_trans_vehicle_rows = Log.objects.filter(timestamp__gt=timestamp, entry_table__in=[
                'Transporter', 'TransportationVehicle'])

            for entry in transporter_trans_vehicle_rows:
                if entry.entry_table == "Transporter" and entry.loop_user == None:
                    if Transporter.objects.get(id=entry.model_id).block.id == requesting_loop_user.village.block.id:
                        list_rows.append(Log.objects.filter(id=entry.id))
                elif entry.entry_table == "TransportationVehicle" and entry.loop_user == None:
                    if TransportationVehicle.objects.get(
                            id=entry.model_id).transporter.block.id == requesting_loop_user.village.block.id:
                        list_rows.append(Log.objects.filter(id=entry.id))

            mandi_list_queryset = Log.objects.filter(
                timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['Mandi'])
            list_rows.append(mandi_list_queryset)
            # for mrow in mandi_rows:
            #     if Mandi.objects.get(id=mrow.model_id) in mandis:
            #         rows = rows | Log.objects.filter(id=mrow.id)

            gaddidar_rows = Log.objects.filter(
                timestamp__gt=timestamp, entry_table__in=['Gaddidar'])
            for grow in gaddidar_rows:
                if Gaddidar.objects.get(id=grow.model_id).mandi in mandis:
                    list_rows.append(Log.objects.filter(id=grow.id))

            gaddidar_commission_rows = Log.objects.filter(
                timestamp__gt=timestamp,entry_table__in=['GaddidarCommission'])
            for gcrow in gaddidar_commission_rows:
                list_rows.append(Log.objects.filter(id=gcrow.id))

            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['CombinedTransaction']))

            list_rows.append(
                Log.objects.filter(timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['DayTransportation']))

            # rows = Log.objects.filter(
            #     timestamp__gt=timestamp, entry_table__in=['Crop', 'Vehicle'])
            # rows = rows | Log.objects.filter(
            #     timestamp__gt=timestamp, village__in=villages, entry_table__in=['Farmer', 'Village'])
            # rows = rows | Log.objects.filter(
            #     timestamp__gt=timestamp, user=user, entry_table__in=['CombinedTransaction'])
            #
            # rows = rows | Log.objects.filter(timestamp__gt=timestamp, loop_user__village__block_id = requesting_loop_user.village.block.id , entry_table__in=[
            #                                  'Transporter', 'TransportationVehicle'])
            #
            # transporter_trans_vehicle_rows = Log.objects.filter(timestamp__gt=timestamp, entry_table__in=[
            #                                  'Transporter', 'TransportationVehicle'])
            #
            # for entry in transporter_trans_vehicle_rows:
            #     if entry.entry_table == "Transporter" and entry.loop_user == None:
            #         if Transporter.objects.get(id=entry.model_id).block.id == requesting_loop_user.village.block.id:
            #             rows = rows | Log.objects.filter(id=entry.id)
            #     elif entry.entry_table == "TransportationVehicle" and entry.loop_user == None:
            #         if TransportationVehicle.objects.get(id=entry.model_id).transporter.block.id == requesting_loop_user.village.block.id:
            #             rows = rows | Log.objects.filter(id=entry.id)
            #
            #
            # rows = rows | Log.objects.filter(               timestamp__gt=timestamp, user=user, entry_table__in=['DayTransportation'])
            #
            # rows = rows | Log.objects.filter(timestamp__gt=timestamp,loop_user__user=user, entry_table__in=['Mandi'])
            # # for mrow in mandi_rows:
            # #     if Mandi.objects.get(id=mrow.model_id) in mandis:
            # #         rows = rows | Log.objects.filter(id=mrow.id)
            #
            #
            # gaddidar_rows = Log.objects.filter(timestamp__gt=timestamp, entry_table__in=['Gaddidar'])
            # for grow in gaddidar_rows:
            #     if Gaddidar.objects.get(id=grow.model_id).mandi in mandis:
            #         rows = rows | Log.objects.filter(id=grow.id)

            village_farmer_list = []
            for village in village_list_queryset:
                if village.action == 1:
                    village_wise_farmer_list = Farmer.objects.filter(
                        village__id=village.model_id)
                    for farmer in village_wise_farmer_list:
                        obj = Log(action=1,
                                  entry_table="Farmer", model_id=farmer.id)
                        village_farmer_list.append(obj)

            list_rows.append(village_farmer_list)

            mandi_gaddidar_list = []
            for mandi in mandi_list_queryset:
                if mandi.action == 1:
                    mandi_wise_gaddidar_list = Gaddidar.objects.filter(
                        mandi__id=mandi.model_id)
                    for gaddidar in mandi_wise_gaddidar_list:
                        obj = Log(action=1,
                                  entry_table="Gaddidar", model_id=gaddidar.id)
                        mandi_gaddidar_list.append(obj)

            list_rows.append(mandi_gaddidar_list)
            data_list = []

            for row in list_rows:
                if row:
                    for i in row:
                        objectData = get_log_object(i, preferred_language)
                        if objectData is not None:
                            data_list.append(objectData)
            if list_rows:
                data = json.dumps(data_list, cls=DatetimeEncoder)
                return HttpResponse(data, content_type="application/json")
    return HttpResponse("0")
