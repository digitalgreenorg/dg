import json
import datetime
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey

from itertools import chain

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


def save_district_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = adminUser.user
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

def save_mandi_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = instance.user_created
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

def save_loopuserassignedmandi_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = instance.user_created
    sender='LoopUserAssignedMandi'
    model_id = instance.id
    district_id=None
    try:
        action = kwargs["created"]
    except Exception:
        action = -1

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_gaddidar_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = instance.user_created
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

def save_gaddidarcommission_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = instance.user_created
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

def save_block_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = adminUser.user
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

def save_village_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = instance.user_created
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

def save_loopuserassignedvillage_log(instance,adminUser,kwargs):
    admin_user = adminUser
    user = instance.user_created
    sender='LoopUserAssignedVillage'
    model_id = instance.id
    district_id=None
    try:
        action = kwargs["created"]
    except Exception:
        action = -1

    Log = get_model('loop', 'AdminLog')
    log = Log(district=district_id, user=user, action=action, entry_table=sender,
              model_id=model_id, admin_user=admin_user)
    log.save()

def save_district_block(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    Mandi = get_model('loop','Mandi')
    Gaddidar = get_model('loop','Gaddidar')
    GaddidarCommission = get_model('loop','GaddidarCommission')
    Block = get_model('loop','Block')
    Village = get_model('loop','Village')
    admin_user = instance.admin_user
    user = instance.user_created
    try:
        action = kwargs["created"]
    except Exception as e:
        action = -1
    block_queryset = Block.objects.filter(district=instance.district)
    for row in block_queryset:
        save_block_log(row,admin_user,kwargs)

def save_district_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    Mandi = get_model('loop','Mandi')
    Gaddidar = get_model('loop','Gaddidar')
    GaddidarCommission = get_model('loop','GaddidarCommission')
    Block = get_model('loop','Block')
    Village = get_model('loop','Village')
    admin_user = instance.admin_user
    user = instance.user_created
    try:
        action = kwargs["created"]
    except Exception as e:
        action = -1

    mandi_queryset = Mandi.objects.filter(district=instance.district)
    mandis =[]
    for row in mandi_queryset:
        save_mandi_log(row,admin_user,kwargs)
        mandis.append(row)

    gaddidar_queryset = Gaddidar.objects.filter(mandi__district=instance.district)
    for row in gaddidar_queryset:
        save_gaddidar_log(row,admin_user,kwargs)
    gaddidarcommission_queryset = GaddidarCommission.objects.filter(mandi__district=instance.district)
    for row in gaddidarcommission_queryset:
        save_gaddidarcommission_log(row,admin_user,kwargs)

    if instance.aggregation_switch==True:
        village_queryset = Village.objects.filter(block__district=instance.district)
        for row in village_queryset:
            save_village_log(row,admin_user,kwargs)

def save_admin_loopuser_mandi_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    Mandi = get_model('loop','Mandi')
    Gaddidar = get_model('loop','Gaddidar')
    GaddidarCommission = get_model('loop','GaddidarCommission')
    District = get_model('loop','District')
    LoopUser = get_model('loop','LoopUser')
    LoopUserAssignedMandi = get_model('loop','LoopUserAssignedMandi')
    admin_user = instance.admin_user
    mandi_queryset = instance.loop_user.get_mandis()
    mandis=[]
    district_set=[]
    districts = instance.admin_user.get_districts()
    for row in mandi_queryset:
        if row.district not in districts and row not in mandis:
            save_mandi_log(row,admin_user,kwargs)
            if row.district not in district_set:
                save_district_log(row.district,admin_user,kwargs)
                district_set.append(row.district)
            mandis.append(row)
    assignedMandi_queryset = LoopUserAssignedMandi.objects.filter(loop_user=instance.loop_user)
    for row in assignedMandi_queryset:
        save_loopuserassignedmandi_log(row,admin_user,kwargs)

    gaddidar_queryset = Gaddidar.objects.filter(mandi__in=mandis)
    for row in gaddidar_queryset:
        save_gaddidar_log(row,admin_user,kwargs)
    gaddidarcommission_queryset = GaddidarCommission.objects.filter(mandi__in=mandis)
    for row in gaddidarcommission_queryset:
        save_gaddidarcommission_log(row,admin_user,kwargs)

def save_loopuser_mandi_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    Mandi = get_model('loop','Mandi')
    Gaddidar = get_model('loop','Gaddidar')
    GaddidarCommission = get_model('loop','GaddidarCommission')
    District = get_model('loop','District')
    LoopUser = get_model('loop','LoopUser')
    AdminAssignedLoopUser = get_model('loop','AdminAssignedLoopUser')
    LoopUserAssignedMandi = get_model('loop','LoopUserAssignedMandi')
    admins_set = AdminUser.objects.filter(adminassignedloopuser__loop_user=instance.loop_user)

    for admin in admins_set:
        mandis_set = []
        district_set = []
        districts = admin.get_districts()
        if instance.mandi.district not in districts and instance.mandi not in mandis_set:
            save_mandi_log(instance.mandi,admin,kwargs)
            save_loopuserassignedmandi_log(instance,admin,kwargs)
            if instance.mandi.district not in district_set:
                save_district_log(instance.mandi.district,admin,kwargs)
                district_set.append(instance.mandi.district)
            mandis_set.append(instance.mandi)

        gaddidar_queryset = Gaddidar.objects.filter(mandi__in=mandis_set)
        for row in gaddidar_queryset:
            save_gaddidar_log(row,admin,kwargs)
        gaddidarcommission_queryset = GaddidarCommission.objects.filter(mandi__in=mandis_set)
        for row in gaddidarcommission_queryset:
            save_gaddidarcommission_log(row,admin,kwargs)

def save_admin_loopuser_village_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    District = get_model('loop','District')
    Block = get_model('loop','Block')
    District = get_model('loop','District')
    LoopUser = get_model('loop','LoopUser')
    AdminAssignedDistrict = get_model('loop','AdminAssignedDistrict')
    LoopUserAssignedVillage = get_model('loop','LoopUserAssignedVillage')
    admin_user = instance.admin_user
    districts = instance.admin_user.get_districts()
    village_queryset = instance.loop_user.get_villages()
    district_set =[]
    block_set =[]
    assignedVillage_queryset = LoopUserAssignedVillage.objects.filter(loop_user=instance.loop_user)
    for row in assignedVillage_queryset:
        save_loopuserassignedvillage_log(row,admin_user,kwargs)
    for row in village_queryset:
        if row.block.district not in districts or AdminAssignedDistrict.objects.get(district=row.block.district,admin_user=admin_user).aggregation_switch==False:
            save_village_log(row,admin_user,kwargs)
            if row.block.district not in districts and row.block.district not in district_set:
                save_district_log(row.block.district,admin_user,kwargs)
                district_set.append(row.block.district)
            if row.block.district not in districts and row.block not in block_set:
                save_block_log(row.block,admin_user,kwargs)
                block_set.append(row.block.district)

def save_loopuser_village_child_log(instance,kwargs):
    AdminUser = get_model('loop','AdminUser')
    District = get_model('loop','District')
    Block = get_model('loop','Block')
    District = get_model('loop','District')
    LoopUser = get_model('loop','LoopUser')
    AdminAssignedLoopUser = get_model('loop','AdminAssignedLoopUser')
    admins_set = AdminUser.objects.filter(adminassignedloopuser__loop_user=instance.loop_user)
    
    for admin in admins_set:
        village_set =[]
        district_set = []
        block_set =[]
        districts = admin.get_districts()
        if instance.village.block.district not in districts and instance.village not in village_set:
            save_village_log(instance.village,admin,kwargs)
            if instance.village.block.district not in district_set:
                save_district_log(instance.village.block.district,admin,kwargs)
                save_loopuserassignedvillage_log(instance,admin,kwargs)
                district_set.append(instance.village.block.district)
            if instance.village.block not in block_set:
                save_block_log(instance.village.block,admin,kwargs)
                block_set.append(instance.village.block)
            village_set.append(instance.village)





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
    elif sender == "Mandi":
        district_id = instance.district.id
    elif sender == "Gaddidar":
        district_id = instance.mandi.district.id
    elif sender == "GaddidarCommission":
        district_id = instance.mandi.district.id
    elif sender == "AdminAssignedDistrict":
        sender = "District"
        model_id = instance.district.id
        admin_user = instance.admin_user
        district_id = instance.district.id
        user = instance.user_created
        if action > -1:
            save_district_child_log(instance,kwargs)
        save_district_block(instance,kwargs)
    elif sender == "AdminAssignedLoopUser":
        sender = "LoopUser"
        model_id = instance.loop_user.id
        admin_user = instance.admin_user
        if action > -1:
            save_admin_loopuser_mandi_child_log(instance,kwargs)
            save_admin_loopuser_village_child_log(instance,kwargs)
    elif sender == "LoopUserAssignedMandi":
        save_loopuser_mandi_child_log(instance,kwargs)
    elif sender == "LoopUserAssignedVillage":
        save_loopuser_village_child_log(instance,kwargs)

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
        data = {'log': model_to_dict(log_object, exclude=['village', 'id']), 'data':obj, 'online_id': obj['id']}
    except Exception, e:
        data = {'log': model_to_dict(
            log_object, exclude=['village', 'id']), 'data': None, 'online_id': log_object.model_id}
    return data

def get_latest_timestamp():
    Log = get_model('loop', 'AdminLog')
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
            District = get_model('loop','District')
            Block = get_model('loop','Block')

            list_rows = []
            #AdminUser Log
            district_queryset = Log.objects.filter(timestamp__gt=timestamp,entry_table="District",admin_user=None)
            for row in district_queryset:
                if District.objects.get(id=row.model_id) in districts:
                    list_rows.append(row)
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table="District",admin_user=requesting_admin_user))

            block_queryset = Log.objects.filter(timestamp__gt=timestamp,entry_table="Block",admin_user=None)
            for row in block_queryset:
                if Block.objects.get(id=row.model_id).district in districts:
                    list_rows.append(row)
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table="Block",admin_user=requesting_admin_user))
            village_list_queryset = Log.objects.filter(timestamp__gt=timestamp,district__in=districts,entry_table__in=['Village'],admin_user=None)
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['Village'],admin_user=requesting_admin_user))
            for vrow in village_list_queryset:
                if AdminAssignedDistrict.objects.get(admin_user=requesting_admin_user,district=vrow.district).aggregation_switch==True:
                    list_rows.append(vrow)
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_admin_user.id,entry_table__in=['AdminUser']))
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['Crop','Vehicle']))
            loopuser_querset=Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUser'],admin_user=None)
            for row in loopuser_querset:
                try:
                    if LoopUser.objects.get(id=row.model_id) in loopusers:
                        list_rows.append(row)
                except:
                    pass
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUser'],admin_user=requesting_admin_user))
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp, entry_table__in=['MandiType'], admin_user=None))
            #Mandi Log
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, district__in=districts, entry_table__in=['Mandi'],admin_user=None))
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, entry_table__in=['Mandi'],admin_user=requesting_admin_user))

            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, district__in=districts, entry_table__in=['Gaddidar'],admin_user=None))
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, entry_table__in=['Gaddidar'],admin_user=requesting_admin_user))
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, district__in=districts, entry_table__in=['GaddidarCommission'],admin_user=None))
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, entry_table__in=['GaddidarCommission'],admin_user=requesting_admin_user))
            loopuserassignedvillage_queryset = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUserAssignedVillage'],admin_user=None)
            loopuserassignedmandi_queryset = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUserAssignedMandi'],admin_user=None)
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['LoopUserAssignedMandi','LoopUserAssignedVillage'],admin_user=requesting_admin_user))
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['Crop','Vehicle']))
            croplanguage_query = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['CropLanguage'])
            for row in croplanguage_query:
                if CropLanguage.objects.get(id=row.model_id).language == preferred_language:
                    list_rows.append(row)
            vehiclelanguage_query = Log.objects.filter(timestamp__gt=timestamp,entry_table__in=['VehicleLanguage'])
            for row in vehiclelanguage_query:
                if VehicleLanguage.objects.get(id=row.model_id).language == preferred_language:
                    list_rows.append(row)
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
