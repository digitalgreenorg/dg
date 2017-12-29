__author__ = 'Lokesh'

import json
from dg.settings import TEXTLOCAL_API_KEY
from loop.config import transaction_sms
from loop.models import CombinedTransaction, DayTransportation
from loop_ivr.utils.config import TEXT_LOCAL_SINGLE_SMS_API, SMS_SENDER_NAME, loop_receipt, kisan, jamakarta
from django.db.models import Count, Sum, Avg, Q, F
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

                transportations_to_consider = DayTransportation.objects.filter(
                    user_created_id=user.id)

                helpline_no = requesting_loop_user.village.block.district.state.helpline_number

                transactions_sms(requesting_loop_user, transactions_to_consider, preferred_language,
                                 transportations_to_consider, helpline_no)
                transportations_sms(requesting_loop_user, transportations_to_consider, preferred_language)

            except Exception as e:
                print e
    return HttpResponse("0")


def transactions_sms(user, transactions, language, transportations, helpline_num):
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
                    if 'transport' not in single_farmer_date_message[(transaction.date, transaction.farmer.phone,
                                                                      transaction.farmer.name)].keys():
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'] = {
                            transaction.mandi.mandi_name_en: [(
                                                                  farmer_specific_transport.transportation_vehicle.vehicle.vehicle_name_en,
                                                                  farmer_specific_transport.transportation_cost)]}
                    elif transaction.mandi.mandi_name_en in single_farmer_date_message[
                        (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport']:
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'][
                            transaction.mandi.mandi_name_en].append((
                            farmer_specific_transport.transportation_vehicle.vehicle.vehicle_name_en,
                            farmer_specific_transport.transportation_cost))
                    else:
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'][
                            transaction.mandi.mandi_name_en] = [(
                                                                    farmer_specific_transport.transportation_vehicle.vehicle.vehicle_name_en,
                                                                    farmer_specific_transport.transportation_cost)]
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

                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transaction_id'].append(
                    transaction.id)

        for key, value in single_farmer_date_message.iteritems():
            farmer_no = key[1]
            farmer_name = key[2].encode('utf-8')
            message = make_transaction_sms(key, farmer_name, user.name, value, language)
            message = make_transaction_vehicle_sms(message, value['transport'])
            helpline_num.encode('utf-8')
            message = ('%s\n%s: %s') % (
            message, transaction_sms['helpline_no'][language].encode('utf-8'), helpline_num.encode('utf-8'))
            sms_response = send_sms_using_textlocal(farmer_no, message)
            if sms_response['status'] == "success":
                transaction_to_update = transactions.filter(id__in=single_farmer_date_message[key]['transaction_id'])
                transaction_to_update.update(payment_sms=True, payment_sms_id=sms_response['messages'][0]['id'])
                status_code=1

            SmsLog = get_model('loop', 'SmsLog')
            smslog_obj = SmsLog(sms_body=message, text_local_id=sms_response['messages'][0]['id'], contact_no=farmer_no, person_type=0, status=status_code)
            smslog_obj.save()

    except Exception as e:
        print e


def make_transaction_vehicle_sms(message, vehicle_details):
    for entry in vehicle_details:
        message = ('%s\n%s') % (message, entry.encode('utf-8'))
        for vehicle in vehicle_details[entry]:
            message = ('%s \n%s:%s') % (message, vehicle[0].encode('utf-8'), str(vehicle[1]))
    return message


def transportations_sms(user, transportations, language):
    return "heelo"


def make_transaction_sms(key, farmer_name, aggregator, value, language):
    message = ('%s %s \n%s %s\n%s %s') % (transaction_sms['loop_receipt'][language].encode('utf-8'), str(key[0]),
                                          transaction_sms['farmer'][language].encode('utf-8'), farmer_name,
                                          transaction_sms['aggregator'][language].encode('utf-8'),
                                          aggregator.encode('utf-8'))
    for row, detail in value.iteritems():
        if isinstance(row, tuple) and len(row) == 2:
            message = ('%s\n%s: %s x %s=%s') % (
                message, row[0].encode('utf-8'), str(row[1]), str(detail['quantity']), str(detail['amount']))
    return message


def make_transportation_sms(key, farmer_name, aggregator, value):
    message = ('%s (%s)\n%s - %s\n%s - %s') % (
        "Loop Receipt", str(key[0]), "Kisan", str(key[2]), "Jamakarta", aggregator)
    for row, detail in value.iteritems():
        if type(row) == 'tuple' and len(row) == 2:
            message = ('%s\n%s: %s x %s=%s') % (
                message, row[0], str(row[1]), str(detail['quantity']), str(detail['amount']))
    return message


def send_sms_using_textlocal(farmer_no, sms_body):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer_no,
                  'message': sms_body, 'test': 'false', 'unicode': 'true'}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    if response_text['status'] == 'success':
        print "we are happy"
        # print response_text
        #        message_id = ','.join([str(message["id"]) for message in response_text['messages']])
        # if price_info_incoming_obj != None:
        #     if price_info_incoming_obj.textlocal_sms_id == None:
        #         price_info_incoming_obj.textlocal_sms_id = message_id
        #     else:
        #         price_info_incoming_obj.textlocal_sms_id += ',' + message_id
    elif response_text['status'] == 'failure':
        print "we are sad"
    # print response_text
    # module = 'send_sms_using_textlocal'
    # if price_info_incoming_obj != None:
    #     log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj.id))
    # else:
    #     log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj))
    # write_log(LOG_FILE,module,log)
    return response_text