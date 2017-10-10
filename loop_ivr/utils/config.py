# -*- coding: utf-8 -*-
from dg.settings import MEDIA_ROOT, CURRENT_DOMAIN

LOG_FILE = '%s/loop/loop_ivr_log.log'%(MEDIA_ROOT,)
AGGREGATOR_SMS_NO = '01139585707'

mandi_hi = 'मंडी'
indian_rupee = 'रु'
helpline_hi = 'हेल्पलाइन'
code_hi = 'कोड:'
agg_sms_initial_line = 'लूप मंडी रेट\n'
agg_sms_crop_line = 'फसल'
agg_sms_no_price_for_combination = 'रेट उपलब्ध नही है\n'
agg_sms_no_price_available = 'इस मंडी और फसल के लिए पिछले तीन दिनो के रेट उपलब्ध नही है.'
agg_sms_no_price_all_mandi = '%s का पिछले तीन दिनो के रेट उपलब्ध नही है.'
agg_sms_no_price_crop_mandi = '%s का %s मंडी मे पिछले तीन दिनो के रेट उपलब्ध नही है.'
# This is common string in no price messages.
string_for_no_rate_query = 'पिछले तीन दिनो के रेट उपलब्ध नही है'
MONTH_NAMES = {1:'जनवरी', 2:'फरवरी', 3:'मार्च', 4:'अप्रैल', 5:'मई', 6:'जून', 7:'जुलाई', 8:'अगस्त',
				9:'सितंबर', 10:'अक्टूबर', 11:'नवंबर', 12:'दिसंबर'}
crop_and_code = 'फसल और उनके कोड:\n\
बोड़ा - 1\n\
बैंगन - 2\n\
करेला - 16\n\
परवल - 17\n\
नेनुआ - 20\n\
भिंडी - 22\n'
call_failed_sms = 'नमस्ते। हमने आपको कॉल किया पर संपर्क नहीं हो पाया। किसी भी फसल का रेट जानने के लिए 011-39585707 पर दोबारा कॉल करें और फसल का कोड डालें।'
remaining_crop_line = 'बाकी फसलों का कोड जानने के लिए कॉल करें:'
first_time_caller = 'लूप में कॉल करने के लिए धन्यवाद। किसी भी फसल का रेट जानने के लिए 011-39585707 पर कॉल करें और फसल का कोड डालें।'

MARKET_INFO_CALL_RESPONSE_URL = 'http://%s%s'%(CURRENT_DOMAIN, '/loopivr/market_info_response/')
PUSH_MESSAGE_SMS_RESPONSE_URL = 'http://%s%s'%(CURRENT_DOMAIN, '/loopivr/push_message_sms_response/')
MARKET_INFO_APP = '137265'
