__author__ = 'Vikas Saini'

from django.shortcuts import render
from django.http import HttpResponse

from threading import Thread

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog
from loop_ivr.helper_function import get_valid_list, send_info, get_price_info

from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE
from loop.helpline_view import fetch_info_of_incoming_call, write_log


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
        except Exception as e:
            module = 'mandi_info'
            log = "Call Id: %s Error: %s"%(str(call_id),str(e))
            write_log(HELPLINE_LOG_FILE,module,log)
            return HttpResponse(status=200)
        crops_info = price_info_incoming_obj.query_for_crop
        crop_list = get_valid_list('loop', 'crop', crops_info)
        mandi_list = get_valid_list('loop', 'mandi', mandis_info)
        price_info_incoming_obj.query_for_mandi = mandis_info
        if not crop_list:
            final_result = 'Please correct crop list'
            price_info_incoming_obj.info_status = 2
            price_info_incoming_obj.save()
            #send_info(from_number, final_result)
            return HttpResponse(status=200)
        if not mandi_list:
            final_result = 'Please correct mandi list'
            price_info_incoming_obj.info_status = 2
            price_info_incoming_obj.save()
            #send_info(from_number, final_result)
            return HttpResponse(status=200)
        Thread(target=get_price_info, args=[from_number, crop_list, mandi_list, price_info_incoming_obj]).start()
        return HttpResponse(status=200)
    return HttpResponse(status=403)
