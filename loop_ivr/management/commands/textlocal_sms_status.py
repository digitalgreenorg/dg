import urllib
from loop_ivr.models import SmsStatus
from datetime import datetime
from dg.settings import TEXTLOCAL_API_KEY 
from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):

    # Get TextLocal Sms Status
    def get_textlocal_sms_status(self, apikey, messageID):
        params = {'apikey': apikey, 'message_id': messageID}
        f = urllib.urlopen('https://api.textlocal.in/status_message/?'
            + urllib.urlencode(params))
        return f.read()

    def handle(self, *args, **options):
        today = datetime.now().date()
        sms_status_obj = SmsStatus.objects.filter(api_call_initiation_time__contains=today)
        for smsobj in sms_status_obj:
            resp = self.get_textlocal_sms_status(TEXTLOCAL_API_KEY, smsobj.textlocal_sms_id)
            resp = json.loads(resp)
            
            smsobj.status = resp['message']['status']
            smsobj.delivery_time = resp['message']['date']
            smsobj.save()
            