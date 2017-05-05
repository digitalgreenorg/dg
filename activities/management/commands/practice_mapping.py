import os

from django.core.management.base import BaseCommand
from django.conf import settings
from openpyxl import load_workbook

class Command(BaseCommand):

	def handle(self, *args, **options):
		pm_file = '/Users/nikhilverma/workspace/DG/dg/practice_map.xlsx'
		# path = os.path.abspath(pm_file)
		wb = load_workbook(pm_file)
		# This
		sheet_names = ['APTel', 'Bihar', 'Jharkhand', 'Maharashtra', 'Odisha', 'Rajasthan',
						'Karnataka', 'MP', 'UP', 'Ethiopia']
		for sheet_iterable in sheet_names:
			ws = wb.get_sheet_by_name(sheet_iterable)
			print "wsssss", ws.title
			video_data_list = []
			row_num = ws.max_row

			for row_index in range(2,row_num):
				# print ws[row_index][1].value, ws[row_index][6].value, ws[row_index][7].value, ws[row_index][8].value
				# if ws[row_index][1].value is not None and ws[row_index][6].value is not None and ws[row_index][8].value is not None: 
					video_data_list.append([{'id': ws[row_index][1].value,
											 'category_name': ws[row_index][6].value.lower() if ws[row_index][6].value is not None else ws[row_index][6].value,
											 'sub_category_name': ws[row_index][7].value.lower() if ws[row_index][7].value is not None else ws[row_index][7],
											 'subcategory_name': ws[row_index][8].value.lower()}]) if ws[row_index][8].value is not None else ws[row_index][8]
		print video_data_list