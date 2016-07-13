__author__ = 'Lokesh'
1464448510443

import datetime
import xlwt

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from loop.models import CombinedTransaction, DayTransportation


class Command(BaseCommand):
    def handle(self, *args, **options):
        # ct_list = CombinedTransaction.objects.all()
        # tst = "1464448511500"
        # for ct in ct_list:
        #     print ct.id
        #     print ct.timestamp
        #     if ct.timestamp == None or ct.timestamp == "":
        #         ct.timestamp = tst
        #         tst = str(int(tst) + 1)
        #     ct.save()

        dt_list = DayTransportation.objects.all()
        tst2 = "1464448511500"
        for dt in dt_list:
            if dt.timestamp == None or dt.timestamp == "test":
                dt.timestamp = tst2
                tst2 = str(int(tst2) + 1)
            dt.save()
