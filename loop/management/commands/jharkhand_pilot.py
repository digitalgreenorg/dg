__author__ = 'Vikas Saini'

import time
import csv
import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, MEDIA_ROOT

from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing
from loop.helpline_view import get_status, make_helpline_call, write_log
from loop.utils.ivr_helpline.helpline_data import HELPLINE_LOG_FILE
import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_header = ['phone']
        file_name = 'jharkhand_list.xlsx'
        open_file = pd.ExcelFile(file_name)
        contact_detail = open_file.parse("Sheet1")
        print contact_detail.head()
        for row,contact in contact_detail.iterrows():
            name =  contact['name']
            phone = contact['phone']