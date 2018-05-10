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
import ap_data_integration as ap


class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetDiseaseDetails', auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
		xml_file = open("ap/pest_tag.xml", 'w')
		xml_file.write(req.content)
		xml_file.close()
		# partner=Partner.objects.get(id=50)
		csv_file = open('ap/pest_tag.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		# tree = ET.parse('ap/crop.xml')
		# root = tree.getroot()
		try:
			data = json.loads(req.json(), strict=False)
		except Exception as e:
			print e
		state = State.objects.get(id=6)
		user_obj = User.objects.get(username="apvideo")
		for data_iterable in data:
			tag_code = data_iterable.get('pest_id')
			tag_name = data_iterable.get('pest_name')
			tag_regional_name = data_iterable.get('pest_name_telugu')
			

			try:
				tag_obj, created = \
					Tag.objects.get_or_create(tag_code=tag_code,
											  tag_name=tag_name,
											  user_created_id=user_obj.id,
											  tag_regional_name=tag_regional_name)
			except Exception as e:
				wtr.writerow(['Not able to Tag in Tag TABLE', tag_code, tag_name, e])
		csv_file.close()


