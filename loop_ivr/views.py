__author__ = 'Vikas Saini'

from django.shortcuts import render
from django.http import HttpResponse

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog
from loop_ivr.utils.marketinfo import raw_sql
from loop_ivr.helper_function import get_valid_list, run_query, send_info
from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE
from loop.helpline_view import fetch_info_of_incoming_call


def home(request):
    return HttpResponse(status=200)

def crop_info(request):
    # Serve only Get request
    if request.method == 'GET':
        call_id, farmer_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        try:
            crops_info = str(request.GET.get('digits')).strip('"')
            price_info_incoming_obj = PriceInfoIncoming(call_id=call_id, from_number=farmer_number,
                                        to_number=dg_number, incoming_time=incoming_time, query_for_crop=crops_info)
            price_info_incoming_obj.save()
        except Exception as e:
            module = 'crop_info'
            log = "Call Id: %s Error: %s"%(str(call_id),str(e))
            write_log(HELPLINE_LOG_FILE,module,log)
            return HttpResponse(status=500)
        return HttpResponse(status=200)
    return HttpResponse(status=403)


def mandi_info(request):
    # Serve only Get request
    if request.method == 'GET':
        call_id, from_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        mandis_info = str(request.GET.get('digits')).strip('"')
        try:
            price_info_incoming_obj = PriceInfoIncoming.objects.get(call_id=call_id, from_number=from_number,
                                        to_number=dg_number, info_status = 0, incoming_time=incoming_time)
        except:
            module = 'mandi_info'
            log = "Call Id: %s Error: %s"%(str(call_id),str(e))
            write_log(HELPLINE_LOG_FILE,module,log)
            return HttpResponse(status=200)
        crops_info = price_info_incoming_obj.query_for_crop
        crop_list = get_valid_list('loop', 'crop', crops_info)
        mandi_list = get_valid_list('loop', 'mandi', mandis_info)
        if not crop_list:
            final_result = 'Please correct crop list'
            send_info(from_number, final_result)
            return HttpResponse(status=200)
        if not mandi_list:
            final_result = 'Please correct mandi list'
            return HttpResponse(status=200)
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
        return HttpResponse(status=200)
    return HttpResponse(status=403)
