from loop.models import *
from loop.utils.emailers_support.excel_generator import *

class FarmerData():
	def farmerData(self):
		farmers = Farmer.objects.all()
		farmers = list(farmers)
		
