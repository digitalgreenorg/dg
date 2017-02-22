import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.db.models import Count

import dg.settings
from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing, HelplineCallLog

class Command(BaseCommand):

    def send_mail(self,total_pending_call_count,
            total_declined_call_count,
            yesterday_declined_call_count,
            yesterday_off_hours_incoming_call_count,
            yesterday_received_call_count,
            yesterday_resolved_call_count):
    
        today_date = datetime.datetime.now().date()
        yesterday_date = today_date-timedelta(days=1)
        subject = "Loop IVR Helpline Call Status"
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['vikas@digitalgreen.org']
        body = 'Dear Team,\n\nThis is the status of calls:\n\nTotal Pending Calls:%s\nTotal Declined Calls: %s\nTotal Declined Calls on %s: %s\nTotal Receiving Calls During Off Hours on %s:%s\n\nPlease contact system@digitalgreen.org for any clarification.\n\nThank you.\n'%(total_pending_call_count,total_declined_call_count,
                                                                                                                                                                                                                                                                                    yesterday_date,yesterday_declined_call_count,
                                                                                                                                                                                                                                                                                    yesterday_date,yesterday_off_hours_incoming_call_count)
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        msg.send()

    def handle(self, *args, **options):
        today_date = datetime.datetime.now().date()
        yesterday_date = today_date-timedelta(days=1)
        working_hours = range(9,18)
        total_pending_call_count = 0
        total_declined_call_count = HelplineIncoming.objects.filter(call_status=2).count()
        yesterday_received_call_count = HelplineIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date).count()
        yesterday_resolved_call_count = HelplineIncoming.objects.filter(call_status=1,incoming_time__gte=yesterday_date,incoming_time__lt=today_date).count()
        yesterday_declined_call_count = HelplineIncoming.objects.filter(call_status=2,time_modified__gte=yesterday_date,time_modified__lt=today_date).count()
        # Change dates from Yesterday 6:00 PM to Today 9:00 AM (Non-Operational Hours of Helpline) 
        today_date = datetime.datetime.now().replace(hour=9,minute=0,second=0)
        yesterday_date = (today_date-timedelta(days=1)).replace(hour=18,minute=0,second=0)
        yesterday_off_hours_incoming_call_count = HelplineCallLog.objects.filter(call_type=0,start_time__gte=yesterday_date,start_time__lte=today_date).count()
        pending_call = HelplineIncoming.objects.filter(call_status=0).values('id','incoming_time','last_incoming_time')
        for call in pending_call:
            incoming_hour = call['incoming_time'].hour
            last_incoming_hour = call['last_incoming_time'].hour
            # Count Pending calls of working hours i.e. incoming time and last incoming time between 9 AM to 6 PM
            if (incoming_hour in working_hours) and (last_incoming_hour in working_hours):
                total_pending_call_count += 1

        self.send_mail(total_pending_call_count,
            total_declined_call_count,
            yesterday_declined_call_count,
            yesterday_off_hours_incoming_call_count,
            yesterday_received_call_count,
            yesterday_resolved_call_count)
