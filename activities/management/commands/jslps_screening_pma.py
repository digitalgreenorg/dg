import urllib2
from datetime import * 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from geographies.models import *
from people.models import *
from programs.models import *
from videos.models import *
from activities.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		
		partner = Partner.objects.get(id = 24)
		
		#saving videos
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioScreeingMemberData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Abhishek\Desktop\\screening.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		tree = ET.parse('C:\Users\Abhishek\Desktop\\screening.xml')
		root = tree.getroot()

		for c in root.findall('VedioScreeingMasterData'):
			sc = c.find('VDO_ID').text
			vc = c.find('VillageCode').text
			ac = c.find('AKMCode').text
			sd = datetime.strptime(c.find('ScreeningDate').text, '%d/%m/%Y')
			st = datetime.strptime(c.find('start_time').text, '%H:%M:%S')
			et = datetime.strptime(c.find('End_time').text, '%H:%M:%S')
			vdc = map(int, c.find('Video').text.split(','))
			gc = map(int, c.find('GroupCode').text.split(','))

			error = 0
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
				animator = JSLPS_Animator.objects.get(animator_code = ac)
				video = JSLSP_Video(vc = vc, null=True, blank=True)
			except (JSLPS_Village.DoesNotExist, JSLPS_Animator.DoesNotExist, JSLPS_Video.DoesNotExist) as e:
				print e
				error = 1

			if (error==0):
				sc_set = JSLPS_Screening.objects.values_list('screening_code')
				sc_set = [i[0] for i in sc_set]
				if sc not in sc_set:
					try:
						scr = Screening(date = sd,
										start_time = st,
										end_time = et,
										village = village,
										animator = animator,
										partner = partner)
						scr.save()
					except Exception as e:
						print e
					try:
						screening = Screening.objects.filter(date = sd,start_time = st,end_time = et,village = village,animator = animator,partner = partner).get()
						for i in gd:
							screening.farmer_groups_targeted.add(i)
							screening.save()
						for i in vdc:
							screening.videoes_screened.add(i)
							screening.save()
					except Exception as e:
						print e

		#saving pma
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioScreeingMemberData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Abhishek\Desktop\\pma.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		tree = ET.parse('C:\Users\Abhishek\Desktop\\pma.xml')
		root = tree.getroot()

		for c in root.findall('VedioScreeingMemberData'):
			sc = c.find('VDO_ID').text
			mc = c.find('MemberId').text
			try:
				screening = JSLSP_Screening

