
from dg.settings import TEXTLOCAL_API_KEY
from loop.models import Farmer,RegistrationSms,SMS_STATE,FarmerTransportCode
from loop_ivr.utils.config import TEXT_LOCAL_SINGLE_SMS_API, SMS_SENDER_NAME, REG_RECEIPT_URL,REG_AUTH_RECEIPT_URL
from loop.config import registration_sms
import requests
from django.views.decorators.csrf import csrf_exempt

from loop_ivr.utils.config import AGGREGATOR_IDEO
import json
from random import randint


def send_reg_sms(farmer):
	reg_sms = RegistrationSms(farmer=farmer,state=SMS_STATE['S'][0])
	reg_sms.save()
	response = send_sms_using_textlocal(farmer.phone,reg_sms.id)
	status_code = 0
	if response['status'] == "success":
		status_code = 1
		sms_id = response['messages'][0]['id']
		reg_sms.state = SMS_STATE['F'][0]
	reg_sms.text_local_id = sms_id
	reg_sms.sms_status = status_code
	reg_sms.save()


def send_sms_using_textlocal(farmer_no, custom_id):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    sms_body = registration_sms['welcome']['en']
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

def send_first_transportation_code(farmer_no,query_code,custom_id):
	custom_id = 1
	if(query_code=='1'):
		sms_body = registration_sms['transportion_code_beg']['en'] + '12345' + registration_sms['transportion_code_end']
    elif(query_code=='0'):
		sms_body = registration_sms['wrong_reg']['en']	
    else:
    	sms_body = registration_sms['input_error']['en']
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer_no,
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
        farmer_number = re.sub('^91', '0', farmer_number)
        to_number = str(request.POST.get('inNumber'))

        try:
            query_code = str(request.POST.get('content')).replace(" ", "")
        except Exception as e:
            query_code = ''
        farmer = Farmer.objects.filter(phone=farmer_number)[0]
        if farmer.user_created_id in AGGREGATOR_IDEO and not farmer.verified:
        	code = random_with_N_digits(5)
			reg_sms = FarmerTransportCode(code = code,phone=farmer_number,state=SMS_STATE['S'][0])
			reg_sms.save()
			response = send_first_transportation_code(farmer_number,query_code,farmer_number)
			status_code = 0
			if response['status'] == "success":
				status_code = 1
				sms_id = response['messages'][0]['id']
				reg_sms.state = SMS_STATE['F'][0]
			reg_sms.text_local_id = sms_id
			reg_sms.sms_status = status_code
			reg_sms.save()
        	

	return HttpResponse("0")

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)