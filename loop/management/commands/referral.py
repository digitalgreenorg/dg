# coding=utf-8
import copy
import collections
import re
import datetime
__author__ = 'Sourabh'

from loop.models import LoopUser,CombinedTransaction,Farmer
from django.core.management.base import BaseCommand
from loop.config import *
from dg.settings import MEDIA_ROOT, EMAIL_HOST_USER
from loop_ivr.utils.config import AGGREGATORS_IDEO
from loop.utils.send_log.registration import send_msg_after_first_trans,update_referrals,automated_ivr
from loop.views import referral_farmer
import os

id_map = {}
obj = LoopUser.objects.exclude(role=1).values_list('name', 'user_id')
for item in obj:
    id_map[item[0]] = item[1]

class Command(BaseCommand):
    # parse arguments from command line
    def add_arguments(self, parser):
        # create mutually exclusive command line switches
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-sd',
                           dest='from_date',
                           default=None)


        parser.add_argument('-ed',
                            dest='to_date',
                            default=None)

        parser.add_argument('-t',
                            dest='type',
                            default='msg')

    # generate the excel for the given command line arguments
    def handle(self, *args, **options):
        # from_to_date = date_setter.set_from_to_date(options.get('from_date'), options.get('to_date'))
        
        from_date = re.sub('-', '', options.get('from_date'))
        from_date = datetime.datetime.strptime(from_date, "%d%m%Y").date()
        to_date = re.sub('-', '', options.get('to_date'))
        to_date = datetime.datetime.strptime(to_date, "%d%m%Y").date()
        type = options.get('type')
        if type == 'msg':
            update_referrals()
            send_msg_after_first_trans(from_date,to_date)
        elif type == 'csv':
            referral_farmer(from_date,to_date,AGGREGATORS_IDEO)
        elif type == 'ivr':
            automated_ivr(from_date,to_date)
        else:
            pass
