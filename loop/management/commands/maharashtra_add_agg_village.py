from django.core.management.base import BaseCommand
from loop.models import LoopUser, Village, LoopUserAssignedVillage

import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **options):
        df = pd.DataFrame()
        filename = 'Maharashtra Admin Data Sheet.xlsx'

        try:
            df = pd.read_excel(filename, sheetname='Aggregator - Villages')
        except Exception  as e:
            sys.exit()
        headers = list(df.columns.values)
        status = [None]*len(df[headers[0]])
        df['Status'] = pd.Series(status).values
        df['Exception'] = pd.Series(status).values

        all_aggregators = LoopUser.objects.values('id', 'name')
        dict_aggregators = {}
        agg_wise_village = {}
        for aggregator in all_aggregators:
            dict_aggregators[aggregator['name']] = aggregator['id']
            agg_wise_village[aggregator['id']] = [] 

        all_villages = Village.objects.values('id', 'village_name')
        dict_villages = {}
        for village in all_villages:
            dict_villages[village['village_name']] = village['id']

        loop_user_village = LoopUserAssignedVillage.objects.values('village','loop_user')
        
        for item in loop_user_village:
            agg_wise_village[item['loop_user']].append(item['village'])

        for i, row in df.iterrows():
            try:
                aggregator_name = row['Name (Regional)'].strip()
                village_name = row['Village Name (Regional)'].strip()
                if dict_aggregators.get(aggregator_name):
                    aggregator_id = dict_aggregators[aggregator_name]
                else:
                    df.set_value(i, 'Status', 'Fail')
                    df.set_value(i, 'Exception', 'Agg not found')
                    continue
                if dict_villages.get(village_name):
                    village_id = dict_villages[village_name]
                else:
                    df.set_value(i, 'Status', 'Fail')
                    df.set_value(i, 'Exception', 'Village not found')
                    continue    
                if village_id not in agg_wise_village[aggregator_id]:
                    agg_wise_village[aggregator_id].append(agg_wise_village)
                    aggregator_mandi = LoopUserAssignedVillage(loop_user_id = aggregator_id, village_id = village_id)
                    aggregator_mandi.save()
                    df.set_value(i, 'Status', 'Pass')
                else:
                    df.set_value(i, 'Status', 'Fail')
                    df.set_value(i, 'Exception', 'combination exists') 
            except Exception as e:
                df.set_value(i, 'Status', 'Fail')
                df.set_value(i, 'Exception', str(e))
        excel_writer = pd.ExcelWriter("AggregatorVillageStatus.xlsx")
        df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
        excel_writer.save()