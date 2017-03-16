# -*- coding: utf-8 -*-

helpline_data = {'sms_body':'लूप मे कॉल के लिए धन्यवाद,आपको कुछ समय मे संपर्क करेगे, न.-01139595953', 
				 'working_hours_start': 9,
				 'working_hours_end': 21
				 }
CALL_STATUS_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Calls/%s?details=true'
CALL_REQUEST_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Calls/connect'
CALL_RESPONSE_URL = 'http://www.digitalgreen.org/loop/helpline_call_response/'
SMS_REQUEST_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Sms/send'
APP_REQUEST_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Calls/connect'
APP_URL = 'http://my.exotel.in/exoml/start/%s'
