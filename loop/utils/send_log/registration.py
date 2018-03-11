
from dg.settings import TEXTLOCAL_API_KEY
from loop.models import Farmer,RegistrationSms,SMS_STATE,FarmerTransportCode,CombinedTransaction,FarmerTransportCode,Referral
from loop_ivr.utils.config import TEXT_LOCAL_SINGLE_SMS_API, SMS_SENDER_NAME, REG_RECEIPT_URL,REG_AUTH_RECEIPT_URL,REG_RESP_NUMBER
from loop.config import registration_sms,first_transaction_sms,referral_transport_sms,already_exist_sms
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from loop_ivr.utils.config import AGGREGATORS_IDEO
import json
from random import randint
import re
import datetime

from django.db.models import Min


def send_reg_sms(farmer):
	reg_sms = RegistrationSms(farmer=farmer,state=SMS_STATE['S'][0],msg_type=0)
	reg_sms.save()
	msg_type=0
	response = send_sms_using_textlocal(farmer.phone,reg_sms.id,msg_type)
	status_code = 0
	if response['status'] == "success":
		status_code = 1
		sms_id = response['messages'][0]['id']
		reg_sms.state = SMS_STATE['F'][0]
	reg_sms.text_local_id = sms_id
	reg_sms.sms_status = status_code
	reg_sms.save()


def send_sms_using_textlocal(farmer_no, custom_id,msg_type):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    if msg_type==0:
    	sms_body = registration_sms['welcome']['hi'] 
    if msg_type==4:
    	sms_body = already_exist_sms['hi']
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer_no,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom':custom_id, 'receipt_url': REG_RECEIPT_URL}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    return response_text


@csrf_exempt
def sms_response_from_txtlcl(request):
    if request.method == 'POST':
    	log_obj = RegistrationSms.objects.get(farmer_id=request.POST['customID'])
    	log_obj.update(state=SMS_STATE[request.POST['status']][0])

	return HttpResponse("0")

def send_first_transportation_code(farmer,code,query_code,custom_id):
	if query_code=='1':
		sms_body = ('%s %s %s') % (registration_sms['transportion_code_beg']['hi'],code ,registration_sms['transportion_code_end']['hi'])
		#sms_body = registration_sms['transportion_code_beg']['en'] + code + registration_sms['transportion_code_end']
	else:
		sms_body = registration_sms['input_error']['hi']
	sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
	parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer.phone,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom':custom_id, 'receipt_url': REG_AUTH_RECEIPT_URL}
	response = requests.post(sms_request_url, params=parameters)
	response_text = json.loads(str(response.text))
	return response_text

@csrf_exempt
def sms_reg_response_from_txtlcl(request):
    if request.method == 'POST':
    	log_obj = FarmerTransportCode.objects.get(phone=request.POST['customID'])
    	log_obj.update(state=SMS_STATE[request.POST['status']][0])

	return HttpResponse("0")

@csrf_exempt
def registration_auth_response(request):
	if request.method == 'POST':
		msg_id = str(request.POST.get('msgId'))
        farmer_number = str(request.POST.get('sender'))
        farmer_number = re.sub('^91', '', farmer_number)
        to_number = str(request.POST.get('inNumber'))

        try:
            query_code = str(request.POST.get('content')).replace(" ", "")
        except Exception as e:
            query_code = ''
        #import pdb;pdb.set_trace()
        farmer = Farmer.objects.filter(phone=farmer_number)
        if farmer.count()>0:
			if farmer[0].user_created_id in AGGREGATORS_IDEO and not farmer[0].verified and RegistrationSms.objects.filter(farmer=farmer[0],msg_type=0).count()>0:
				if query_code=='1':
					code = random_with_N_digits(5)
					reg_sms = FarmerTransportCode(code=code,phone=farmer_number,state=SMS_STATE['S'][0],msg_type=2)
					reg_sms.save()
					response = send_first_transportation_code(farmer[0],code,query_code,farmer_number)
					status_code = 0
					if response['status'] == "success":
						status_code = 1
						sms_id = response['messages'][0]['id']
						reg_sms.state = SMS_STATE['F'][0]
						farmer.update(verified=True)
					reg_sms.text_local_id = sms_id
					reg_sms.sms_status = status_code
					reg_sms.save()
				else:
					response = send_first_transportation_code(farmer[0],1,query_code,farmer_number)
        	
	return HttpResponse("0")

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    code = randint(range_start, range_end)
    used_codes = FarmerTransportCode.objects.values_list('code',flat=True)
    while code in used_codes:
    	code = randint(range_start, range_end)
    return code

def send_msg_sms_using_textlocal(farmer_no, custom_id):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    sms_body = first_transaction_sms['hi']
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer_no,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom':custom_id, 'receipt_url': REG_RECEIPT_URL}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    return response_text


def send_msg_after_first_trans(from_date,to_date):
	# import pdb;pdb.set_trace()
	farmer_list = getFirstTransportFarmers(from_date,to_date)
	for farmer in farmer_list:
		if RegistrationSms.objects.filter(farmer=farmer,msg_type=2).count()==0 and farmer.time_created>=datetime.datetime.strptime('05032018', "%d%m%Y"):
			reg_sms = RegistrationSms(farmer=farmer,state=SMS_STATE['S'][0],msg_type=2)
			reg_sms.save()
			response = send_msg_sms_using_textlocal(farmer.phone,reg_sms.id)
			status_code = 0
			if response['status'] == "success":
				status_code = 1
				sms_id = response['messages'][0]['id']
				reg_sms.state = SMS_STATE['F'][0]
			reg_sms.text_local_id = sms_id
			reg_sms.sms_status = status_code
			reg_sms.save()
		send_refer_transport_code(farmer)

def send_referral_transportation_code(farmer,code,custom_id):
	sms_body = ('%s %s %s') % (referral_transport_sms['beg']['hi'],code ,referral_transport_sms['end']['hi'])
		#sms_body = registration_sms['transportion_code_beg']['en'] + code + registration_sms['transportion_code_end']
	sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
	parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer.phone,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom':custom_id, 'receipt_url': REG_AUTH_RECEIPT_URL}
	response = requests.post(sms_request_url, params=parameters)
	response_text = json.loads(str(response.text))
	return response_text


def send_refer_transport_code(farmer):
	# farmer_list = getFirstRefferelFarmers(farmer_list)
	# for farmer in farmer_list:
	referred_by = farmer.referred_by
	farmer_refer = Farmer.objects.filter(phone=referred_by)
	if farmer_refer.count()>0 and not farmer_refer[0].referral_free_transport:
		if  farmer_refer[0].time_created>datetime.datetime.strptime('05032018','%d%m%Y'):
			code = random_with_N_digits(5)
			reg_sms = FarmerTransportCode(code=code,phone=farmer_refer[0].phone,state=SMS_STATE['S'][0],msg_type=3)
			reg_sms.save()
			response = send_referral_transportation_code(farmer_refer[0],code,farmer_refer[0].phone)
			status_code = 0
			if response['status'] == "success":
				status_code = 1
				sms_id = response['messages'][0]['id']
				reg_sms.state = SMS_STATE['F'][0]
				farmer_refer.update(referral_free_transport=True)
			reg_sms.text_local_id = sms_id
			reg_sms.sms_status = status_code
			reg_sms.save()



def getFirstTransportFarmers(from_date,to_date):
	farmers = Farmer.objects.filter(user_created_id__in=AGGREGATORS_IDEO)
	#farmer_first = CombinedTransaction.objects.values('farmer').annotate(Min('date')).filter(farmer__in=farmers).filter(date__min__gte=from_date,date__min__lte=to_date)
	farmer_first = CombinedTransaction.objects.values('farmer').annotate(Min('date')).filter(farmer__in=farmers)
	return Farmer.objects.filter(id__in=farmer_first.values('farmer'))

def getFirstRefferelFarmers(farmer_list):
	farmers_phone = Farmer.objects.filter(id__in=farmer_list).values('referred_by')
	farmerss = Farmer.objects.filter(phone__in=farmers_phone,referral_free_transport=False)
	return farmerss

def update_referrals():
	referrals = Referral.objects.filter(used=False)
	for referral in referrals:
		referred_farmer = Farmer.objects.filter(phone=referral.referred_farmer)
		referred_by = Farmer.objects.filter(phone=referral.referred_by)
		if referred_farmer.count()>0 and referred_by.count()>0 and (referred_farmer[0].referred_by=='' or referred_farmer[0].referred_by is None):
			referred_farmer.update(referred_by=referred_by[0].phone)
			obj = Referral.objects.get(id=referral.id)
			obj.used=True
			obj.save()
		elif referred_farmer.count()>0 and referred_by.count()>0 and (referred_farmer[0].time_created< datetime.datetime.strptime('05032018','%d%m%Y') or (len(referred_farmer[0].referred_by)>1) and referred_farmer[0].referred_by != referral.referred_by):
			reg_sms = RegistrationSms(farmer=referred_by[0],state=SMS_STATE['S'][0],msg_type=4)
			reg_sms.save()
			msg_type=4
			obj = Referral.objects.get(id=referral.id)
			obj.used=True
			obj.save()
			response = send_sms_using_textlocal(referred_by[0].phone,reg_sms.id,msg_type)
			if response['status'] == "success":
				status_code = 1
				sms_id = response['messages'][0]['id']
				reg_sms.state = SMS_STATE['F'][0]
			reg_sms.text_local_id = sms_id
			reg_sms.sms_status = status_code
			reg_sms.save()


