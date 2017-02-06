import os
import sys
import django.core.management.base import BaseCommand
from dg.settings import DATABASES
from loop.models import LoopUser, CombinedTransaction, Village, Crop, Mandi, Farmer, DayTransportation, Gaddidar, \
    Transporter, Language, CropLanguage, GaddidarCommission, GaddidarShareOutliers, AggregatorIncentive, \
    AggregatorShareOutliers, IncentiveParameter, IncentiveModel
import subprocess
import MySQLdb
import datetime

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

class LoopStatistics():
    def __init__(self,mysql_root_username,mysql_root_password):
        from django.db import connection
        self.db_cursor = connection.cursor()
        self.db_root_user = mysql_root_username
        self.db_root_pass = mysql_root_password

    def recompute_myisam(self):


class Command(BaseCommand):
    help = '''This command updates stats displayed on Loop dashboard.
    arguments : mysql_root_username, mysql_root_password '''

    def add_arguments(self,parser):
        parser.add_argument('username')
        parser.add_argument('passsword')

    def handle(self,*args,**options):
        print("LOOP ETL LOG")
        print(datetime.date.today())
        mysql_root_username = options['username']
        mysql_root_password = options['passsword']
        loop_statistics = LoopStatistics(mysql_root_username,mysql_root_password)
        loop_statistics.recompute_myisam()
