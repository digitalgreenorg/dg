import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.db.models import Count

import dg.settings
from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing, HelplineCallLog

class Command(BaseCommand):

    def handle(self, *args, **options):
        today_date = datetime.datetime.now().date()
        yesterday_date = today_date-timedelta(days=1)
        yesterday_declined_call_count = HelplineIncoming.objects.filter(call_status=2,time_modified__gte=yesterday_date,time_modified__lt=today_date).count()
        # Change dates from Yesterday 6:00 PM to Today 9:00 AM (Non-Operational Hours of Helpline) 
        today_date = datetime.datetime.now().replace(hour=9,minute=0,second=0)
        yesterday_date = (today_date-timedelta(days=1)).replace(hour=18,minute=0,second=0)
        total_pending_call_count = HelplineIncoming.objects.filter(call_status=0).count()
        total_declined_call_count = HelplineIncoming.objects.filter(call_status=2).count()
        yesterday_off_hours_incoming_call_count = HelplineCallLog.objects.filter(call_type=0,start_time__gte=yesterday_date,start_time__lte=today_date).count()

