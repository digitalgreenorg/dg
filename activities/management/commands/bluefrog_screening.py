#python imports
import requests
import json
import datetime
import unicodecsv as csv
import xml.etree.ElementTree as ET
#django imports
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
#app imports
from geographies.models import *
from videos.models import *
from people.models import *
from activities.models import *
import ap_data_integration as ap



class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetPicoDisseminationDetails', auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
		xml_file = open("ap/screening.xml", 'w')
		xml_file.write(req.content)
		xml_file.close()
		partner=Partner.objects.get(id=72)
		csv_file = open('ap/screening.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		# tree = ET.parse('ap/screening.xml')
		# root = tree.getroot()
		try:
			data = json.loads(req.json(), strict=False)
		except Exception as e:
			pass
		# state = State.objects.get(id=6)
		user_obj = User.objects.get(username="apvideo")
		district_data_list = []

		for data_iterable in data:
			screening_code = data_iterable.get('ID')
			start_date = data_iterable.get('Date of Screening')
			start_time = data_iterable.get('Date & Time of Data Entry')
			district_code = data_iterable.get('District ID')
			block_code = data_iterable.get('Date of Screening')
			village_code = data_iterable.get('Village ID')

			mediator_code = data_iterable.get('CRP/CA ID')
			videos = data_iterable.get('Video IDs')
			no_of_male = data_iterable.get('No. of Male')

			no_of_female = data_iterable.get('No. of Female')
			total_members = data_iterable.get('Total')
			screening_duration = data_iterable.get('Duration of Screening')

			# for saving in screening
			start_date = start_date
			start_time = datetime.datetime.strptime(start_time.split(' ')[1], '%H:%M:%S').time()
			parentcategory_id=2
			# for village
			try:
				village_obj = AP_Village.objects.filter(village_code=village_code)
				if village_obj.count() >= 1:
					village = village_obj[0]
					village = village.village
			except AP_Village.DoesNotExist:
				village = None
			# for animator
			try:
				animator_obj = AP_Animator.objects.filter(animator_code=mediator_code)
				if animator_obj.count() >= 1:
					animator = animator_obj[0]
					animator = animator.animator
				else:
					animator = None
			except AP_Village.DoesNotExist as e:
				animator = None

			#videos
			try:
				videoes_screened = [int(item) for item in videos.strip().split(',') if item != '0']
				# try:
				# 	videoes_screened = filter(0, videoes_screened)
				# except Exception as e:
				# 	print e
			except:
				videoes_screened = []
			partner = partner
			farmer_groups_targeted=[1]
			if animator:
				screening_dict = {'village': village, 'animator':animator, 'start_time': start_time,
								  'date': start_date, 'parentcategory_id': parentcategory_id,
								  'partner_id':partner.id
								  }
				try:
					scr_obj, created = Screening.objects.get_or_create(**screening_dict)
					videoes_screened = [item for item in videoes_screened if item != 0]
					if len(videoes_screened) >=1:
						try:
							scr_obj.videoes_screened.add(*videoes_screened)
						except:
							pass
						scr_obj.farmer_groups_targeted.add(*farmer_groups_targeted)

						if scr_obj:
							try:
								ap_scr_obj, created = \
									AP_Screening.objects.get_or_create(screening_code=screening_code,
																	   screening=scr_obj,
																	   no_of_male=no_of_male,
																	   no_of_female=no_of_female,
																	   user_created_id=user_obj.id,
																	   total_members=total_members)
							except Exception as e:
								wtr.writerow(['Not able to Save Screening in AP Screening TABLE', screening_code, e])
				except Screening.DoesNotExist as e:
					wtr.writerow(['Not able to save screening',screening_code, e])
			else:
				wtr.writerow(['Not able to save screening',screening_code, 'meditor was not present'])

			
		csv_file.close()


