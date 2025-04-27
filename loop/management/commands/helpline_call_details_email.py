import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.db.models import Count, Sum

import dg.settings
from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing, HelplineCallLog, \
    Farmer, LoopUserAssignedVillage

from loop.utils.ivr_helpline.helpline_data import helpline_data
from loop.management.commands.helpline_summary import Command

class Command(BaseCommand):

    def send_mail(self,total_pending_call_count,
            total_declined_call_count,
            yesterday_declined_call_count,
            yesterday_off_hours_incoming_call_count,
            yesterday_received_call_count,
            yesterday_resolved_call_count,
            total_calls_received,
            total_unique_caller,
            total_repeat_caller,
            total_calls_from_repeat_caller,
            repeat_caller_contribute_percentage,
            cluster_wise_call_detail_list):

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
                    '<tr><td>Total Calls Received</td><td> %s</td></tr>'%(total_calls_received,),
                    '<tr><td>Total Unique Callers</td><td> %s</td></tr>'%(total_unique_caller,),
                    '<tr><td>Total number of repeat caller</td><td> %s</td></tr>'%(total_repeat_caller,),
                    '<tr><td>Total Calls from repeat callers</td><td> %s</td></tr>'%(total_calls_from_repeat_caller,),
                    '<tr><td>%% of calls contributed by repeat callers</td><td> %s</td></tr>'%(repeat_caller_contribute_percentage,),
                    '<tr><td>Total Pending Calls Till Now</td><td> %s</td></tr>'%(total_pending_call_count,),
                    '<tr><td>Total Received Calls on %s from %s:00 AM to %s:00 PM</td><td> %s</td></tr>'%(yesterday_date,working_hours_start,working_hours_end%12,yesterday_received_call_count),
                    '<tr><td>Total Attended Calls on %s from %s:00 AM to %s:00 PM</td><td> %s</td></tr>'%(yesterday_date,working_hours_start,working_hours_end%12,yesterday_resolved_call_count),
                    '<tr><td>Total Declined Calls Till now</td><td> %s</td></tr>'%(total_declined_call_count,),
                    '<tr><td>Total Declined Calls on %s</td><td> %s</td></tr>'%(yesterday_date,yesterday_declined_call_count),
                    '<tr><td>Total Received Calls During Off Hours i.e. %s:00 PM, %s to %s:00 AM, %s</td><td> %s</td></tr>'%(working_hours_end%12,yesterday_date,working_hours_start,today_date,yesterday_off_hours_incoming_call_count),
                    '</table>',
                    '<br/>'] + \
                    cluster_wise_call_detail_list + \
                    ['<br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>',
                    'Disclaimer: Please note that it\'s a automated system generated mail intended to provide notification for approximate number of OFF hours calls. ',
                    'You are requested to login to Exotel platform daily in the morning to plan your day accordingly.<br/><br/>',
                    'Thank you.<br/>',
                    '</body></html>'
                    ]
        body = ''.join(email_body)
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()


    def cluster_wise_bifurcation(self,from_date,to_date):
        phone_to_village_map = dict()
        village_to_call_detail_map = dict()
        cluster_wise_call_detail = dict()
        farmer_detail = Farmer.objects.values('phone','village_id')
        call_count_per_no = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).values('from_number').annotate(call_count=Count('from_number'))
        for farmer in farmer_detail:
            phone_to_village_map[farmer['phone']] = farmer['village_id']
        for call in call_count_per_no:
            farmer_number = call['from_number']
            farmer_number_possibilities = [farmer_number.lstrip('0'), farmer_number, '0'+farmer_number, '91'+farmer_number.lstrip('0'), '+91'+farmer_number.lstrip('0')]
            for number in farmer_number_possibilities:
                if number in phone_to_village_map:
                    if phone_to_village_map[number] not in village_to_call_detail_map:
                        village_to_call_detail_map[phone_to_village_map[number]] = {'farmer_count':1,'total_calls':call['call_count']}
                    else:
                        village_to_call_detail_map[phone_to_village_map[number]]['farmer_count'] += 1
                        village_to_call_detail_map[phone_to_village_map[number]]['total_calls'] += call['call_count']
                    break
        loopuser_assigned_village = LoopUserAssignedVillage.objects.values('loop_user_id','loop_user__name','village_id')
        for user in loopuser_assigned_village:
            if user['loop_user_id'] not in cluster_wise_call_detail:
                cluster_wise_call_detail[user['loop_user_id']] = dict()
                cluster_wise_call_detail[user['loop_user_id']]['cluster_name'] = user['loop_user__name']
                cluster_wise_call_detail[user['loop_user_id']]['farmer_count'] = 0
                cluster_wise_call_detail[user['loop_user_id']]['total_calls'] = 0
            if user['village_id'] in village_to_call_detail_map:
                cluster_wise_call_detail[user['loop_user_id']]['farmer_count'] += village_to_call_detail_map[user['village_id']]['farmer_count']
                cluster_wise_call_detail[user['loop_user_id']]['total_calls'] += village_to_call_detail_map[user['village_id']]['total_calls']
        return cluster_wise_call_detail


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
        # Total Calls received during operational hours only and got declined Till now from beginning.
        total_declined_call_count = HelplineIncoming.objects.filter(call_status=2).count()#.values('id','incoming_time','last_incoming_time')
        # Total Calls received by unique callers in working hours of previous day (i.e. x AM to y PM).
        yesterday_received_call_count = HelplineIncoming.objects.filter(incoming_time__gte=yesterday_date_morning,incoming_time__lte=yesterday_date_evening).count()
        # Total Calls received by unique callers and resolved within working hours of previous day (i.e. x AM to y PM).
        yesterday_resolved_call_count = HelplineIncoming.objects.filter(call_status=1,incoming_time__gte=yesterday_date_morning,incoming_time__lte=yesterday_date_evening).count()
        # Total Calls received by unique callers in non-working hours i.e. y PM of previous day to x AM of today.
        yesterday_off_hours_incoming_call_count = HelplineCallLog.objects.filter(call_type=0,start_time__gte=yesterday_date_evening,start_time__lte=today_date).count()
        today_date = datetime.datetime.now().date()
        yesterday_date = today_date-timedelta(days=1)
        # Total pending Calls received in operation hours that were not addressed for last two days, hence turned into declined previous day.
        yesterday_declined_call_count = HelplineIncoming.objects.filter(call_status=2,time_modified__gte=yesterday_date,time_modified__lte=today_date).count()#.values('id','incoming_time','last_incoming_time')
        total_pending_call_count = HelplineIncoming.objects.filter(call_status=0).count()#.values('id','incoming_time','last_incoming_time')

        #total_pending_call_count = self.during_working_hour(pending_call)
        #total_declined_call_count = self.during_working_hour(total_declined_call)
        #yesterday_declined_call_count = self.during_working_hour(yesterday_declined_call)

        # Extra Information
        from_date = datetime.datetime.now().date()-timedelta(days=1)
        to_date = datetime.datetime.now().date()
        total_calls_received = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).count()
        total_unique_caller = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).values_list('from_number').distinct().count()
        total_repeat_caller = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).values('from_number').annotate(call_count=Count('from_number')).filter(call_count__gt=1).count()
        total_calls_from_repeat_caller = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).values('from_number').annotate(call_count=Count('from_number')).filter(call_count__gt=1).aggregate(Sum('call_count')).get('call_count__sum')
        if total_calls_from_repeat_caller == None:
            total_calls_from_repeat_caller = 0
        if total_calls_received > 0:
            repeat_caller_contribute_percentage = round((total_calls_from_repeat_caller*100.0) / total_calls_received,2)
        else:
            repeat_caller_contribute_percentage = 0
        if total_calls_received > 0:
            cluster_wise_call_detail = self.cluster_wise_bifurcation(from_date,to_date)
            cluster_wise_call_detail_list = ['<br/><br/>Cluster-wise bifurcation of calls received:<br/><br/>',
                                            '<table><tr><th>Cluster Name</th><th>Farmer Count</th><th>No of calls</th></tr>']
            other_cluster_farmer_count = total_unique_caller
            other_cluster_call_count = total_calls_received
            for cluster in cluster_wise_call_detail:
                if cluster_wise_call_detail[cluster]['total_calls'] != 0:
                    other_cluster_farmer_count -= cluster_wise_call_detail[cluster]['farmer_count']
                    other_cluster_call_count -= cluster_wise_call_detail[cluster]['total_calls']
                    cluster_wise_call_detail_list.append('<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(cluster_wise_call_detail[cluster]['cluster_name'],cluster_wise_call_detail[cluster]['farmer_count'],cluster_wise_call_detail[cluster]['total_calls']))
            if other_cluster_call_count > 0:
                cluster_wise_call_detail_list.append('<tr><td>Others</td><td>%s</td><td>%s</td></tr>'%(other_cluster_farmer_count,other_cluster_call_count))
            cluster_wise_call_detail_list.append('</table>')
        else:
            cluster_wise_call_detail_list = []

        self.send_mail(total_pending_call_count,
            total_declined_call_count,
            yesterday_declined_call_count,
            yesterday_off_hours_incoming_call_count,
            yesterday_received_call_count,
            yesterday_resolved_call_count,
            total_calls_received,
            total_unique_caller,
            total_repeat_caller,
            total_calls_from_repeat_caller,
            repeat_caller_contribute_percentage,
            cluster_wise_call_detail_list)
