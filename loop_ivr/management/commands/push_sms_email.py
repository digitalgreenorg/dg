__author__ = 'Vikas Saini'

from datetime import datetime, timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q, Count

from loop_ivr.models import PriceInfoIncoming
from loop.models import Farmer, LoopUser

from dg.settings import EMAIL_HOST_USER, team_contact

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('days', type=int)

    def send_mail(self, email_subject, period_label, active_caller_count, active_loop_farmer_count,
                active_non_loop_farmer_count, active_aggregators_count, total_queries_count,
                total_correct_queries_count, correct_queries_resolved_count, correct_queries_via_sms_count,
                correct_queries_via_call_count, total_queries_count_content, total_queries_via_sms_content, 
                total_queries_via_call_content, queries_per_person_content, top_users_content, matrix_date):
        from_email = EMAIL_HOST_USER
        # to_email = ['tech@digitalgreen.org']
        
        to_email = ['rikin@digitalgreen.org', 'saureen@digitalgreen.org', 'aditya@digitalgreen.org',
                    'vinay@digitalgreen.org', 'ashok@digitalgreen.org','bipin@digitalgreen.org', 
                    'lokesh@digitalgreen.org', 'sujit@digitalgreen.org','melbin@digitalgreen.org',
                    'erica@digitalgreen.org', 'abhisheklodha@digitalgreen.org']
        
        body_content = ['''Dear Team <br/><br/>%s Metrics: <b>(%s)</b><br>'''%(period_label, matrix_date),
                            '''<html>
                                <head>

                                    <style>
                                        tr, td { 
                                            border : 0.3px solid black;
                                            border-spacing : 0;
                                            padding : 10px;
                                            width: 250px;
                                        }
                                        table {
                                            border-spacing : 0;
                                        }
                                    </style>
                                </head>
                                <body>
                                    <br>
                                    <b><u>User breakdown</u></b>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <td><b>%s Active Users excluding DG staff*</b></td>
                                                <td><b>%s</b></td>
                                            </tr>
                                            <tr>
                                                <td>&emsp;&emsp;Loop Farmers </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td>&emsp;&emsp;Non-Loop Farmers </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td>&emsp;&emsp;Aggregators </td>
                                                <td>%s</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <br></br>
                                    <b><u>Channel Breakdown</u></b>
                                    <table>
                                        <tbody>
                                           <tr>
                                                <td><b>Total Request - Recieved</b></td>
                                                <td>%s</td>
                                           </tr>
                                            <tr>
                                                <td>&emsp;&emsp;via SMS</td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td>&emsp;&emsp;via Calls</td>
                                                <td>%s</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <br></br>
                                    <b><u>Requests - Correctness & Resolution</b></u>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <td><b>Total Requests</b></td>
                                                <td><b>%s</b></td>
                                            </tr>
                                            <tr>
                                                <td> &emsp;&emsp;&#37; Correct Requests </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> &emsp;&emsp;&emsp;&emsp;&#37; Correct Requests via SMS </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> &emsp;&emsp;&emsp;&emsp;&#37; Correct Requests via Calls </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> &emsp;&emsp;&#37; Correct Queries Resolved</td>
                                                <td>%s</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <br></br>
                                    <b><u>General :</u></b>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <td>Request Per User</td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td>Top Users</td>
                                                <td>%s</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </body></html>'''%(period_label, active_caller_count, active_loop_farmer_count,
                active_non_loop_farmer_count, active_aggregators_count, total_queries_count_content, total_queries_via_sms_content, 
                total_queries_via_call_content, total_queries_count, total_correct_queries_count, correct_queries_via_sms_count,
                correct_queries_via_call_count, correct_queries_resolved_count, queries_per_person_content,
                top_users_content), 
                '<br/><br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>Thank you.']
        body = ''.join(body_content)
        msg = EmailMultiAlternatives(email_subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()


    def handle(self, *args, **options):
        date_range = options['days']
        period_label = {'1': 'Daily', '7' : 'Weekly'}
        comparison_param_label = {'1': 'DoD', '7': 'WoW' }

        today_date = datetime.now().date()
        # today_date = datetime(2017, 11, 1).date()
        start_date = today_date-timedelta(days=date_range)
        prev_start_date = start_date - timedelta(days=date_range)
        
        if date_range == 1 :
            email_subject = 'Loop Mandi Master - Daily Metrics: %s'%(start_date.strftime("%Y-%m-%d"),)
        elif date_range == 7 :
            email_subject = 'Loop Mandi Master - Weekly Metrics: %s - %s'%(start_date.strftime("%Y-%m-%d"),today_date.strftime("%Y-%m-%d"),) 
            
        comparison_param_label_str = comparison_param_label[str(options['days'])]
        period_label_str = period_label[str(options['days'])]

        # Active Users excluding DG staff
        # from_number__in=last_fifteen_day_caller_no
        active_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=start_date,incoming_time__lt=today_date).exclude(from_number__in=team_contact)
        active_caller_count_object = active_caller_object.values_list('from_number', flat=True).distinct()
        # active_caller_count = active_caller_object.count()

        # Loop Farmers List
        loop_farmer_list = Farmer.objects.values_list('phone', flat=True).distinct()
        loop_farmer_list = map(lambda no: str(no) if no.startswith('0') else str('0'+no),loop_farmer_list)

        loop_aggregators_list = LoopUser.objects.values_list('phone_number', flat=True).distinct()
        loop_aggregators_list = map(lambda no: str(no) if no.startswith('0') else str('0'+no),loop_aggregators_list)

        # Yesterday active user Info
        active_caller_count, active_loop_farmer_count, active_non_loop_farmer_count,\
         active_aggregators_count = active_user_info(active_caller_object,\
                                                    loop_farmer_list, loop_aggregators_list)

        # Day before Yesterday active user info
        yesterday_active_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=prev_start_date,incoming_time__lt=start_date).exclude(from_number__in=team_contact)
        yesterday_active_caller_count_object = yesterday_active_caller_object.values_list('from_number', flat=True).distinct()
        active_caller_count_y, active_loop_farmer_count_y, active_non_loop_farmer_count_y,\
         active_aggregators_count_y = active_user_info(yesterday_active_caller_object,\
                                                    loop_farmer_list, loop_aggregators_list)
        # Active user info content
        active_caller_count_content = get_active_user_comp_info(active_caller_count, active_caller_count_y, comparison_param_label_str)
        active_loop_farmer_count_content = get_active_user_comp_info(active_loop_farmer_count, active_loop_farmer_count_y, comparison_param_label_str)
        active_non_loop_farmer_count_content = get_active_user_comp_info(active_non_loop_farmer_count, active_non_loop_farmer_count_y, comparison_param_label_str)
        active_aggregators_count_content = get_active_user_comp_info(active_aggregators_count, active_aggregators_count_y, comparison_param_label_str)

        # Total Queries
        total_queries_count = active_caller_object.count()
        total_queries_sms_count = active_caller_object.filter(call_source=3).count()
        total_queries_call_count = active_caller_object.filter(call_source__in=[1, 2]).count()

        # Yesterday Total queries
        total_queries_count_y = yesterday_active_caller_object.count()
        total_queries_sms_count_y = yesterday_active_caller_object.filter(call_source=3).count()
        total_queries_call_count_y = yesterday_active_caller_object.filter(call_source__in=[1, 2]).count()

        # Total Correct Queries
        total_correct_queries_obj = active_caller_object.filter(info_status=1)
        total_correct_queries_count = total_correct_queries_obj.count()

        # Correct Queries Resolved
        correct_queries_resolved_count = total_correct_queries_obj.exclude(Q(textlocal_sms_id='') | Q(textlocal_sms_id__isnull=True)).count()

        # Correct Queries via SMS
        correct_queries_via_sms_count = total_correct_queries_obj.filter(call_source=3).count()    

        # Correct Queries via Calls
        correct_queries_via_call_count = total_correct_queries_obj.filter(call_source__in=[1,2]).count()
        
        # Total queries Content
        total_queries_count_content = get_active_user_comp_info(total_queries_count, total_queries_count_y, comparison_param_label_str)
        total_queries_sms_count_content =  get_active_user_comp_info(total_queries_sms_count, total_queries_sms_count_y, comparison_param_label_str)
        total_queries_call_count_content =  get_active_user_comp_info(total_queries_call_count, total_queries_call_count_y, comparison_param_label_str)

        per_total_correct_queries_content = get_total_queries_content(total_correct_queries_count, total_queries_count)
        per_correct_queries_resolved_content = get_total_queries_content(correct_queries_resolved_count, total_correct_queries_count)
        per_correct_queries_via_sms_content = get_total_queries_content(correct_queries_via_sms_count, total_queries_sms_count)
        per_correct_queries_via_call_content = get_total_queries_content(correct_queries_via_call_count, total_queries_call_count)

        # Queries per person
        if active_caller_count == 0:
            queries_per_person_content = '-'
        else:
            queries_per_person = round(float(total_queries_count) / active_caller_count, 1)
            if active_caller_count_y == 0:
                queries_per_person_content = str(queries_per_person)
            else :
                queries_per_person_y = round(float(total_queries_count_y) / active_caller_count_y, 1)
                queries_per_person_content = get_active_user_comp_info(queries_per_person, queries_per_person_y, comparison_param_label_str)


        # Top Users
        top_users = list(active_caller_object.values('from_number').annotate(query_count=Count('call_id')).order_by('-query_count').values('from_number', 'query_count'))[:3]
        top_users_content = ''
        for obj in top_users :
            top_users_content = top_users_content + str(obj['from_number']) + \
                                ' (%s)'%(obj['query_count']) + '<br>'


        self.send_mail(email_subject, period_label_str, active_caller_count_content, active_loop_farmer_count_content,
         active_non_loop_farmer_count_content, active_aggregators_count_content, total_queries_count,
         per_total_correct_queries_content, per_correct_queries_resolved_content, per_correct_queries_via_sms_content,
         per_correct_queries_via_call_content,total_queries_count_content, total_queries_sms_count_content, total_queries_call_count_content,
         queries_per_person_content, top_users_content, start_date)

def active_user_info(active_caller_object, loop_farmer_list, loop_aggregators_list) :

    active_caller_object = active_caller_object.values_list('from_number', flat=True)
    # Active Users excluding DG staff
    active_caller_count = active_caller_object.distinct().count()

    # Daily Active Loop Farmers 
    active_loop_farmer_count = active_caller_object.filter(from_number__in=loop_farmer_list).exclude(from_number__in=loop_aggregators_list).distinct().count()

    # Daily Active Non-Loop Farmers
    active_non_loop_farmer_count = active_caller_object.exclude(from_number__in=loop_farmer_list).exclude(from_number__in=loop_aggregators_list).distinct().count()

    # Daily Active Aggregators 
    active_aggregators_count = active_caller_object.filter(from_number__in=loop_aggregators_list).distinct().count()

    return active_caller_count, active_loop_farmer_count, active_non_loop_farmer_count,\
         active_aggregators_count

def get_active_user_comp_info(active_user_today_info, active_user_yesterday_info, comparison_param_label_str) :
    res = str(active_user_today_info)
    diff = active_user_today_info - active_user_yesterday_info
    
    if active_user_yesterday_info == 0 :
        res = res + r' (- % up ' + '%s)' %(comparison_param_label_str,)
    else :
        if diff >= 0 :
            res = res + ' (%s '%(round(float(diff) / active_user_yesterday_info * 100)) + r' % up ' + '%s)' %(comparison_param_label_str,)
        else :
            res = res + ' (%s '%(round(float(abs(diff)) / active_user_yesterday_info * 100)) + r' % down ' + '%s)' %(comparison_param_label_str,)

    return res

def get_total_queries_content(total_correct_info, total_count_info) :
    if total_correct_info > 0 :
        per_total_correct_info = round(float(total_correct_info) / total_count_info * 100)
    else :
        per_total_correct_info = 0
    res = str(per_total_correct_info) + r'% ' + '(%s out of %s)'%(total_correct_info, total_count_info)
    return res
