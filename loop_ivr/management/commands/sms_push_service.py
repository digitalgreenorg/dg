__author__ = 'Vikas Saini'

import time
import datetime
import requests
import itertools
import json
import xml.etree.ElementTree as xml_parse

from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, TEXTLOCAL_API_KEY

from loop.models import Crop, Mandi, CropLanguage
from loop.utils.ivr_helpline.helpline_data import SMS_REQUEST_URL
from loop.helpline_view import write_log

from loop_ivr.models import Subscriber, Subscription, SubscriptionLog
from loop_ivr.helper_function import get_valid_list, run_query
from loop_ivr.utils.marketinfo import raw_sql
from loop_ivr.utils.config import LOG_FILE, AGGREGATOR_SMS_NO, mandi_hi, indian_rupee, \
    agg_sms_initial_line, agg_sms_no_price_for_combination, agg_sms_no_price_available, \
    agg_sms_crop_line, helpline_hi, PUSH_MESSAGE_SMS_RESPONSE_URL, MONTH_NAMES, \
    TEXT_LOCAL_SINGLE_SMS_API, SMS_SENDER_NAME

class Command(BaseCommand):

    crop_map = dict()
    mandi_map = dict()
    crop_in_hindi_map = dict()
    all_crop = Crop.objects.values('id', 'crop_name')
    all_mandi = Mandi.objects.values('id', 'mandi_name')
    crop_in_hindi = CropLanguage.objects.filter(language_id=1).values('crop_id', 'crop_name')
    for crop in all_crop:
       crop_map[crop['id']] = crop['crop_name']
    for mandi in all_mandi:
       mandi_map[mandi['id']] = mandi['mandi_name']
    for crop in crop_in_hindi:
        crop_in_hindi_map[crop['crop_id']] = crop['crop_name']


    def send_sms(self,subscription_id, from_number,user_no,sms_body):
        current_time = datetime.datetime.now(timezone('Asia/Kolkata')).replace(tzinfo=None)
        subscription_log_obj = SubscriptionLog(subscription_id=subscription_id, date=current_time)
        try:
            subscription_log_obj.save()
        except Exception as e:
            print "Error aa gayi: ", str(e)
            module = 'push_message_send_sms'
            log = "Status Code: %s (subscription_id: %s) (Exception: %s)"%('Failed', str(subscription_id), str(e))
            write_log(LOG_FILE,module,log)
            return
        recipient_custom_id = subscription_log_obj.id
        sms_request_url = TEXT_LOCAL_SINGLE_SMS_API
        headers = {'content-type': 'application/json' }
        parameters = {'apiKey': TEXTLOCAL_API_KEY, 'sender': SMS_SENDER_NAME, 'numbers':user_no,
                        'message': sms_body, 'receipt_url': PUSH_MESSAGE_SMS_RESPONSE_URL, 'unicode': 'true',
                        'custom': recipient_custom_id}
        response = requests.post(sms_request_url, params=parameters)
        response_text = json.loads(str(response.text))
        if response_text['status'] == 'success':
            message_id = ','.join([str(message["id"]) for message in response_text['messages']])
            subscription_log_obj.sms_id = message_id
            subscription_log_obj.save()
        elif response_text['status'] == 'failure':
            error_codes = ','.join([str(error["code"]) for error in response_text['errors']])
            subscription_log_obj.status = 2
            subscription_log_obj.failed_code = error_codes
            subscription_log_obj.save()
        '''
        sms_request_url = SMS_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
        parameters = {'From':from_number,'To':user_no,'Body':sms_body,'Priority':'high','EncodingType':'unicode','StatusCallback':PUSH_MESSAGE_SMS_RESPONSE_URL}
        response = requests.post(sms_request_url,data=parameters)
        outgoing_sms_time = (datetime.datetime.now(timezone('Asia/Kolkata'))).replace(tzinfo=None)
        if response.status_code == 200:
            response_tree = xml_parse.fromstring((response.text).encode('utf-8'))
            call_detail = response_tree.findall('SMSMessage')[0]
            outgoing_sms_id = str(call_detail.find('Sid').text)
            outgoing_status = str(call_detail.find('Status').text)
            if outgoing_status == 'failed_dnd':
                status = 3
            elif outgoing_status == 'failed':
                status = 2
            elif outgoing_status == 'sent':
                status = 1
            else: 
                status = 0
            subscription_log_obj = SubscriptionLog(subscription_id=subscription_id,
                                                    sms_id=outgoing_sms_id,date=outgoing_sms_time,status=status)
            try:
                subscription_log_obj.save()
            except Exception as e:
                module = 'push_message_send_sms'
                log = "Status Code: %s (SMS ID: %s) (Exception: %s)"%(str(response.status_code),outgoing_sms_id,str(e))
                write_log(LOG_FILE,module,log)
        else:
            module = 'push_message_send_sms'
            log = "Status Code: %s (Parameters: %s)"%(str(response.status_code),parameters)
            write_log(LOG_FILE,module,log)
        '''


    def send_info(self,subscription_id, user_no, content):
        index = 0
        from_number = AGGREGATOR_SMS_NO
        while index < len(content):
            self.send_sms(subscription_id, from_number, user_no, content[index:index+1998])
            index += 1998
            time.sleep(1)


    def get_price_info(self,subscription_id, user_no, crop_list, mandi_list, all_crop_flag, all_mandi_flag):
        price_info_list = []
        price_info_list.append(agg_sms_initial_line)
        today_date = (datetime.datetime.now(timezone('Asia/Kolkata'))).replace(tzinfo=None)
        raw_query = raw_sql.last_three_trans.format('(%s)'%(crop_list[0],) if len(crop_list) == 1 else crop_list, '(%s)'%(mandi_list[0],) if len(mandi_list) == 1 else mandi_list, tuple((today_date-timedelta(days=day)).strftime('%Y-%m-%d') for day in range(0,3)))
        query_result = run_query(raw_query)
        if not query_result:
            return
        else:
            prev_crop, prev_mandi, crop_name, mandi_name = -1, -1, '', ''
            for row in query_result:
                crop, mandi, date, min_price, max_price, mean = row['crop'], row['mandi'], row['date'], int(row['minp']), int(row['maxp']), int(row['mean'])
                if crop != prev_crop or mandi != prev_mandi:
                    crop_name = self.crop_in_hindi_map.get(crop).encode("utf-8") if self.crop_in_hindi_map.get(crop) else self.crop_map[crop].encode("utf-8")
                    mandi_name = self.mandi_map[mandi].encode("utf-8")
                    if crop != prev_crop:
                        temp_str = ('\n%s: %s\n%s %s\n')%(agg_sms_crop_line,crop_name,mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                    else:
                        temp_str = ('\n%s %s\n')%(mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                    price_info_list.append(temp_str)
                    prev_crop, prev_mandi = crop, mandi
                if max_price-min_price >= 2:
                    min_price = mean-1
                    max_price = mean+1
                if min_price != max_price:
                    temp_str = ('%s %s: %s %s-%s\n')%(date.strftime('%d'),MONTH_NAMES[int(date.strftime('%m'))],indian_rupee,str(min_price),str(max_price))
                else:
                    temp_str = ('%s %s: %s %s\n')%(date.strftime('%d'),MONTH_NAMES[int(date.strftime('%m'))],indian_rupee,str(max_price))
                price_info_list.append(temp_str)
            price_info_list.append(('\n%s: %s')%(helpline_hi, EXOTEL_HELPLINE_NUMBER))
            final_result = ''.join(price_info_list)
            self.send_info(subscription_id, user_no, final_result)


    def handle(self, *args, **options):
        print "Start"
        self.send_sms(28,AGGREGATOR_SMS_NO, '9205812770', 'hello test SMS %0A Next line')
        print "End"
        return
        all_subscriptions = Subscription.objects.filter(status=1).values('id', 'subscription_code', 'subscriber__phone_no')
        for subscription in all_subscriptions:
            subscription_id, subscription_code, user_no = subscription['id'], subscription['subscription_code'], subscription['subscriber__phone_no']
            if not subscription_code:
                continue
            query_code = subscription_code.split('**')
            if len(query_code) >= 2:
                crop_info, mandi_info = query_code[0], query_code[1]
            elif len(query_code) == 1:
                crop_info = query_code[0]
                mandi_info = ''
            else:
                continue
            crop_list, all_crop_flag = get_valid_list('loop', 'crop', crop_info, user_no)
            mandi_list, all_mandi_flag = get_valid_list('loop', 'mandi', mandi_info, user_no)
            if (all_crop_flag and all_mandi_flag) or (not crop_list) or (not mandi_list):
                continue
            self.get_price_info(subscription_id, user_no, crop_list, mandi_list, all_crop_flag, all_mandi_flag)
