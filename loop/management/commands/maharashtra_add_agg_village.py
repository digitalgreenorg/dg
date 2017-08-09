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

		all_aggregators = LoopUser.objects.values('user_id', 'name')
		dict_aggregators = {}
		for aggregator in all_aggregators:
			dict_aggregators[aggregator['name']] = aggregator['user_id']

		all_villages = Village.objects.values('id', 'village_name')
		dict_villages = {}
		for village in all_villages:
			dict_villages[village['village_name']] = village['id']

		loop_user_village = LoopUserAssignedVillage.objects.values('village','loop_user')
		agg_wise_village = {}
		for item in loop_user_village:
			if item['loop_user'] not in agg_wise_village:
				agg_wise_village[item['loop_user']] = set()
			agg_wise_village[item['loop_user']].add(item['village'])

		for i, row in df.iterrows():
			try:
				aggregator_name = row['Name (Regional)'].strip()
				village_name = row['Village Name (Regional)'].strip()
				aggregator_id  = 0
				village_id = 0
				aggregator_id = dict_aggregators[aggregator_name]
				village_id = dict_villages[village_name]

				if village_id not in agg_wise_village[aggregator_id]:
				aggregator_mandi = LoopUserAssignedVillage(loop_user_id = aggregator_id, village_id = village_id)
				aggregator_mandi.save()
				df.set_value(i, 'Status', 'Pass')
				else:
					raise Exception('Duplicate Entry')it 
			except Exception as e:
				df.set_value(i, 'Status', 'Fail')
				df.set_value(i, 'Exception', str(e))
		excel_writer = pd.ExcelWriter("AggregatorVillageStatus.xlsx")
		df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
		excel_writer.save()