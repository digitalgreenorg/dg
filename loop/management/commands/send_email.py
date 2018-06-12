from loop.utils.emailers_support.melbin_data import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	def handle(self,*args,**options):
		print "Loop Scripts"
		far = FarmerData()
		far.farmerData()
		workbook = create_workbook("LoopWorkBook")
		


