import os

from django.core.management.base import BaseCommand

from xlrd import *

class Command(BaseCommand):

	def handle(self, *args, **options):
		filename = 'loop/samples/loop_village_data.xlsx'
		filename2 = 'loop/samples/aggregator_pilot_data.xlsx'
		path = os.path.abspath(filename)
		path2 = os.path.abspath(filename2)
		wb = open_workbook(path)
		wb2 = open_workbook(path2)
		# This
		for s in wb.sheets():
			print 'Sheet:',s.name
			for row in range(s.nrows):
				for col in range(s.ncols):
					print s.cell(row,col).value
		# OR This
		worksheet = wb.sheet_by_index(0)
		rows = []
		for i, row in enumerate(range(worksheet.nrows)):
		    r = []
		    for j, col in enumerate(range(worksheet.ncols)):
		        r.append(worksheet.cell_value(i, j))
		    rows.append(r)
		print rows[0]
		print rows[1]
