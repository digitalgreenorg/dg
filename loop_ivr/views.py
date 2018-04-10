# -*- coding: utf-8 -*-

__author__ = 'Vikas Saini'

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from threading import Thread
from datetime import datetime, timedelta
from pytz import timezone
import time
import re

from dg.settings import EXOTEL_HELPLINE_NUMBER

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog, SubscriptionLog
from loop_ivr.helper_function import get_valid_list, send_info, get_price_info, make_market_info_call, \
    send_info_using_textlocal, get_top_selling_crop_quantity_wise, get_crop_code_list, send_crop_code_sms_content, \
    send_wrong_query_sms_content
from loop_ivr.utils.config import LOG_FILE, agg_sms_initial_line, call_failed_sms, remaining_crop_line, \
    no_code_entered, wrong_code_entered, crop_and_code_hi, TOP_SELLING_CROP_WINDOW, N_TOP_SELLING_CROP, code_hi, \
    AGGREGATOR_SMS_NO, ALL_FLAG_TRUE, ALL_FLAG_FALSE, PATTERN_REGEX, CONTAINS_ZERO, EXOTEL_MI_LINE, LIMIT_EXCEEDED

from loop.helpline_view import fetch_info_of_incoming_call, write_log
import logging
logger = logging.getLogger(__name__)

def market_info_incoming(request):
    """
    When user calls on textlocal or exotel number and the call is disconnected by the platform
    """
    if request.method == 'GET':
        call_id, to_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        if request.GET.getlist('call_source'):
            call_source = request.GET.getlist('call_source')[0]
        else:
            call_source = 1
        today_date = datetime.now().date()
        if PriceInfoIncoming.objects.filter(incoming_time__gte=today_date, from_number=to_number).count() < 10:
            time.sleep(2)
            make_market_info_call(to_number, dg_number, incoming_time, call_id, call_source)
        else:
            crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
            message = [LIMIT_EXCEEDED, '\n\n', crop_code_list, '\n', remaining_crop_line]
            message = ''.join(message)
            send_info_using_textlocal(to_number, message)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

@csrf_exempt
def textlocal_market_info_incoming_call(request):
    logger.debug("Reached here in CALL View")
    logger.debug(request.body)
    if request.method == 'POST':
        farmer_number = str(request.POST.getlist('sender')[0])
        farmer_number = re.sub('^91', '0', farmer_number)
        dummy_incoming_request = HttpRequest()
        current_time = datetime.now(timezone('Asia/Kolkata')).replace(tzinfo=None)
        dummy_incoming_request.method = 'GET'
        dummy_incoming_request.GET['CallSid'] = 0
        dummy_incoming_request.GET['From'] = farmer_number      # User Number
        dummy_incoming_request.GET['To'] = EXOTEL_MI_LINE    # DG number
        dummy_incoming_request.GET['StartTime'] = current_time
        dummy_incoming_request.GET['call_source'] = 2
        market_info_incoming(dummy_incoming_request)
        return HttpResponse(status=200)
    return HttpResponse(status=403)

@csrf_exempt
def textlocal_market_info_incoming_sms(request):
    logger.debug("Reached here in SMS View")
    logger.debug(request.body)
    if request.method == 'POST':
        msg_id = str(request.POST.get('msgId'))
        farmer_number = str(request.POST.get('sender'))
        farmer_number = re.sub('^91', '0', farmer_number)
        to_number = str(request.POST.get('inNumber'))

        try:
            query_code = str(request.POST.get('content')).replace(" ", "")
        except Exception as e:
            query_code = ''
        current_time = datetime.now(timezone('Asia/Kolkata')).replace(tzinfo=None)
        price_info_incoming_obj = PriceInfoIncoming(call_id=msg_id, from_number=farmer_number, query_code=query_code,
                                    to_number=to_number, incoming_time=current_time, call_source=3, info_status=0)
        try:
            price_info_incoming_obj.save()
        except Exception as e:
            # Save Errors in Logs
            module = 'textlocal_market_info_incoming_sms'
            write_log(LOG_FILE,module,str(e))
            return HttpResponse(status=200)

        # Creating and sending message on the basis of Query Code.
        response = handle_query_code(query_code, price_info_incoming_obj, farmer_number)
        return response
    return HttpResponse(status=403)

@csrf_exempt
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
            if price_info_incoming_obj.count() > 0:
                price_info_incoming_obj = price_info_incoming_obj[0]
                if price_info_incoming_obj.prev_query_code is None:
                    price_info_incoming_obj.prev_query_code = price_info_incoming_obj.query_code
                    price_info_incoming_obj.prev_info_status = price_info_incoming_obj.info_status
                    price_info_incoming_obj.query_code = query_code
                    # If it is retry then set status to pending and remaining code will change this according to input.
                    # price_info_incoming_obj.info_status = 0
                    price_info_incoming_obj.save()
            else:
                price_info_incoming_obj = PriceInfoIncoming(call_id=call_id, from_number=farmer_number,
                                        to_number=dg_number, incoming_time=incoming_time, query_code=query_code)
                price_info_incoming_obj.save()

        except Exception as e:
            module = 'crop_info'
            log = "Call Id: %s Error: %s"%(str(call_id),str(e))
            write_log(LOG_FILE,module,log)
            return HttpResponse(status=404)

        # Creating and sending message on the basis of Query Code.
        response = handle_query_code(query_code, price_info_incoming_obj, farmer_number)
        return response
    return HttpResponse(status=403)


def handle_query_code(query_code, price_info_incoming_obj, farmer_number):
    if query_code == '' or query_code == 'None':
        if price_info_incoming_obj.call_source == 3:
            sms_content = [agg_sms_initial_line, no_code_entered,'\n\n']
            send_crop_code_sms_content(price_info_incoming_obj, sms_content, farmer_number)
        else:
            price_info_incoming_obj.info_status = 3
            price_info_incoming_obj.save()
        return HttpResponse(status=404)
    elif query_code == '0':
        if price_info_incoming_obj.call_source == 3:
            sms_content = []
            send_crop_code_sms_content(price_info_incoming_obj, sms_content, farmer_number)
        else:
            price_info_incoming_obj.info_status = 3
            price_info_incoming_obj.save()
        return HttpResponse(status=404)
    elif re.search(PATTERN_REGEX, query_code) is None:
        # send wrong query code
        if price_info_incoming_obj.call_source == 3:
            send_wrong_query_sms_content(price_info_incoming_obj, farmer_number)
        else:
            price_info_incoming_obj.info_status = 2
            price_info_incoming_obj.save()
        return HttpResponse(status=404)
    else :
        # send corresponding response
        query_code = query_code.split('**')
        all_crop_flag = False
        all_mandi_flag = False

        if len(query_code) >= 2:
            crop_info, mandi_info = query_code[0], query_code[1]
        elif len(query_code) == 1:
            crop_info = query_code[0]
            mandi_info = ''
        if re.search(CONTAINS_ZERO,crop_info) is not None:
            all_crop_flag = True
        if re.search(CONTAINS_ZERO,mandi_info) is not None or mandi_info == '':
            all_mandi_flag = True

        crop_list = get_valid_list('loop', 'crop', crop_info, farmer_number, all_crop_flag)
        mandi_list = get_valid_list('loop', 'mandi', mandi_info, farmer_number, all_mandi_flag)
        if len(crop_list) == 0:
            if price_info_incoming_obj.call_source == 3:
                send_wrong_query_sms_content(price_info_incoming_obj, farmer_number, query_code)
            else:
                price_info_incoming_obj.info_status = 2
                price_info_incoming_obj.save()
            return HttpResponse(status=404)
        else:
            Thread(target=get_price_info, args=[farmer_number, crop_list, mandi_list, price_info_incoming_obj, all_crop_flag, all_mandi_flag]).start()
            return HttpResponse(status=200)
    return HttpResponse(status=403)

@csrf_exempt
def market_info_response(request):
    logger.debug("Reached here in Market Info Response View")
    logger.debug(request)
    logger.debug(request.POST)

    if request.method == 'POST':
        status = str(request.POST.getlist('Status')[0])
        outgoing_call_id = str(request.POST.getlist('CallSid')[0])
        price_info_incoming_obj = PriceInfoIncoming.objects.filter(call_id=outgoing_call_id).order_by('-id')
        price_info_incoming_obj = price_info_incoming_obj[0] if price_info_incoming_obj.count() > 0 else ''
        # If call failed then send acknowledgement to user
        if status != 'completed':
            # if call found in our database, then fetch number of caller and send SMS
            if price_info_incoming_obj != '':
                user_no = price_info_incoming_obj.from_number
                crop_code_list = get_crop_code_list(N_TOP_SELLING_CROP, TOP_SELLING_CROP_WINDOW)
                message = [call_failed_sms,'\n\n', crop_code_list, '\n', remaining_crop_line]
                message = ''.join(message)
                #send_info(user_no, message)
                send_info_using_textlocal(user_no, message, price_info_incoming_obj)
        # If call is completed, then check if Initial status is Not Picked, if yes then change it to No Input
        else:
            if price_info_incoming_obj != '':
                if price_info_incoming_obj.info_status == 2:  #WRONG QUERY
                    send_wrong_query_sms_content(price_info_incoming_obj, price_info_incoming_obj.from_number)
                elif price_info_incoming_obj.info_status == 3:  #NO INPUT
                    if price_info_incoming_obj.prev_info_status != None and price_info_incoming_obj.prev_info_status == 2:
                        send_wrong_query_sms_content(price_info_incoming_obj, price_info_incoming_obj.from_number, str(price_info_incoming_obj.prev_query_code))
                    else:
                        sms_content = [agg_sms_initial_line, no_code_entered,'\n\n']
                        send_crop_code_sms_content(price_info_incoming_obj, sms_content, price_info_incoming_obj.from_number)
                elif price_info_incoming_obj.info_status == 4:
                    price_info_incoming_obj.info_status = 3
                    price_info_incoming_obj.save()
    return HttpResponse(status=200)

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
