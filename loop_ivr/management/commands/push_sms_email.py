__author__ = 'Vikas Saini'

from datetime import datetime, timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

from loop_ivr.models import PriceInfoIncoming, SubscriptionLog, Subscription

from loop_ivr.utils.config import string_for_no_rate_query

from dg.settings import EMAIL_HOST_USER, team_contact

class Command(BaseCommand):

    def send_mail(self, email_subject, yesterday_call_count, active_caller_count,
                        yeseterday_subscriber_caller, total_subscription,
                        successfully_sent_subscription, yesterday_unique_call_count,
                        yeseterday_unique_subscriber_caller):
        from_email = EMAIL_HOST_USER
        to_email = ['rikin@digitalgreen.org', 'saureen@digitalgreen.org', 'aditya@digitalgreen.org',
                    'vinay@digitalgreen.org', 'divish@digitalgreen.org', 'ashok@digitalgreen.org',
                    'bipin@digitalgreen.org', 'lokesh@digitalgreen.org', 'vikas@digitalgreen.org',
                    'melbin@digitalgreen.org', 'erica@digitalgreen.org']
        body_content = ['Dear Team,<br/><br/>Here are daily stats for market information line:<br/><br/>',
                '<b>Push Messaging Market Information Line:<br/><br/></b>',
                'Total subscribers: %s<br/>Subscribers who received SMS: %s<br/><br/>'%(total_subscription, successfully_sent_subscription),
                '<b>Pull-based Market Information Line:<br/><br/></b>',
                'Daily calls: %s <br/>Daily Unique callers: %s <br/> Repeat Callers (in last 15 days): %s <br/>'%(yesterday_call_count, yesterday_unique_call_count, active_caller_count),
                'Calls by push subscribers: %s <br/> Unique Callers subscribed to push messaging: %s <br/><br/>'%(yeseterday_subscriber_caller,yeseterday_unique_subscriber_caller),
                'Please contact system@digitalgreen.org for any clarification.<br/><br/>Thanks you.']
        body = ''.join(body_content)
        msg = EmailMultiAlternatives(email_subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()


    def handle(self, *args, **options):
        today_date = datetime.now().date()
        yesterday_date = datetime.now().date()-timedelta(days=1)
        fifteen_day_back_date = datetime.now().date()-timedelta(days=16)
        # Daily Callers
        yesterday_call_count = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date).exclude(from_number__in=team_contact).count()
        # Daily unique callers
        yesterday_unique_call_count = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date).exclude(from_number__in=team_contact).values_list('from_number', flat=True).distinct().count()
        # excluding yesterday, because we are counting matrices for yeseterday.
        last_fifteen_day_caller_no = list(PriceInfoIncoming.objects.filter(incoming_time__gte=fifteen_day_back_date,incoming_time__lt=yesterday_date).exclude(from_number__in=team_contact).values_list('from_number',flat=True))
        # Active callers are who called in last fifteen days.
        active_caller_count = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date,from_number__in=last_fifteen_day_caller_no).exclude(from_number__in=team_contact).values_list('from_number', flat=True).distinct().count()
        # Responses with market rate.
        yesterday_call_count_with_market_rate = PriceInfoIncoming.objects.filter(~Q(price_result__contains=string_for_no_rate_query),incoming_time__gte=yesterday_date,
                                        incoming_time__lt=today_date,info_status=1).exclude(from_number__in=team_contact).count()
        if yesterday_call_count > 0:
            percent_calls_with_market_rate = round((yesterday_call_count_with_market_rate*100.0) / yesterday_call_count,2)
        else:
            percent_calls_with_market_rate = 0
        subscriber_no = list(SubscriptionLog.objects.filter(status=1).values_list('subscription__subscriber__phone_no',flat=True))
        subscriber_no = map(lambda no: str(no) if no.startswith('0') else str('0'+no),subscriber_no)
        yeseterday_non_subscriber_caller = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,
                                            incoming_time__lt=today_date).exclude(from_number__in=subscriber_no).exclude(from_number__in=team_contact).count()
        yeseterday_subscriber_caller = yesterday_call_count - yeseterday_non_subscriber_caller
        # unique subscriber
        yeseterday_unique_non_subscriber_caller = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,
                                            incoming_time__lt=today_date).exclude(from_number__in=subscriber_no).exclude(from_number__in=team_contact).values_list('from_number', flat=True).distinct().count()
        yeseterday_unique_subscriber_caller = yesterday_unique_call_count - yeseterday_unique_non_subscriber_caller
        total_subscription = Subscription.objects.filter(status=1).exclude(subscriber__phone_no__in=team_contact).values('subscriber__phone_no').distinct().count()
        successfully_sent_subscription = SubscriptionLog.objects.filter(status=1,date__gte=yesterday_date,date__lt=today_date).exclude(subscription__subscriber__phone_no__in=team_contact).values('subscription__subscriber__phone_no').distinct().count()
        email_subject = 'Loop Market Information Summary for %s'%(yesterday_date.strftime("%Y-%m-%d"),)
        self.send_mail(email_subject, yesterday_call_count, active_caller_count,
                        yeseterday_subscriber_caller,total_subscription,
                        successfully_sent_subscription,yesterday_unique_call_count,
                        yeseterday_unique_subscriber_caller)
