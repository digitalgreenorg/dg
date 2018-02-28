import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from loop.models import Mandi, Village

class Command(BaseCommand):
    help = '''This command fills geo-coordinates for mandi and village in database from a csv file '''

    def handle(self,*args,**options):
        df_distance = pd.read_csv('mandi_village_mapping.csv')
        df_distance.drop(['Unnamed: 0','loop_user__id','loop_user__name_en','loop_user__user__id'], axis = 1,inplace = True)
        # print df_distance.head()
        # print df_distance.groupby(['mandi__id','mandi__latitude','mandi__longitude']).head()
        mandi_list = df_distance.drop_duplicates('mandi__id')
        village_list = df_distance.drop_duplicates('village__id')

        print "Filling mandi coordinates"
        for index,row in mandi_list.iterrows():
            mandi_obj = Mandi.objects.get(id=row['mandi__id'])
            mandi_obj.latitude = row['mandi__latitude']
            mandi_obj.longitude = row['mandi__longitude']
            mandi_obj.save()

        print "Filling Village coordinates"
        for index, row in village_list.iterrows():
            village_obj = Village.objects.get(id=row['village__id'])
            village_obj.latitude = row['village__latitude']
            village_obj.longitude = row['village__longitude']
            village_obj.save()
