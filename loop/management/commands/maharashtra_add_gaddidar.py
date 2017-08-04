from django.core.management.base import BaseCommand
from loop.models import Mandi, Gaddidar

import pandas as pd

class Command(BaseCommand):

	def handle(self, *args, **options):
		df = pd.DataFrame()

		df = pd.read_excel('Maharashtra Admin Data Sheet.xlsx', sheetname='Traders')
		print df
		status = [None]*len(df['Market Name'])
		df['Status'] = pd.Series(status).values
		df['Exception'] = pd.Series(status).values

		for i, row in df.iterrows():
			try:
					market_name = row['Market Name'].strip()
					trader_name = row['Trader Name (Regional)'].strip()
					trader_name_en = row['Trader Name (English)'].strip()
					market = Mandi.objects.get(mandi_name=market_name)
					gaddidar = Gaddidar(gaddidar_name=trader_name, gaddidar_name_en=trader_name_en, gaddidar_phone='1234567890',mandi=mandi, is_visible=1)
					gaddidar.save()

					df.set_value(i, 'Status', 'Pass')
			except Exception as e:
				df.set_value(i, 'Status', 'Fail')
				df.set_value(i, 'Exception', str(e))
		print df
		excel_writer = pd.ExcelWriter("GaddidarsStatus.xlsx")
		df.to_excel(excel_writer = excel_writer, sheet_name= 'Sheet1', index = False)
		excel_writer.save()