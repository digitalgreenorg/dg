# -*- coding: utf-8 -*-
__author__ = 'Vikas Saini'

import requests
import time
import itertools
import MySQLdb
import json
from datetime import datetime, timedelta
from pytz import timezone
import xml.etree.ElementTree as xml_parse

from django.db.models import get_model, Sum

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, DATABASES, TEXTLOCAL_API_KEY

from loop.models import Crop, Mandi, CropLanguage, CombinedTransaction
from loop.utils.ivr_helpline.helpline_data import SMS_REQUEST_URL, CALL_REQUEST_URL, APP_REQUEST_URL, \
    APP_URL
from loop.helpline_view import write_log

from loop_ivr.utils.marketinfo import raw_sql, get_query
from loop_ivr.utils.config import *
from loop_ivr.models import PriceInfoLog, PriceInfoIncoming

from loop_ivr.outliers.removal import remove_crop_outliers
import logging
logger = logging.getLogger(__name__)

def make_market_info_call(caller_number, dg_number, incoming_time, incoming_call_id, call_source):
    app_request_url = APP_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
    app_id = MARKET_INFO_APP
    app_url = APP_URL%(app_id,)
    call_response_url = MARKET_INFO_CALL_RESPONSE_URL
    parameters = {'From':caller_number,'CallerId':dg_number,'CallType':'trans','Url':app_url,'StatusCallback':call_response_url}
    #parameters = {'From':caller_number,'CallerId':dg_number,'CallType':'trans','Url':app_url}
    response = requests.post(app_request_url,data=parameters)
    module = 'make_market_info_call'
    if response.status_code == 200:
        response_tree = xml_parse.fromstring((response.text).encode('utf-8'))
        call_detail = response_tree.findall('Call')[0]
        outgoing_call_id = str(call_detail.find('Sid').text)
        outgoing_call_time = str(call_detail.find('StartTime').text)
        price_info_incoming_obj = PriceInfoIncoming(call_id=outgoing_call_id, from_number=caller_number,
                                    to_number=dg_number, incoming_time=outgoing_call_time, call_source=call_source)
    else:
        # Enter in Log
        price_info_incoming_obj = PriceInfoIncoming(call_id=incoming_call_id, from_number=caller_number,
                                        to_number=dg_number, incoming_time=incoming_time, info_status=0, call_source=call_source)
        log = 'Status Code: %s (Parameters: %s)'%(str(response.status_code),parameters)
        write_log(LOG_FILE,module,log)
        if response.status_code == 403:
            send_info_using_textlocal(caller_number, DND_MESSAGE, price_info_incoming_obj)
    try:
        price_info_incoming_obj.save()
    except Exception as e:
        # Save Errors in Logs
        write_log(LOG_FILE,module,str(e))

def send_sms(from_number,to_number,sms_body):
    sms_request_url = SMS_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
    parameters = {'From':from_number,'To':to_number,'Body':sms_body,'Priority':'high'}
    response = requests.post(sms_request_url,data=parameters)
    if response.status_code == 200:
        pass
    else:
        module = 'send_sms'
        log = "Status Code: %s (Parameters: %s)"%(str(response.status_code),parameters)
        write_log(LOG_FILE,module,log)

def get_valid_list(app_name, model_name, requested_item, farmer_number, all_flag=False):
    model = get_model(app_name, model_name)
    if model_name == 'mandi':
        # If call from Bangladesh then return Mandi of Bangladesh
        if farmer_number.startswith('01'):
            id_list = set(model.objects.filter(district__state__country_id=2).values_list('id', flat=True))
        else:
            # Only Bihar Crops and Mandi.
            id_list = set(model.objects.filter(district__state_id=1).values_list('id', flat=True))
    else:
        # For Fetch id of all crops
        #id_list = set(model.objects.values_list('id', flat=True))
        # Only fetch id of crops which have Hindi name in database,
        # because we are sharing Hindi crops code as of now.
        id_list = set(CropLanguage.objects.filter(language_id=1).values_list('crop_id', flat=True))
    requested_list = set(int(item) for item in requested_item.split('*') if item.isdigit())
    if all_flag :
        return tuple(map(int,id_list))
    else :
        return tuple(map(int,requested_list.intersection(id_list)))

def run_query(query):
    mysql_cn = MySQLdb.connect(host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'],
        user=DATABASES['default']['USER'] ,
        passwd=DATABASES['default']['PASSWORD'],
        db=DATABASES['default']['NAME'],
        charset = 'utf8',
        use_unicode = True)
    cursor = mysql_cn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def send_info(to_number, content):
    index = 0
    from_number = AGGREGATOR_SMS_NO
    while index < len(content):
        send_sms(from_number, to_number, content[index:index+1998])
        index += 1998
        time.sleep(1)

def send_sms_using_textlocal(user_no, sms_body, price_info_incoming_obj):
    # recipient_custom_id = subscription_log_obj.id
    sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
    #headers = {'content-type': 'application/json' }
    # parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers':user_no,
    #                 'message': sms_body, 'receipt_url': PUSH_MESSAGE_SMS_RESPONSE_URL, 'unicode': 'true',
    #                 'custom': recipient_custom_id}
    parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers':user_no,
                     'message': sms_body, 'unicode': 'true'}
    response = requests.post(sms_request_url, params=parameters)
    response_text = json.loads(str(response.text))
    if response_text['status'] == 'success':
        message_id = ','.join([str(message["id"]) for message in response_text['messages']])
        if price_info_incoming_obj != None:
            if price_info_incoming_obj.textlocal_sms_id == None:
                price_info_incoming_obj.textlocal_sms_id = message_id
            else:
                price_info_incoming_obj.textlocal_sms_id += ',' + message_id
            price_info_incoming_obj.save()
    elif response_text['status'] == 'failure':
        module = 'send_sms_using_textlocal'
        if price_info_incoming_obj != None:
            log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj.id))
        else:
            log = "Status Code: %s (price_info_incoming_obj_id: %s)"%(response_text['status'], str(price_info_incoming_obj))
        write_log(LOG_FILE,module,log)

def send_info_using_textlocal(user_no, content, price_info_incoming_obj=None):
    # Replace ascii next line with textlocal next line identifier (i.e. %0A)
    content = content.replace('\n','%0A')
    if price_info_incoming_obj != None:
        price_info_incoming_obj.server_response_time = datetime.now(timezone('Asia/Kolkata')).replace(tzinfo=None)
        price_info_incoming_obj.save()
    while len(content) > 0:
        # If length of content is less than 750, then send whole content once.
        if len(unicode(content,'utf-8')) < 400:
            send_sms_using_textlocal(user_no, content, price_info_incoming_obj)
            break
        # If length of content is more than 750, then devide in packets of length < 750
        # based on two new line.
        else:
            current_index = content[:750].rfind('%0A%0A')
            # If two new line not found then devide simply in chunks of 750
            if current_index < 0:
                current_index = 750
            current_content = content[:current_index]
            content = content[current_index:]
            send_sms_using_textlocal(user_no, current_content, price_info_incoming_obj)
            time.sleep(1)

def get_top_selling_crop_quantity_wise(number_of_crop, from_duration):
    crop_id_list = list(CropLanguage.objects.filter(language_id=1).values_list('crop_id', flat=True))
    crop_list = list(CombinedTransaction.objects.filter(date__gte=from_duration, crop_id__in=crop_id_list, farmer__village__block__district__state_id=1)
                .values('crop_id').annotate(total_quantity=Sum('quantity'))
                .order_by('-total_quantity').values_list('crop_id', flat=True)[:number_of_crop])
    crop_code_names = CropLanguage.objects.filter(language_id=1, crop_id__in=crop_list).values('crop_id', 'crop_name')
    return list(crop_code_names)

def get_crop_code_list(number_of_crop, selling_crop_window):
    from_date = datetime.now()-timedelta(days=selling_crop_window)
    top_selling_crops = get_top_selling_crop_quantity_wise(number_of_crop, from_date)
    crop_code_list = '\n'.join('%s - %s'%(crop['crop_name'].encode("utf-8").strip(), crop['crop_id']) for crop in top_selling_crops)
    return '\n'.join([crop_and_code_hi, crop_code_list])

def get_price_info(from_number, crop_list, mandi_list, price_info_incoming_obj, all_crop_flag, all_mandi_flag):
    price_info_list = []
    # price_info_log_list = []
    crop_mandi_comb = []
    crop_map = dict()
    mandi_map = dict()
    crop_in_hindi_map = dict()
    all_crop = Crop.objects.filter(id__in=crop_list).values('id', 'crop_name')
    all_mandi = Mandi.objects.filter(id__in=mandi_list).values('id', 'mandi_name')
    crop_in_hindi = CropLanguage.objects.filter(language_id=1, crop_id__in=crop_list).values('crop_id', 'crop_name')
    for crop in all_crop:
       crop_map[crop['id']] = crop['crop_name']
    for mandi in all_mandi:
       mandi_map[mandi['id']] = mandi['mandi_name']
    for crop in crop_in_hindi:
        crop_in_hindi_map[crop['crop_id']] = crop['crop_name']
    # Fetching price from DB
    price_info_list.append(agg_sms_initial_line_with_content)
    # price_info_list.append(AGGREGATOR_SMS_NO)
    # price_info_list.append('\n')

    query = get_query.query_for_rates(crop_list , mandi_list, date_range=3)
    result = run_query(query)
    dataframe = remove_crop_outliers(ct_data = result)

    try:
        if (not result) or dataframe is None or dataframe.empty:
            if not all_crop_flag and not all_mandi_flag:
                crop_name_list = ','.join(map(lambda crop_id: '%s (%s: %s)'%(crop_in_hindi_map.get(crop_id).encode("utf-8"),code_hi,str(crop_id)) if crop_in_hindi_map.get(crop_id) else '%s (%s: %s)'%(crop_map[crop_id].encode("utf-8"),code_hi,str(crop_id)), crop_list))
                mandi_name_list = ','.join(map(lambda mandi_id: mandi_map[mandi_id].encode("utf-8").rstrip(mandi_hi).rstrip(), mandi_list))
                no_price_message = (agg_sms_no_price_crop_mandi)%(crop_name_list, mandi_name_list)
            # If query for all Mandi
            elif all_mandi_flag:
                crop_name_list = ','.join(map(lambda crop_id: '%s (%s: %s)'%(crop_in_hindi_map.get(crop_id).encode("utf-8"),code_hi,str(crop_id)) if crop_in_hindi_map.get(crop_id) else '%s (%s: %s)'%(crop_map[crop_id].encode("utf-8"),code_hi,str(crop_id)), crop_list))
                no_price_message = ('%s : %s') % (fasal,(agg_sms_no_price_all_mandi % (crop_name_list,)))
            # If query for all crops
            else:
                no_price_message = agg_sms_no_price_available
            price_info_list.append('\n')
            price_info_list.append(no_price_message)
            crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
            price_info_list.append(('\n\n%s')%(crop_code_list,))
        else:
            prev_crop, prev_mandi, crop_name, mandi_name = -1, -1, '', ''
            for index, row in dataframe.iterrows():
                crop, mandi, date, Av_Rate, STD, PriceMax, PriceMin = row['Crop'], row['Market_Real'], row['Date'], row['Av_Ratemean'], row['STDmean'], row['Pricemax'], row['Pricemin']
                delta = PriceMax - PriceMin
                if crop != prev_crop or mandi != prev_mandi:
                    if not all_crop_flag and not all_mandi_flag:
                        crop_mandi_comb.append((crop,mandi))
                    # price_info_log_obj = PriceInfoLog(price_info_incoming=price_info_incoming_obj,
                                        # crop_id=crop, mandi_id=mandi)
                    # price_info_log_list.append(price_info_log_obj)
                    crop_name = crop_in_hindi_map.get(crop).encode("utf-8") if crop_in_hindi_map.get(crop) else crop_map[crop].encode("utf-8")
                    mandi_name = mandi_map[mandi].encode("utf-8")
                    if crop != prev_crop:
                        temp_str = ('\n%s: %s (%s: %s)\n\n%s %s\n')%(fasal,crop_name,code_hi,str(crop),mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                    else:
                        temp_str = ('\n%s %s\n')%(mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                    price_info_list.append(temp_str)
                    prev_crop, prev_mandi = crop, mandi
                if delta < 1:
                    Av_Rate = round(Av_Rate)
                    temp_str = ('%s %s: %s %s\n')%(date.strftime('%d'),MONTH_NAMES[int(date.strftime('%m'))],indian_rupee,str(Av_Rate))
                elif 1 <= delta <=2:
                    if STD <= delta * 0.4:
                        Av_Rate = round(Av_Rate)
                        temp_str = ('%s %s: %s %s\n')%(date.strftime('%d'),MONTH_NAMES[int(date.strftime('%m'))],indian_rupee,str(Av_Rate))
                    else:
                        max_price = round(PriceMax)
                        min_price = round(PriceMin)
                        temp_str = ('%s %s: %s %s-%s\n')%(date.strftime('%d'),MONTH_NAMES[int(date.strftime('%m'))],indian_rupee,str(min_price),str(max_price))
                elif delta > 2:
                    min_price = round(PriceMin) - 1
                    max_price = round(PriceMax) + 1
                    temp_str = ('%s %s: %s %s-%s\n')%(date.strftime('%d'),MONTH_NAMES[int(date.strftime('%m'))],indian_rupee,str(min_price),str(max_price))
                price_info_list.append(temp_str)
        # Save combination of crop and mandi for which data is not present in query on if query not for all mandi and crops.
        if not all_crop_flag and not all_mandi_flag:
            prev_crop, prev_mandi, crop_name, mandi_name = -1, -1, '', ''
            for crop, mandi in itertools.product(crop_list, mandi_list):
                if (crop,mandi) not in crop_mandi_comb:
                    price_info_log_obj = PriceInfoLog(price_info_incoming=price_info_incoming_obj,
                                crop_id=crop, mandi_id=mandi)
                    # price_info_log_list.append(price_info_log_obj)
                    if result and dataframe is not None and (not dataframe.empty):
                        crop_name = crop_in_hindi_map.get(crop).encode("utf-8") if crop_in_hindi_map.get(crop) else crop_map[crop].encode("utf-8")
                        mandi_name = mandi_map[mandi].encode("utf-8")
                        if crop != prev_crop:
                            prev_crop = crop
                            temp_str = ('\n%s: %s (%s: %s)\n\n%s %s\n')%(fasal,crop_name,code_hi,str(crop),mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                        else:
                            prev_mandi = mandi
                            temp_str = ('\n%s %s\n')%(mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                        price_info_list.append(temp_str)
                        price_info_list.append(agg_sms_no_price_for_combination)

        # price_info_list.append(('\n%s: %s')%(helpline_hi, EXOTEL_HELPLINE_NUMBER))
        final_result = ''.join(price_info_list)

        price_info_incoming_obj.price_result = final_result
        price_info_incoming_obj.return_result_to_app = 0
        price_info_incoming_obj.info_status = 1
        price_info_incoming_obj.save()
        send_info_using_textlocal(from_number, final_result, price_info_incoming_obj)
    except Exception as e:
        logger.debug(e)

    # If caller is calling first time then send crop code to them.
    if PriceInfoIncoming.objects.filter(from_number=from_number).count() == 1:
        crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
        if result and not dataframe.empty:
            first_time_caller_message = [first_time_caller,'\n\n', crop_code_list, '\n', remaining_crop_line]
            first_time_caller_message = ''.join(first_time_caller_message)
            #send_sms(AGGREGATOR_SMS_NO, from_number, first_time_caller_message)
            send_info_using_textlocal(from_number, first_time_caller_message)
        else:
            #send_sms(AGGREGATOR_SMS_NO, from_number, crop_code_list)
            send_info_using_textlocal(from_number, crop_code_list)

def send_crop_code_sms_content(price_info_incoming_obj, sms_content, farmer_number) :
    # Send No code entered message to user
    crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
    sms_content = sms_content + [crop_code_list, '\n\n', remaining_crop_line]
    sms_content = ''.join(sms_content)

    price_info_incoming_obj.price_result = sms_content
    price_info_incoming_obj.info_status = 3
    price_info_incoming_obj.save()

    send_info_using_textlocal(farmer_number, sms_content, price_info_incoming_obj)

def send_wrong_query_sms_content(price_info_incoming_obj, farmer_number, query_code = None) :
    # Send Wrong code entered message to user.
    if query_code == None:
        try:
            wrong_query_code = str(price_info_incoming_obj.query_code[0]) if price_info_incoming_obj.query_code else ''
        except Exception as e:
            wrong_query_code = ''
    else:
        wrong_query_code = query_code
    wrong_code_entered_message = wrong_code_entered
    if wrong_query_code == '':
        wrong_code_entered_message = wrong_code_entered_message%(wrong_query_code,)
    else:
        wrong_code_entered_message = wrong_code_entered_message % ('(%s)' % wrong_query_code[0])
    crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
    sms_content = [agg_sms_initial_line, wrong_code_entered_message,'\n\n', crop_code_list, '\n\n', remaining_crop_line]
    sms_content = ''.join(sms_content)

    price_info_incoming_obj.price_result = sms_content
    price_info_incoming_obj.info_status = 2
    price_info_incoming_obj.save()

    send_info_using_textlocal(farmer_number, sms_content, price_info_incoming_obj)
