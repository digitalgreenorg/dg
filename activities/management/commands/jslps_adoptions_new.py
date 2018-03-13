import urllib2
import unicodecsv as csv
from datetime import datetime 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from people.models import *
from programs.models import *
from videos.models import *
from activities.models import *
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):
		
		partner = Partner.objects.get(id = 24)
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportAdoptionData'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/adoption.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		csv_file = open('jslps_data_integration_files/adoption_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/adoption.xml')
		root = tree.getroot()
		user_obj = User.objects.get(username="jslps_bot")
		for c in root.findall('AdoptionData'):
			pc = c.find('MemberCode').text
			try:
				vc = c.find('Video').text
			except Exception as e:
				wtr.writerow(['video data missing (Member code ->)', pc, e])
				jslps.other_error_count += 1
				continue
			da = datetime.datetime.strptime(c.find('DOA').text, '%d/%m/%Y')
			de = datetime.datetime.strptime(c.find('DOE').text, '%d/%m/%Y')
			ac = c.find('AKMCode').text
			animator = JSLPS_Animator.objects.filter(animator_code = ac, activity="LIVELIHOOD")
			if len(animator) == 0:
				wtr.writerow(['Can not save adoption without animator', ac, "animator not found"])
				continue
			else:
				animator = animator[0]

			try:
				video = JSLPS_Video.objects.get(vc = vc, activity="LIVELIHOOD")
			except Exception as e:
				wtr.writerow(['video not exist', vc, e])
				continue
			
			person = JSLPS_Person.objects.filter(person_code = pc, activity="LIVELIHOOD")
			if len(person) == 0:
				wtr.writerow(['person not exist', pc, "Person not found"])
				continue
			else:
				person = person[0]
			try:
				pap, created = \
					PersonAdoptPractice.objects.get_or_create(person=person.person,
										  					  video=video.video,
										  					  date_of_adoption = da,
										  					  partner=partner,
										  					  animator=animator.animator,
										  					  user_created_id=user_obj.id)
				jslps.new_count += 1
				try:
					obj, created = \
						JSLPS_Adoption.objects.get_or_create(member_code=pc,
															 jslps_video_id=video.id,
															 jslps_date_of_adoption=da,
															 jslps_akmcode_id=animator.id,
															 adoption=pap,
															 user_created_id=user_obj.id
															 )
				except Exception as e:
					wtr.writerow(['Not able to save Adoption', e])
			except Exception as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['Adoption not saved (video code %s)'%(str(vc)), pc, e])
				else:
					jslps.duplicate_count += 1



			


