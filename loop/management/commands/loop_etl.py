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
import inspect

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

class LoopStatistics():

    def recompute_myisam(self):
        database = DATABASES['default']['NAME']
        username = DATABASES['default']['USER']
        password = DATABASES['default']['PASSWORD']
        print 'Database : ', database
        print datetime.datetime.utcnow()

        create_schema = subprocess.call("mysql -u%s -p%s %s < %s" % (username, password, database, os.path.join(DIR_PATH,'recreate_schema.sql')), shell=True)

        if create_schema !=0:
            raise Exception("Could not create schema for loop etl")
        print "Schema created successfully"

        try:
            start_time = time.time()
            self.mysql_cn = MySQLdb.connect(host='localhost',user=DATABASES['default']['USER'], passwd=DATABASES['default']['PASSWORD'], db=DATABASES['default']['NAME'], charset='utf8', use_unicode=True)
            # .cursor()

            df_loopuser = pd.DataFrame(list(LoopUser.objects.values('id','user__id','name_en')))
            df_loopuser.rename(columns={"user__id":"user_created__id","name_en":"name"},inplace=True)

            print "Loop User Shape",df_loopuser.shape

            df_ct = pd.DataFrame(list(CombinedTransaction.objects.values('date','user_created__id','mandi__id','mandi__mandi_name_en','gaddidar__id','gaddidar__gaddidar_name_en').order_by('date').annotate(Sum('quantity'),Sum('amount'))))
            df_ct.rename(columns={"mandi__mandi_name_en":"mandi__mandi_name","gaddidar__gaddidar_name_en":"gaddidar__gaddidar_name"},inplace=True)

            print "Combined Transaction Shape",df_ct.shape

            df_ct = pd.merge(df_ct,df_loopuser,left_on='user_created__id',right_on='user_created__id',how='left')

            df_dt = pd.DataFrame(list(DayTransportation.objects.values('date','user_created__id','mandi__id').order_by('-date').annotate(Sum('transportation_cost'),Avg('farmer_share'))))

            print "Day Transportation Shape",df_dt.shape

            ct_merge_dt = pd.merge(df_ct,df_dt,left_on=['date','user_created__id','mandi__id'],right_on=['date','user_created__id','mandi__id'],how='left')

            print "Combined Transaction merged with Day Transportation ",ct_merge_dt.shape

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
                    'gaddidar'], 'mandi__id': CT['mandi'], 'gaddidar_share_amount': amount_sum})

            gaddidar_share = pd.DataFrame(gaddidar_share_result)

            print "Gaddidar Share",gaddidar_share.shape

            # CALCULATING AGGREGATOR INCENTIVE
            ai_queryset = AggregatorIncentive.objects.all()
            aso_queryset = AggregatorShareOutliers.objects.all()
            combined_ct_queryset = CombinedTransaction.objects.values(
                'date', 'user_created_id', 'mandi').order_by('-date').annotate(Sum('quantity'), Sum('amount'),
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
                            amount_sum += CT['quantity__sum']*0.25
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
                    {'date': CT['date'], 'user_created__id': CT['user_created_id'], 'mandi__id': CT['mandi'], 'aggregator_incentive': amount_sum})

            aggregator_incentive = pd.DataFrame(aggregator_incentive_result)

            print "Aggregator Incentive",aggregator_incentive.shape

            merged_ct_dt_gaddidar = pd.merge(ct_merge_dt,gaddidar_share,left_on=['user_created__id','mandi__id','gaddidar__id','date'],right_on=['user_created__id','mandi__id','gaddidar__id','date'],how='left')

            print "After merging Gaddidar Share", merged_ct_dt_gaddidar.shape

            result = pd.merge(merged_ct_dt_gaddidar,aggregator_incentive,left_on=['user_created__id','mandi__id','date'],right_on=['user_created__id','mandi__id','date'],how='left')

            print "After adding aggregator incentive", result.shape
            result.fillna(value=0,axis=1,inplace=True)

            df_farmer_count = pd.read_sql("SELECT T.date, count(T.farmer_id) as distinct_farmer_count FROM ( SELECT farmer_id, min(date) as date FROM loop_combinedtransaction GROUP BY farmer_id) as T GROUP BY T.date",con=self.mysql_cn)

            df_farmer_count['cummulative_distinct_farmer'] = df_farmer_count['distinct_farmer_count'].cumsum()
            df_farmer_count.drop(['distinct_farmer_count'],axis=1,inplace=True)

            result = pd.merge(result,df_farmer_count,left_on='date',right_on='date',how='left')
            result['cummulative_distinct_farmer'].fillna(method='ffill',inplace=True)

            print "After adding cummulative distinct farmer ", result.shape

            for index,row in result.iterrows():
                self.mysql_cn.cursor().execute("""INSERT INTO loop_aggregated_myisam (date,aggregator_id,mandi_id,gaddidar_id,quantity,amount,transportation_cost,farmer_share,gaddidar_share,aggregator_incentive,aggregator_name,mandi_name,gaddidar_name,cum_distinct_farmer) values(""" + '"'+row['date'].strftime('%Y-%m-%d %H:%M:%S')+'"' + "," + str(row['user_created__id']) + ","
                + str(row['mandi__id']) + ","
                + str(row['gaddidar__id']) + ","
                + str(row['quantity__sum']) + ","
                + str(row['amount__sum']) + ","
                + str(row['transportation_cost__sum']) + ","
                + str(row['farmer_share__avg']) + ","
                + str(row['gaddidar_share_amount']) + ","
                + str(row['aggregator_incentive']) + ","
                + '"'+row['name']+'"' + ","
                + '"'+row['mandi__mandi_name']+'"' + ","
                + '"'+row['gaddidar__gaddidar_name']+'",'
                + str(row['cummulative_distinct_farmer']) + """)""")

            print "Myisam insertion complete"
            end_time = time.time()
            print "Total time taken (secs) : %f" % (end_time-start_time)

        except Exception as e:
            print "Error : %s" % (e)
            sys.exit(1)

class Command(BaseCommand):
    help = '''This command updates stats displayed on Loop dashboard.
    arguments : mysql_root_username, mysql_root_password '''

    def handle(self,*args,**options):
        print("LOOP ETL LOG")
        print(datetime.date.today())
        loop_statistics = LoopStatistics()
        loop_statistics.recompute_myisam()
