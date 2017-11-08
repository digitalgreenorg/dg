# -*- coding: utf-8 -*-

__author__ = 'Vikas Saini'

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from threading import Thread
from datetime import datetime, timedelta
import time

from dg.settings import EXOTEL_HELPLINE_NUMBER

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog, SubscriptionLog
from loop_ivr.helper_function import get_valid_list, send_info, get_price_info, make_market_info_call, \
    send_info_using_textlocal, get_top_selling_crop_quantity_wise, get_crop_code_list
from loop_ivr.utils.config import LOG_FILE, call_failed_sms, crop_and_code, helpline_hi, remaining_crop_line, \
    no_code_entered, wrong_code_entered, crop_and_code_hi, TOP_SELLING_CROP_WINDOW, N_TOP_SELLING_CROP, code_hi

from loop.helpline_view import fetch_info_of_incoming_call, write_log

import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse(status=403)

def market_info_incoming(request):
    if request.method == 'GET':
        call_id, to_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        today_date = datetime.now().date()
        if PriceInfoIncoming.objects.filter(incoming_time__gte=today_date, from_number=to_number).count() < 10:
            time.sleep(2)
            make_market_info_call(to_number, dg_number, incoming_time, call_id)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

@csrf_exempt
def market_info_response(request):
    if request.method == 'POST':
        status = str(request.POST.getlist('Status')[0])
        outgoing_call_id = str(request.POST.getlist('CallSid')[0])
        price_info_incoming_obj = PriceInfoIncoming.objects.filter(call_id=outgoing_call_id).order_by('-id')
        price_info_incoming_obj = price_info_incoming_obj[0] if len(price_info_incoming_obj) > 0 else ''
        # If call failed then send acknowledgement to user
        if status != 'completed':
            # if call found in our database, then fetch number of caller and send SMS
            if price_info_incoming_obj != '':
                user_no = price_info_incoming_obj.from_number
                crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
                message = [call_failed_sms,'\n\n', crop_code_list, '\n',('%s\n%s')%(remaining_crop_line, EXOTEL_HELPLINE_NUMBER)]
                message = ''.join(message)
                #send_info(user_no, message)
                send_info_using_textlocal(user_no, message, price_info_incoming_obj)
        # If call is completed, then check if Initial status is Not Picked, if yes then change it to No Input
        else:
            if price_info_incoming_obj != '' and price_info_incoming_obj.info_status == 4:
                price_info_incoming_obj.info_status = 3
                price_info_incoming_obj.save()
    return HttpResponse(status=200)


def crop_price_query(request):
    # Serve only Get request
    if request.method == 'GET':
        call_id, farmer_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        # Check if request contain some input combination.
        try:
            query_code = str(request.GET.get('digits')).strip('"')
        except Exception as e:
            query_code = ''
        # Check if its retry or first time request.
        try:
            # Search if this request generated in second try.
            price_info_incoming_obj = PriceInfoIncoming.objects.filter(call_id=call_id,from_number=farmer_number,
                                        to_number=dg_number)
            # If it is second try, then take this object else create new object.
            if len(price_info_incoming_obj) > 0:
                price_info_incoming_obj = price_info_incoming_obj[0]
                price_info_incoming_obj.prev_query_code = price_info_incoming_obj.query_code
                price_info_incoming_obj.prev_info_status = price_info_incoming_obj.info_status
                price_info_incoming_obj.query_code = query_code
                # If it is retry then set status to pending and remaining code will change this according to input.
                price_info_incoming_obj.info_status = 0
                price_info_incoming_obj.save()
            else:
                price_info_incoming_obj = PriceInfoIncoming(call_id=call_id, from_number=farmer_number,
                                        to_number=dg_number, incoming_time=incoming_time, query_code=query_code)
                price_info_incoming_obj.save()
            # If this request has no query code then save object as No input.
            if query_code == '' or query_code == None or query_code == 'None':
                # If Wrong Query in 'first try' and now user didn't enter anything 
                # then set info_status to Wrong query.
                if price_info_incoming_obj.prev_info_status == 2:
                    price_info_incoming_obj.info_status = 2
                else:
                    price_info_incoming_obj.info_status = 3
                price_info_incoming_obj.save()
                return HttpResponse(status=200)
        except Exception as e:
            module = 'crop_info'
            log = "Call Id: %s Error: %s"%(str(call_id),str(e))
            write_log(LOG_FILE,module,log)
            return HttpResponse(status=404)
        query_code = query_code.split('**')
        # If query code is not in correct format
        #if len(query_code) != 2:
        #    price_info_incoming_obj.info_status = 2
        #    price_info_incoming_obj.save()
        #    return HttpResponse(status=404)
        if len(query_code) >= 2:
            crop_info, mandi_info = query_code[0], query_code[1]
        elif len(query_code) == 1:
            crop_info = query_code[0]
            mandi_info = ''
        else:
            price_info_incoming_obj.info_status = 2
            price_info_incoming_obj.save()
            return HttpResponse(status=404)
        crop_list, all_crop_flag = get_valid_list('loop', 'crop', crop_info, farmer_number)
        mandi_list, all_mandi_flag = get_valid_list('loop', 'mandi', mandi_info, farmer_number)
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

def no_code_message(request):
    if request.method == 'HEAD':
        return HttpResponse(status=200, content_type='text/plain')
    if request.method == 'GET':
        crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
        sms_content = [no_code_entered,'\n\n', crop_code_list, '\n\n', ('%s\n%s')%(remaining_crop_line, EXOTEL_HELPLINE_NUMBER)]
        sms_content = ''.join(sms_content)
        response = HttpResponse(sms_content, content_type='text/plain')
        return response
    return HttpResponse(status=403)

def wrong_code_message(request):
    if request.method == 'HEAD':
        return HttpResponse(status=200, content_type='text/plain')
    if request.method == 'GET':
        crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
        call_id = str(request.GET.getlist('CallSid')[0])
        farmer_number = str(request.GET.getlist('From')[0])
        dg_number = str(request.GET.getlist('To')[0])
        try:
            price_info_obj = PriceInfoIncoming.objects.get(call_id=call_id, from_number=farmer_number,
                                        to_number=dg_number)
            wrong_query_code = str(price_info_obj.query_code) if price_info_obj.query_code else ''
        except Exception as e:
            wrong_query_code = ''
        wrong_code_entered_message = wrong_code_entered
        if wrong_query_code == '':
            wrong_code_entered_message = wrong_code_entered_message%(wrong_query_code,)
        else:
            wrong_code_entered_message = wrong_code_entered_message%((' (%s:%s)')%(code_hi,wrong_query_code),)
        sms_content = [wrong_code_entered_message,'\n\n', crop_code_list, '\n\n', ('%s\n%s')%(remaining_crop_line, EXOTEL_HELPLINE_NUMBER)]
        sms_content = ''.join(sms_content)
        response = HttpResponse(sms_content, content_type='text/plain')
        return response
    return HttpResponse(status=403)

@csrf_exempt
def push_message_sms_response(request):
    if request.method == 'POST':
        status = str(request.POST.getlist('Status')[0])
        outgoing_sms_id = str(request.POST.getlist('SmsSid')[0])
        outgoing_obj = SubscriptionLog.objects.filter(sms_id=outgoing_sms_id)
        outgoing_obj = outgoing_obj[0] if len(outgoing_obj) > 0 else ''
        # If call Successfully completed then mark call as resolved
        if outgoing_obj:
            if status == 'sent':
                outgoing_obj.status = 1
            elif status == 'failed':
                outgoing_obj.status = 2
            elif status == 'failed_dnd':
                outgoing_obj.status = 3
            outgoing_obj.save()
    return HttpResponse(status=200)

@csrf_exempt
def test_text_local(request) :
    logger.debug(request.body)
    return HttpResponse(status=200)