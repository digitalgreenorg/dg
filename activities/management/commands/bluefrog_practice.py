#python imports
import requests
import json
import unicodecsv as csv
import xml.etree.ElementTree as ET
#django imports
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
#app imports
from geographies.models import *
from videos.models import *
import ap_data_integration as ap


class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetPestManagementDetails', auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
		xml_file = open("ap/practice.xml", 'w')
		xml_file.write(req.content)
		xml_file.close()
		partner=Partner.objects.get(id=50)
		csv_file = open('ap/practice_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('ap/practice.xml')
		root = tree.getroot()
		try:
			data = json.loads(root.text, strict=False)
		except Exception as e:
			print e
		state = State.objects.get(id=6)
		user_obj = User.objects.get(username="apvideo")
		for data_iterable in data:
			pest_code = data_iterable.get('Pest_Id')
			pest_name = data_iterable.get('Pest_Method_Name')
			pest_name_telgu = data_iterable.get('Pest_Method_Name_Telugu')
			

			try:
				crop_obj, created = \
					APPractice.objects.get_or_create(pest_name=pest_name,
													 pest_code=pest_code,
													 user_created_id=user_obj.id,
													 pest_name_telgu=pest_name_telgu)
			except Exception as e:
				wtr.writerow(['Not able to Save Crop n AP Practice TABLE', pest_name, pest_code, e])
		csv_file.close()


