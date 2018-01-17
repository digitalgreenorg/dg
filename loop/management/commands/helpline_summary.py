from datetime import datetime, timedelta
from pytz import timezone
import calendar

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.db.models import Count, Sum

from loop.models import HelplineIncoming, HelplineCallLog, Farmer, LoopUserAssignedVillage
from dg.settings import EMAIL_HOST_USER

class Command(BaseCommand):
    # parse arguments from command line
    def add_arguments(self, parser):
        # create mutually exclusive command line switches
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-fd',
                           dest='from_date',default=None,
                           help='Enter From date in format \'yyyy-mm-dd\' without quotes')

        parser.add_argument('-td',
                            dest='to_date',default=None,
                            help='Enter To date in format \'yyyy-mm-dd\' without quotes')

        group.add_argument('-nd',
                           dest='last_n_days',default=None,
                           help='Data of last n days')

        group.add_argument('-lm',
                           dest='last_month',default=None,
                           help='Enter 1 with this option for retrieve data of last month')

        parser.add_argument('-a',
                            dest='all_data',default=None,
                            help='Enter 1 with this option for retrieve all data')

        parser.add_argument('-e',
                            dest='to_email',default=None,
                            help='Enter email id to which you want to mail summary')

    # send Email
    def send_mail(self,summary_data,subject):
        from_email = EMAIL_HOST_USER
        to_email = ['vikas@digitalgreen.org','erica@digitalgreen.org','lokesh@digitalgreen.org','divish@digitalgreen.org']
        body = 'Dear Team,<br/><br/>This is the status of calls on LOOP IVR Helpline number:<br/><br/>'
        body += summary_data
        body += '<br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>Thanks you.'
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()

    # Cluster-wise bifurcation of calls received(farmer count, number of calls)
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

    def helpline_summary(self,from_date,to_date,include_extra_summary=0):
        total_calls_received = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).count()
        total_unique_caller = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).values_list('from_number').distinct().count()
        total_repeat_caller = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).values('from_number').annotate(call_count=Count('from_number')).filter(call_count__gt=1).count()
        total_calls_from_repeat_caller = HelplineCallLog.objects.filter(call_type=0,start_time__gte=from_date,start_time__lte=to_date).values('from_number').annotate(call_count=Count('from_number')).filter(call_count__gt=1).aggregate(Sum('call_count')).get('call_count__sum')
        if total_calls_from_repeat_caller == None:
            total_calls_from_repeat_caller = 0
        total_calls_resolved = HelplineIncoming.objects.filter(call_status=1,incoming_time__gte=from_date,incoming_time__lte=to_date).count()
        cluster_wise_call_detail = self.cluster_wise_bifurcation(from_date,to_date)
        if total_calls_received > 0:
            repeat_caller_contribute_percentage = round((total_calls_from_repeat_caller*100.0) / total_calls_received,2)
        else:
            repeat_caller_contribute_percentage = 0
        summary_data = '<html>'
        summary_data += '<head><style>table, th, td {border: 1px solid black;}</style></head><body>'
        if from_date == to_date:
            summary_data += 'Total Calls Received: %s<br/>Total Calls Handled by experts: %s<br/>\
Total Unique Callers: %s<br/>Cluster-wise bifurcation of calls received:<br/>'%(total_calls_received,total_calls_resolved,
        total_unique_caller)
        else:
            summary_data += 'Total Calls Received: %s<br/>Total Unique Callers: %s<br/>\
Total number of repeat caller: %s<br/>Total Calls from repeat callers: %s<br/>\
%% of calls contributed by repeat callers: %s<br/>Cluster-wise bifurcation of calls received:<br/><br/>'%(total_calls_received,
        total_unique_caller,total_repeat_caller,total_calls_from_repeat_caller,repeat_caller_contribute_percentage)
        summary_data += '<table><tr><th>Cluster Name</th><th>Farmer Count</th><th>No of calls</th></tr>'
        for cluster in cluster_wise_call_detail:
            summary_data += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(cluster_wise_call_detail[cluster]['cluster_name'],cluster_wise_call_detail[cluster]['farmer_count'],cluster_wise_call_detail[cluster]['total_calls'])
        summary_data += '</table>'
        if include_extra_summary == 1:
            call_resoved_per_expert = HelplineIncoming.objects.filter(call_status=1).values('resolved_by__name').annotate(call_count=Count('id'))
            summary_data += '<br/>Total Calls Handled by experts: %s<br/>Bifurcation of calls per expert:<br/><br/>'%(total_calls_resolved,)
            summary_data += '<table><tr><th>Expert Name</th><th>No of calls handled</th></tr>'
            for expert in call_resoved_per_expert:
                summary_data += '<tr><td>%s</td><td>%s</td></tr>'%(expert['resolved_by__name'],expert['call_count'])
            summary_data += '</table>'
        summary_data += '</body><html>'
        return summary_data

    # generate the summary for the given command line arguments
    def handle(self, *args, **options):
        all_data = options.get('all_data')
        last_month = options.get('last_month')
        last_n_days = options.get('last_n_days')
        from_date = options.get('from_date')
        to_date = options.get('to_date')
        to_email = options.get('to_email')

        if all_data != None:
            summary_data = self.helpline_summary('2017-01-01',datetime.now().date(),1)
            email_subject = 'Loop helpline Summary from the begining'
            self.send_mail(summary_data,email_subject)
        elif last_month != None:
            current_month = datetime.now().month
            current_year = datetime.now().year
            if current_month == 1:
                from_date = '%s-12-01'%(current_year-1,)
                to_date = '%s-01-01'%(current_year,)
            else:
                from_date = '%s-%s-01'%(current_year,current_month-1)
                to_date = '%s-%s-01'%(current_year,current_month)
            summary_data = self.helpline_summary(from_date,to_date)
            summary_data += '<br/><br/>Helpline Summary from Begining.<br/><br/>'
            summary_data += self.helpline_summary('2017-01-01',datetime.now().date(),1)
            email_subject = 'Loop helpline Summary from %s to %s'%(from_date,to_date)
            self.send_mail(summary_data,email_subject)
        elif last_n_days != None:
            from_date = datetime.now().date()-timedelta(days=int(last_n_days))
            to_date = datetime.now().date()
            if last_n_days == '1':
                email_subject = 'Loop helpline Summary for %s'%(from_date,)
            else:
                email_subject = 'Loop helpline Summary from %s to %s'%(from_date.strftime("%Y-%m-%d"),(datetime.now().date()-timedelta(days=1)).strftime("%Y-%m-%d"))
            summary_data = self.helpline_summary(from_date,to_date)
            self.send_mail(summary_data,email_subject)
        elif from_date != None:
            if not to_date:
                print 'Please enter to_date with -td option'
                return
            elif from_date > current_date:
                print 'From date is greater than current date'
                return
            email_subject = 'Loop helpline Summary from the begining from %s to %s'%(from_date.strftime("%Y-%m-%d"),to_date.strftime("%Y-%m-%d"))
            summary_data = self.helpline_summary(from_date,to_date)
            self.send_mail(summary_data,email_subject)
        else:
            print "Please Enter atleast one choice, user -h option for see available options"
