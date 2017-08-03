from django.core.management.base import BaseCommand
from loop.models import District, Mandi

import pandas as pd

df = pd.DataFrame()
class Command(BaseCommand):

	def handle(self, *args, **options):
		global df

		df = pd.read_excel('Maharashtra Admin Data Sheet.xlsx', sheetname='Markets')
		print df

		district = District.objects.get(id=5)
		print district
		
		print df['Market Name (Regional)']
		print df['Market Name (English)']

		# for i, row in df.iterrows():
		# 	district = District.objects.filter(district_name=row['District'])
		# 	mandi = Mandi(mandi_name=row['Market Name (Regional)'], district=district, is_visible=1)
		# 	mandi.save()