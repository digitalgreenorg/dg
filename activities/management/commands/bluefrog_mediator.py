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
from people.models import *
from programs.models import *
import ap_data_integration as ap


class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetCRPCADetails', auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
		xml_file = open("ap/mediator.xml", 'w')
		xml_file.write(req.content)
		xml_file.close()
		partner=Partner.objects.get(id=72)
		csv_file = open('ap/mediator_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		# tree = ET.parse('ap/mediator.xml')
		# root = tree.getroot()
		data = json.loads(req.json(), strict = False)
		state = State.objects.get(id=6)
		user_obj = User.objects.get(username="apvideo")
		for data_iterable in data:
			mediator_code = data_iterable.get('ID')
			mediator_name = data_iterable.get('Name')
			designation = data_iterable.get('Designation')
			gender = data_iterable.get('Gender')
			if gender == "Male":
				gender = "M"
			else:
				gender = "F"
			
			mobile = data_iterable.get('Mobile', None)
			district_code = data_iterable.get('District Id')
			block_code = data_iterable.get('Mandal Id')
			village_code = data_iterable.get('Village ID')
			habitation_code = data_iterable.get('Habitation ID')
			try:
				district = AP_District.objects.get(district_code=district_code)
			except AP_District.DoesNotExist as e:
				wtr.writerow(['AP district not exist '+str(district_code), e])
				continue
			
			try:
				village_list = [AP_Village.objects.get(village_code=village_code)]
			except Exception as e:
				village_list = []
				wtr.writerow(['village not exist', mediator_name, village_code, e])

			try:
				animator, created = \
					Animator.objects.get_or_create(name=mediator_name,
												   gender=gender,
												   partner=partner,
												   district=district.district,
												   phone_no=mobile,
												   user_created_id=user_obj.id,
												   )
				ap.new_count += 1
			except Exception as e:
				animator = None
				if "Duplicate entry" not in str(e):
					ap.other_error_count += 1
					wtr.writerow(['Animator save error', mediator_name, mediator_code, e])
				else:
					ap.duplicate_count += 1

			if animator != None:
				assigned_villages = AnimatorAssignedVillage.objects.filter(animator=animator).values_list('village_id', flat=True)
				for village in village_list:
					if village.village.id not in assigned_villages:
						animator_village, created = \
							AnimatorAssignedVillage.objects.get_or_create(animator=animator,
																		  village=village.village,
																		  user_created_id=user_obj.id)

				ap_animator_list = AP_Animator.objects.filter(animator_code=mediator_code)
				if len(ap_animator_list) == 0:
					ap_animator, created = \
						AP_Animator.objects.get_or_create(animator_code=mediator_code,
														  animator=animator,
														  user_created_id=user_obj.id,
														  designation=designation)
				else:
					ap_animator = ap_animator_list[0]
					ap_animator.animator = animator
					ap_animator.save()
			else:
				if mobile != '':
					animator_list = Animator.objects.filter(name=mediator_name,
															gender=gender,
															partner=partner,
															district=district.district,
															phone_no=mobile)
				else:
					animator_list = Animator.objects.filter(name=mediator_name,
															gender=gender,
															partner=partner,
															district=district.district)
				if animator_list.count() != 0:
					animator = animator_list[0]
					assigned_villages = AnimatorAssignedVillage.objects.filter(animator=animator).values_list('village_id', flat=True)
					for village in village_list:
						if village.village.id not in assigned_villages:
							animator_village, created = \
								AnimatorAssignedVillage.objects.get_or_create(animator=animator,
																			  village=village.village,
																			  user_created_id=user_obj.id)
					ap_animator_list = \
						AP_Animator.objects.filter(animator_code=mediator_code,
												   animator=animator)
					if ap_animator_list.count() == 0:
						ap_animator, created = \
							AP_Animator.objects.get_or_create(animator_code=mediator_code,
															  animator=animator,
															  user_created_id=user_obj.id,
															  designation=designation)
					else:
						ap_animator = ap_animator_list[0]
						if ap_animator.animator == None:
							ap_animator.animator = animator
							ap_animator.save()
				else:
					wtr.writerow(['Animator not saved and duplicate also not exist',mediator_code, "not saved"])

		
		

		csv_file.close()


