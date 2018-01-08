import os
import sys
import pandas as pd
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q, Count, Sum, Avg

from loop.models import LoopUser, CombinedTransaction, Crop, Mandi, Farmer, DayTransportation

class Command(BaseCommand):
    help = '''This command plost graph for transportation details for Market Recommendation. '''

    def handle(self,*args,**options):
        print("Transportation Graphs")

        df_dt = pd.DataFrame(list(DayTransportation.objects.filter(Q(transportation_vehicle__vehicle__id = 4) | Q(transportation_vehicle__vehicle__id =5)).filter(mandi__district__id=1).values('mandi__id','user_created_id','date','transportation_vehicle__vehicle__id', 'transportation_vehicle__vehicle__vehicle_name_en').order_by('date').annotate(Sum('transportation_cost'))))

        df_dt.rename(columns={"transportation_vehicle__vehicle__id":"vehicle_id","transportation_vehicle__vehicle__vehicle_name_en":"vehicle_name"},inplace=True)
        # print df_dt.head()

        df_distance = pd.read_csv('mandi_village_mapping.csv')
        df_distance.drop(['Unnamed: 0','loop_user__id','mandi__latitude','mandi__longitude','village__latitude','village__longitude', 'village__village_name_en', 'village__id'], axis = 1,inplace = True)
        df_distance.rename(columns={"loop_user__user__id":"user_created_id"},inplace=True)

        # print df_distance.head()

        df_dt_distance = pd.merge(df_dt,df_distance,left_on=['user_created_id','mandi__id'],right_on=['user_created_id','mandi__id'],how='left')

        df_dt_distance.dropna(inplace=True)
        print df_dt_distance.head()
