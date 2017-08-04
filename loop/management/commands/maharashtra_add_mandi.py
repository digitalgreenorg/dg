from django.core.management.base import BaseCommand
from loop.models import District, Mandi

import pandas as pd

class Command(BaseCommand):

	def handle(self, *args, **options):
		df = pd.DataFrame()

		df = pd.read_excel('Maharashtra Admin Data Sheet.xlsx', sheetname='Markets')
		print df
		status = [None]*len(df['District'])
		df['Status'] = pd.Series(status).values
		df['Exception'] = pd.Series(status).values

		for i, row in df.iterrows():
			try:
					district_name = row['District'].strip()
					mandi_name = row['Market Name (Regional)'].strip()
					mandi_name_en = row['Market Name (English)'].strip()
					district = District.objects.get(district_name=district_name)
					mandi = Mandi(mandi_name=mandi_name, mandi_name_en=mandi_name_en, district=district, is_visible=1)
					mandi.save()

					df.set_value(i, 'Status', 'Pass')
			except Exception as e:
				df.set_value(i, 'Status', 'Fail')
				df.set_value(i, 'Exception', str(e))
		print df
		# excel_writer = pd.ExcelWriter("MarketsStatus.xlsx")
		# df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
		# excel_writer.save()