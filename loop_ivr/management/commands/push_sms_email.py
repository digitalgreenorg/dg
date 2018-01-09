__author__ = 'Vikas Saini'

from datetime import datetime, timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

from loop_ivr.models import PriceInfoIncoming
from loop.models import Farmer, LoopUser

from dg.settings import EMAIL_HOST_USER, team_contact

class Command(BaseCommand):

    def send_mail(self, email_subject, active_caller_count, active_loop_farmer_count,
                active_non_loop_farmer_count, active_aggregators_count, total_queries_count,
                total_correct_queries_count, correct_queries_resolved_count, correct_queries_via_sms_count,
                correct_queries_via_call_count):
        from_email = EMAIL_HOST_USER
        to_email = ['sujit@digitalgreen.org', 'abhisheklodha@digitalgreen.org', 'aditya@digitalgreen.org']

        # to_email = ['rikin@digitalgreen.org', 'saureen@digitalgreen.org', 'aditya@digitalgreen.org',
        #             'vinay@digitalgreen.org', 'divish@digitalgreen.org', 'ashok@digitalgreen.org',
        #             'bipin@digitalgreen.org', 'lokesh@digitalgreen.org', 'sujit@digitalgreen.org',
        #             'melbin@digitalgreen.org', 'erica@digitalgreen.org', 'abhisheklodha@digitalgreen.org']
        
        body_content = ['''Dear Team <br/><br/>''',
                            '''<html>
                                <head>
                                    <style>
                                        tr, td { 
                                            border : 0.3px solid black;
                                            border-spacing : 0;
                                            padding : 10px;
                                        }
                                        table {
                                            border-spacing : 0;
                                        }
                                    </style>
                                </head>
                                <body>
                                    <i>How We are doing at user engagement?</i>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <td><b>Daily Active Users excluding DG staff*</b></td>
                                                <td><b>%s</b></td>
                                            </tr>
                                            <tr>
                                                <td> Daily Active Loop Farmers </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> Daily Active Non-Loop Farmers </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> Daily Active Aggregators </td>
                                                <td>%s</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <br></br>
                                    <i>Are we able to meet users requirements? </i>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <td><b>Total Queries</b></td>
                                                <td><b>%s</b></td>
                                            </tr>
                                            <tr>
                                                <td> &#37; Correct Queries </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> &#37; Correct Queries Resolved </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> &#37; Correct Queries via SMS </td>
                                                <td>%s</td>
                                            </tr>
                                            <tr>
                                                <td> &#37; Correct Queries via Calls </td>
                                                <td>%s</td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </body></html>'''%(active_caller_count, active_loop_farmer_count,
                active_non_loop_farmer_count, active_aggregators_count, total_queries_count,
                total_correct_queries_count, correct_queries_resolved_count, correct_queries_via_sms_count,
                correct_queries_via_call_count), 
                '<br/><br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>Thanks you.']
        body = ''.join(body_content)
        msg = EmailMultiAlternatives(email_subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()


    def handle(self, *args, **options):
        today_date = datetime.now().date()
        # today_date = datetime(2017, 11, 1).date()
        yesterday_date = today_date-timedelta(days=1)
        one_day_before_yesterday_date = yesterday_date - timedelta(days=1)
        fifteen_day_back_date = today_date-timedelta(days=16)
        sixteen_day_back_date = today_date-timedelta(days=17)

        # excluding yesterday, because we are counting matrices for yeseterday.
        last_fifteen_day_caller_no = list(PriceInfoIncoming.objects.filter(incoming_time__gte=fifteen_day_back_date,incoming_time__lt=yesterday_date).exclude(from_number__in=team_contact).values_list('from_number',flat=True))

        last_sixteen_day_caller_no = list(PriceInfoIncoming.objects.filter(incoming_time__gte=sixteen_day_back_date,incoming_time__lt=one_day_before_yesterday_date).exclude(from_number__in=team_contact).values_list('from_number',flat=True))

        email_subject = 'Loop Mandi Master - Daily Metrics: %s'%(yesterday_date.strftime("%Y-%m-%d"),)

        # Active Users excluding DG staff
        active_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date,from_number__in=last_fifteen_day_caller_no).exclude(from_number__in=team_contact).values_list('from_number', flat=True).distinct()
        # active_caller_count = active_caller_object.count()

        # Loop Farmers List
        loop_farmer_list = Farmer.objects.values_list('phone', flat=True).distinct()
        loop_farmer_list = map(lambda no: str(no) if no.startswith('0') else str('0'+no),loop_farmer_list)

        loop_aggregators_list = LoopUser.objects.values_list('phone_number', flat=True).distinct()
        loop_aggregators_list = map(lambda no: str(no) if no.startswith('0') else str('0'+no),loop_aggregators_list)

        # Yesterday active user Info
        active_caller_count, active_loop_farmer_count, active_non_loop_farmer_count,\
         active_aggregators_count = active_user_info(active_caller_object, last_fifteen_day_caller_no,\
                                                    loop_farmer_list, loop_aggregators_list)

        # Day before Yesterday active user info
        yesterday_active_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=one_day_before_yesterday_date,incoming_time__lt=yesterday_date,from_number__in=last_fifteen_day_caller_no).exclude(from_number__in=team_contact).values_list('from_number', flat=True).distinct()
        active_caller_count_y, active_loop_farmer_count_y, active_non_loop_farmer_count_y,\
         active_aggregators_count_y = active_user_info(yesterday_active_caller_object, last_sixteen_day_caller_no,\
                                                    loop_farmer_list, loop_aggregators_list)
        # Active user info content
        active_caller_count_content = get_active_user_comp_info(active_caller_count, active_caller_count_y)
        active_loop_farmer_count_content = get_active_user_comp_info(active_loop_farmer_count, active_loop_farmer_count_y)
        active_non_loop_farmer_count_content = get_active_user_comp_info(active_non_loop_farmer_count, active_non_loop_farmer_count_y)
        active_aggregators_count_content = get_active_user_comp_info(active_aggregators_count, active_aggregators_count_y)

        # Total Queries
        total_queries_count = active_caller_object.count()
        total_queries_sms_count = active_caller_object.filter(call_source=3).count()
        total_queries_call_count = active_caller_object.filter(call_source__in=[1, 2]).count()

        # Total Correct Queries
        total_correct_queries_obj = active_caller_object.filter(info_status=1)
        total_correct_queries_count = total_correct_queries_obj.count()

        # Correct Queries Resolved
        correct_queries_resolved_count = total_correct_queries_obj.exclude(Q(textlocal_sms_id='') | Q(textlocal_sms_id__isnull=True)).count()

        # Correct Queries via SMS
        correct_queries_via_sms_count = total_correct_queries_obj.filter(call_source=3).count()    

        # Correct Queries via Calls
        correct_queries_via_call_count = total_correct_queries_obj.filter(call_source__in=[1,2]).count()
        

        per_total_correct_queries_content = get_total_queries_content(total_correct_queries_count, total_queries_count)
        per_correct_queries_resolved_content = get_total_queries_content(correct_queries_resolved_count, total_correct_queries_count)
        per_correct_queries_via_sms_content = get_total_queries_content(correct_queries_via_sms_count, total_queries_sms_count)
        per_correct_queries_via_call_content = get_total_queries_content(correct_queries_via_call_count, total_queries_call_count)


        self.send_mail(email_subject, active_caller_count_content, active_loop_farmer_count_content,
         active_non_loop_farmer_count_content, active_aggregators_count_content, total_queries_count,
         per_total_correct_queries_content, per_correct_queries_resolved_content, per_correct_queries_via_sms_content,
         per_correct_queries_via_call_content)

def active_user_info(active_caller_object, last_fifteen_day_caller_no, loop_farmer_list, loop_aggregators_list) :

    # Active Users excluding DG staff
    active_caller_count = active_caller_object.count()

    # Daily Active Loop Farmers 
    active_loop_farmer_count = active_caller_object.filter(from_number__in=loop_farmer_list).count()

    # Daily Active Non-Loop Farmers
    active_non_loop_farmer_count = active_caller_object.exclude(from_number__in=loop_farmer_list).exclude(from_number__in=loop_aggregators_list).count()

    # Daily Active Aggregators 
    active_aggregators_count = active_caller_object.filter(from_number__in=loop_aggregators_list).count()

    return active_caller_count, active_loop_farmer_count, active_non_loop_farmer_count,\
         active_aggregators_count


def get_active_user_comp_info(active_user_today_info, active_user_yesterday_info) :
    res = str(active_user_today_info)
    diff = active_user_today_info - active_user_yesterday_info
    
    if active_user_yesterday_info == 0 :
        res = res + r' ( - % up DoD)'
    else :
        if diff >= 0 :
            res = res + ' ( %s '%(round(float(diff) / active_user_yesterday_info * 100)) + r' % up DoD)'
        else :
            res = res + ' ( %s '%(round(float(abs(diff)) / active_user_yesterday_info * 100)) + r' % down DoD)'

    return res

def get_total_queries_content(total_correct_info, total_count_info) :
    if total_correct_info > 0 :
        per_total_correct_info = round(float(total_correct_info) / total_count_info * 100)
    else :
        per_total_correct_info = 0
    res = str(per_total_correct_info) + r'% ' + '(%s out of %s)'%(total_correct_info, total_count_info)
    return res
