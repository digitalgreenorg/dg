# -*- coding: utf-8 -*-
from dg.settings import MEDIA_ROOT, CURRENT_DOMAIN

helpline_data = {'sms_body':'लूप मे कॉल के लिए धन्यवाद,आपको कुछ समय मे संपर्क करेगे, न.-01139595953', 
				 'working_hours_start': 9,
				 'working_hours_end': 21
				 }
CALL_STATUS_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Calls/%s?details=true'
CALL_REQUEST_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Calls/connect'
CALL_RESPONSE_URL = 'http://%s%s'%(CURRENT_DOMAIN, '/loop/helpline_call_response/')
SMS_REQUEST_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Sms/send'
APP_REQUEST_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Calls/connect'
APP_URL = 'http://my.exotel.in/exoml/start/%s'
HELPLINE_LOG_FILE = '%s/loop/helpline_log.log'%(MEDIA_ROOT,)
BROADCAST_RESPONSE_URL = 'http://%s%s'%(CURRENT_DOMAIN, '/loop/broadcast_call_response/')
BROADCAST_S3_BUCKET_NAME = 'dg_ivrs'
BROADCAST_S3_UPLOAD_PATH = 'broadcast/%s'
BROADCAST_S3_AUDIO_URL = 'https://s3.amazonaws.com/%s/%s'%(BROADCAST_S3_BUCKET_NAME,BROADCAST_S3_UPLOAD_PATH)
BROADCAST_PENDING_TIME = 2
BROADCAST_AUDIO_PATH = '%s/loop/broadcast/audio/'%(MEDIA_ROOT,)
BROADCAST_FARMER_PATH = '%s/loop/broadcast/farmer/'%(MEDIA_ROOT,)
