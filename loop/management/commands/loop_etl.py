import os
import sys
from django.core.management.base import BaseCommand, CommandError
from dg.settings import DATABASES
from loop.models import LoopUser, CombinedTransaction, Village, Crop, Mandi, Farmer, DayTransportation, Gaddidar, \
    Transporter, Language, CropLanguage, GaddidarCommission, GaddidarShareOutliers, AggregatorIncentive, \
    AggregatorShareOutliers, IncentiveParameter, IncentiveModel
import subprocess
import MySQLdb
import datetime, time
import subprocess
import pandas as pd
import numpy as np
from django.db.models import Count, Min, Sum, Avg, Max, F, IntegerField

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

class LoopStatistics():
    def __init__(self):
        from django.db import connection
        self.db_cursor = connection.cursor()
        # self.db_root_user = mysql_root_username
        # self.db_root_pass = mysql_root_password

    def recompute_myisam(self):
        database = DATABASES['default']['NAME']
        username = DATABASES['default']['USER']
        password = DATABASES['default']['PASSWORD']
        print 'Database : ', database
        print datetime.datetime.now()

        create_schema = subprocess.call("mysql -u%s -p%s %s < %s" % (username, password, database, os.path.join(DIR_PATH,'recreate_schema.sql')), shell=True)

        if create_schema !=0:
            raise Exception("Could not create schema for loop etl")
        print "Schema created successfully"

        try:
            # mysql_cn = MySQLdb.connect(host='localhost',user=DATABASES['default']['USER'], passwd=DATABASES['default']['PASSWORD'], db=DATABASES['default']['NAME'], charset='utf8', use_unicode=True)

            # df_ct = pd.read_sql(,con=mysql_cn)
            df_loopuser = pd.DataFrame(list(LoopUser.objects.values('id','user__id','name')))
            df_loopuser.rename(columns={"user__id":"user_created__id"},inplace=True)
            print df_loopuser

            df_ct = pd.DataFrame(list(CombinedTransaction.objects.values('date','user_created__id','mandi__id','mandi__mandi_name','gaddidar__id','gaddidar__gaddidar_name','gaddidar__discount_criteria').annotate(Sum('quantity'),Sum('amount'), Count('farmer',distinct=True))))
            # df_ct.set_index(['user_created__id','mandi__id','date'],inplace=True)
            # print df_ct.head()
            # print df_ct.shape

            df_dt = pd.DataFrame(list(DayTransportation.objects.values('date','user_created__id','mandi__id').annotate(Sum('transportation_cost'),Avg('farmer_share'))))
            # df_dt.set_index(['user_created__id','mandi__id','date'],inplace=True)

            ct_merge_dt = pd.merge(df_ct,df_dt,left_on=['user_created__id','mandi__id','date'],right_on=['user_created__id','mandi__id','date'],how='left')

            df_gaddidar_outlier = pd.DataFrame(list(GaddidarShareOutliers.objects.values('date','aggregator','mandi__id','gaddidar__id').annotate(Sum('amount'))))
            df_gaddidar_outlier.rename(columns={"aggregator":"id","amount__sum":"gaddidar_share"},inplace=True)

            df_gaddidar_outlier = pd.merge(df_loopuser,df_gaddidar_outlier,left_on='id',right_on='id',how='inner')
            df_gaddidar_outlier.drop(['id','name'],axis=1,inplace=True)
            print df_gaddidar_outlier.head()

            result = pd.merge(df_ct,df_gaddidar_outlier,left_on=['user_created__id','mandi__id','date','gaddidar__id'],right_on=['user_created__id','mandi__id','date','gaddidar__id'],how='left')
            result.fillna(value=0,axis=1,inplace=True)
            print result.head()
            print result.shape

            



        except Exception as e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)


class Command(BaseCommand):
    help = '''This command updates stats displayed on Loop dashboard.
    arguments : mysql_root_username, mysql_root_password '''

    # def add_arguments(self,parser):
    #     parser.add_argument('username')
    #     parser.add_argument('passsword')

    def handle(self,*args,**options):
        print("LOOP ETL LOG")
        print(datetime.date.today())
        # mysql_root_username = options['username']
        # mysql_root_password = options['passsword']
        loop_statistics = LoopStatistics()
        loop_statistics.recompute_myisam()
