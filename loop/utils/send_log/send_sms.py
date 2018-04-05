from threading import Thread

__author__ = 'Lokesh'

import json
from dg.settings import TEXTLOCAL_API_KEY
from loop.config import sms_text
from loop.models import CombinedTransaction, DayTransportation, SMS_STATE
from loop_ivr.utils.config import TEXT_LOCAL_SINGLE_SMS_API, SMS_SENDER_NAME, RECEIPT_URL

from django.db.models import Count, Sum, Avg, Q, F
import requests
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey
import ast
import datetime

class UserDoesNotExist(Exception):
    pass

@csrf_exempt
def deprecated_send_sms(request):
    return HttpResponse("0")

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
                if requesting_loop_user.village.block.district.state.country.country_name == 'India':
                    preferred_language = requesting_loop_user.preferred_language.notation
                    transactions_to_consider = CombinedTransaction.objects.filter(user_created_id=user.id, payment_sms=0,
                                                                                  status=1, date__gt=str(datetime.datetime.now().date() - datetime.timedelta(days=7)))

                    transportations_to_consider = DayTransportation.objects.filter(user_created_id=user.id, payment_sms=0, date__gt=str(datetime.datetime.now().date() - datetime.timedelta(days=7)))

                    transportations_to_consider_for_ct = DayTransportation.objects.filter(user_created_id=user.id, date__gt=str(datetime.datetime.now().date() - datetime.timedelta(days=7)))
                    if requesting_loop_user.partner.id != 2:
                        helpline_no = requesting_loop_user.partner.helpline_number
                    else:
                        helpline_no = requesting_loop_user.village.block.district.state.helpline_number
                    Thread(target=transactions_sms,
                           args=[requesting_loop_user, transactions_to_consider, preferred_language,
                                 transportations_to_consider_for_ct, helpline_no]).start()

                    Thread(target=transportations_sms,
                           args=[requesting_loop_user, transportations_to_consider, preferred_language]).start()
                else:
                    return HttpResponse("0")
            except Exception as e:
                pass
    return HttpResponse("0")


def transactions_sms(user, transactions, language, transportations, helpline_num):
    try:
        
        single_farmer_date_message = {}
        transactions_list = []
        for transaction in transactions:
            transactions_list.append(transaction)
            if (transaction.date, transaction.farmer.phone,
                transaction.farmer.name) not in single_farmer_date_message.keys():

                CropLanguage = get_model('loop', 'CropLanguage')
                Language = get_model('loop', 'Language')
                VehicleLanguage = get_model('loop', 'VehicleLanguage')

                lang_code = Language.objects.get(notation=language)
                language_crop = CropLanguage.objects.get(crop=transaction.crop, language=lang_code.id)

                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.name)] = {
                    (language_crop.crop_name, transaction.price): {'quantity': transaction.quantity,
                                                                   'amount': transaction.amount}}
                single_farmer_date_message[
                    (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transaction_id'] = [
                    transaction.id]

                farmer_specific_transportations = transportations.filter(date=transaction.date,
                                                                         mandi=transaction.mandi.id)
                for farmer_specific_transport in farmer_specific_transportations:
                    language_vehicle = VehicleLanguage.objects.get(
                        vehicle=farmer_specific_transport.transportation_vehicle.vehicle, language=lang_code.id)
                    if 'transport' not in single_farmer_date_message[(transaction.date, transaction.farmer.phone,
                                                                      transaction.farmer.name)].keys():
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'] = {}
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'] = {
                            transaction.mandi.mandi_name: [(
                                                               language_vehicle.vehicle_name,
                                                               farmer_specific_transport.transportation_cost)]}
                    elif transaction.mandi.mandi_name in single_farmer_date_message[
                        (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport']:
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'][
                            transaction.mandi.mandi_name].append((
                            language_vehicle.vehicle_name,
                            farmer_specific_transport.transportation_cost))
                    else:
                        single_farmer_date_message[
                            (transaction.date, transaction.farmer.phone, transaction.farmer.name)]['transport'][
                            transaction.mandi.mandi_name] = [(
                                                                 language_vehicle.vehicle_name,
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
            if 'transport' in value.keys():
                message = make_transaction_vehicle_sms(message, value['transport'])

            helpline_num.encode('utf-8')
            message = ('%s\n%s: %s') % (
            message, sms_text['helpline_no'][language].encode('utf-8'), helpline_num.encode('utf-8'))

            status_code = 0
            sms_id = None

            transaction_to_update = transactions.filter(id__in=single_farmer_date_message[key]['transaction_id'])
            for trans in transaction_to_update:
                trans.payment_sms=SMS_STATE['S'][0]
                trans.save()
            SmsLog = get_model('loop', 'SmsLog')
            smslog_obj = SmsLog(sms_body=message ,contact_no=farmer_no, person_type=0, model_ids = str(single_farmer_date_message[key]['transaction_id']))
            smslog_obj.save()

            sms_response = send_sms_using_textlocal(farmer_no, message, smslog_obj.id)
            if sms_response['status'] == "success":
                status_code = 1
                sms_id = sms_response['messages'][0]['id']
                for trans in transaction_to_update:
                    trans.payment_sms=SMS_STATE['F'][0]
                    trans.payment_sms_id=sms_response['messages'][0]['id']
                    trans.save()

            smslog_obj.text_local_id = sms_id
            smslog_obj.status = status_code
            smslog_obj.save()

    except Exception as e:
        pass


def make_transaction_vehicle_sms(message, vehicle_details):
    for entry in vehicle_details:
        message = ('%s\n%s') % (message, entry.encode('utf-8'))
        for vehicle in vehicle_details[entry]:
            message = ('%s \n%s:%s') % (message, vehicle[0].encode('utf-8'), str(vehicle[1]))
    return message


def transportations_sms(user, transportations, language):
    try:
        single_transporter_details = {}
        VehicleLanguage = get_model('loop', 'VehicleLanguage')
        Language = get_model('loop', 'Language')
        for dt in transportations:
            lang_code = Language.objects.get(notation=language)
            lang_vehicle = VehicleLanguage.objects.get(vehicle = dt.transportation_vehicle.vehicle, language=lang_code.id)

            if (dt.transportation_vehicle.transporter.transporter_name,
                dt.transportation_vehicle.transporter.transporter_phone,
                dt.date) in single_transporter_details.keys():

                transporter_wise_data = single_transporter_details[(
                    dt.transportation_vehicle.transporter.transporter_name,
                    dt.transportation_vehicle.transporter.transporter_phone,
                    dt.date)]

                transporter_wise_data['dt'].append(
                    (dt.mandi.mandi_name, lang_vehicle.vehicle_name, dt.transportation_cost))
                transporter_wise_data['dt_id'].append(dt.id)

            else:
                single_transporter_details[(dt.transportation_vehicle.transporter.transporter_name,
                                            dt.transportation_vehicle.transporter.transporter_phone, dt.date)] = {
                'dt': [
                    (dt.mandi.mandi_name, lang_vehicle.vehicle_name, dt.transportation_cost)],
                'dt_id': [dt.id]}

        for entity in single_transporter_details:
            transporter_num = entity[1]
            message = ('%s (%s)') % (sms_text['loop_receipt'][language].encode('utf-8'), entity[2])
            for elements in single_transporter_details[entity]['dt']:
                message = ('%s\n %s %s %s %s %s %s') % (
                    message, elements[0].encode('utf-8'), sms_text['ke_liye'][language].encode('utf-8'),
                    elements[1].encode('utf-8'), sms_text['ka kiraya'][language].encode('utf-8'),
                    sms_text['currency'][language].encode('utf-8'),
                    str(elements[2]))
            transportations_to_update = transportations.filter(id__in=single_transporter_details[entity]['dt_id'])
            for trans in transportations_to_update:
                trans.payment_sms=SMS_STATE['S'][0]
                trans.save()
            SmsLog = get_model('loop', 'SmsLog')
            smslog_obj = SmsLog(sms_body=message, contact_no=transporter_num, person_type=1,model_ids = str(single_transporter_details[entity]['dt_id']))
            smslog_obj.save()

            sms_response = send_sms_using_textlocal(transporter_num, message, smslog_obj.id)
            status_code = 0
            sms_id = None

            if sms_response['status'] == "success":
                status_code = 1
                sms_id = sms_response['messages'][0]['id']
                for trans in transportations_to_update:
                    trans.payment_sms=SMS_STATE['F'][0]
                    trans.payment_sms_id=sms_response['messages'][0]['id']
                    trans.save()

            smslog_obj.text_local_id = sms_id
            smslog_obj.status = status_code
            smslog_obj.save()

    except Exception as e:
        print e


def make_transaction_sms(key, farmer_name, aggregator, value, language):
    message = ('%s %s \n%s %s\n%s %s') % (sms_text['loop_receipt'][language].encode('utf-8'), str(key[0]),
                                          sms_text['farmer'][language].encode('utf-8'), farmer_name,
                                          sms_text['aggregator'][language].encode('utf-8'),
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


def send_sms_using_textlocal(farmer_no, sms_body, custom_id):
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers': farmer_no,
                  'message': sms_body, 'test': 'false', 'unicode': 'true', 'custom': custom_id, 'receipt_url': RECEIPT_URL}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    return response_text

@csrf_exempt
def sms_receipt_from_txtlcl(request):
    if request.method == 'POST':
        SmsLog = get_model('loop', 'SmsLog')
        entries_from_smslog = SmsLog.objects.get(id=request.POST['customID'])
        if entries_from_smslog.person_type == 0:
            entries = ast.literal_eval(entries_from_smslog.model_ids)
            CombinedTransaction = get_model('loop', 'CombinedTransaction')
            transactions = CombinedTransaction.objects.filter(id__in=entries)
            transactions.update(payment_sms=SMS_STATE[request.POST['status']][0])
        elif entries_from_smslog.person_type == 1:
            entries = ast.literal_eval(entries_from_smslog.model_ids)
            DayTransportation = get_model('loop', 'DayTransportation')
            day_transportations = DayTransportation.objects.filter(id__in=entries)
            day_transportations.update(payment_sms=SMS_STATE[request.POST['status']][0])

    return HttpResponse("0")
