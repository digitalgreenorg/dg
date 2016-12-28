import urllib2
import unicodecsv as csv
from datetime import datetime 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from people.models import *
from programs.models import *
from videos.models import *
from activities.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		
		partner = Partner.objects.get(id = 24)
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportAdoptionData?pUsername=admin&pPassword=JSLPSSRI')
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

			try:
				video = JSLPS_Video.objects.get(vc = vc)
			except Exception as e:
				wtr.writerow(['video not exist', vc, e])
				continue
			
			person = JSLPS_Person.objects.filter(person_code = pc)
			if len(person) == 0:
				wtr.writerow(['person not exist', pc, "Person not found"])
				continue
			else:
				person = person[0]
				
			try:
				pap = PersonAdoptPractice(person = person.person,
										  video = video.video,
										  date_of_adoption = da,
										  partner = partner)
				pap.save()
			except Exception as e:
				wtr.writerow(['Adoption not saved (video code %s)'%(str(vc)), pc, e])
