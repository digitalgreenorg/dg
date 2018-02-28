#python imports
import requests
import json
import datetime
import unicodecsv as csv
import xml.etree.ElementTree as ET
#django imports
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
#app imports
from geographies.models import *
from videos.models import *
from people.models import *
from activities.models import *
import ap_data_integration as ap



class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetAdoptionDetails', auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
		xml_file = open("ap/adoption.xml", 'w')
		xml_file.write(req.content)
		xml_file.close()
		partner=Partner.objects.get(id=50)
		csv_file = open('ap/adoption.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('ap/adoption.xml')
		root = tree.getroot()
		try:
			data = json.loads(root.text, strict=False)
		except Exception as e:
			print e
		state = State.objects.get(id=6)
		user_obj = User.objects.get(username="apvideo")
		district_data_list = []
		for data_iterable in data:
			member_code = data_iterable.get('Person ID')
			member_name = data_iterable.get('Person Name')
			video_id = data_iterable.get('Video ID')
			village_code = data_iterable.get('Village ID')
			animator_code = data_iterable.get("Animator ID")
			date_of_adoption = data_iterable.get('Date of Adoption')
			adoption_type = data_iterable.get('Type of Adoption')
			ap_adopt_practice = data_iterable.get('Adoption')

			try:
				ap_adopt_practice_obj = APPractice.objects.get(pest_name=ap_adopt_practice)
			except Exception as e:
				wtr.writerow(['Not able to fetch Practice'])
				ap_adopt_practice_obj = None

			try:
				ap_video = Video.objects.get(id=video_id)
			except Exception as e:
				wtr.writerow(['Not able to fetch Video'])
				ap_video = None

			try:
				ap_animator = AP_Animator.objects.get(animator_code=animator_code)
			except Exception as e:
				wtr.writerow(['Not able to fetch Animator'])
				ap_animator = None

			if ap_adopt_practice_obj and ap_video and ap_animator:
				try:
					adoption_obj, created = \
						AP_Adoption.objects.get_or_create(member_code=member_code,
														  member_name=member_name,
														  ap_video_id=ap_video_id,
														  ap_animator_id=animator_id,
														  date_of_adoption=date_of_adoption,
														  adoption_type=adoption_type,
														  ap_adopt_practice=ap_adopt_practice_obj)
				except Exception as e:
					wtr.writerow(['Not able to Save Adoption in AP Adoption TABLE', member_code, ap_adopt_practice, e])



