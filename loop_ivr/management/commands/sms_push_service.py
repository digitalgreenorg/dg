__author__ = 'Vikas Saini'

import time
import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN

from loop.models import Crop, Mandi, CropLanguage
from loop_ivr.models import Subscriber, Subscription, SubscriptionLog
from loop_ivr.helper_function import get_valid_list, run_query
from loop_ivr.utils.marketinfo import raw_sql
from loop_ivr.utils.config import LOG_FILE, AGGREGATOR_SMS_NO, mandi_hi, indian_rupee, \
    agg_sms_initial_line, agg_sms_no_price_for_combination, agg_sms_no_price_available

class Command(BaseCommand):

    crop_map = dict()
    mandi_map = dict()
    crop_in_hindi_map = dict()
    all_crop = Crop.objects.values('id', 'crop_name')
    all_mandi = Mandi.objects.values('id', 'mandi_name')
    crop_in_hindi = CropLanguage.objects.filter(language_id=1, crop_id__in=crop_list).values('crop_id', 'crop_name')
    for crop in all_crop:
       crop_map[crop['id']] = crop['crop_name']
    for mandi in all_mandi:
       mandi_map[mandi['id']] = mandi['mandi_name']
    for crop in crop_in_hindi:
        crop_in_hindi_map[crop['crop_id']] = crop['crop_name']

    def get_price_info(self, farmer_number, crop_list, mandi_list, all_crop_flag, all_mandi_flag):
        price_info_list = []
        crop_mandi_comb = []
        price_info_list.append(agg_sms_initial_line)
        today_date = (datetime.datetime.now(timezone('Asia/Kolkata'))).replace(tzinfo=None)
        raw_query = raw_sql.last_three_trans.format('(%s)'%(crop_list[0],) if len(crop_list) == 1 else crop_list, '(%s)'%(mandi_list[0],) if len(mandi_list) == 1 else mandi_list, tuple((today_date-timedelta(days=day)).strftime('%Y-%m-%d') for day in range(0,3)))
        query_result = run_query(raw_query)
        if not query_result:
            price_info_list.append(agg_sms_no_price_available)
        else:
            prev_crop, prev_mandi, crop_name, mandi_name = -1, -1, '', ''
            for row in query_result:
                crop, mandi, date, min_price, max_price, mean = row['crop'], row['mandi'], row['date'], int(row['minp']), int(row['maxp']), int(row['mean'])
                if crop != prev_crop or mandi != prev_mandi:
                    if not all_crop_flag and not all_mandi_flag:
                        crop_mandi_comb.append((crop,mandi))
                    prev_crop, prev_mandi = crop, mandi
                    crop_name = self.crop_in_hindi_map.get(crop).encode("utf-8") if self.crop_in_hindi_map.get(crop) else self.crop_map[crop].encode("utf-8")
                    mandi_name = self.mandi_map[mandi].encode("utf-8")
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
                for crop, mandi in itertools.product(crop_list, mandi_list):
                    if (crop,mandi) not in crop_mandi_comb:
                        crop_name = self.crop_in_hindi_map.get(crop).encode("utf-8") if self.crop_in_hindi_map.get(crop) else self.crop_map[crop].encode("utf-8")
                        mandi_name = self.mandi_map[mandi].encode("utf-8")
                        temp_str = ('\n%s,%s %s\n')%(crop_name,mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                        price_info_list.append(temp_str)
                        price_info_list.append(agg_sms_no_price_for_combination)
        final_result = ''.join(price_info_list)
        print final_result


    def handle(self, *args, **options):
        all_subscriptions = Subscription.objects.filter(status=1).values('id', 'subscription_code', 'subscription__subscriber__phone_no')
        for subscription in all_subscriptions:
            subscription_id, subscription_code, user_no = subscription['id'], subscription['subscription_code'], subscription['subscription__subscriber__phone_no']
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
            crop_list, all_crop_flag = get_valid_list('loop', 'crop', crop_info, farmer_number)
            mandi_list, all_mandi_flag = get_valid_list('loop', 'mandi', mandi_info, farmer_number)
            if (all_crop_flag and all_mandi_flag) or (not crop_list) or (not mandi_list):
                continue
            self.get_price_info(user_no, crop_list, mandi_list, all_crop_flag, all_mandi_flag)
            time.sleep(1)
