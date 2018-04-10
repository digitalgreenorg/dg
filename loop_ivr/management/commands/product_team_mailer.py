from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from dg.settings import EMAIL_HOST_USER, team_contact
from push_sms_email import get_active_user_comp_info, get_total_queries_content
from loop_ivr.models import PriceInfoIncoming, SmsStatus
from django.core.mail import EmailMultiAlternatives
import pandas as pd


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('days', type=int)
        parser.add_argument('delay', type=int)

    def send_mail(self, email_subject, start_date, period_label, no_incoming_sms, no_sms_users, per_correct_code_entered_sms, no_incoming_call \
                        ,per_correct_code_entered_call, no_call_backs_time_limit, no_first_attempt_success, today_caller_object_sms_count, no_sms_sent \
                        , no_sms_dilivered, no_sms_diliver_time_limit, today_caller_object_call_count, today_rates_available_count):
        from_email = EMAIL_HOST_USER

        # to_email = ['sujit@digitalgreen.org']
        to_email = ['sujit@digitalgreen.org', 'abhisheklodha@digitalgreen.org']

        body_content = ['''Dear Team<br></br>%s Matrics: <b>(%s)</b><br>'''%(email_subject, start_date),
                        '''
                            <html>
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
                                        <b><u>UX - Incoming SMS</u></b>
                                        <table>
                                            <tbody>
                                                <tr>
                                                    <td><b># Incoming SMS</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b># SMS Users</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b>Correct Code Entered</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <br></br>
                                        <b><u> UX - Call</u></b>
                                        <table>
                                            <tbody>
                                                <tr>
                                                    <td><b># Incoming Calls </b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b> Correct Code Entered</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b># Call backs with time > t</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b># First Attempt Success </b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <br><br>
                                        <b><u>UX - Outgoing SMS</u></b>
                                        <table>
                                            <tbody>
                                                <tr>
                                                    <td><b>Total Queries</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b># SMS Sent</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b># SMS Delivered </b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b># SMS with Delivery Time > t sec </b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b>Total Correct Queries</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                                <tr>
                                                    <td><b> Queries with Rates NA</b></td>
                                                    <td><b>%s</b></td>
                                                </tr>
                                            </tbody>
                                        </table>
                        '''%(no_incoming_sms, no_sms_users, per_correct_code_entered_sms, no_incoming_call \
                        ,per_correct_code_entered_call, no_call_backs_time_limit, no_first_attempt_success, today_caller_object_sms_count, no_sms_sent \
                        , no_sms_dilivered, no_sms_diliver_time_limit, today_caller_object_call_count, today_rates_available_count),
                        '<br/><br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>Thank you.']
                                                # <tr>
                                                #     <td><b></b></td>
                                                #     <td><b></b></td>
                                                # </tr>
        body = ''.join(body_content)
        msg = EmailMultiAlternatives(email_subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()

    def handle(self, *args, **options):
        date_range = options['days']
        # delay should be in seconds
        delay = options['delay']
        period_label = {'1': 'Daily', '7' : 'Weekly'}
        comparison_param_label = {'1': 'DoD', '7': 'WoW' }

        # today_date = datetime.now().date()
        today_date = datetime(2018, 04, 11).date()
        start_date = today_date-timedelta(days=date_range)
        prev_start_date = start_date - timedelta(days=date_range)

        # Email Subject
        if date_range == 1 :
            email_subject = 'Loop Mandi Master - Daily Metrics: %s'%(start_date.strftime("%Y-%m-%d"),)
        elif date_range == 7 :
            email_subject = 'Loop Mandi Master - Weekly Metrics: %s - %s'%(start_date.strftime("%Y-%m-%d"),today_date.strftime("%Y-%m-%d"),) 

        comparison_param_label_str = comparison_param_label[str(options['days'])]
        period_label_str = period_label[str(options['days'])]

        # Today caller Object
        today_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=start_date,incoming_time__lt=today_date).exclude(from_number__in=team_contact)
        
        # Previous_start_date caller Object
        yesterday_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=prev_start_date,incoming_time__lt=start_date).exclude(from_number__in=team_contact)

        # SMS count
        today_caller_object_sms_count = today_caller_object.filter(call_source=3).count()
        yesterday_caller_object_sms_count = yesterday_caller_object.filter(call_source=3).count()

        no_incoming_sms = get_active_user_comp_info(today_caller_object_sms_count, yesterday_caller_object_sms_count, comparison_param_label_str)

        # SMS user count
        today_caller_object_sms_user_count = today_caller_object.filter(call_source=3).values_list('from_number', flat=True).distinct().count()
        yesterday_caller_object_sms_user_count = yesterday_caller_object.filter(call_source=3).values_list('from_number', flat=True).distinct().count()

        no_sms_users = get_active_user_comp_info(today_caller_object_sms_user_count, yesterday_caller_object_sms_user_count, comparison_param_label_str)

        # Correct Queries
        today_caller_object_correct_query_sms_count = today_caller_object.filter(call_source=3, info_status=1).count()
        yesterday_caller_object_correct_query_sms_count = yesterday_caller_object.filter(call_source=3, info_status=1).count()

        per_correct_code_entered_sms = get_active_user_comp_info(today_caller_object_correct_query_sms_count, yesterday_caller_object_correct_query_sms_count, comparison_param_label_str)

        # Incoming Calls
        today_caller_object_call_count = today_caller_object.filter(call_source__in=[1, 2]).count()
        yesterday_caller_object_call_count = yesterday_caller_object.filter(call_source__in=[1, 2]).count()

        no_incoming_call = get_active_user_comp_info(today_caller_object_call_count, yesterday_caller_object_call_count, comparison_param_label_str)

        today_caller_object_correct_query_call_count = today_caller_object.filter(call_source__in=[1, 2], info_status=1).count()
        yesterday_caller_object_correct_query_call_count = yesterday_caller_object.filter(call_source__in=[1, 2], info_status=1).count()

        per_correct_code_entered_call = get_active_user_comp_info(today_caller_object_correct_query_call_count, yesterday_caller_object_correct_query_call_count, comparison_param_label_str)

        # Wrong Code Entered via call
        today_caller_object_wrong_query_count = today_caller_object.filter(info_status=2).count()
        yesterday_caller_object_wrong_query_count = yesterday_caller_object.filter(info_status=2).count()

        no_wrong_query_code = get_active_user_comp_info(today_caller_object_wrong_query_count, yesterday_caller_object_wrong_query_count, comparison_param_label_str)

        # Total SMS Sent using textlocal
        today_smsstatus_obj = SmsStatus.objects.filter(price_info_incoming=today_caller_object)
        no_sms_sent = today_smsstatus_obj.count()
        no_sms_dilivered = today_smsstatus_obj.filter(status='D').count()

        # Queries with rates available
        today_rates_available_count = today_caller_object.filter(is_rate_available__in=[2, 3]).count()

        # values to be calculated
        no_call_backs_time_limit = ''
        no_first_attempt_success = today_caller_object.filter(info_status=1, prev_query_code__isnull=False).count()
        
        # timedelay for delivered messages
        df = pd.DataFrame(list(SmsStatus.objects.filter(price_info_incoming=today_caller_object).values('id','price_info_incoming','status', 'delivery_time', 'api_call_initiation_time')))
        df['time_delay'] = df.groupby('price_info_incoming')['api_call_initiation_time', 'delivery_time'].diff(axis='columns')['delivery_time']
        df_max = df.groupby('price_info_incoming')['time_delay'].max()
        time_delay = pd.Timedelta(seconds=delay)
        print type(df_max)
        no_sms_diliver_time_limit = df_max.loc[lambda x : x > time_delay].count()
        
        
        self.send_mail(email_subject, start_date, period_label_str, no_incoming_sms, no_sms_users, per_correct_code_entered_sms, no_incoming_call \
                        ,per_correct_code_entered_call, no_call_backs_time_limit, no_first_attempt_success, today_caller_object_sms_count, no_sms_sent \
                        , no_sms_dilivered, no_sms_diliver_time_limit, today_caller_object_call_count, today_rates_available_count )





        











