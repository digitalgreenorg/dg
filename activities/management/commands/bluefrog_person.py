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
from people.models import *
from programs.models import *
import ap_data_integration as ap


class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		district_code_list = ['0101', '0102', '0103', '0104', '0105', '0106', '0107', '0108', '0109', '0110', '0111', '0112', '0113']

		for item in district_code_list:
			req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetFarmerDetails/?District_ID=%s' % item, auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
			xml_file = open("ap/person_%s.xml" % item, 'w')
			xml_file.write(req.content)
			xml_file.close()
			partner=Partner.objects.get(id=72)
			csv_file = open('ap/person_error_%s.csv' %item, 'wb')
			wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
			# tree = ET.parse('ap/person.xml')
			# root = tree.getroot()
			data = json.loads(req.json())
			state = State.objects.get(id=6)
			user_obj = User.objects.get(username="apvideo")
			district_data_list = []
			for data_iterable in data:
				person_code = data_iterable.get('ID')
				person_name = data_iterable.get('Name')
				gender = data_iterable.get('Gender')
				if gender == "Male":
					gender = "M"
				else:
					gender = "F"
				age = data_iterable.get('Age', None)
				father_name = data_iterable.get('Father/Husband Name')
				mobile = data_iterable.get('Mobile', None)
				village_code = data_iterable.get('Village ID')
				habitation_code = data_iterable.get('Habitation ID')
				
				try:
					village = AP_Village.objects.filter(village_code=village_code).latest('id')
				except AP_Village.DoesNotExist as e:
					wtr.writerow(['AP village not EXIST: '+str(person_code), village_code, e])
					continue

				try:
					person, created = \
						Person.objects.get_or_create(person_name=person_name,
													 father_name=father_name,
													 partner=partner,
													 gender=gender,
													 village=village.village,
													 )
					if age:
						person.age = age
					person.phone_no = mobile
					person.user_created_id = user_obj.id
					person.save()
					ap.new_count += 1
					print "Person saved in DG Person table"
				except Exception as e:
					person = None
					if "Duplicate entry" not in str(e):
						ap.other_error_count += 1
						wtr.writerow(["Not able to save person", person_code, e])
					else:
						ap.duplicate_count += 1

				if person != None:
					ap_person_list = AP_Person.objects.filter(person_code=person_code)
					if len(ap_person_list) == 0:
						ap_person, created = \
							AP_Person.objects.get_or_create(person_code=person_code,
														    person=person,
														    user_created_id=user_obj.id,
														    )
					else:
	                                        try:
						    ap_person = \
							AP_Person.objects.get(person_code=person_code,
											      person=person,
											      user_created_id=user_obj.id,
											      )
	                                        except Exception as e:
	                                            pass
				else:
					person_list = \
						Person.objects.filter(person_name=person_name,
											  father_name=father_name,
											  village=village.village)
					if len(person_list) != 0:
						person = person_list[0]
						ap_person_list = AP_Person.objects.filter(person_code=person_code,
																  person=person)
						if len(ap_person_list) == 0:
							ap_person, created = \
								AP_Person.objects.get_or_create(person_code=person_code,
															    person=person,
															    user_created_id=user_obj.id
															    )
					else:
						wtr.writerow(['Person not saved and duplicate also not exist',person_code, "not saved"])

			csv_file.close()




			
