__author__ = 'Vikas Saini'

from django.shortcuts import render
from django.http import HttpResponse

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog
from loop_ivr.utils.marketinfo import raw_sql
from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE
from loop.helpline_view import fetch_info_of_incoming_call, get_valid_list

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


def get_price_info(crop_id,mandi_id):


def mandi_info(request):
    # Serve only Get request
    if request.method == 'GET':
        call_id, farmer_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        mandis_info = str(request.GET.get('digits')).strip('"')
        try:
            price_info_incoming_obj = PriceInfoIncoming.objects.get(call_id=call_id, from_number=farmer_number,
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
            # send sms for correct crop
            pass
        if not mandi_list:
            # send sms for correct mandi
            pass
        price_info_list = []
        crop_map = dict()
        mandi_map = dict()
        all_crop = Crop.objects.filter(id__in=crop_list).values('id', 'crop_name')
        all_mandi = Mandi.objects.filter(id__in=mandi_list).values('id', 'mandi_name')
        for crop in all_crop:
            crop_map[crop['id']] = crop['crop_name']
        for mandi in all_mandi:
            crop_map[mandi['id']] = mandi['mandi_name']
        last_three_trans = raw_sql.last_three_trans%(','.join(crop_list),','.join(mandi_list))
        return HttpResponse(status=200)
    return HttpResponse(status=403)
