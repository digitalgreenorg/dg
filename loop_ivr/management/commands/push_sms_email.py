__author__ = 'Vikas Saini'

from datetime import datetime, timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

from loop_ivr.models import PriceInfoIncoming, SubscriptionLog

from loop_ivr.utils.config import agg_sms_no_price_available

from dg.settings import EMAIL_HOST_USER

class Command(BaseCommand):

    def send_mail(self, email_subject, yesterday_call_count, active_caller_count,
                        percent_calls_with_market_rate, yeseterday_non_subscriber_caller):
        from_email = EMAIL_HOST_USER
        to_email = ['vikas@digitalgreen.org']
        body_content = ['Dear Team,<br/><br/>This is the status of calls on Loop Market Information:<br/><br/>',
                'Total Calls Received: %s <br/> Active Caller Count (Called in last 15 days): %s <br/>'%(yesterday_call_count,active_caller_count),
                '%% Calls with Market Rate: %s <br/><b>Non-Subscription Callers: %s <br/>'%(percent_calls_with_market_rate,yeseterday_non_subscriber_caller),
                '<br/>Please contact system@digitalgreen.org for any clarification.<br/><br/>Thanks you.']
        body = ''.join(body_content)
        msg = EmailMultiAlternatives(email_subject, body, from_email, to_email)
        msg.content_subtype = "html"
        msg.send()


    def handle(self, *args, **options):
        today_date = datetime.now().date()
        yesterday_date = datetime.now().date()-timedelta(days=1)
        fifteen_day_back_date = datetime.now().date()-timedelta(days=16)
        yesterday_call_count = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date).count()
        # excluding yesterday, because we are counting matrices for yeseterday.
        last_fifteen_day_caller_no = list(PriceInfoIncoming.objects.filter(incoming_time__gte=fifteen_day_back_date,incoming_time__lt=yesterday_date).values_list('from_number',flat=True))
        # Active callers are who called in last fifteen days.
        active_caller_count = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,incoming_time__lt=today_date,from_number__in=last_fifteen_day_caller_no).count()
        yesterday_call_count_with_market_rate = PriceInfoIncoming.objects.filter(~Q(price_result__contains=agg_sms_no_price_available),incoming_time__gte=yesterday_date,
                                        incoming_time__lt=today_date,info_status=1).count()

        if yesterday_call_count > 0:
            percent_calls_with_market_rate = round((yesterday_call_count_with_market_rate*100.0) / yesterday_call_count,2)
        else:
            percent_calls_with_market_rate = 0
        subscriber_no = list(SubscriptionLog.objects.filter(status=1).values_list('subscription__subscriber__phone_no',flat=True))
        yeseterday_non_subscriber_caller = PriceInfoIncoming.objects.filter(incoming_time__gte=yesterday_date,
                                            incoming_time__lt=today_date).exclude(from_number__in=subscriber_no).count()
        email_subject = 'Loop Market Information Summary for %s'%(yesterday_date.strftime("%Y-%m-%d"),)
        self.send_mail(email_subject, yesterday_call_count, active_caller_count,
                        percent_calls_with_market_rate, yeseterday_non_subscriber_caller)

        