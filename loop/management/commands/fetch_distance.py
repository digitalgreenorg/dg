import os
import sys
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import pandas as pd
from libs.distance_matrix import DistanceMatrix
from loop.models import Mandi, Village, LoopUserAssignedVillage, LoopUserAssignedMandi

class Command(BaseCommand):
    help = '''This command fetches distance between source and destination. '''

    def handle(self,*args,**options):
        # mandi_matrix = pd.DataFrame(list(Mandi.objects.values('id','mandi_name_en','latitude','longitude').filter(district__state=1).filter(Q(latitude__isnull=False) & Q(latitude__gte=2))))
        assigned_mandis = pd.DataFrame(list(LoopUserAssignedMandi.objects.values('loop_user__id','loop_user__name_en','mandi__mandi_name_en','mandi__latitude','mandi__longitude').filter(loop_user__village__block__district=1).filter(Q(mandi__latitude__isnull=False) & Q(mandi__latitude__gte=2))))

        # print assigned_mandis.head()

        assigned_villages = pd.DataFrame(list(LoopUserAssignedVillage.objects.values('loop_user__id','village__village_name_en','village__latitude','village__longitude').filter(loop_user__village__block__district=1).filter(Q(village__latitude__isnull=False) & Q(village__latitude__gte=2))))
        # print assigned_villages.head()

        mandi_village_matrix = assigned_mandis.merge(assigned_villages, on='loop_user__id')
        print mandi_village_matrix.head()
        print mandi_village_matrix.count()

        for index, item in mandi_village_matrix.iterrows():
            print item['mandi__mandi_name_en'] + "  TO  " + item['village__village_name_en'] + " : "
            source = str(item['mandi__latitude']) + "," + str(item['mandi__longitude'])
            destination = str(item['village__latitude']) + "," + str(item['village__longitude'])
            mandi_village_matrix.loc[index,'distance'] = self.get_distance(source=source, destination=destination, mode='driving')

        mandi_village_matrix.to_csv("mandi_village_mapping.csv")

        # mandi_matrix['tmp']=1
        # mandi_matrix = mandi_matrix.merge(mandi_matrix,on='tmp', suffixes=('_src','_dest')).drop('tmp', axis=1)

        # for index, item in mandi_matrix.iterrows():
        #     print item['mandi_name_en_src'] + "  TO  " + item['mandi_name_en_dest'] + " : "
        #     source = str(item['latitude_src']) + "," + str(item['longitude_src'])
        #     destination = str(item['latitude_dest']) + "," + str(item['longitude_dest'])
        #     mandi_matrix.loc[index,'distance'] = self.get_distance(source=source, destination=destination, mode='driving')
        # mandi_matrix.to_csv('distance.csv')
        # print mandi_matrix

    def get_distance(self,source=None,destination=None, mode=None):
        distanceMatrix = DistanceMatrix()
        if distanceMatrix.distance(source=source, destination=destination, mode=mode):
            try:
                return distanceMatrix.getDistance()
            except Exception as e:
                print e
