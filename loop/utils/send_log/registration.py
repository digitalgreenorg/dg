
from dg.settings import TEXTLOCAL_API_KEY
from loop.models import Farmer,RegistrationSms,SMS_STATE,FarmerTransportCode,CombinedTransaction,FarmerTransportCode,Referral,LoopUser
from loop_ivr.utils.config import TEXT_LOCAL_SINGLE_SMS_API, SMS_SENDER_NAME, REG_RECEIPT_URL,REG_AUTH_RECEIPT_URL,REG_RESP_NUMBER,REG_CODE_RESPONSE_URL,IVR_RECEIPT_URL
from loop.config import registration_sms,first_transaction_sms,referral_transport_sms,already_exist_sms
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from loop_ivr.utils.config import AGGREGATORS_IDEO
import json
from random import randint
import re
import datetime
import xml.etree.ElementTree as xml_parse
from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, DATABASES, TEXTLOCAL_API_KEY
from loop.utils.ivr_helpline.helpline_data import CALL_REQUEST_URL, APP_REQUEST_URL, APP_URL

from django.db.models import Min


def send_reg_sms(farmer,language):
	reg_sms = RegistrationSms(farmer=farmer,state=SMS_STATE['S'][0],msg_type=0)
	reg_sms.save()
	msg_type=0
	response = send_sms_using_textlocal(farmer.phone,reg_sms.id,msg_type,language)
	status_code = 0
	if response['status'] == "success":
		status_code = 1
		sms_id = response['messages'][0]['id']
		reg_sms.state = SMS_STATE['F'][0]
	reg_sms.text_local_id = sms_id
	reg_sms.sms_status = status_code
	reg_sms.save()


def send_sms_using_textlocal(farmer_no, custom_id,msg_type,language):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    if msg_type==0:
    	sms_body = registration_sms['welcome'][language.notation] 
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
    	log_obj = RegistrationSms.objects.filter(id=request.POST['customID'])
    	log_obj.update(state=SMS_STATE[request.POST['status']][0])

	return HttpResponse("0")

def send_first_transportation_code(farmer,code,query_code,custom_id,language):
	if query_code=='1':
		sms_body = ('%s %s %s') % (registration_sms['transportion_code_beg'][language.notation],code ,registration_sms['transportion_code_end'][language.notation])
		#sms_body = registration_sms['transportion_code_beg']['en'] + code + registration_sms['transportion_code_end']
	else:
		sms_body = registration_sms['input_error'][language.notation]
	sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
	parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer.phone,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom':custom_id, 'receipt_url': REG_CODE_RESPONSE_URL}
	response = requests.post(sms_request_url, params=parameters)
	response_text = json.loads(str(response.text))
	return response_text

@csrf_exempt
def sms_reg_response_from_txtlcl(request):
    if request.method == 'POST':
    	log_obj = FarmerTransportCode.objects.filter(phone=request.POST['customID'])
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
			user = LoopUser.objects.filter(user=farmer[0].user_created_id)
			if farmer[0].user_created_id in AGGREGATORS_IDEO and not farmer[0].verified and RegistrationSms.objects.filter(farmer=farmer[0],msg_type=0).count()>0:
				if query_code=='1':
					code = random_with_N_digits(5)
					reg_sms = FarmerTransportCode(code=code,phone=farmer_number,state=SMS_STATE['S'][0],msg_type=2)
					reg_sms.save()
					response = send_first_transportation_code(farmer[0],code,query_code,farmer_number,user[0].preferred_language)
					farmer.update(referral_free_transport_count=farmer[0].referral_free_transport_count+1)
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
					response = send_first_transportation_code(farmer[0],1,query_code,farmer_number,user[0].preferred_language)
        	
	return HttpResponse("0")

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    code = randint(range_start, range_end)
    used_codes = FarmerTransportCode.objects.values_list('code',flat=True)
    while code in used_codes:
    	code = randint(range_start, range_end)
    return code

def send_msg_sms_using_textlocal(farmer_no, custom_id,language):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    sms_body = first_transaction_sms[language.notation]
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer_no,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom':custom_id, 'receipt_url': REG_RECEIPT_URL}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    return response_text


def send_msg_after_first_trans(from_date,to_date):
	# import pdb;pdb.set_trace()
	farmer_list = getFirstTransportFarmers(from_date,to_date)
	for farmer in farmer_list:
		if RegistrationSms.objects.filter(farmer=farmer,msg_type=1).count()==0 and farmer.time_created>=datetime.datetime.strptime('05032018', "%d%m%Y"):
			reg_sms = RegistrationSms(farmer=farmer,state=SMS_STATE['S'][0],msg_type=1)
			reg_sms.save()
			user = LoopUser.objects.filter(user=farmer.user_created_id)
			response = send_msg_sms_using_textlocal(farmer.phone,reg_sms.id,user[0].preferred_language)
			status_code = 0
			if response['status'] == "success":
				status_code = 1
				sms_id = response['messages'][0]['id']
				reg_sms.state = SMS_STATE['F'][0]
			reg_sms.text_local_id = sms_id
			reg_sms.sms_status = status_code
			reg_sms.save()
		send_refer_transport_code(farmer)

def send_referral_transportation_code(farmer,code,custom_id,language):
	sms_body = ('%s %s %s') % (referral_transport_sms['beg'][language.notation],code ,referral_transport_sms['end'][language.notation])
		#sms_body = registration_sms['transportion_code_beg']['en'] + code + registration_sms['transportion_code_end']
	sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
	parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer.phone,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom':custom_id, 'receipt_url': REG_CODE_RESPONSE_URL}
	response = requests.post(sms_request_url, params=parameters)
	response_text = json.loads(str(response.text))
	return response_text


def send_refer_transport_code(farmer):
	# farmer_list = getFirstRefferelFarmers(farmer_list)
	# for farmer in farmer_list:
	referred_by = farmer.referred_by
	farmer_refer = Farmer.objects.filter(phone=referred_by)
	if farmer_refer.count()>0 and FarmerTransportCode.objects.filter(phone=referred_by,msg_type=3).count()<1: #and not farmer_refer[0].referral_free_transport:
		if  farmer_refer[0].time_created>datetime.datetime.strptime('05032018','%d%m%Y'):
			code = random_with_N_digits(5)
			reg_sms = FarmerTransportCode(code=code,phone=farmer_refer[0].phone,state=SMS_STATE['S'][0],msg_type=3)
			reg_sms.save()
			user = LoopUser.objects.filter(user=farmer_refer[0].user_created_id)
			response = send_referral_transportation_code(farmer_refer[0],code,farmer_refer[0].phone,user[0].preferred_language)
			status_code = 0
			if farmer.referral_free_transport_count>=0:
				farmer.referral_free_transport_count=int(farmer.referral_free_transport_count)+1
			else:
				farmer.referral_free_transport_count=1
			farmer.save()
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
			language = LoopUser.objects.filter(user=referred_farmer[0].user_created_id)
			response = send_sms_using_textlocal(referred_by[0].phone,reg_sms.id,msg_type,language)
			if response['status'] == "success":
				status_code = 1
				sms_id = response['messages'][0]['id']
				reg_sms.state = SMS_STATE['F'][0]
			reg_sms.text_local_id = sms_id
			reg_sms.sms_status = status_code
			reg_sms.save()






@csrf_exempt
def registration_ivr_response(request):
	#import pdb;pdb.set_trace()
	if request.method == 'GET':
		call_id = str(request.GET['CallSid'])
		farmer_number = str(request.GET['From'])
		farmer_number = re.sub('^0', '', farmer_number)
		# msg_id = str(request.POST.get('msgId'))
		# farmer_number = str(request.POST.get('sender'))
		# farmer_number = re.sub('^91', '', farmer_number)
		# to_number = str(request.POST.get('inNumber'))

        try:
            query_code = str(request.GET['digits'])
            query_code = re.sub('"','',query_code)
        except Exception as e:
            query_code = ''
        #import pdb;pdb.set_trace()
        farmer = Farmer.objects.filter(phone=farmer_number)
        if farmer.count()>0:
			if farmer[0].user_created_id in AGGREGATORS_IDEO and not farmer[0].verified and RegistrationSms.objects.filter(farmer=farmer[0],msg_type=0).count()>0:
				user = LoopUser.objects.filter(user=farmer[0].user_created_id)
				if query_code=="1":
					code = random_with_N_digits(5)
					reg_sms = FarmerTransportCode(code=code,phone=farmer_number,state=SMS_STATE['S'][0],msg_type=2)
					reg_sms.save()
					response = send_first_transportation_code(farmer[0],code,query_code,farmer_number,user[0].preferred_language)
					farmer.update(referral_free_transport_count=farmer[0].referral_free_transport_count+1)
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
					response = send_first_transportation_code(farmer[0],1,query_code,farmer_number,user[0].preferred_language)
        	
	return HttpResponse("0")



@csrf_exempt
def ivr_response(request):
	if request.method == 'POST':
		call_id = request.POST['CallSid']
		log_obj = RegistrationSms.objects.filter(text_local_id=call_id)
		log_obj.update(call_state=str(request.POST['Status']))
	return HttpResponse("0")




#def initiate_ivr_call(caller_number, dg_number, incoming_time, incoming_call_id, call_source):

def initiate_ivr_call(farmer,language,type):

	app_request_url = APP_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
	# app_id_br = 171536
	# app_id_ap= 171536
	app_id_br = 165528 # MARKET_INFO_APP
	app_id_ap = 168599
	
	# dg_number_br='09513886363'
	# dg_number_ap='09513886363'
	dg_number_br='01139589707'
	dg_number_ap = '01139587500'

	if language == 'hi' or language.notation == 'hi':
		dg_number= dg_number_br
		app_id = app_id_br
	else:
		dg_number= dg_number_ap
		app_id = app_id_ap
	app_url = APP_URL%(app_id,)
	phone_number = '0'+str(farmer.phone)
	call_response_url = IVR_RECEIPT_URL #MARKET_INFO_CALL_RESPONSE_URL
	msg_type=0
	if type==2:
		msg_type=5
	reg_sms = RegistrationSms(farmer=farmer,state=SMS_STATE['S'][0],msg_type=msg_type)
	reg_sms.save()
	msg_type=0
	parameters = {'From':phone_number,'CallerId':dg_number,'CallType':'trans','Url':app_url,'StatusCallback':call_response_url}
	# parameters = {'From':caller_number,'CallerId':dg_number,'CallType':'trans','Url':app_url}
	call_id=0
	status_code = 0
	response = requests.post(app_request_url,data=parameters)
	if response.status_code == 200:
		status_code = 1
		response_tree = xml_parse.fromstring((response.text).encode('utf-8'))
		call_detail = response_tree.findall('Call')[0]
		call_id = str(call_detail.find('Sid').text)
		#sms_id = response['messages'][0]['id']
	reg_sms.state = SMS_STATE['F'][0]
	reg_sms.text_local_id = call_id
	reg_sms.sms_status = status_code
	reg_sms.save()


    # module = 'make_market_info_call'
    # if response.status_code == 200:
        
    #     #outgoing_call_time = str(call_detail.find('StartTime').text)
    #     #price_info_incoming_obj = PriceInfoIncoming(call_id=outgoing_call_id, from_number=caller_number,
    #                                 to_number=dg_number, incoming_time=outgoing_call_time, call_source=call_source)
    # else:
    #     # Enter in Log
    #     price_info_incoming_obj = PriceInfoIncoming(call_id=incoming_call_id, from_number=caller_number,
    #                                     to_number=dg_number, incoming_time=incoming_time, info_status=0, call_source=call_source)
    #     log = 'Status Code: %s (Parameters: %s)'%(str(response.status_code),parameters)
    #     write_log(LOG_FILE,module,log)
    #     if response.status_code == 403:
    #         send_info_using_textlocal(caller_number, DND_MESSAGE, price_info_incoming_obj)
    # try:
    #     price_info_incoming_obj.save()
    # except Exception as e:
    #     # Save Errors in Logs
    #     write_log(LOG_FILE,module,str(e)) 
def automated_ivr(start_date,end_date):
	user = LoopUser.objects.filter(user_id__in=AGGREGATORS_IDEO).values('user_id','preferred_language__notation')
	cold_farmers = Farmer.objects.filter(time_created__gte=start_date,time_created__lt=end_date+datetime.timedelta(days=1),verified=0,user_created_id__in=user.values('user_id'))
	for farmer in cold_farmers:
		initiate_ivr_call(farmer,(item['preferred_language__notation'] for item in user if item['user_id']==farmer.user_created_id).next(),2)

#cold farmers: Farmers who did not pick up the ivr call



def ideo_incoming(request):
	#import pdb;pdb.set_trace()
	if request.method == 'GET':
		call_id = str(request.GET['CallSid'])
		farmer_number = str(request.GET['CallFrom'])
		farmer_number = re.sub('^0', '', farmer_number)
        farmer = Farmer.objects.filter(phone=farmer_number)

        if farmer.count()>0:
			
			if farmer[0].user_created_id in AGGREGATORS_IDEO and not farmer[0].verified and RegistrationSms.objects.filter(farmer=farmer[0],msg_type=0).count()>0:
				user = LoopUser.objects.filter(user=farmer[0].user_created_id)
				initiate_ivr_call(farmer,user.preferred_language,1)
				if query_code=="1":
					code = random_with_N_digits(5)
					reg_sms = FarmerTransportCode(code=code,phone=farmer_number,state=SMS_STATE['S'][0],msg_type=2)
					reg_sms.save()
					response = send_first_transportation_code(farmer[0],code,query_code,farmer_number,user[0].preferred_language)
					farmer.update(referral_free_transport_count=farmer[0].referral_free_transport_count+1)
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
					response = send_first_transportation_code(farmer[0],1,query_code,farmer_number,user[0].preferred_language)
        	
	return HttpResponse("0")

