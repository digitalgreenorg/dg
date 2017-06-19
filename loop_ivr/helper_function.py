__author__ = 'Vikas Saini'

from django.db import connection
from django.db.models import get_model
from loop.models import Crop, Mandi
from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE
from loop.helpline_view import send_helpline_sms

def get_valid_list(app_name, model_name, requested_item):
    model = get_model(app_name, model_name)
    id_list = set(model.objects.values_list('id', flat=True))
    requested_list = set(int(item) for item in requested_item.split('*') if item)
    if 0 in requested_list:
        return list(id_list)
    return list(id_list-requested_list)

def run_query(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def send_info(to_number, content):
    index = 0
    from_number = '01139589707'
    while index < len(final_result):
        send_helpline_sms(from_number, to_number, content[index,index+1998])
        index += 1998

def get_price_info(from_number, crop_list, mandi_list):
    price_info_list = []
    crop_map = dict()
    mandi_map = dict()
    all_crop = Crop.objects.filter(id__in=crop_list).values('id', 'crop_name')
    all_mandi = Mandi.objects.filter(id__in=mandi_list).values('id', 'mandi_name')
    for crop in all_crop:
        crop_map[crop['id']] = crop['crop_name']
    for mandi in all_mandi:
        mandi_map[mandi['id']] = mandi['mandi_name']
    last_three_trans = raw_sql.last_three_trans%(','.join(map(str,crop_list)),','.join(map(str,mandi_list)))
    query_result = run_query(last_three_trans)
    pre_mandi = -1
    pre_crop = -1
    for row in query_results:
        if (pre_crop != row[0]) or (pre_mandi != row[1]):
            temp_str = ('\n%s,%s\n')%(crop_map[row[0]],mandi_map[row[1]])
            price_info_list.append(temp_str)
            pre_crop, pre_mandi = row[0], row[1]
        date, min_price, max_price, mean = row[2], row[3], row[4], row[5]
        if max_price-min_price >= 2:
            min_price = mean-1
            max_price = mean+1
        temp_str = ('%s: %s to %s\n')%(date.strftime('%d-%m-%Y'),str(min_price),str(max_price))
        price_info_list.append(temp_str)
    final_result = ''.join(price_info_list)
    send_info(from_number, final_result)
