__author__ = 'Vikas Saini'

import time
import csv
import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, MEDIA_ROOT

from loop.models import JharkhandIncoming
from loop.helpline_view import get_status, write_log
from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE

import pandas as pd

class Command(BaseCommand):

    def make_helpline_call(self,name,to_number,from_number):
        CALL_REQUEST_URL = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Calls/connect'
        CALL_RESPONSE_URL = 'http://sandbox.digitalgreen.org/loop/helpline_call_response/'
        EXOTEL_HELPLINE_NUMBER = from_number
        call_request_url = CALL_REQUEST_URL%(EXOTEL_ID,EXOTEL_TOKEN,EXOTEL_ID)
        call_response_url = CALL_RESPONSE_URL
        # CallType is either Transactional or Promotional
        parameters = {'From':from_number,'To':to_number,'CallerId':EXOTEL_HELPLINE_NUMBER,'CallType':'trans','StatusCallback':call_response_url}
        response = requests.post(call_request_url,data=parameters)
        module = 'make_helpline_call'
        if response.status_code == 200:
            response_tree = xml_parse.fromstring((response.text).encode('utf-8'))
            call_detail = response_tree.findall('Call')[0]
            outgoing_call_id = str(call_detail.find('Sid').text)
            outgoing_call_time = str(call_detail.find('StartTime').text)
            outgoing_obj = JharkhandIncoming(call_id=outgoing_call_id,name=name,from_number=from_number,
                                            to_number=to_number,start_time=outgoing_call_time, is_broadcast=1,
                                            call_type=1)
            try:
                outgoing_obj.save()    
            except Exception as e:
                # Save Errors in Logs
                write_log(HELPLINE_LOG_FILE,module,str(e))
        else:
            # Enter in Log
            log = 'Status Code: %s (Parameters: %s)'%(str(response.status_code),parameters)
            write_log(HELPLINE_LOG_FILE,module,log)

    def handle(self, *args, **options):
        csv_header = ['phone']
        file_name = 'jharkhand_list.xlsx'
        from_number = '01139589707'
        open_file = pd.ExcelFile(file_name)
        contact_detail = open_file.parse("Sheet1")
        print contact_detail.head()
        for row,contact in contact_detail.iterrows():
            name =  contact['name']
            phone = contact['phone']
            self.call_to_number(name,phone,from_number)
            time.sleep(1)
