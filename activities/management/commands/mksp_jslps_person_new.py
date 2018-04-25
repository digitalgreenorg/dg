import urllib2
import unicodecsv as csv
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from geographies.models import *
from people.models import *
from programs.models import *
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportSRIRegistrationDataMKSP'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/mksp_person.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		user_obj = User.objects.get(username="jslps_bot")
		csv_file = open('jslps_data_integration_files/mksp_person_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/mksp_person.xml')
		root = tree.getroot()
		data_list = []
		for c in root.findall('SRIRegistrationDataMKSP'):
			pc = c.find('MemID').text
			# Mem Id coming as combination
			try:
				pc = pc.split('-')[-1]
				data_list.append(pc)
			except Exception as e:
				pc = pc
			pn = unicode(c.find('MemberName').text)
			if c.find('FatherName') is not None:
				pfn = unicode(c.find('FatherName').text)
			else:
				pfn = ''
			if c.find('PhoneNo') is not None:
				phone = c.find('PhoneNo').text
			else:
				phone = ''
			if c.find('Age') is not None:
				age = int(c.find('Age').text)
			else:
				age = None
			if c.find('Gender') is not None:
				gender = c.find('Gender').text
			else:
				gender = 'F'
			vc = c.find('VillageCode').text
			gc = c.find('GroupCode').text

			try:
				village = JSLPS_Village.objects.get(village_code = vc)
			except JSLPS_Village.DoesNotExist as e:
				wtr.writerow(['JSLPS village not EXIST: '+str(pc), vc, e])
				continue
			error = 0
			try:
				group = JSLPS_Persongroup.objects.get(group_code = gc)
			except JSLPS_Persongroup.DoesNotExist as e:
				wtr.writerow(['JSLPS group not EXIST: '+str(pc), gc, e])
				error = 1

			if error == 1:
				try:
					person, created = \
						Person.objects.get_or_create(person_name = pn,
													 father_name = pfn,
													 partner=partner,
													 gender=gender,
													 village = village.Village,
													 )
					person.age = age
					person.phone_no = phone
					person.user_created_id = user_obj.id
					person.save()
					jslps.new_count += 1
				except Exception as e:
					person = None
					if "Duplicate entry" not in str(e):
						jslps.other_error_count += 1
						wtr.writerow(['Error in save person group: ',pc, e])
					else:
						jslps.duplicate_count += 1
			else:
				try:
					person, created = \
						Person.objects.get_or_create(person_name = pn,
													 father_name = pfn,
													 partner=partner,
													 gender=gender,
													 village = village.Village,
													 )
					person.age = age
					person.phone_no = phone
					person.user_created_id = user_obj.id
					person.group=group.group
					person.save()
					jslps.new_count += 1
				except Exception as e:
					person = None
					if "Duplicate entry" not in str(e):
						jslps.other_error_count += 1
						wtr.writerow(['Error in save person (group(%s)): '%(str(gc)),pc, e])
					else:
						jslps.duplicate_count += 1

			if person != None:
				jslps_person_list = JSLPS_Person.objects.filter(person_code=pc, person=person)
				if len(jslps_person_list) == 0:
					if group is not None:
						jslps_person, created = \
							JSLPS_Person.objects.get_or_create(person_code=pc,
															   person=person,
															   user_created_id=user_obj.id,
															   activity="MKSP",
															   group=group
															   )
					else:
						jslps_person, created = \
							JSLPS_Person.objects.get_or_create(person_code=pc,
															   person=person,
															   user_created_id=user_obj.id,
															   activity="MKSP",
															   )

				else:
					jslps_person = jslps_person_list[0]
					jslps_person.person = person
					jslps_person.save()
			else:
				person_list = Person.objects.filter(person_name = pn,father_name = pfn,village = village.Village)
				if len(person_list) != 0:
					person = person_list[0]
					jslps_person_list = JSLPS_Person.objects.filter(person_code=pc, person=person)
					if len(jslps_person_list) == 0:
						if group is not None:
							jslps_person, created = \
								JSLPS_Person.objects.get_or_create(person_code=pc,
																   person=person,
																   user_created_id=user_obj.id,
																   activity="MKSP",
																   group=group
																   )
						else:
							jslps_person, created = \
								JSLPS_Person.objects.get_or_create(person_code=pc,
																   person=person,
																   user_created_id=user_obj.id,
																   activity="MKSP",
																   )
					else:
						jslps_person = jslps_person_list[0]
						if jslps_person.person == None:
							jslps_person.person = person
							jslps_person.save()
				else:
					wtr.writerow(['Person not saved and duplicate also not exist',pc, "not saved"])

		JSLPS_Person.objects.filter(person_code__in=data_list).update(activity="MKSP")

