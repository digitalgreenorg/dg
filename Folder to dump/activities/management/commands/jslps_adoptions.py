import urllib2
import unicodecsv as csv
from datetime import datetime 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.conf import settings
from people.models import *
from programs.models import *
from videos.models import *
from activities.models import *
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):
		
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportAdoptionData'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		partner = Partner.objects.get(id = 24)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/adoption.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		csv_file = open('jslps_data_integration_files/adoption_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/adoption.xml')
		root = tree.getroot()
		for c in root.findall('AdoptionData'):
			pc = c.find('MemberCode').text
			vc = c.find('Video').text
			da = datetime.datetime.strptime(c.find('DOA').text, '%d/%m/%Y')
			de = datetime.datetime.strptime(c.find('DOE').text, '%d/%m/%Y')

			error = 0
			try:
				video = JSLPS_Video.objects.get(vc = vc)
			except JSLPS_Video.DoesNotExist as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['video not exist', vc, e])
				error = 1
			try:
				person = JSLPS_Person.objects.get(person_code = pc)
			except (JSLPS_Video.DoesNotExist, JSLPS_Person.DoesNotExist) as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['person not exist', pc, e])
				error = 1

			if error==0:
				try:
					pap = PersonAdoptPractice(person = person.person,
											video = video.video,
											date_of_adoption = da,
											time_created = de,
											partner = partner)
					pap.save()
					jslps.new_count += 1
					print "pap saved"
				except Exception as e:
					print vc, pc, e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['Adoption', 'Person', pc, 'Video', vc, e])
