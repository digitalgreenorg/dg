import urllib2
import unicodecsv as csv
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from geographies.models import *
from people.models import *
from programs.models import *
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnN?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("jslps_data_integration_files/hnn-person.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		user_obj = User.objects.get(username="jslps_bot")
		csv_file = open('jslps_data_integration_files/hnn-person.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/hnn-person.xml')
		root = tree.getroot()
		
		for c in root.findall('GroupMemberData'):
			village_code = c.find('VillageCode').text
			group_code = c.find('GroupCode').text
			member_code = c.find('Group_M_Code').text
			member_name = c.find('MemberName').text
			father_name = c.find('FatherName').text if c.find('FatherName') else 'X'
			gender = 'F'

			try:
				village = JSLPS_Village.objects.get(village_code=village_code)
			except JSLPS_Village.DoesNotExist as e:
				wtr.writerow(['JSLPS village not EXIST: '+ str(member_code), village_code, group_code, e])
				continue
			error = 0
			try:
				group = JSLPS_Persongroup.objects.get(group_code=group_code)
			except JSLPS_Persongroup.DoesNotExist as e:
				wtr.writerow(['JSLPS group not EXIST: '+str(member_code), group_code, e])
				error = 1
			# where group is not present we are trying to save person
			if error == 1:
				try:
					person, created = \
						Person.objects.get_or_create(person_name=member_name,
													 partner=partner,
													 gender=gender,
													 village = village.Village,
													 )
					jslps.new_count += 1
				except Exception as e:
					person = None
					if "Duplicate entry" not in str(e):
						jslps.other_error_count += 1
						wtr.writerow(['Error in save person group: ',member_code, e])
					else:
						jslps.duplicate_count += 1
			# where group is present we are trying to save person
			else:
				try:
					person, created = \
						Person.objects.get_or_create(person_name=member_name,
													 partner=partner,
													 gender=gender,
													 village = village.Village,
													 father_name=father_name,
													 group=group.group,
													 user_created_id=user_obj.id
													 )
					# person.group=group.group
					# person.user_created_id = user_obj.id
					# person.save()
					jslps.new_count += 1
				except Exception as e:
					# import pdb;pdb.set_trace()
					person = None
					if "Duplicate entry" not in str(e):
						jslps.other_error_count += 1
						wtr.writerow(['Error in save person (group(%s)): '%(str(group_code)), member_code, e])
					else:
						jslps.duplicate_count += 1

			if person != None:
				jslps_person_list = JSLPS_Person.objects.filter(person_code=member_code)
				if len(jslps_person_list) == 0:
					if group is not None:
						jslps_person, created = \
							JSLPS_Person.objects.get_or_create(person_code=member_code,
															   person=person,
															   user_created_id=user_obj.id,
															   activity="HNN"
															   )
						jslps_person.group=group
						jslps_person.save()
					else:
						jslps_person, created = \
							JSLPS_Person.objects.get_or_create(person_code=member_code,
															   person=person,
															   user_created_id=user_obj.id,
															   activity="HNN",
															   )
				else:
					jslps_person = jslps_person_list[0]
					jslps_person.person = person
					jslps_person.save()
			else:
				person_list = Person.objects.filter(person_name=member_name,
													village=village.Village)
				if len(person_list) != 0:
					person = person_list[0]
					jslps_person_list = JSLPS_Person.objects.filter(person_code=member_code,person=person)
					if len(jslps_person_list) == 0:
						if group is not None:
							jslps_person, created = \
								JSLPS_Person.objects.get_or_create(person_code=member_code,
																   person=person,
																   user_created_id=user_obj.id,
																   activity="HNN"
																   )
							jslps_person.group=group
							jslps_person.save()
						else:
							jslps_person, created = \
								JSLPS_Person.objects.get_or_create(person_code=member_code,
																   person=person,
																   user_created_id=user_obj.id,
																   activity="HNN",
																   )
					else:
						jslps_person = jslps_person_list[0]
						if jslps_person.person == None:
							jslps_person.person = person
							jslps_person.save()
				else:
					wtr.writerow(['Person not saved and duplicate also not exist',member_code, "not saved"])

		csv_file.close()




			