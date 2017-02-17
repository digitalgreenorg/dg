import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now

import dg.settings
from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing

class Command(BaseCommand):

    def send_mail(self,call_count,off_hours_call_count,pending_call_count,resolved_call_count,declined_call_count):
        subject = "JSLPS data entry status"
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['vikas@digitalgreen.org']
        body = '''Dear Team,\n\nThis is the status of yesterday calls:\n\n
                Total Incoming Calls: %s\nTotal Receiving Calls During Off Hours:%s\n
                Total Resolved Calls: %s\n
                Total Pending Calls: %s\nTotal Declined Calls: %s\n
                Please contact system@digitalgreen.org for any clarification.\n\n
                Thank you.\n
                '''%(call_count,off_hours_call_count,resolved_call_count,pending_call_count,declined_call_count)
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        msg.send()

    def handle(self, *args, **options):
        today_date = datetime.datetime.now().date()
        yesterday_date = today_date-timedelta(days=1)
        yesterday_incoming_call_count = HelplineCallLog.objects.filter(call_type=0,start_time__gte=yesterday_date,start_time__lt=today_date).count()
        yesterday_call_count = HelplineIncoming.objects.filter(last_incoming_time__gte=yesterday_date,last_incoming_time__lt=today_date).values('call_status').annotate(count=Count('call_status'))
        yesterday_resolved_call_count = yesterday_pending_call_count = yesterday_declined_call_count = 0
        # Change dates from Yesterday 6:00 PM to Today 9:00 AM (Non-Operational Hours of Helpline) 
        today_date = datetime.datetime.now().replace(hour=7,minute=0,second=0)
        yesterday_date = (today_date-timedelta(days=1)).replace(hour=18,minute=0,second=0)
        yesterday_off_hours_incoming_call_count = HelplineCallLog.objects.filter(call_type=0,start_time__gte=yesterday_date,start_time__lt=today_date).count()
        for call_count in yesterday_call_count:
            if call_count['call_status'] == 0:
                yesterday_pending_call_count = call_count['count']
            elif call_count['call_status'] == 1:
                yesterday_resolved_call_count = call_count['count']
            elif call_count['call_status'] == 2:
                yesterday_declined_call_count = call_count['count']
            else
                pass
        self.send_mail(yesterday_incoming_call_count,
            yesterday_off_hours_incoming_call_count,
            yesterday_pending_call_count,yesterday_resolved_call_count,
            yesterday_declined_call_count)
