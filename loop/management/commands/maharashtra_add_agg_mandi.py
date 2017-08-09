from django.core.management.base import BaseCommand
from loop.models import LoopUser, Mandi, LoopUserAssignedMandi

import pandas as pd

class Command(BaseCommand):

	def handle(self, *args, **options):
		df = pd.DataFrame()
		filename = 'Maharashtra Admin Data Sheet.xlsx'
		try:
            df = pd.read_excel(filename, sheetname='Aggregator - Markets')
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

		all_mandis = Mandi.objects.values('id', 'mandi_name')
		dict_mandis = {}
		for mandi in all_mandis:
			dict_mandis[mandi['mandi_name']] = mandi['id']

		loop_user_mandi = LoopUserAssignedMandi.objects.values('mandi','loop_user')
		agg_wise_mandi = {}
		for item in loop_user_mandi:
			if item['loop_user'] not in agg_wise_mandi:
				agg_wise_mandi[item['loop_user']] = set()
			agg_wise_mandi[item['loop_user']].add(item['mandi'])

		for i, row in df.iterrows():
			try:
				aggregator_name = row['Name (Regional)'].strip()
				mandi_name = row['Market (Regional)'].strip()
				aggregator_id  = 0
				mandi_id = 0
				aggregator_id = dict_aggregators[aggregator_name]
				mandi_id = dict_mandis[mandi_name]
				if mandi_id not in agg_wise_mandi[aggregator_id]:
					aggregator_mandi = LoopUserAssignedMandi(loop_user_id = aggregator_id, mandi_id = mandi_id)
					aggregator_mandi.save()
					df.set_value(i, 'Status', 'Pass')
				else:
					raise Exception('Duplicate Entry')
			except Exception as e:
				df.set_value(i, 'Status', 'Fail')
				df.set_value(i, 'Exception', str(e))
		excel_writer = pd.ExcelWriter("AggregatorMandiStatus.xlsx")
		df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
		excel_writer.save()