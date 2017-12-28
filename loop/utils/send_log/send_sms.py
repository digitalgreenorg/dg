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

                transactions_sms(requesting_loop_user, transactions_to_consider, preferred_language,
                                 transportations_to_consider)
                transportations_sms(requesting_loop_user, transportations_to_consider, preferred_language)

            except Exception as e:
                print e
                # raise UserDoesNotExist(
                # 'User with id: ' + str(user.id) + 'does not exist')

    return HttpResponse("0")


def transactions_sms(user, transactions, language, transportations):
    try:
        single_farmer_date_message = {}
        transactions_list = []
        for transaction in transactions:
            transactions_list.append(transaction)
            if (transaction.date, transaction.farmer.phone,
                transaction.farmer.name) not in single_farmer_date_message.keys():

                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.name)] = {
                    (transaction.crop.crop_name, transaction.price): {'quantity': transaction.quantity,
                                                                      'amount': transaction.amount}}
                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transaction_id'] = [
                    transaction.id]

                farmer_specific_transportations = transportations.filter(date=transaction.date,
                                                                         mandi=transaction.mandi.id)
                for farmer_specific_transport in farmer_specific_transportations:
#                    print single_farmer_date_message
                    if 'transport' not in single_farmer_date_message[(transaction.date, transaction.farmer.phone,
                                                                      transaction.farmer.name)].keys():
#                        print 'inside if'
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'] = {
                            transaction.mandi.mandi_name_en: [(
                                                                  farmer_specific_transport.transportation_vehicle.vehicle.vehicle_name_en,
                                                                  farmer_specific_transport.transportation_cost)]}
#                        print "done if"
                    elif transaction.mandi.mandi_name_en in single_farmer_date_message[
                        (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport']:
#                        print "inside elif"
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'][
                            transaction.mandi.mandi_name_en].append((
                            farmer_specific_transport.transportation_vehicle.vehicle.vehicle_name_en,
                            farmer_specific_transport.transportation_cost))
                    else:
#                        print "inside else"
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'][
                            transaction.mandi.mandi_name_en] = [(
                            farmer_specific_transport.transportation_vehicle.vehicle.vehicle_name_en,
                            farmer_specific_transport.transportation_cost)]
 #               print 'done for'
            else:
                farmer_level_transaction = single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.name)]

                if (transaction.crop.crop_name, transaction.price) in farmer_level_transaction:
                    farmer_level_transaction[(transaction.crop.crop_name, transaction.price)][
                        'quantity'] += transaction.quantity
                    farmer_level_transaction[(transaction.crop.crop_name, transaction.price)][
                        'amount'] += transaction.amount
                else:
                    farmer_level_transaction[(transaction.crop.crop_name, transaction.price)] = {
                        'quantity': transaction.quantity, 'amount': transaction.amount}

#                print farmer_level_transaction
                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transaction_id'].append(
                    transaction.id)

        print len(single_farmer_date_message)
        for key, value in single_farmer_date_message.iteritems():
            # print "______________________________________________________"
            # print "NEW FARMER CASE =================" + str(key[1])
            # print key
            # print value
#            print key
            farmer_no = key[1]
            farmer_name = key[2].encode('utf-8')
            message = make_transaction_sms(key, farmer_name, user.name, value, language)
#            print message
            message = make_transaction_vehicle_sms(message, value['transport'])
            # print message

            # print "*************************************"
            sms_response = send_sms_using_textlocal(farmer_no, message)
            # print sms_response
            if sms_response['status'] == "success":
                print "We are successful"
                # transaction_to_update = transactions.filter(id__in=single_farmer_date_message[key]['transaction_id'])
                # transaction_to_update.update(payment_sms=False, payment_sms_id=sms_response['messages'][0]['id'])
    except Exception as e:
        print e


def make_transaction_vehicle_sms(message, vehicle_details):
    # print "inside mtvs"
    # print vehicle_details
    # print message
    for entry in vehicle_details:
        # print entry
        message = ('%s\n%s') % (message, entry.encode('utf-8'))
        for vehicle in vehicle_details[entry]:
            # print vehicle
            message = ('%s \n%s:%s') % (message, vehicle[0].encode('utf-8'), str(vehicle[1]))

    return message


def transportations_sms(user, transportations, language):
    return "heelo"


def make_transaction_sms(key, farmer_name, aggregator, value, language):
    # message = "hello we are testing"
    # print "_________________________________"
    # print key
    # print "#################################"
    # print value
    # farmer_name = unicode(key[2], "utf-8")
    # print "hellp"
    #    aggregator_name = unicode(aggregator)
    #    print message
    # print "yoyoyoyyo"
    # print language
    # print transaction_sms['farmer'][language].encode('utf-8')
    # print transaction_sms['loop_receipt'][language].encode('utf-8')
    # print transaction_sms['aggregator'][language]
    # message = ('%s %s \n %s %s\n %s %s') % (transaction_sms['loop_receipt'][language].encode('utf-8'), str(key[0]), transaction_sms['farmer'][language].encode('utf-8'), str(key[2]), transaction_sms['aggregator'][language].encode('utf-8'), str(aggregator))
    message = ('%s %s \n%s %s\n%s %s') % (transaction_sms['loop_receipt'][language].encode('utf-8'), str(key[0]),
                                          transaction_sms['farmer'][language].encode('utf-8'), farmer_name,
                                          transaction_sms['aggregator'][language].encode('utf-8'),
                                          aggregator.encode('utf-8'))
    # print "_+_+_+_+_++_+_+_+_+_+_+_+_+_+__"
    # print value
    for row, detail in value.iteritems():
        # print type(row)
        # print len(row)
        if isinstance(row, tuple) and len(row) == 2:
            # print "I m inside IF"
            # print message
            # print row[0].encode('utf-8')
            # print str(row[1])
            # print str(detail['quantity'])
            # print str(detail['amount'])
            message = ('%s\n%s: %s x %s=%s') % (
                message, row[0].encode('utf-8'), str(row[1]), str(detail['quantity']), str(detail['amount']))
    #         print message
    # print message
    return message


def make_transportation_sms(key, farmer_name, aggregator, value):
    # message = "hello we are testing"
    # print "_________________________________"
    # print key
    # print "#################################"
    # print value
    # farmer_name = unicode(key[2], "utf-8")
    # print "hellp"
    #    aggregator_name = unicode(aggregator)
    #    print message
    message = ('%s (%s)\n%s - %s\n%s - %s') % (
        "Loop Receipt", str(key[0]), "Kisan", str(key[2]), "Jamakarta", aggregator)
    for row, detail in value.iteritems():
        if type(row) == 'tuple' and len(row) == 2:
            message = ('%s\n%s: %s x %s=%s') % (
                message, row[0], str(row[1]), str(detail['quantity']), str(detail['amount']))
    return message


def send_sms_using_textlocal(farmer_no, sms_body):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    # headers = {'content-type': 'application/json' }
    # parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers':user_no,
    # 'message': sms_body, 'receipt_url': PUSH_MESSAGE_SMS_RESPONSE_URL, 'unicode': 'true',
    # 'custom': recipient_custom_id}
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