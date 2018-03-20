import urllib
from loop_ivr.models import PriceInfoIncoming
from datetime import datetime, timedelta
from dg.settings import TEXTLOCAL_API_KEY 
from django.core.management.base import BaseCommand
from pytz import timezone

class Command(BaseCommand):

    # Get TextLocal Sms Status
    def get_textlocal_sms_status(apikey, messageID):
        params = {'apikey': apikey, 'message_id': messageID}
        f = urllib.urlopen('https://api.textlocal.in/status_message/?'
            + urllib.urlencode(params))
        return (f.read(), f.code)

    def handle(self, *args, **options):
        today = datetime.now(timezone('Asia/Kolkata')).replace(tzinfo=None)

        sms_status_obj = SmsStatus.objects.filter(api_call_initiation_time=today)
        for smsobj in sms_status_obj:
            resp, code = self.get_textlocal_sms_status(TEXTLOCAL_API_KEY, smsobj['id'])
            smsobj = smsobj(status=resp['status'], delivery_time=resp['date'])
            smsobj.save()