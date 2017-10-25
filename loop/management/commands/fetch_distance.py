import os
import sys
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import pandas as pd
from libs.distance_matrix import DistanceMatrix
from loop.models import Mandi, Village

class Command(BaseCommand):
    help = '''This command fetches distance between source and destination. '''

    def handle(self,*args,**options):
        mandi_matrix = pd.DataFrame(list(Mandi.objects.values('id','mandi_name_en','latitude','longitude').filter(district__state=1).filter(Q(latitude__isnull=False) & Q(latitude__gte=2))))
        mandi_matrix['tmp']=1
        mandi_matrix = mandi_matrix.merge(mandi_matrix,on='tmp', suffixes=('_src','_dest')).drop('tmp', axis=1)
        # print mandi_matrix.head()
        # mandi_matrix = mandi_matrix.head(n=10)
        for index, item in mandi_matrix.iterrows():
            print item['mandi_name_en_src'] + "  TO  " + item['mandi_name_en_dest'] + " : "
            source = str(item['latitude_src']) + "," + str(item['longitude_src'])
            destination = str(item['latitude_dest']) + "," + str(item['longitude_dest'])
            mandi_matrix.loc[index,'distance'] = self.get_distance(source=source, destination=destination, mode='driving')
        mandi_matrix.to_csv('distance.csv')
        print mandi_matrix
        # mandi_list = Mandi.objects.prefetch_related()
        # source = str(mandi_list[0].latitude) + "," + str(mandi_list[0].longitude)
        # destination = str(mandi_list[1].latitude) + "," + str(mandi_list[1].longitude)
        # self.get_distance(source=source,destination=destination,mode='driving')

    def get_distance(self,source=None,destination=None, mode=None):
        distanceMatrix = DistanceMatrix()
        if distanceMatrix.distance(source=source, destination=destination, mode=mode):
            try:
                return distanceMatrix.getDistance()
            except Exception as e:
                print e
