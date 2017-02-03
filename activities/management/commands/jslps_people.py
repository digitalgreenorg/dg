import urllib2
import unicodecsv as csv
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from geographies.models import *
from people.models import *
from programs.models import *
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportSRIRegistrationData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("jslps_data_integration_files/person.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		csv_file = open('jslps_data_integration_files/person_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/person.xml')
		root = tree.getroot()
		for c in root.findall('SRIRegistrationData'):
			pc = c.find('MemID').text
			pn = unicode(c.find('MemberName').text)
			if c.find('FatherName') is not None:
				pfn = unicode(c.find('FatherName').text)
			else:
				pfn = ''
			vc = c.find('VillageCode').text
			gc = c.find('GroupCode').text
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

			error = 0
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
			except JSLPS_Village.DoesNotExist as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['JSLPS village not EXIST: '+str(pc), vc, e])
				error = 1
			
			#TODO: Code clean up
			try:
				group = JSLPS_Persongroup.objects.get(group_code = gc)
			except JSLPS_Persongroup.DoesNotExist as e:
				error = 1
				try:
					person = Person(person_name = pn,
									father_name = pfn,
									age = age,
									phone_no = phone,
									gender = gender,
									village = village.Village,
									partner = partner)
					person.save()
					jslps.new_count += 1
				except Exception as e:
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
						wtr.writerow(['duplicate entry: '+str(pc), gc, e])
					else:
						jslps.other_error_count += 1
						wtr.writerow(['village group not exist: '+str(pc), gc, e])
				try:
					person = Person.objects.filter(person_name = pn, father_name = pfn, village_id = village.Village.id).get()
					person_added = JSLPS_Person.objects.values_list('person_code',flat=True)
					#person_added = [i[0] for i in person_added]
				except Exception as e:
					print e
				if pc not in person_added:
					try:
						jp = JSLPS_Person(person_code = pc,
											person = person)
						jp.save()
						print pc, "saved in new"
					except Exception as e:
						print pc, e
						if "Duplicate entry" not in str(e):
							jslps.other_error_count += 1
							wtr.writerow(['JSLPS person error save', pc, e])
			
			if (error == 0):
				full_name_xml = pn+' '+pfn
				person_set = dict(Person.objects.filter(village_id = village.Village.id, group_id = group.group.id).values_list('person_name','father_name'))
				full_name = []
				for key, value in person_set.iteritems():
					name = key+' '+value
					full_name.append(name)
				
				if full_name_xml not in full_name:
					try:
						person = Person(person_name = pn,
										father_name = pfn,
										age = age,
										phone_no = phone,
										gender = gender,
										village = village.Village,
										group = group.group,
										partner = partner)
						person.save()
						jslps.new_count += 1
						print pc,"person saved in old"
					except Exception as e:
						print pc, e
						if "Duplicate entry" in str(e):
							jslps.duplicate_count += 1
						else:
							jslps.other_error_count += 1
							wtr.writerow(['person save', pc, e])
					try:
						person = Person.objects.filter(person_name = pn, father_name = pfn, group_id = group.group.id, village_id = village.Village.id).get()
						person_added = JSLPS_Person.objects.values_list('person_code',flat=True)
						#person_added = [i[0] for i in person_added]
					except Exception as e:
						print e
						if "Duplicate entry" not in str(e):
							jslps.other_error_count += 1
							wtr.writerow(['person exist', pc, e])
					if pc not in person_added:
						try:
							jp = JSLPS_Person(person_code = pc,
												person = person)
							jp.save()
							print pc, "saved in new"
						except Exception as e:
							print pc, e
							if "Duplicate entry" not in str(e):
								jslps.other_error_count += 1
								wtr.writerow(['JSLPS person save error', pc, e])
