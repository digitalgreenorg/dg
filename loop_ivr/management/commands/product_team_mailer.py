from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from dg.settings import EMAIL_HOST_USER, team_contact
from push_sms_email import get_active_user_comp_info, get_total_queries_content, active_user_info
from loop_ivr.models import PriceInfoIncoming

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('days', type=int)

    def handle(self, *args, **options):
        date_range = options['days']
        

        # today_date = datetime.now().date()
        today_date = datetime(2018, 03, 21).date()
        start_date = today_date-timedelta(days=date_range)
        prev_start_date = start_date - timedelta(days=date_range)

        # Today caller Object
        today_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=start_date,incoming_time__lt=today_date).exclude(from_number__in=team_contact)
        
        # Previous_start_date caller Object
        yesterday_caller_object = PriceInfoIncoming.objects.filter(incoming_time__gte=prev_start_date,incoming_time__lt=start_date).exclude(from_number__in=team_contact)

        # SMS count
        today_caller_object_sms_count = today_caller_object.filter(call_source=3).count()
        yesterday_caller_object_sms_count = yesterday_caller_object.filter(call_source=3).count()


        print 'Total Request %s \n'%today_caller_object.count()
        print 'Total Sms Request %s'%today_caller_object_sms_count

        no_incoming_sms = get_active_user_comp_info(today_caller_object_sms_count, yesterday_caller_object_sms_count, '')
        
        print 'No Of Incoming SMS %s'%no_incoming_sms
        # SMS user count
        today_caller_object_sms_user_count = today_caller_object.filter(call_source=3).values_list('from_number', flat=True).distinct().count()
        yesterday_caller_object_sms_user_count = yesterday_caller_object.filter(call_source=3).values_list('from_number', flat=True).distinct().count()

        no_sms_users = get_active_user_comp_info(today_caller_object_sms_user_count, yesterday_caller_object_sms_user_count, '')

        print 'SMS users %s'%no_sms_users

        # Correct Queries
        today_caller_object_correct_query_sms_count = today_caller_object.filter(call_source=3, info_status=1).count()
        yesterday_caller_object_correct_query_sms_count = yesterday_caller_object.filter(call_source=3, info_status=1).count()

        per_correct_code_entered_sms = get_active_user_comp_info(today_caller_object_correct_query_sms_count, yesterday_caller_object_correct_query_sms_count, '')

        print ' Correct Code Entered via sms %s'%per_correct_code_entered_sms

        # Incoming Calls
        today_caller_object_call_count = today_caller_object.filter(call_source__in=[1, 2]).count()
        yesterday_caller_object_call_count = yesterday_caller_object.filter(call_source__in=[1, 2]).count()

        no_incoming_call = get_active_user_comp_info(today_caller_object_call_count, yesterday_caller_object_call_count, '')

        print 'No of incoming call %s'%(no_incoming_call)

        today_caller_object_correct_query_call_count = today_caller_object.filter(call_source__in=[1, 2], info_status=1).count()
        yesterday_caller_object_correct_query_call_count = yesterday_caller_object.filter(call_source__in=[1, 2], info_status=1).count()

        per_correct_code_entered_call = get_active_user_comp_info(today_caller_object_correct_query_call_count, yesterday_caller_object_correct_query_call_count, '')

        print ' Correct Code Entered via call %s'%per_correct_code_entered_call

        # Wrong Code Entered via call
        today_caller_object_wrong_query_count = today_caller_object.filter(info_status=2).count()
        yesterday_caller_object_wrong_query_count = yesterday_caller_object.filter(info_status=2).count()

        no_wrong_query_code = get_active_user_comp_info(today_caller_object_wrong_query_count, yesterday_caller_object_wrong_query_count, '')

        print 'Wrong Query Code %s'%(no_wrong_query_code)

        











