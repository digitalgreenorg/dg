
import json
import datetime
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey
from loop.models import *

from itertools import chain

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
def send_admin_loopuser_mandi_child(admin_user,loopusers,districts):
	mandis=[]
	district_set=[]
	gaddidar_set=[]
	gaddidarcommission_set = []
	for loop_user in loopusers:
		mandi_queryset = loop_user.get_mandis()
		for row in mandi_queryset:
			if row.district not in districts and row not in mandis:
				if row.district not in district_set:
					district_set.append(row.district)
				mandis.append(row)

		gaddidar_queryset = Gaddidar.objects.filter(mandi__in=mandis)
		for row in gaddidar_queryset:
			gaddidar_set.append(row)
		gaddidarcommission_queryset = GaddidarCommission.objects.filter(mandi__in=mandis)
		for row in gaddidarcommission_queryset:
			gaddidarcommission_set.append(row)
	return district_set,mandis,gaddidar_set,gaddidarcommission_set

def send_admin_loopuser_village_child(admin_user,loopusers,districts):
	block_set = []
	district_set = []
	village_set = []
	for loop_user in loopusers:
		village_queryset = loop_user.get_villages()
		for row in village_queryset:
			if row.block.district not in districts or AdminAssignedDistrict.objects.get(district=row.block.district,admin_user=admin_user).aggregation_switch==False:
				village_set.append(row)
			if row.block.district not in districts and row.block.district not in district_set:
				district_set.append(row.block.district)
			if row.block not in block_set:
				block_set.append(row.block)
	return district_set,block_set,village_set

def createLogObject():
	pass
def createJsonObject(extradata,timestamp,entry_table,admin_user):
	data_list =[]
	for data in extradata:
		log={"action":1,"timestamp":timestamp,"entry_table":entry_table,"model_id":data.id,"admin_user":admin_user.id,"user":admin_user.id}
		obj = model_to_dict(data)
		data_row = {'log': log, 'data':obj, 'online_id': obj['id']}
		data_list.append(data_row)
	return data_list

@csrf_exempt
def sendData(request):
	if request.method == 'POST':
		apikey = request.POST['ApiKey']
		timestamp = request.POST['timestamp']
		if timestamp:
			try:
				apikey_object = ApiKey.objects.get(key=apikey)
				user = apikey_object.user
			except Exception:
				return HttpResponse("-1", status=401)
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
	extraDistrict,extraMandi,extraGaddidar,extraGaddidarCommission = send_admin_loopuser_mandi_child(requesting_admin_user,loopusers,districts)
	extraVillageDistrict,extraBlock,extraVillage = send_admin_loopuser_village_child(requesting_admin_user,loopusers,districts)
	extraDistrict = list(set(extraDistrict+extraVillageDistrict))
	data_list = []
	data_list = list(chain(createJsonObject(extraDistrict,timestamp,"District",requesting_admin_user),createJsonObject(extraBlock,timestamp,"Block",requesting_admin_user),createJsonObject(extraVillage,timestamp,'Village',requesting_admin_user),createJsonObject(extraMandi,timestamp,'Mandi',requesting_admin_user),createJsonObject(extraGaddidar,timestamp,'Gaddidar',requesting_admin_user),createJsonObject(extraGaddidarCommission,timestamp,'GaddidarCommission',requesting_admin_user)))
	if data_list:
	    data = json.dumps(data_list, cls=DatetimeEncoder)
	    return HttpResponse(data, content_type="application/json")
	return HttpResponse("0")

'''
"log": {
            "action": 1,
            "timestamp": "2017-08-12 12:50:12",
            "entry_table": "Village",
            "model_id": 121
        }
'''

