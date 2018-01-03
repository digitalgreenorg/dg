# -*- coding: utf-8 -*-
from dg.settings import MEDIA_ROOT, CURRENT_DOMAIN

LOG_FILE = '%s/loop/loop_ivr_log.log'%(MEDIA_ROOT,)
AGGREGATOR_SMS_NO = '9246108080'
EXOTEL_MI_LINE = '01139585707'

mandi_hi = 'मंडी'
indian_rupee = 'रु'
helpline_hi = 'हेल्पलाइन'
code_hi = 'कोड'
crop_and_code_hi = 'फसल और उनके कोड:\n'
agg_sms_initial_line = 'लूप मंडी मास्टर (9246108080) को कॉल करने के लिए धन्यवाद।\n'
agg_sms_initial_line_with_content = 'लूप मंडी मास्टर (9246108080)\n'
fasal = 'फसल'
agg_sms_no_price_for_combination = 'रेट उपलब्ध नही है\n'
agg_sms_no_price_available = 'इस मंडी और फसल के लिए पिछले तीन दिनो के रेट उपलब्ध नही है।\n\nकिसी भी फसल का रेट जानने के लिए 9246108080 पर मिस कॉल या SMS द्वारा फसल का कोड डालें।'
agg_sms_no_price_all_mandi = '%s\nमाफ़ कीजिए, इस फसल का पिछले तीन दिनो का रेट उपलब्ध नही है।\n\nकिसी भी फसल का रेट जानने के लिए 9246108080 पर मिस कॉल या SMS द्वारा फसल का कोड डालें।'
agg_sms_no_price_crop_mandi = '%s का %s मंडी मे पिछले तीन दिनो के रेट उपलब्ध नही है।\n\nकिसी भी फसल का रेट जानने के लिए 9246108080 पर मिस कॉल या SMS द्वारा फसल का कोड डालें।'
MONTH_NAMES = {1:'जनवरी', 2:'फरवरी', 3:'मार्च', 4:'अप्रैल', 5:'मई', 6:'जून', 7:'जुलाई', 8:'अगस्त',
				9:'सितंबर', 10:'अक्टूबर', 11:'नवंबर', 12:'दिसंबर'}
call_failed_sms = 'हमने आपको कॉल किया पर संपर्क नहीं हो पाया।\n\nकिसी भी फसल का रेट जानने के लिए 9246108080 पर मिस कॉल या SMS द्वारा फसल का कोड डालें।'
remaining_crop_line = 'बाकी फसलों का कोड जानने के लिए अपने लूप प्रतिनिधि से संपर्क करें।'
first_time_caller = 'लूप मंडी मास्टर को कॉल करने के लिए धन्यवाद।\n\nकिसी भी फसल का रेट जानने के लिए 9246108080 पर मिस कॉल या SMS द्वारा फसल का कोड डालें।'
no_code_entered = 'माफ़ कीजिए, आपने फसल का कोड नही डाला है।\n\nकिसी भी फसल का रेट जानने के लिए 9246108080 पर मिस कॉल या SMS द्वारा फसल का कोड डालें।'
wrong_code_entered = 'माफ़ कीजिए, आपके द्वारा डाला गया कोड %s गलत है।\n\nकिसी भी फसल का रेट जानने के लिए 9246108080 पर मिस कॉल या SMS द्वारा फसल का कोड डालें।'
DND_MESSAGE = 'PLEASE CALL 01139585707 TO ACTIVATE THE SERVICE'

MARKET_INFO_CALL_RESPONSE_URL = 'http://%s%s'%(CURRENT_DOMAIN, '/loopivr/market_info_response/')
PUSH_MESSAGE_SMS_RESPONSE_URL = 'http://%s%s'%(CURRENT_DOMAIN, '/loopivr/push_message_sms_response/')
# For production
MARKET_INFO_APP = '137265'
# For Development
# MARKET_INFO_APP = '140902'

SMS_SENDER_NAME = 'LOOPDG'
TEXT_LOCAL_SINGLE_SMS_API = 'https://api.textlocal.in/send/'

TOP_SELLING_CROP_WINDOW = 30
N_TOP_SELLING_CROP = 5
ALL_FLAG_TRUE = 1
ALL_FLAG_FALSE = 0

PATTERN_REGEX = r'^([1-9]([0-9]*)[*, **]*)*$|^([0][*]{2}([1-9][*]?)+)$|^([1-9][0-9]*[*]{0,1})+[*]{2}[0]$'
CONTAINS_ZERO = r'^[0]$'
