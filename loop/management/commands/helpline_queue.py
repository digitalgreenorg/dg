__author__ = 'Vikas Saini'

import time
import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, MEDIA_ROOT

from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing
from loop.helpline_view import get_status, make_helpline_call, write_log
from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE

class Command(BaseCommand):

    def check_pending_or_not(self,incoming_call_id):
        incoming_call_obj = HelplineIncoming.objects.filter(id=incoming_call_id)
        if incoming_call_obj:
            incoming_call_obj = incoming_call_obj[0]
            # Check If Status of call is pending
            if incoming_call_obj.call_status == 0:
                # Fetch latest outgoing of respective Incoming
                latest_outgoing_of_incoming = HelplineOutgoing.objects.filter(incoming_call=incoming_call_obj).order_by('-id').values_list('call_id', flat=True)[:1]
                if len(latest_outgoing_of_incoming) != 0:
                    call_status = get_status(latest_outgoing_of_incoming[0])
                else: 
                    call_status = ''
                # Check If Pending call is already in-progress
                if call_status != '' and call_status['response_code'] == 200 and (call_status['status'] in ('ringing', 'in-progress')):
                        return ''
                return incoming_call_obj
            # If Status of call is not pending
            else:
                return ''
        # If Incoming Call object not found
        else:
            return ''

    def handle(self, *args, **options):
        # Check if State filter is required or not
        expert_obj = HelplineExpert.objects.filter(expert_status=1)[:1]
        working_hours = range(9,18)
        if expert_obj:
            expert_obj = expert_obj[0]
        else:
            #Log in file that no expert available
            module = "helpline_queue"
            write_log(HELPLINE_LOG_FILE,module,"No Expert Available")
            return
        old_time = datetime.datetime.now(timezone('Asia/Kolkata'))-timedelta(days=2)
        old_time = old_time.replace(tzinfo=None)
        try:
            HelplineIncoming.objects.filter(call_status=0,last_incoming_time__lte=old_time).update(call_status=2,time_modified=datetime.datetime.now())
        except Exception as e:
            module = "helpline_queue"
            write_log(HELPLINE_LOG_FILE,module,str(e))
        pending_incoming_call = HelplineIncoming.objects.filter(call_status=0).values('id','incoming_time','last_incoming_time')
        # Select pending calls from working hours only.
        for pending_call in pending_incoming_call:
            #incoming_hour = pending_call['incoming_time'].hour
            #last_incoming_hour = pending_call['last_incoming_time'].hour
            # Select calls which are incoming or last incoming between 9 AM to 6 PM
            #if (incoming_hour in working_hours) and (last_incoming_hour in working_hours):
            incoming_call_obj = self.check_pending_or_not(pending_call['id'])
            if incoming_call_obj:
                farmer_number = incoming_call_obj.from_number
                # Last parameter more than 0 only when we do not want to acknowledge User if call is not successfull
                make_helpline_call(incoming_call_obj,expert_obj,farmer_number,1)
                time.sleep(240)
