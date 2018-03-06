
from loop.models import *
from django.core.management.base import BaseCommand, CommandError
import xlrd

class LoopQRMapping():
	def update(self):
		xl_file = xlrd.open_workbook('/Users/sourabhsingh/Downloads/Loop Farmer QR Codes.xlsx')
		print xl_file.sheet_names
		sheets = ['Village1_mapping','Village2_mapping','Village3_mapping','Village4_mapping']
		c=0
		for sheet in sheets: 
			d = xl_file.sheet_by_name(sheet)
			
			for r in range(1,d.nrows):
				url = str(d.cell(r,0).value)
				code = str(int(d.cell(r,1).value))
				mapping = QrMapping(url=url,code=code)
				mapping.save()
				c=c+1
				print c

class Command(BaseCommand):
    help = '''This is to update QR Code Mappings '''

    def handle(self,*args,**options):
        print("LOOP QR Mapping")
        print(datetime.date.today())
        qr_mapping = LoopQRMapping()
        qr_mapping.update()