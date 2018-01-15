import os
import sys
import pandas as pd
import csv
import matplotlib.pyplot as plt

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
        df_dt_distance['distance_km'] = df_dt_distance['distance'].str.split(' ').str[0].astype('float64')
        print df_dt_distance.head()
        # print df_dt_distance.dtypes

        df_dt_distance_pickup = df_dt_distance[(df_dt_distance['vehicle_id']==4) & (df_dt_distance['distance_km'] < 100)]
        # df_dt_distance_pickup = df_dt_distance[(df_dt_distance['vehicle_id']==4) & (df_dt_distance['distance_km']==3.5)]
        # df_dt_distance_pickup = df_dt_distance

        df_dt_distance_pickup_frequency = df_dt_distance_pickup.groupby(['user_created_id','distance_km','transportation_cost__sum']).agg({'mandi__id':'count'}).reset_index()
        df_dt_distance_pickup_frequency.rename(columns={'mandi__id':'frequency'},inplace=True)
        print df_dt_distance_pickup_frequency

        df_dt_distance_pickup_frequency.plot(use_index=False,kind='scatter',x='distance_km',y='frequency',figsize=(18,8),s=df_dt_distance_pickup_frequency['frequency']*5, xticks=df_dt_distance_pickup_frequency['distance_km'])
        plt.xticks(rotation=90)
        plt.show()

        # df_dt_distance_pickup = df_dt_distance_pickup.groupby(['mandi__id','distance_km','vehicle_id']).agg({'transportation_cost__sum':['mean','median']}).reset_index()
        # df_dt_distance_pickup.columns = ["".join(row) for row in df_dt_distance_pickup.columns.ravel()]
        # print df_dt_distance_pickup.count()
        # plot_mean = df_dt_distance_pickup.plot(use_index=False,kind='scatter',x='distance_km',y='transportation_cost__summean',figsize=(18,8), color='Red', label='Mean')
        # df_dt_distance_pickup.plot(use_index=False,kind='scatter',x='distance_km',y='transportation_cost__summedian',figsize=(18,8), color='DarkGreen', label='Median', ax=plot_mean)
        # plt.show()
