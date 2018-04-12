#python imports
import requests
import json
import unicodecsv as csv
import xml.etree.ElementTree as ET
#django imports
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from geographies.models import *
#app imports
from videos.models import *


class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetCropMasterDetails', auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
		xml_file = open("ap/crop.xml", 'w')
		xml_file.write(req.content)
		xml_file.close()
		# partner=Partner.objects.get(id=50)
		csv_file = open('ap/crop_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('ap/crop.xml')
		root = tree.getroot()
		try:
			data = json.loads(root.text, strict=False)
		except Exception as e:
			print e
		state = State.objects.get(id=6)
		user_obj = User.objects.get(username="apvideo")
		district_data_list = []
		for data_iterable in data:
			crop_code = data_iterable.get('Crop_Id')
			crop_name = data_iterable.get('Crop_Name')
			crop_name_telgu = data_iterable.get('Crop_Name_Telugu')
			
			try:
				subcategory_obj = SubCategory.objects.filter(subcategory_name=crop_name)
				if subcategory_obj.count() >= 1:
					subcategory_obj = subcategory_obj[0]
				else:
					subcategory_obj, created = \
						SubCategory.objects.get_or_create(subcategory_name=crop_name,
														  category_id=5)
			except Exception as e:
				wtr.writerow(['Not able to Save Crop', crop_code, crop_name, e])

			try:
				crop_obj, created = \
					APCrop.objects.get_or_create(subcategory=subcategory_obj,
												 crop_name=crop_name,
												 crop_code=crop_code,
												 user_created_id=user_obj.id,
												 crop_name_telgu=crop_name_telgu)
			except Exception as e:
				wtr.writerow(['Not able to Save Crop n AP_CROP TABLE', crop_code, crop_name, e])
		csv_file.close()


