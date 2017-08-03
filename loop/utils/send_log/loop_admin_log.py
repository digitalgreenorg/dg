import json
import datetime
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


def save_district_log(instance,kwargs):
    admin_user = None
    user = None
    sender='District'
    model_id = instance.id
    district_id = instance.id
    try:
        action = kwargs["created"]
    except Exception:
        action = -1

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_mandi_log(instance,kwargs):
    admin_user = None
    user = None
    sender='Mandi'
    model_id = instance.id
    district_id = instance.district.id
    try:
        action = kwargs["created"]
    except Exception:
        action = -1

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_gaddidar_log(instance,kwargs):
    admin_user = None
    user = None
    sender='Gaddidar'
    model_id = instance.id
    district_id = instance.mandi.district.id
    try:
        action = kwargs["created"]
    except Exception:
        action = -1
    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_gaddidarcommission_log(instance,kwargs):
    admin_user = None
    user = None
    sender='GaddidarCommission'
    model_id = instance.id
    district_id = instance.mandi.district.id
    try:
        action = kwargs["created"]
    except Exception:
        action = -1

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_block_log(instance,kwargs):
    admin_user = None
    user = None
    sender='Block'
    model_id = instance.id
    district_id = instance.district.id
    try:
        action = kwargs["created"]
    except Exception:
        action = -1

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_village_log(instance,kwargs):
    admin_user = None
    user = None
    sender='Village'
    model_id = instance.id
    district_id = instance.block.district.id
    try:
        action = kwargs["created"]
    except Exception:
        action = -1

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_district_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    Mandi = get_model('loop','Mandi')
    Gaddidar = get_model('loop','Gaddidar')
    GaddidarCommission = get_model('loop','GaddidarCommission')
    Block = get_model('loop','Block')
    Village = get_model('loop','Village')
    action = kwargs['created']
    if action == 1:
        mandi_queryset = Mandi.objects.filter(district=instance.district)
        mandis =[]
        for row in mandi_queryset:
            save_mandi_log(row,kwargs)
            mandis.append(row)

        gaddidar_queryset = Gaddidar.objects.filter(mandi__district=instance.district)
        for row in gaddidar_queryset:
            save_gaddidar_log(row,kwargs)
        gaddidarcommission_queryset = GaddidarCommission.objects.filter(mandi__district=instance.district)
        for row in gaddidarcommission_queryset:
            save_gaddidarcommission_log(row,kwargs)

        block_queryset = Block.objects.filter(district=instance.district)
        for row in block_queryset:
            save_block_log(row,kwargs)
    if instance.aggregation_switch==True:
        village_queryset = Village.objects.filter(block__district=instance.district)
        for row in village_queryset:
            save_village_log(row,kwargs)


def save_loopuser_mandi_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    Mandi = get_model('loop','Mandi')
    Gaddidar = get_model('loop','Gaddidar')
    GaddidarCommission = get_model('loop','GaddidarCommission')
    District = get_model('loop','District')
    

    #mandi_queryset = Mandi.objects.filter(district=instance.mandi.district)
    #mandis =[]
    save_mandi_log(instance.mandi,kwargs)
    save_district_log(instance.mandi.district,kwargs)
    #mandis.append(row)

    gaddidar_queryset = Gaddidar.objects.filter(mandi=instance.mandi)
    for row in gaddidar_queryset:
        save_gaddidar_log(row,kwargs)
    gaddidarcommission_queryset = GaddidarCommission.objects.filter(mandi=instance.mandi)
    for row in gaddidarcommission_queryset:
        save_gaddidarcommission_log(row,kwargs)
def save_loopuser_village_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    District = get_model('loop','District')
    Block = get_model('loop','Block')
    save_village_log(instance.village,kwargs)
    save_district_log(instance.village.block.district,kwargs)
    save_block_log(instance.village.block,kwargs)


def save_admin_log(sender, **kwargs):
    AdminUser = get_model('loop', 'AdminUser')
    instance = kwargs["instance"]
    sender = sender.__name__  # get the name of the table which sent the request
    try:
        action = kwargs["created"]
    except Exception:
        action = -1
    try:
        # user = User.objects.get(id=instance.user_modified_id) if instance.user_modified_id else User.objects.get(
            # id=instance.user_created_id)
        user = instance.user_created
    except Exception:
        user = None

    model_id = instance.id
    admin_user = None
    district_id = None
    
    if sender == "Village":
        district_id = instance.block.district.id
        if instance.user_created is not None:
            admin_user = AdminUser.objects.get(user=instance.user_created)
    elif sender == "Mandi":
        district_id = instance.district.id
        if instance.user_created is not None:
            admin_user = AdminUser.objects.get(user=instance.user_created)
    elif sender == "Gaddidar":
        district_id = instance.mandi.district.id
        if instance.user_created is not None:
            admin_user = AdminUser.objects.get(user=instance.user_created)
    elif sender == "GaddidarCommission":
        district_id = instance.mandi.district.id
        if instance.user_created is not None:
            admin_user = AdminUser.objects.get(user=instance.user_created)
    elif sender == "AdminAssignedDistrict":
        sender = "District"
        model_id = instance.district.id
        save_district_child_log(instance,kwargs)
    elif sender == "AdminAssignedLoopUser":
        sender = "LoopUser"
        model_id = instance.loop_user.id
        admin_user = instance.admin_user
    elif sender == "LoopUserAssignedMandi":
        save_loopuser_child_log(instance,kwargs)

    elif sender == "Block":
        district_id = instance.district.id

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

    # if action == -1:
    #     LogDeleted = get_model('loop','LogDeleted')
    #     obj = model_to_dict(instance)
    #     deletedObject = LogDeleted(entry_table=sender,table_object=obj)
    #     deletedObject.save()


def get_admin_log_crop_vehicle_object(log_object, preferred_language):
    import pdb;pdb.set_trace()
    Obj_model = get_model('loop', log_object.entry_table)
    if log_object.entry_table == 'CropLanguage':
        table = 'Crop'
        attr = 'crop_name'
    else:
        table = 'Vehicle'
        attr = 'vehicle_name'

    obj = Obj_model.objects.get(id=log_object.model_id,language__notation=preferred_language)
    obj = model_to_dict(obj)
    Obj_model = get_model('loop',table)
    attr_value = obj[attr]
    obj = Obj_model.objects.get(id = obj[table.lower()])
    obj = model_to_dict(obj)
    obj[attr] = attr_value
    log_object.entry_table = table
    log_object.model_id = obj['id']
    return obj,log_object

def get_admin_log_object(log_object, preferred_language):
    Obj_model = get_model('loop', log_object.entry_table)
    try:
        obj = Obj_model.objects.get(id=log_object.model_id)
        # if Obj_model.__name__=='CropLanguage' or Obj_model.__name__=='VehicleLanguage':
        #     if obj.language.notation == preferred_language:
        #         obj,log_object = get_log_crop_vehicle_object(log_object,preferred_language)
        #     else:
        #         return
        if Obj_model.__name__=='Village':
            Obj_model_temp = get_model('loop','Farmer')
            obj = model_to_dict(obj)
            obj['farmer_count']=Obj_model_temp.objects.filter(village=obj['id']).count()
        else:
            obj = model_to_dict(obj)
        data = {'log': model_to_dict(log_object, exclude=['admin_user', 'user', 'village', 'id']), 'data':obj, 'online_id': obj['id']}
    except Exception, e:
        data = {'log': model_to_dict(
            log_object, exclude=['admin_user', 'user', 'village', 'id']), 'data': None, 'online_id': log_object.model_id}
    return data

def get_latest_timestamp():
    Log = get_model('loop', 'Log')
    try:
        timestamp = Log.objects.latest('id')
    except Exception:
        timestamp = None
    return timestamp


@csrf_exempt
def send_updated_admin_log(request):
    if request.method == 'POST':
        apikey = request.POST['ApiKey']
        timestamp = request.POST['timestamp']
        if timestamp:
            try:
                apikey_object = ApiKey.objects.get(key=apikey)
                user = apikey_object.user
            except Exception:
                return HttpResponse("-1", status=401)
            AdminUser = get_model('loop', 'AdminUser')
            try:
                requesting_admin_user = AdminUser.objects.get(user_id=user.id)
                preferred_language = requesting_admin_user.preferred_language.notation
                user_list = AdminUser.objects.filter(
                    id=requesting_admin_user.id).values_list('user__id', flat=True)
            except Exception:
                raise UserDoesNotExist(
                    'User with id: ' + str(user.id) + 'does not exist')
            districts = requesting_admin_user.get_districts()
            loopusers = requesting_admin_user.get_loopusers()
            Log = get_model('loop', 'AdminLog')
            Mandi = get_model('loop', 'Mandi')
            Gaddidar = get_model('loop', 'Gaddidar')
            Village = get_model('loop', 'Village')
            GaddidarCommission = get_model('loop','GaddidarCommission')
            AdminAssignedDistrict = get_model('loop','AdminAssignedDistrict')
            LoopUser = get_model('loop','LoopUser')
            Farmer = get_model('loop','Farmer')
            CropLanguage = get_model('loop','CropLanguage')
            VehicleLanguage = get_model('loop','VehicleLanguage')
            LoopUserAssignedVillage = get_model('loop','loopuserassignedvillage')
            LoopUserAssignedMandi = get_model('loop','loopuserassignedmandi')

            list_rows = []
            #AdminUser Log
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_admin_user.id,entry_table__in=['AdminUser']))
            #list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_admin_user.village.block.id,entry_table__in=['Block']))
            #list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_admin_user.village.block.id,entry_table__in=['Block']))
            #list_queryset = Log.objects.filter(timestamp__gt=timestamp, entry_table__in=['CropLanguage','VehicleLanguage'])
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['Crop','Vehicle']))
            

            '''
            Village Log
            TODO : district switch check for villages
            '''
            village_list_queryset = Log.objects.filter(
                timestamp__gt=timestamp,district__in=districts,entry_table__in=['Village'])
            loopuser_querset=Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUser'])
            for row in loopuser_querset:
                try:
                    if LoopUser.objects.get(id=row.model_id) in loopusers:
                        list_rows.append(row)
                except:
                    pass
            for vrow in village_list_queryset:
                if AdminAssignedDistrict.objects.get(admin_user=requesting_admin_user,district=vrow.district).aggregation_switch==True:
                    list_rows.append(vrow)

            #Mandi Log
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, district__in=districts, entry_table__in=['Mandi']))

            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, district__in=districts, entry_table__in=['Gaddidar']))
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, district__in=districts, entry_table__in=['GaddidarCommission']))
            loopuserassignedvillage_queryset = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUserAssignedVillage'])
            loopuserassignedmandi_queryset = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUserAssignedMandi'])
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['Crop','Vehicle']))
            croplanguage_query = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['CropLanguage'])
            for row in croplanguage_query:
                if CropLanguage.objects.get(id=row.model_id).language == preferred_language:
                    list_rows.append(row)
            vehiclelanguage_query = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['VehicleLanguage'])
            for row in croplanguage_query:
                if VehicleLanguage.objects.get(id=row.model_id).language == preferred_language:
                    list_rows.append(row)
            #import pdb;pdb.set_trace()
            for row in loopuserassignedvillage_queryset:
                try:
                    if LoopUserAssignedVillage.objects.get(id=row.model_id).loop_user in loopusers:
                        list_rows.append(row)
                except:
                    pass
            for row in loopuserassignedmandi_queryset:
                try:
                    if LoopUserAssignedMandi.objects.get(id=row.model_id).loop_user in loopusers:
                        list_rows.append(row)
                except :
                    pass
                

            data_list = []

            for row in list_rows:
                if row:
                    try:
                        for i in row:
                            objectData = get_admin_log_object(i, preferred_language)
                            if objectData is not None:
                                data_list.append(objectData)
                    except TypeError:
                        data_list.append(get_admin_log_object(row, preferred_language))
            if list_rows:
                data = json.dumps(data_list, cls=DatetimeEncoder)
                return HttpResponse(data, content_type="application/json")
    return HttpResponse("0")
