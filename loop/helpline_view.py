import time
import datetime
import requests
import unicodecsv as csv
import xml.etree.ElementTree as xml_parse
from pytz import timezone

from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing, \
    HelplineCallLog, HelplineSmsLog

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, MEDIA_ROOT

from loop.utils.ivr_helpline.helpline_data import CALL_STATUS_URL, CALL_REQUEST_URL, \
    CALL_RESPONSE_URL, SMS_REQUEST_URL, APP_REQUEST_URL, APP_URL, BROADCAST_RESPONSE_URL

HELPLINE_LOG_FILE = '%s/loop/helpline_log.log'%(MEDIA_ROOT,)

def write_log(log_file,module,log):
    curr_india_time = datetime.datetime.now(timezone('Asia/Kolkata'))
    with open(log_file, 'ab') as csvfile:
        file_write = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        file_write.writerow([curr_india_time,module,log])

# Call Type is 0 for Incoming Call and 1 for Outgoing Call
def save_call_log(call_id,from_number,to_number,call_type,start_time):
    call_obj = HelplineCallLog(call_id=call_id,from_number=from_number,to_number=to_number,call_type=call_type,start_time=start_time)
    try:
        call_obj.save()
    except Exception as e:
        # if error then log
        module = 'save_call_log'
        write_log(HELPLINE_LOG_FILE,module,str(e))

def save_sms_log(sms_id,from_number,to_number,sms_body,sent_time):
    sms_obj = HelplineSmsLog(sms_id=sms_id,from_number=from_number,to_number=to_number,sms_body=sms_body,sent_time=sent_time)
    try:
        sms_obj.save()
    except Exception as e:
        # if error then log
        module = 'save_sms_log'
        write_log(HELPLINE_LOG_FILE,module,str(e))

def get_status(call_id):
    call_status_url = CALL_STATUS_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID,call_id)
    response = requests.get(call_status_url)
    call_status = dict()
    # Status code 200 if API call is successful, 429 if Too many request 
    if response.status_code == 200:
        response_tree = xml_parse.fromstring((response.text).encode('utf-8'))
        call_detail = response_tree.findall('Call')[0]
        call_status['response_code'] = 200
        call_status['status'] = str(call_detail.find('Status').text)
        call_status['to'] = str(call_detail.find('To').text)
        call_status['from'] = str(call_detail.find('From').text)
        call_status['start_time'] = str(call_detail.find('StartTime').text)
        call_status['end_time'] = str(call_detail.find('EndTime').text)
        extra_detail = call_detail.findall('Details')[0]
        call_status['from_status'] = str(extra_detail.find('Leg1Status').text)
        call_status['to_status'] = str(extra_detail.find('Leg2Status').text)
    else:
        call_status['response_code'] = response.status_code
    return call_status

def get_info_through_api(outgoing_call_id):
    call_status = get_status(outgoing_call_id)
    if call_status['response_code'] == 200:
        # Search latest pending Incoming object
        incoming_obj = HelplineIncoming.objects.filter(from_number=call_status['to'],call_status=0).order_by('-id')
        expert_obj = HelplineExpert.objects.filter(phone_number=call_status['from'])
        if len(incoming_obj) > 0 and len(expert_obj) > 0:
            incoming_obj = incoming_obj[0]
            expert_obj = expert_obj[0]
            to_number = call_status['to']
            return (incoming_obj,expert_obj,to_number)
    return ''

def update_incoming_acknowledge_user(incoming_call_obj,acknowledge_user):
    if acknowledge_user == 0:
        incoming_call_obj.acknowledge_user = 0
    else:    
        incoming_call_obj.acknowledge_user += 1
    try:
        incoming_call_obj.save()
    except Exception as e:
        module = 'update_incoming_acknowledge_user'
        write_log(HELPLINE_LOG_FILE,module,str(e))     

# When we do not want to acknowledge User in case of call is not successfull
# then acknowledge_user parameter is more than 1
# (For cases like call generated from queue module)
def make_helpline_call(incoming_call_obj,from_number_obj,to_number,acknowledge_user=0):
    call_request_url = CALL_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
    call_response_url = CALL_RESPONSE_URL
    from_number = from_number_obj.phone_number
    # CallType is either Transactional or Promotional
    parameters = {'From':from_number,'To':to_number,'CallerId':EXOTEL_HELPLINE_NUMBER,'CallType':'trans','StatusCallback':call_response_url}
    response = requests.post(call_request_url,data=parameters)
    module = 'make_helpline_call'
    if response.status_code == 200:
        update_incoming_acknowledge_user(incoming_call_obj,acknowledge_user)
        response_tree = xml_parse.fromstring((response.text).encode('utf-8'))
        call_detail = response_tree.findall('Call')[0]
        outgoing_call_id = str(call_detail.find('Sid').text)
        outgoing_call_time = str(call_detail.find('StartTime').text)
        save_call_log(outgoing_call_id,from_number,to_number,1,outgoing_call_time)
        outgoing_obj = HelplineOutgoing(call_id=outgoing_call_id,incoming_call=incoming_call_obj,outgoing_time=outgoing_call_time,from_number=from_number_obj,to_number=to_number)
        try:
            outgoing_obj.save()    
        except Exception as e:
            # Save Errors in Logs
            write_log(HELPLINE_LOG_FILE,module,str(e))
    else:
        # Enter in Log
        log = 'Status Code: %s (Parameters: %s)'%(str(response.status_code),parameters)
        write_log(HELPLINE_LOG_FILE,module,log)

def send_helpline_sms(from_number,to_number,sms_body):
    sms_request_url = SMS_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
    parameters = {'From':from_number,'To':to_number,'Body':sms_body,'Priority':'high'}
    response = requests.post(sms_request_url,data=parameters)
    if response.status_code == 200:
        response_tree = xml_parse.fromstring((response.text).encode('utf-8'))
        sms_detail = response_tree.findall('SMSMessage')[0]
        sms_id = str(sms_detail.find('Sid').text)
        sent_time = str(sms_detail.find('DateCreated').text)
        save_sms_log(sms_id,from_number,to_number,sms_body,sent_time)
    else:
        module = 'send_helpline_sms'
        log = "Status Code: %s (Parameters: %s)"%(str(response.status_code),parameters)
        write_log(HELPLINE_LOG_FILE,module,log)
 
def connect_to_app(to_number,app_id):
    app_request_url = APP_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
    app_url = APP_URL%(app_id,)
    parameters = {'From':to_number,'CallerId':EXOTEL_HELPLINE_NUMBER,'CallType':'trans','Url':app_url}
    response = requests.post(app_request_url,data=parameters)
    module = 'connect_to_app'
    log = "App Id: %s Status Code: %s (Response text: %s)"%(app_id,str(response.status_code),str(response.text))
    write_log(HELPLINE_LOG_FILE,module,log)
    
def fetch_info_of_incoming_call(request):
    call_id = str(request.GET.getlist('CallSid')[0])
    farmer_number = str(request.GET.getlist('From')[0])
    dg_number = str(request.GET.getlist('To')[0])
    incoming_time = str(request.GET.getlist('StartTime')[0])
    return (call_id,farmer_number,dg_number,incoming_time)

def update_incoming_obj(incoming_obj,call_status,recording_url,expert_obj,resolved_time):
    incoming_obj.call_status = call_status
    incoming_obj.recording_url = recording_url
    incoming_obj.resolved_by = expert_obj
    incoming_obj.resolved_time = resolved_time
    try:
        incoming_obj.save()
    except Exception as e:
        # if error in updating incoming object then Log
        module = 'update_incoming_obj'
        write_log(HELPLINE_LOG_FILE,module,str(e))

def send_acknowledge(incoming_call_obj):
    if incoming_call_obj.acknowledge_user == 0:
        return 0
    else:
        return 1

def send_voicemail(farmer_number,OFF_HOURS_VOICEMAIL_APP_ID):
    time.sleep(2)
    connect_to_app(farmer_number,OFF_HOURS_VOICEMAIL_APP_ID)

def connect_to_broadcast(to_number,broadcast_number,app_id):
    app_request_url = APP_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
    app_url = APP_URL%(app_id,)
    response_url = BROADCAST_RESPONSE_URL
    # Here From parameter is actually user number to whom we want to connect.
    parameters = {'From':to_number,'CallerId':broadcast_number,'CallType':'trans','Url':app_url,'StatusCallback':response_url}
    response = requests.post(app_request_url,data=parameters)
    module = 'connect_to_broadcast'
    log = "App Id: %s Status Code: %s (Response text: %s)"%(app_id,str(response.status_code),str(response.text))
    write_log(HELPLINE_LOG_FILE,module,log)
