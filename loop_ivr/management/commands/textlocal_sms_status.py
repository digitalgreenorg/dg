from loop_ivr.models import SmsStatus
from datetime import datetime
from dg.settings import TEXTLOCAL_API_KEY 
from django.core.management.base import BaseCommand
from loop_ivr.helper_function import get_textlocal_sms_status
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        # today = datetime(2018, 03, 21).date()
        today = datetime.now().date()
        sms_status_obj = SmsStatus.objects.filter(api_call_initiation_time__contains=today)
        for smsobj in sms_status_obj:
            resp = get_textlocal_sms_status(TEXTLOCAL_API_KEY, smsobj.textlocal_sms_id)
            resp = json.loads(resp)
            
            smsobj.status = resp['message']['status']
            smsobj.delivery_time = resp['message']['date']
            smsobj.save()
            