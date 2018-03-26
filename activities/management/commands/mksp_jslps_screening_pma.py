import urllib2
import unicodecsv as csv
from datetime import datetime 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from geographies.models import *
from people.models import *
from programs.models import *
from videos.models import *
from activities.models import *
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):
		

		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportVedioScreeingMasterDataMKSP'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		partner = Partner.objects.get(id = 24)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/mksp_screening.xml", 'w')
		xml_file.write(contents)
		xml_file.close()
		user_obj = User.objects.get(username="jslps_bot")
		csv_file = open('jslps_data_integration_files/mksp_screening_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/mksp_screening.xml')
		root = tree.getroot()
		for c in root.findall('VedioScreeingMasterDataMKSP'):
			sc = c.find('VDO_ID').text
			vc = c.find('VillageCode').text
			ac = c.find('AKMCode').text
			sd = datetime.datetime.strptime(c.find('ScreeningDate').text, '%d/%m/%Y')
			st = datetime.datetime.strptime(c.find('start_time').text, '%H:%M:%S')
			#et = datetime.datetime.strptime(c.find('End_time').text, '%H:%M:%S')
			try:
				vdc = map(int, c.find('Video').text.split(','))
			except Exception as e:
				vdc = []
				jslps.other_error_count += 1
				wtr.writerow(['scr id',sc,'Can not save screening without video'])
				continue
			try:
				gc = map(int, c.find('GroupCode').text.split(','))
			except Exception as e:
				gc = []
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
						if "Duplicate entry" not in str(e):
							jslps.other_error_count += 1
							wtr.writerow(['scr id',sc,'video not exist',v, e])
				for g in gc:
					try:
						grp = JSLPS_Persongroup.objects.get(group_code = g)
						groups.append(grp.group)
					except JSLPS_Persongroup.DoesNotExist as e:
						if "Duplicate entry" not in str(e):
							jslps.other_error_count += 1
							wtr.writerow(['scr id',sc,'group not exist',g, e])
			except (JSLPS_Village.DoesNotExist, JSLPS_Animator.DoesNotExist) as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['village',vc,'akm',ac,'scr id',sc, e])
				error = 1
			if (error==0):				
				try:
					scr_already_exist = \
						Screening.objects.filter(date=sd,
												 start_time=st,
												 village=village.Village,
												 animator=animator.animator,
												 partner=partner)
					
					if len(scr_already_exist) == 0:
						scr, created = \
							Screening.objects.get_or_create(date=sd,
															start_time=st,
															village=village.Village,
															animator=animator.animator,
															partner=partner)
						jslps.new_count += 1
						obj,created = \
							JSLPS_Screening.objects.get_or_create(screenig_code = sc,
																  screening = screening,
																  activity="MKSP",
																  user_created_id=user_obj.id)
				except Exception as e:
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['Screening save',sc,e])
				try:
					screening = Screening.objects.filter(date = sd,start_time = st, village_id = village.Village.id,animator_id = animator.animator.id,partner_id = partner.id)
					if len(screening) >= 1:
						screening = screening[0]
					for i in groups:
						if not i.screening_set.filter(id=screening.id).exists():
							jslps.new_count += 1
						else:
							jslps.duplicate_count += 1
						screening.farmer_groups_targeted.add(i)
					for i in videos:
						if not i.screening_set.filter(id=screening.id).exists():
							jslps.new_count += 1
						else:
							jslps.duplicate_count += 1
						screening.videoes_screened.add(i)
				except Exception as e:
					print e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['Groups save',gc,'video save',vc])

				try:
					screening = Screening.objects.filter(date=sd, start_time=st,village_id=village.Village.id,animator_id = animator.animator.id,partner = partner.id)
					if len(screening) >= 1:
						screening = screening[0]
					sc_added = JSLPS_Screening.objects.values_list('screenig_code', flat=True)
					if sc not in sc_added:
						try:
							sj, created = \
								JSLPS_Screening.objects.get_or_create(screenig_code = sc,
																	  screening = screening,
																	  activity="MKSP",
																	  user_created_id=user_obj.id)
						except Exception as e:
							if "Duplicate entry" not in str(e):
								jslps.other_error_count += 1
								wtr.writerow(['JSLPS-MKSP screening save',sc])
				except Screening.DoesNotExist as e:
					wtr.writerow(['Screening:::', e])

		csv_file.close()


		#saving pma
		file_url = "http://webservicesri.swalekha.in/Service.asmx/GetExportVedioScreeingMemberDataMKSP"+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/mksp_pma.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		csv_file = open('jslps_data_integration_files/mksp_pma_error.csv', 'wb')
		wtrr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/mksp_pma.xml')
		root = tree.getroot()

		for c in root.findall('VedioScreeingMemberDataMKSP'):
			sc = c.find('VDO_ID').text
			pc = c.find('MemberId').text
			try:
				gc = pc.split('-')[0]
				pc = pc.split('-')[-1]
			except Exception as e:
				pc = pc
				gc = None
			error = 0
			try:
				screening = JSLPS_Screening.objects.get(screenig_code=sc, activity="MKSP")
				if gc is not None:
					try:
						group_obj = JSLPS_Persongroup.objects.get(group_code=gc).group.id

					except JSLPS_Persongroup.DoesNotExist as e:
						jslps.other_error_count += 1
						wtrr.writerow(['pma JSLPS_Persongroup', sc, 'pma Person', pc, e])
						
					try:
						person =  JSLPS_Person.objects.filter(person_code=pc, activity="MKSP",
														   person__group_id=group_obj).latest('id')
					except (JSLPS_Person.DoesNotExist, JSLPS_Person.MultipleObjectsReturned) as e:
						jslps.other_error_count += 1
						wtrr.writerow(['JSLPS_SCRID', sc, 'JSLPS_GROUP', gc, 'pma Person', pc, e])

			except (JSLPS_Screening.DoesNotExist, JSLPS_Person.DoesNotExist) as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtrr.writerow(['pma Screening', sc, 'pma Person', pc, e])
				error = 1

			if (error == 0):
				try:
					pma_already_exist = PersonMeetingAttendance.objects.filter(screening_id = screening.screening.id,person_id=person.person.id)
					if len(pma_already_exist) == 0:
						pma = PersonMeetingAttendance(screening=screening.screening,
													 person=person.person)
						pma.save()
						jslps.new_count += 1
						print "PMA saved in old"
				except Exception as e:
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtrr.writerow(['pma Attendence save', sc, e])

		csv_file.close()
