import json
from dg.settings import TEXTLOCAL_API_KEY
from loop.config import transaction_sms
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
                transactions_to_consider = CombinedTransaction.objects.filter(time_modified__gte=timestamp,
                                                                              user_created_id=user.id, payment_sms=0,
                                                                              status=1)

                transportations_to_consider = DayTransportation.objects.filter(time_modified__gte=timestamp,
                                                                               user_created_id=user.id)

                transactions_sms(requesting_loop_user, transactions_to_consider)
                transportations_sms(requesting_loop_user, transportations_to_consider)

            except Exception as e:
                print e
                # raise UserDoesNotExist(
                # 'User with id: ' + str(user.id) + 'does not exist')

    return HttpResponse("0")

def transactions_sms(user, transactions, language):
    try:
        single_farmer_date_message = {}
        transactions_list = []
        for transaction in transactions:
            transactions_list.append(transaction)
            if (transaction.date, transaction.farmer.phone,
                transaction.farmer.id) not in single_farmer_date_message.keys():
                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.id)] = {
                    (transaction.crop.crop_name, transaction.price): {'quantity': transaction.quantity,
                                                                      'amount': transaction.amount}}
                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.id)]['transaction_id'] = [
                    transaction.id]
            else:
                farmer_level_transaction = single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.id)]

                if (transaction.crop.crop_name, transaction.price) in farmer_level_transaction:
                    farmer_level_transaction[(transaction.crop.crop_name, transaction.price)][
                        'quantity'] += transaction.quantity
                    farmer_level_transaction[(transaction.crop.crop_name, transaction.price)][
                        'amount'] += transaction.amount
                else:
                    farmer_level_transaction[(transaction.crop.crop_name, transaction.price)] = {
                    'quantity': transaction.quantity, 'amount': transaction.amount}
                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.id)]['transaction_id'].append(
                    transaction.id)
        for key, value in single_farmer_date_message.iteritems():
            farmer_no = key[1]
            farmer_name = str(key[2])
            message = make_transaction_sms(key, farmer_name, user.name_en, value, language)
            sms_response = send_sms_using_textlocal(farmer_no, message)
            if sms_response['status'] == "success":
                transaction_to_update = transactions.filter(id__in=single_farmer_date_message[key]['transaction_id'])
                transaction_to_update.update(payment_sms=True, payment_sms_id=sms_response['messages'][0]['id'])
    except Exception as e:
        print e

def transportations_sms(user, transportations):
    return "heelo"



def make_transaction_sms(key, farmer_name, aggregator, value, language):
#    message = "hello we are testing"
    # print "_________________________________"
    # print key
    # print "#################################"
    # print value
    # farmer_name = unicode(key[2], "utf-8")
    #    print "hellp"
    #    aggregator_name = unicode(aggregator)
    #    print message
    message = ('%s (%s)\n%s - %s\n%s - %s') % (transaction_sms['loop_receipt'][language], str(key[0]), transaction_sms['farmer'][language], str(key[2]), transaction_sms['aggregator']['language'], aggregator)
    for row, detail in value.iteritems():
        if type(row) == 'tuple' and len(row) == 2:
            message = ('%s\n%s: %s x %s=%s')%(message, row[0], str(row[1]), str(detail['quantity']), str(detail['amount']))
    return message

def make_transportation_sms(key, farmer_name, aggregator, value):
#    message = "hello we are testing"
    # print "_________________________________"
    # print key
    # print "#################################"
    # print value
    # farmer_name = unicode(key[2], "utf-8")
    #    print "hellp"
    #    aggregator_name = unicode(aggregator)
    #    print message
    message = ('%s (%s)\n%s - %s\n%s - %s') % ("Loop Receipt", str(key[0]), "Kisan", str(key[2]), "Jamakarta", aggregator)
    for row, detail in value.iteritems():
        if type(row) == 'tuple' and len(row) == 2:
            message = ('%s\n%s: %s x %s=%s')%(message, row[0], str(row[1]), str(detail['quantity']), str(detail['amount']))
    return message


def send_sms_using_textlocal(farmer_no, sms_body):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    # headers = {'content-type': 'application/json' }
    # parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers':user_no,
    #                 'message': sms_body, 'receipt_url': PUSH_MESSAGE_SMS_RESPONSE_URL, 'unicode': 'true',
    #                 'custom': recipient_custom_id}
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer_no,
                  'message': sms_body, 'test': 'false', 'unicode': 'true'}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    if response_text['status'] == 'success':
        print "we are happy"
#        print response_text
        message_id = ','.join([str(message["id"]) for message in response_text['messages']])
        # if price_info_incoming_obj != None:
        #     if price_info_incoming_obj.textlocal_sms_id == None:
        #         price_info_incoming_obj.textlocal_sms_id = message_id
        #     else:
        #         price_info_incoming_obj.textlocal_sms_id += ',' + message_id
    elif response_text['status'] == 'failure':
        print "we are sad"
#        print response_text
        # module = 'send_sms_using_textlocal'
        # if price_info_incoming_obj != None:
        #     log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj.id))
        # else:
        #     log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj))
        # write_log(LOG_FILE,module,log)
    return response_text