import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.db.models import Count

import dg.settings
from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing, HelplineCallLog

from loop.utils.ivr_helpline.helpline_data import helpline_data

class Command(BaseCommand):

    def send_mail(self,total_pending_call_count,
            total_declined_call_count,
            yesterday_declined_call_count,
            yesterday_off_hours_incoming_call_count,
            yesterday_received_call_count,
            yesterday_resolved_call_count):

        working_hours_start = helpline_data['working_hours_start']
        working_hours_end = helpline_data['working_hours_end']
        today_date = datetime.datetime.now().date()
        yesterday_date = today_date-timedelta(days=1)
        subject = "Loop IVR Helpline Call Status"
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['bipin@digitalgreen.org', 
                    'ashok@digitalgreen.org', 
                    'aditya@digitalgreen.org', 
                    'erica@digitalgreen.org',
                    'divish@digitalgreen.org',
                    'lokesh@digitalgreen.org',
                    'vikas@digitalgreen.org']
        email_body = ['<html>',
                    '<head><style>table, th, td {border: 1px solid black;}</style></head>',
                    '<body>',
                    'Dear Team,<br/><br/>This is the status of calls received on LOOP IVR Helpline number:<br/><br/>',
                    '<table>',
                    '<tr><th>Parameters</th><th>Count</th></tr>',
                    '<tr><td>Total Pending Calls Till Now (Received during Operational Hours)</td><td> %s</td></tr>'%(total_pending_call_count,),
                    '<tr><td>Total Received Calls on %s from %s:00 AM to %s:00 PM</td><td> %s</td></tr>'%(yesterday_date,working_hours_start,working_hours_end%12,yesterday_received_call_count),
                    '<tr><td>Total Attended Calls on %s from %s:00 AM to %s:00 PM</td><td> %s</td></tr>'%(yesterday_date,working_hours_start,working_hours_end%12,yesterday_resolved_call_count),
                    '<tr><td>Total Declined Calls Till now</td><td> %s</td></tr>'%(total_declined_call_count,),
                    '<tr><td>Total Declined Calls on %s</td><td> %s</td></tr>'%(yesterday_date,yesterday_declined_call_count),
                    '<tr><td>Total Received Calls During Off Hours i.e. %s:00 PM, %s to %s:00 AM, %s</td><td> %s</td></tr>'%(working_hours_end%12,yesterday_date,working_hours_start,today_date,yesterday_off_hours_incoming_call_count),
                    '</table>',
                    '<br/><br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>',
                    'Disclaimer: Please note that it\'s a automated system generated mail intended to provide notification for approximate number of OFF hours calls. ',
                    'You are requested to login to Exotel platform daily in the morning to plan your day accordingly.<br/><br/>',
                    'Thank you.<br/>',
                    '</body></html>'
                    ]
        body = ''.join(email_body)
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()

    def during_working_hour(self,call_obj):
        working_hours_start = helpline_data['working_hours_start']
        working_hours_end = helpline_data['working_hours_end']
        working_hours = range(working_hours_start,working_hours_end)
        count = 0
        for call in call_obj:
            incoming_hour = call['incoming_time'].hour
            last_incoming_hour = call['last_incoming_time'].hour
            # Count calls of working hours i.e. incoming time and last incoming time between 9 AM to 6 PM
            if (incoming_hour in working_hours) and (last_incoming_hour in working_hours):
                count += 1   
        return count     

    def handle(self, *args, **options):
        working_hours_start = helpline_data['working_hours_start']
        working_hours_end = helpline_data['working_hours_end']
        # Change dates from Yesterday 6:00 PM to Today 9:00 AM (Non-Operational Hours of Helpline).
        today_date = datetime.datetime.now().replace(hour=working_hours_start,minute=0,second=0)
        yesterday_date = today_date-timedelta(days=1)
        yesterday_date_morning = yesterday_date.replace(hour=working_hours_start,minute=0,second=0)
        yesterday_date_evening = yesterday_date.replace(hour=working_hours_end,minute=0,second=0)
        total_pending_call_count = 0
        # Total Calls declined Till now from beginning.
        total_declined_call = HelplineIncoming.objects.filter(call_status=2).values('id','incoming_time','last_incoming_time')
        total_declined_call_count = self.during_working_hour(total_declined_call)
        # Total Calls received by unique callers in working hours of previous day (i.e. 9 AM to 6 PM).
        yesterday_received_call_count = HelplineIncoming.objects.filter(incoming_time__gte=yesterday_date_morning,incoming_time__lte=yesterday_date_evening).count()
        # Total Calls received by unique callers and resolved within working hours of previous day (i.e. 9 AM to 6 PM).
        yesterday_resolved_call_count = HelplineIncoming.objects.filter(call_status=1,incoming_time__gte=yesterday_date_morning,incoming_time__lte=yesterday_date_evening).count()
        # Total Calls received by unique callers in non-working hours i.e. 6 PM of previous day to 9 AM of today.
        yesterday_off_hours_incoming_call_count = HelplineCallLog.objects.filter(call_type=0,start_time__gte=yesterday_date_evening,start_time__lte=today_date).count()
        # Total pending Calls that were not addressed for last two days,hence turned into declined previous day.
        today_date = datetime.datetime.now().date()
        yesterday_date = today_date-timedelta(days=1)
        yesterday_declined_call = HelplineIncoming.objects.filter(call_status=2,time_modified__gte=yesterday_date,time_modified__lte=today_date).values('id','incoming_time','last_incoming_time')
        yesterday_declined_call_count = self.during_working_hour(yesterday_declined_call)
        pending_call = HelplineIncoming.objects.filter(call_status=0).values('id','incoming_time','last_incoming_time')
        total_pending_call_count = self.during_working_hour(pending_call)

        self.send_mail(total_pending_call_count,
            total_declined_call_count,
            yesterday_declined_call_count,
            yesterday_off_hours_incoming_call_count,
            yesterday_received_call_count,
            yesterday_resolved_call_count)
