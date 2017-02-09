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
            # print df_gaddidar_outlier.head()

            result = pd.merge(ct_merge_dt,df_gaddidar_outlier,left_on=['user_created__id','mandi__id','date','gaddidar__id'],right_on=['user_created__id','mandi__id','date','gaddidar__id'],how='left')
            result.fillna(value=0,axis=1,inplace=True)
            print result.head()
            print result.shape

            # start_time = time.time()
            #CALCULATING GADDIDAR SHARE
            gc_queryset = GaddidarCommission.objects.all()
            gso_queryset = GaddidarShareOutliers.objects.all()
            combined_ct_queryset = CombinedTransaction.objects.values(
                'date', 'user_created_id', 'gaddidar', 'mandi', 'gaddidar__discount_criteria').order_by('-date').annotate(
                Sum('quantity'), Sum('amount'))
            gaddidar_share_result = []
            # gso_list = [gso.date for gso in gso_queryset.filter(gaddidar=CT['gaddidar'], aggregator=user.id)]
            for CT in combined_ct_queryset:
                amount_sum = 0
                user = LoopUser.objects.get(user_id=CT['user_created_id'])
                if CT['date'] not in [gso.date for gso in gso_queryset.filter(gaddidar=CT['gaddidar'], aggregator=user.id)]:
                    try:
                        gc_list_set = gc_queryset.filter(start_date__lte=CT['date'], gaddidar=CT[
                            'gaddidar']).order_by('-start_date')
                        if CT['gaddidar__discount_criteria'] == 0 and gc_list_set.count() > 0:
                            amount_sum += CT['quantity__sum'] * \
                                   gc_list_set[0].discount_percent
                        elif gc_list_set.count() > 0:
                            amount_sum += CT['amount__sum'] * gc_list_set[0].discount_percent
                    except GaddidarCommission.DoesNotExist:
                        pass
                else:
                    try:
                        gso_gaddidar_date_aggregator = gso_queryset.filter(
                            date=CT['date'], aggregator=user.id, gaddidar=CT['gaddidar']).values_list('amount', flat=True)
                        if gso_gaddidar_date_aggregator.count():
                            amount_sum += gso_gaddidar_date_aggregator[0]
                    except GaddidarShareOutliers.DoesNotExist:
                        pass
                gaddidar_share_result.append({'date': CT['date'], 'user_created__id': CT['user_created_id'], 'gaddidar__id': CT[
                    'gaddidar'], 'mandi__id': CT['mandi'], 'gaddidar_share_amount': amount_sum, 'quantity__sum': CT['quantity__sum']})

            gaddidar_share = pd.DataFrame(gaddidar_share_result)
            # end_time = time.time()
            # print "total_time = %d" %(end_time-start_time)
            print gaddidar_share.head()

            # CALCULATING AGGREGATOR INCENTIVE
            ai_queryset = AggregatorIncentive.objects.all()
            aso_queryset = AggregatorShareOutliers.objects.all()
            combined_ct_queryset = CombinedTransaction.objects.values(
                'date', 'user_created_id', 'mandi','mandi__mandi_name_en').order_by('-date').annotate(Sum('quantity'), Sum('amount'),
                                                                               Count('farmer_id', distinct=True))
            aggregator_incentive_result = []

            incentive_param_queryset = IncentiveParameter.objects.all()

            for CT in combined_ct_queryset:
                amount_sum = 0.0
                user = LoopUser.objects.get(user_id=CT['user_created_id'])
                if CT['date'] not in [aso.date for aso in aso_queryset.filter(mandi=CT['mandi'], aggregator=user.id)]:
                    try:
                        ai_list_set = ai_queryset.filter(start_date__lte=CT['date'], aggregator=user.id).order_by('-start_date')
                        if (ai_list_set.count() > 0):
                            exec (ai_list_set[0].incentive_model.calculation_method)
                            paramter_list = inspect.getargspec(calculate_inc)[0]
                            for param in paramter_list:
                                param_to_apply = incentive_param_queryset.get(notation=param)
                                x = calculate_inc(CT[param_to_apply.notation_equivalent])
                            amount_sum += x
                        else:
                            amount_sum += calculate_inc_default(CT['quantity__sum'])
                    except Exception:
                        pass
                else:
                    try:
                        aso_share_date_aggregator = aso_queryset.filter(
                            date=CT['date'], aggregator=user.id, mandi=CT['mandi']).values('amount', 'comment')
                        if aso_share_date_aggregator.count():
                            amount_sum += aso_share_date_aggregator[0]['amount']
                    except AggregatorShareOutliers.DoesNotExist:
                        pass
                aggregator_incentive_result.append(
                    {'date': CT['date'], 'user_created__id': CT['user_created_id'], 'mandi__name' : CT['mandi__mandi_name_en'], 'mandi__id': CT['mandi'], 'amount': amount_sum, 'quantity__sum': CT['quantity__sum']})

                aggregator_incentive = pd.DataFrame(aggregator_incentive_result)
                print aggregator_incentive.head()





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
