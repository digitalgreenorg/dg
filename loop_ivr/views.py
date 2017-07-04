# -*- coding: utf-8 -*-

__author__ = 'Vikas Saini'

from django.shortcuts import render
from django.http import HttpResponse

from threading import Thread

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog
from loop_ivr.helper_function import get_valid_list, send_info, get_price_info
from loop_ivr.utils.data import LOG_FILE

from loop.helpline_view import fetch_info_of_incoming_call, write_log


def home(request):
    return HttpResponse(status=403)

def crop_price_query(request):
    # Serve only Get request
    if request.method == 'GET':
        call_id, farmer_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        try:
            query_code = str(request.GET.get('digits')).strip('"')
            price_info_incoming_obj = PriceInfoIncoming(call_id=call_id, from_number=farmer_number,
                                        to_number=dg_number, incoming_time=incoming_time, query_code=query_code)
            price_info_incoming_obj.save()
        except Exception as e:
            module = 'crop_info'
            log = "Call Id: %s Error: %s"%(str(call_id),str(e))
            write_log(LOG_FILE,module,log)
            return HttpResponse(status=404)
        query_code = query_code.split('**')
        # If query code is not in correct format
        if len(query_code) != 2:
            price_info_incoming_obj.info_status = 2
            price_info_incoming_obj.save()
            return HttpResponse(status=404)
        crop_info, mandi_info = query_code[0], query_code[1]
        crop_list, all_crop_flag = get_valid_list('loop', 'crop', crop_info)
        mandi_list, all_mandi_flag = get_valid_list('loop', 'mandi', mandi_info)
        if (all_crop_flag and all_mandi_flag) or (not crop_list) or (not mandi_list):
            price_info_incoming_obj.info_status = 2
            price_info_incoming_obj.save()
            return HttpResponse(status=404)
        Thread(target=get_price_info, args=[farmer_number, crop_list, mandi_list, price_info_incoming_obj, all_crop_flag, all_mandi_flag]).start()
        return HttpResponse(status=200)
    return HttpResponse(status=403)

def crop_price_sms_content(request):
    if request.method == 'HEAD':
        return HttpResponse(status=200, content_type='text/plain')
    if request.method == 'GET':
        call_id = str(request.GET.getlist('CallSid')[0])
        farmer_number = str(request.GET.getlist('From')[0])
        dg_number = str(request.GET.getlist('To')[0])
        try:
            price_info_obj = PriceInfoIncoming.objects.get(call_id=call_id, from_number=farmer_number,
                                        to_number=dg_number)
            if price_info_obj.return_result_to_app == 1:
                sms_content = price_info_obj.price_result
                price_info_obj.info_status = 1
                price_info_obj.save()
                response = HttpResponse(sms_content, content_type='text/plain')
            else:
                response = HttpResponse(status=200, content_type='text/plain')
        except Exception as e:
            response = HttpResponse(status=200, content_type='text/plain')
        return response
    return HttpResponse(status=403)
