import urllib2
from unicodecsv as csv
from datetime import datetime 
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
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioScreeingMasterData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Abhishek\Desktop\\screening.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		#csv_file = open('/home/ubuntu/code/dg_coco_test/dg/activities/management/screening_error.csv', 'wb')
		csv_file = open('C:\Users\Abhishek\Desktop\screening_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('C:\Users\Abhishek\Desktop\\screening.xml')
		root = tree.getroot()
		for c in root.findall('VedioScreeingMasterData'):
			sc = c.find('VDO_ID').text
			vc = c.find('VillageCode').text
			ac = c.find('AKMCode').text
			sd = datetime.datetime.strptime(c.find('ScreeningDate').text, '%d/%m/%Y')
			st = datetime.datetime.strptime(c.find('start_time').text, '%H:%M:%S')
			et = datetime.datetime.strptime(c.find('End_time').text, '%H:%M:%S')
			vdc = map(int, c.find('Video').text.split(','))
			gc = map(int, c.find('GroupCode').text.split(','))
			error = 0
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
				animator = JSLPS_Animator.objects.get(animator_code = ac)
				groups = []
				videos = []
				for v in vdc:
					try:
						vid = JSLPS_Video.objects.get(vc = v)
						videos.append(vid.video)
					except JSLPS_Video.DoesNotExist as e:
						print v, e
						wtr.writerow(['video',vc, e])
				for g in gc:
					try:
						grp = JSLPS_Persongroup.objects.get(group_code = g)
						groups.append(grp.group)
					except JSLPS_Persongroup.DoesNotExist as e:
						print g, e
						wtr.writerow(['group',gc, e])
			except (JSLPS_Village.DoesNotExist, JSLPS_Animator.DoesNotExist, JSLPS_Video.DoesNotExist) as e:
				print e
				wtr.writerow(['village',vc,'akm',ac,'video',vc, e])
				error = 1

			if (error==0):				
				try:
					scr = Screening(date = sd,
									start_time = st,
									end_time = et,
									village = village.Village,
									animator = animator.animator,
									partner = partner)
					scr.save()
					print "Screening saved in old"
				except Exception as e:
					print e
					wtr.writerow(['Screening',sc,e])
				try:
					screening = Screening.objects.filter(date = sd,start_time = st,end_time = et,village_id = village.Village.id,animator_id = animator.animator.id,partner_id = partner.id).get()
					for i in groups:
						screening.farmer_groups_targeted.add(i)
						screening.save()
						print "Groups saved in old"
					for i in videos:
						screening.videoes_screened.add(i)
						screening.save()
						print "Videos saved in old"
				except Exception as e:
					print e
					wtr.writerow(['Groups',gc,'video',vc])

				try:
					screening = Screening.objects.filter(date = sd,start_time = st,end_time = et,village_id = village.Village.id,animator_id = animator.animator.id,partner = partner.id).get()
					sc_added = JSLPS_Screening.objects.values_list('screenig_code')
					sc_added = [i[0] for i in sc_added]
					if sc not in sc_added:
						try:
							sj = JSLPS_Screening(screenig_code = sc,
										screening = screening)
							sj.save()
							print "Screening saved in new"
						except Exception as e:
							print sc, e
				except Screening.DoesNotExist as e:
					print e


		#saving pma
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioScreeingMemberData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Abhishek\Desktop\\pma.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		#csv_file = open('/home/ubuntu/code/dg_coco_test/dg/activities/management/pma_error.csv', 'wb')
		csv_file = open('C:\Users\Abhishek\Desktop\pma_error.csv', 'wb')
		wtrr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('C:\Users\Abhishek\Desktop\\pma.xml')
		root = tree.getroot()

		for c in root.findall('VedioScreeingMemberData'):
			sc = c.find('VDO_ID').text
			pc = c.find('MemberId').text
			error = 0
			try:
				screening = JSLPS_Screening.objects.get(screenig_code = sc)
				person = JSLPS_Person.objects.get(person_code = pc)

			except (JSLPS_Screening.DoesNotExist, JSLPS_Person.DoesNotExist) as e:
				#print e
				wtrr.writerow(['Screening', sc, 'Person', pc])
				error = 1

			if (error == 0):
				try:
					pma = PersonMeetingAttendance(screening = screening.screening,
												person = person.person,
												interested = True)
					pma.save()
					print "PMA saved in old"
				except Exception as e:
					wtrr.writerow(['Attendence', sc, e])
					print e
