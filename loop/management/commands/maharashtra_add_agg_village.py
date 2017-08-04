from django.core.management.base import BaseCommand
from loop.models import LoopUser, Village, LoopUserAssignedVillage

import pandas as pd

class Command(BaseCommand):

	def handle(self, *args, **options):
		df = pd.DataFrame()

		df = pd.read_excel('Maharashtra Admin Data Sheet.xlsx', sheetname='Aggregator - Villages')
		print df
		status = [None]*len(df['Name (Regional)'])
		df['Status'] = pd.Series(status).values
		df['Exception'] = pd.Series(status).values

		for i, row in df.iterrows():
			try:
					aggregator_name = row['Name (Regional)'].strip()
					village_name = row['Village Name (Regional)'].strip()
					aggregator = LoopUser.objects.get(name=aggregator_name)
					village = Mandi.objects.get(village_name = village_name)
					aggregator_village = LoopUserAssignedVillage(loop_user = aggregator, village = village)
					aggregator_village.save()

					df.set_value(i, 'Status', 'Pass')
			except Exception as e:
				df.set_value(i, 'Status', 'Fail')
				df.set_value(i, 'Exception', str(e))
		print df
		# excel_writer = pd.ExcelWriter("AggregatorVillageStatus.xlsx")
		# df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
		# excel_writer.save()