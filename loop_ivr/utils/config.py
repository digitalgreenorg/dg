# -*- coding: utf-8 -*-
from dg.settings import MEDIA_ROOT

LOG_FILE = '%s/loop/loop_ivr_log.log'%(MEDIA_ROOT,)
AGGREGATOR_SMS_NO = '01139585707'

mandi_hi = 'मंडी'
indian_rupee = 'रु'
agg_sms_initial_line = 'लूप मंडी रेट\n'
agg_sms_no_price_for_combination = 'रेट उपलब्ध नही है\n'
agg_sms_no_price_available = 'इस मंडी और फसल के लिए पिछले तीन दिन के रेट उपलब्ध नही है.'

MARKET_INFO_CALL_RESPONSE_URL = 'http://www.digitalgreen.org/loopivr/market_info_response/'
MARKET_INFO_APP = '141649'