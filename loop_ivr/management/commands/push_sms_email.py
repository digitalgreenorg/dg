__author__ = 'Vikas Saini'

from datetime import datetime, timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

from loop_ivr.models import PriceInfoIncoming, SubscriptionLog, Subscription

from loop_ivr.utils.config import agg_sms_no_price_available

from dg.settings import EMAIL_HOST_USER, team_contact

class Command(BaseCommand):

    def send_mail(self, email_subject, yesterday_call_count, active_caller_count,
                        percent_calls_with_market_rate, yeseterday_non_subscriber_caller,
                        yeseterday_subscriber_caller, total_subscription,
                        successfully_sent_subscription, failed_sent_subscription):
        from_email = EMAIL_HOST_USER
        to_email = ['rikin@digitalgreen.org', 'saureen@digitalgreen.org', 'aditya@digitalgreen.org',
                    'vinay@digitalgreen.org', 'divish@digitalgreen.org', 'ashok@digitalgreen.org',
                    'bipin@digitalgreen.org', 'lokesh@digitalgreen.org', 'vikas@digitalgreen.org',
                    'melbin@digitalgreen.org']
        body_content = ['Dear Team,<br/><br/>This is the status of calls on Loop Market Information Line:<br/><br/>',
                'Total Callers on Market Information Line: %s <br/> Active Caller Count (Called in last 15 days): %s <br/>'%(yesterday_call_count,active_caller_count),
                '%% Calls with Market Rate: %s %%<br/><br/>'%(percent_calls_with_market_rate,),
                '<b>Push Message Service Stats (We are pushing rates to some farmers once in a day):<br/><br/>',
                'Total Call by Subscribed callers (We are pushing rates to these callers on daily basis): %s<br/>Total Call by Non-Subscribed Callers: %s<br/><br/>'%(yeseterday_subscriber_caller, yeseterday_non_subscriber_caller),
                'Total Push Messages: %s<br/>Successfully Pushed Rates: %s<br/>Failed Pushed Rates: %s<br/></b>'%(total_subscription,successfully_sent_subscription,failed_sent_subscription),
                '<br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>Thanks you.']
        body = ''.join(body_content)
        msg = EmailMultiAlternatives(email_subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()


    def handle(self, *args, **options):
        today_date = datetime.now().date()
        yesterday_date = datetime.now().date()-timedelta(days=1)
        fifteen_day_back_date = datetime.now().date()-timedelta(days=16)
        yesterday_call_count = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date).exclude(from_number__in=team_contact).count()
        # excluding yesterday, because we are counting matrices for yeseterday.
        last_fifteen_day_caller_no = list(PriceInfoIncoming.objects.filter(incoming_time__gte=fifteen_day_back_date,incoming_time__lt=yesterday_date).exclude(from_number__in=team_contact).values_list('from_number',flat=True))
        # Active callers are who called in last fifteen days.
        active_caller_count = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date,from_number__in=last_fifteen_day_caller_no).exclude(from_number__in=team_contact).count()
        yesterday_call_count_with_market_rate = PriceInfoIncoming.objects.filter(~Q(price_result__contains=agg_sms_no_price_available),incoming_time__gte=yesterday_date,
                                        incoming_time__lt=today_date,info_status=1).exclude(from_number__in=team_contact).count()

        if yesterday_call_count > 0:
            percent_calls_with_market_rate = round((yesterday_call_count_with_market_rate*100.0) / yesterday_call_count,2)
        else:
            percent_calls_with_market_rate = 0
        subscriber_no = list(SubscriptionLog.objects.filter(status=1).values_list('subscription__subscriber__phone_no',flat=True))
        yeseterday_non_subscriber_caller = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,
                                            incoming_time__lt=today_date).exclude(from_number__in=subscriber_no).exclude(from_number__in=team_contact).count()
        yeseterday_subscriber_caller = yesterday_call_count - yeseterday_non_subscriber_caller
        email_subject = 'Loop Market Information Summary for %s'%(yesterday_date.strftime("%Y-%m-%d"),)
        total_subscription = Subscription.objects.filter(status=1).exclude(subscriber__phone_no__in=team_contact).count()
        successfully_sent_subscription = SubscriptionLog.objects.filter(status=1,date__gte=yesterday_date,date__lt=today_date).exclude(subscription__subscriber__phone_no__in=team_contact).count()
        failed_sent_subscription = total_subscription - successfully_sent_subscription
        self.send_mail(email_subject, yesterday_call_count, active_caller_count,
                        percent_calls_with_market_rate, yeseterday_non_subscriber_caller,
                        yeseterday_subscriber_caller,total_subscription,
                        successfully_sent_subscription, failed_sent_subscription)
