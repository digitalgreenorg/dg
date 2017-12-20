import json
from dg.settings import TEXTLOCAL_API_KEY
from loop.models import CombinedTransaction, DayTransportation
from loop_ivr.utils.config import TEXT_LOCAL_SINGLE_SMS_API, SMS_SENDER_NAME, loop_receipt, kisan, jamakarta
from django.db.models import Count, Sum, Avg, Q, F


__author__ = 'Lokesh'

import requests
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey

class UserDoesNotExist(Exception):
    pass

@csrf_exempt
def send_sms(request):
    if request.method == 'POST':
        apikey = request.POST['ApiKey']
        timestamp = request.POST['timestamp']
        if timestamp:
            try:
                apikey_object = ApiKey.objects.get(key=apikey)
                user = apikey_object.user
            except Exception:
                return HttpResponse("-1", status=401)
            LoopUser = get_model('loop', 'LoopUser')
            CombinedTransaction = get_model('loop', 'CombinedTransaction')
            DayTransportation = get_model('loop', 'DayTransportation')
            try:
                requesting_loop_user = LoopUser.objects.get(user_id=user.id)
                preferred_language = requesting_loop_user.preferred_language.notation
                transactions_to_consider = CombinedTransaction.objects.filter(time_modified__gte=timestamp, user_created_id = user.id, payment_sms = 0)

                transportations_to_consider = DayTransportation.objects.filter(time_modified__gte=timestamp, user_created_id = user.id)

                print transportations_to_consider
                print len(transportations_to_consider)

                transactions_to_consider_grouped = transactions_to_consider.values('date', 'farmer', 'farmer__name' ,'farmer__phone', 'mandi', 'mandi__mandi_name', 'crop', 'crop__crop_name' ,'price').annotate(Sum('quantity'),Sum('amount'))

                single_farmer_date_message = {}

                for transaction in transactions_to_consider_grouped:
                    if (transaction['date'], transaction['farmer__phone'], transaction['farmer__name']) not in single_farmer_date_message.keys():
                        single_farmer_date_message[(transaction['date'], transaction['farmer__phone'], transaction['farmer__name'])] = {transaction['crop__crop_name'] : {transaction['price'] :[transaction['quantity__sum'], transaction['amount__sum']]}}
                    else:
                        if transaction['crop__crop_name'] in single_farmer_date_message[(transaction['date'], transaction['farmer__phone'], transaction['farmer__name'])]:
                            single_farmer_date_message[(transaction['date'], transaction['farmer__phone'], transaction['farmer__name'])][transaction['crop__crop_name']][transaction['price']] = [transaction['quantity__sum'], transaction['amount__sum']]
                        else:
                            single_farmer_date_message[(transaction['date'], transaction['farmer__phone'], transaction['farmer__name'])][transaction['crop__crop_name']] = {transaction['price']: [transaction['quantity__sum'], transaction['amount__sum']]}

                for key, value in single_farmer_date_message.iteritems():
                    farmer_no = key[1]
                    print "akaad"
                    farmer_name = key[2].encode("utf-8")
                    print "bhaabhahbahbakaad"
                    message = make_sms(key, farmer_name, requesting_loop_user.name_en, value)
                    send_sms_using_textlocal(farmer_no, message)

            except Exception as e:
                print e
                # raise UserDoesNotExist(
                #     'User with id: ' + str(user.id) + 'does not exist')

    return HttpResponse("0")

def make_sms(key, farmer_name, aggregator, value):
    message = "hello we are testing"
    # print "_________________________________"
    # print key
    # print "#################################"
    # print value
#    farmer_name = unicode(key[2], "utf-8")
#    print "hellp"
#    aggregator_name = unicode(aggregator)
#    print message
    message = ('%s (%s)\n%s - %s\n%s - %s')%(loop_receipt, key[0], kisan, key[1], jamakarta, aggregator)
    return message

def send_sms_using_textlocal(farmer_no, sms_body):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    #headers = {'content-type': 'application/json' }
    # parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers':user_no,
    #                 'message': sms_body, 'receipt_url': PUSH_MESSAGE_SMS_RESPONSE_URL, 'unicode': 'true',
    #                 'custom': recipient_custom_id}
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers':farmer_no,
                     'message': sms_body, 'test': 'true', 'unicode': 'true'}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    if response_text['status'] == 'success':
        print "we are happy"
        print response_text
        message_id = ','.join([str(message["id"]) for message in response_text['messages']])
        # if price_info_incoming_obj != None:
        #     if price_info_incoming_obj.textlocal_sms_id == None:
        #         price_info_incoming_obj.textlocal_sms_id = message_id
        #     else:
        #         price_info_incoming_obj.textlocal_sms_id += ',' + message_id
    elif response_text['status'] == 'failure':
        print "we are sad"
        print response_text
        # module = 'send_sms_using_textlocal'
        # if price_info_incoming_obj != None:
        #     log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj.id))
        # else:
        #     log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj))
        # write_log(LOG_FILE,module,log)
