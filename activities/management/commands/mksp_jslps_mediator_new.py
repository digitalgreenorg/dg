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
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportAKMDataMKSP'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/mksp_mediator.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id=24)
		animator_data_list = []
		csv_file = open('jslps_data_integration_files/mksp_mediator_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/mksp_mediator.xml')
		root = tree.getroot()
		user_obj = User.objects.get(username="jslps_bot")
		print len(root.findall('AKMDataMKSP'))
		for c in root.findall('AKMDataMKSP'):
			ac = c.find('AKM_ID').text
			an = unicode(c.find('AKMName').text)
			gender = c.find('Gender').text
			vc = c.find('VillageCode').text
			dc = c.find('DistrictCode').text
			animator_data_list.append(ac)
			if c.find('PhoneNo') is not None:
				phone = c.find('PhoneNo').text
			else:
				phone = ''
			error = 0
			try:
				district = JSLPS_District.objects.get(district_code=dc)
			except JSLPS_District.DoesNotExist as e:
				wtr.writerow(['JSLPS district not exist '+str(ac), dc, e, c])
				continue
			
			try:
				village_list = [JSLPS_Village.objects.get(village_code=vc)]
			except Exception as e:
				village_list = []
				wtr.writerow(['village not exist '+str(ac), vc, e, c])

			try:
				animator, created = \
					Animator.objects.get_or_create(name=an,
												   gender=gender,
												   partner=partner,
												   district=district.district,
												   phone_no=phone,
												   user_created_id=user_obj.id)
				jslps.new_count += 1
			except Exception as e:
				animator = None
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['Animator save error', ac, e])
				else:
					jslps.duplicate_count += 1

			if animator != None:
				assigned_villages = AnimatorAssignedVillage.objects.filter(animator=animator).values_list('village_id', flat=True)
				for village in village_list:
					if village.Village.id not in assigned_villages:
						animator_village, created = \
							AnimatorAssignedVillage.objects.get_or_create(animator=animator,
																		  village=village.Village,
																		  user_created_id=user_obj.id)

				jslps_animator_list = JSLPS_Animator.objects.filter(animator_code=ac)
				if len(jslps_animator_list) == 0:
					jslps_animator, created = \
						JSLPS_Animator.objects.get_or_create(animator_code=ac,
															 animator=animator,
															 user_created_id=user_obj.id,
															 activity='MKSP'
															 )
				else:
					jslps_animator = jslps_animator_list[0]
					jslps_animator.animator = animator
					jslps_animator.save()
			else:
				if phone != '':
					animator_list = Animator.objects.filter(name=an,
										gender=gender,
										partner=partner,
										district=district.district,
										phone_no=phone)
				else:
					animator_list = Animator.objects.filter(name = an,
										gender=gender,
										partner=partner,
										district=district.district)
				if len(animator_list) != 0:
					animator = animator_list[0]
					assigned_villages = AnimatorAssignedVillage.objects.filter(animator=animator).values_list('village_id', flat=True)
					for village in village_list:
						if village.Village.id not in assigned_villages:
							animator_village, created = \
								AnimatorAssignedVillage.objects.get_or_create(animator=animator,
																		  village=village.Village,
																		  user_created_id=user_obj.id)
					jslps_animator_list = JSLPS_Animator.objects.filter(animator_code=ac,animator=animator)
					if len(jslps_animator_list) == 0:
						jslps_animator, created = \
							JSLPS_Animator.objects.get_or_create(animator_code=ac,
																 animator=animator,
																 activity='MKSP',
																 user_created_id=user_obj.id)
					else:
						jslps_animator = jslps_animator_list[0]
						if jslps_animator.animator == None:
							jslps_animator.animator = animator
							jslps_animator.save()
				else:
					wtr.writerow(['Animator not saved and duplicate also not exist',ac, "not saved"])
			

		JSLPS_Animator.objects.filter(animator_code__in=animator_data_list).update(activity='MKSP')


		#add camera operator to mediator table
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportCameraOperatorMaster?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("jslps_data_integration_files/mediator_co.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		csv_file = open('jslps_data_integration_files/mediator_co_error.csv', 'wb')
		wtrr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/mediator_co.xml')
		root = tree.getroot()
		camera_lst = []
		for c in root.findall('CameraOperatorMasterData'):
			ac = c.find('CameraOperatorID').text
			an = unicode(c.find('CameraOperatorName').text)
			gender = 'F'
			dc = c.find('DistrictCode').text
			camera_lst.append(ac)
			try:
				district = JSLPS_District.objects.get(district_code = dc)
			except JSLPS_District.DoesNotExist as e:
				wtrr.writerow(['JSLPS district not exist '+str(ac), dc, e])
				continue

			try:
				animator, created = \
					Animator.objects.get_or_create(name=an,
												   gender=gender,
												   partner = partner,
												   district = district.district)
				jslps.new_count += 1
			except Exception as e:
				animator = None
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtrr.writerow(['Animator save error', ac, e])
				else:
					jslps.duplicate_count += 1

			if animator != None:
				jslps_animator_list = JSLPS_Animator.objects.filter(animator_code=ac)
				if len(jslps_animator_list) == 0:
					jslps_animator, created = \
						JSLPS_Animator.objects.get_or_create(animator_code=ac,
									   						 animator=animator,
									   						 activity='MKSP',
									   						 user_created_id=user_obj.id)
				else:
					jslps_animator = jslps_animator_list[0]
					jslps_animator.animator = animator
					jslps_animator.save()
			else:
				animator_list = Animator.objects.filter(name = an,
														gender=gender,
														partner=partner,
														district=district.district)
				if len(animator_list) != 0:
					animator = animator_list[0]
					jslps_animator_list = JSLPS_Animator.objects.filter(animator_code=ac,animator=animator)
					if len(jslps_animator_list) == 0:
						jslps_animator, created = \
						JSLPS_Animator.objects.get_or_create(animator_code=ac,
									   						 animator=animator,
									   						 user_created_id=user_obj.id,
									   						 activity='MKSP')
					else:
						jslps_animator = jslps_animator_list[0]
						if jslps_animator.animator == None:
							jslps_animator.animator = animator
							jslps_animator.save()
				else:
					wtr.writerow(['Animator not saved and duplicate also not exist',ac, "not saved"])

		JSLPS_Animator.objects.filter(animator_code__in=camera_lst).update(activity='LIVELIHOOD')


