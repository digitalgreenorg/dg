# -*- coding: utf-8 -*-
__author__ = 'Vikas Saini'

import requests
import time
from datetime import datetime, timedelta

from django.db import connection
from django.db.models import get_model

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN

from loop.models import Crop, Mandi, CropLanguage
from loop.utils.ivr_helpline.helpline_data import SMS_REQUEST_URL

from loop_ivr.utils.marketinfo import raw_sql
from loop_ivr.utils.data import LOG_FILE, AGGREGATOR_SMS_NO, mandi_hi, indian_rupee, \
    agg_sms_initial_line, agg_sms_no_price_for_combination, agg_sms_no_price_available
from loop_ivr.models import PriceInfoLog


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

def get_valid_list(app_name, model_name, requested_item):
    model = get_model(app_name, model_name)
    id_list = set(model.objects.values_list('id', flat=True))
    requested_list = set(int(item) for item in requested_item.split('*') if item)
    if 0 in requested_list:
        return tuple(map(int,id_list)),1
    return tuple(map(int,requested_list.intersection(id_list))),0

def run_query(query):
    cursor = connection.cursor()
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

def get_price_info(from_number, crop_list, mandi_list, price_info_incoming_obj, all_crop_flag, all_mandi_flag):
    price_info_list = []
    price_info_log_list = []
    crop_map = dict()
    mandi_map = dict()
    crop_in_hindi_map = dict()
    all_crop = Crop.objects.filter(id__in=crop_list).values('id', 'crop_name')
    all_mandi = Mandi.objects.filter(id__in=mandi_list).values('id', 'mandi_name')
    crop_in_hindi = CropLanguage.objects.filter(language_id=1, crop_id__in=crop_list).values('crop_id', 'crop_name')
    map(lambda crop: crop_map[crop['id']] = crop['crop_name'], all_crop)
    map(lambda mandi: mandi_map[mandi['id']] = mandi['mandi_name'], all_mandi)
    map(lambda crop: crop_in_hindi_map[crop['crop_id']] = crop['crop_name'], all_mandi)
    # Fetching price from DB
    price_info_list.append(agg_sms_initial_line)
    today_date = datetime.now()
    raw_query = raw_sql.last_three_trans.format('(%s)'%(crop_list[0],) if len(crop_list) == 1 else crop_list, '(%s)'%(mandi_list[0],) if len(mandi_list) == 1 else mandi_list, tuple((today_date-timedelta(days=day)).strftime('%Y-%m-%d') for day in range(0,3)))
    query_result = run_query(raw_query)
    if not query_result:
        price_info_list.append(agg_sms_no_price_available)
    else:
        crop_mandi_comb = []
        prev_crop, prev_mandi, crop_name, mandi_name = -1, -1, '', ''
        for row in query_result:
            crop, mandi, date, min_price, max_price, mean = row[0], row[1], row[2], int(row[3]), int(row[4]), int(row[5])
            if crop != prev_crop or mandi != prev_mandi:
                if not all_crop_flag and not all_mandi_flag:
                    crop_mandi_comb.append((crop,mandi))
                price_info_log_obj = PriceInfoLog(price_info_incoming=price_info_incoming_obj,
                                    crop_id=crop, mandi_id=mandi)
                price_info_log_list.append(price_info_log_obj)
                prev_crop, prev_mandi = crop, mandi
                crop_name = crop_in_hindi_map.get(crop).encode("utf-8") if crop_in_hindi_map.get(crop) else crop_map[crop].encode("utf-8")
                mandi_name = mandi_map[mandi].encode("utf-8")
                temp_str = ('\n%s,%s %s\n')%(crop_name,mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                price_info_list.append(temp_str)
            if max_price-min_price >= 2:
                min_price = mean-1
                max_price = mean+1
            if min_price != max_price:
                temp_str = ('%s: %s %s-%s\n')%(date.strftime('%d-%m-%Y'),indian_rupee,str(min_price),str(max_price))
            else:
                temp_str = ('%s: %s %s\n')%(date.strftime('%d-%m-%Y'),indian_rupee,str(max_price))
            price_info_list.append(temp_str)
        if not all_crop_flag and not all_mandi_flag:
            for crop in crop_list:
                for mandi in mandi_list:
                    if (crop,mandi) not in crop_mandi_comb:
                        price_info_log_obj = PriceInfoLog(price_info_incoming=price_info_incoming_obj,
                                    crop_id=crop, mandi_id=mandi)
                        price_info_log_list.append(price_info_log_obj)
                        crop_name = crop_in_hindi_map.get(crop).encode("utf-8") if crop_in_hindi_map.get(crop) else crop_map[crop].encode("utf-8")
                        mandi_name = mandi_map[mandi].encode("utf-8")
                        temp_str = ('\n%s,%s %s\n')%(crop_name,mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                        price_info_list.append(temp_str)
                        price_info_list.append(agg_sms_no_price_for_combination)
    final_result = ''.join(price_info_list)
    price_info_incoming_obj.price_result = final_result
    if len(final_result) >= 2000:
        price_info_incoming_obj.return_result_to_app = 0
        price_info_incoming_obj.info_status = 1
        price_info_incoming_obj.save()
        send_info(from_number, final_result)
    else:
        price_info_incoming_obj.save()
    PriceInfoLog.objects.bulk_create(price_info_log_list)
