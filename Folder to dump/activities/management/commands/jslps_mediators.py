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
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportAKMData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("jslps_data_integration_files/mediator.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		csv_file = open('jslps_data_integration_files/mediator_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/mediator.xml')
		root = tree.getroot()
		for c in root.findall('AKMData'):
			ac = c.find('AKM_ID').text
			an = unicode(c.find('AKMName').text)
			gender = c.find('Gender').text
			vc = c.find('VillageCode').text
			dc = c.find('DistrictCode').text
			if c.find('PhoneNo') is not None:
				phone = c.find('PhoneNo').text
			else:
				phone = '0'
			error = 0
			try:
				district = JSLPS_District.objects.get(district_code = dc)
			except JSLPS_District.DoesNotExist as e:
				error = 1
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['district not exist', dc, e])
			
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
			except (JSLPS_District.DoesNotExist, JSLPS_Village.DoesNotExist) as e:
				error = 1
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['village not exist', vc, e])

			if(error == 0):
				try:
					animator_set = Animator.objects.filter(name = an, gender = gender, district_id= district.district_id , partner_id = partner.id)
					if not animator_set.exists():
						try:
							anim = Animator(name = an,
											gender = gender,
											partner = partner,
											district = district.district,
											phone_no = phone)
							anim.save()
							jslps.new_count += 1
							print an, "Animator saved in old"
						except Exception as e:
							if "Duplicate entry" in str(e):
								jslps.duplicate_count += 1
							else:
								jslps.other_error_count += 1
								wtr.writerow(['AKM save', ac, e])
				except Exception as e:
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['AKM exists', ac, e])
				try:
					animator = Animator.objects.filter(name = an, gender = gender, district_id= district.district_id , partner_id = partner.id).get()
					village_list = AnimatorAssignedVillage.objects.values_list('village_id', flat=True)
					#village_list = [i[0] for i in village_list]
					if village.Village.id not in village_list:
						anim_assigned = AnimatorAssignedVillage(animator = animator,
																village = village.Village)
						anim_assigned.save()
						jslps.new_count += 1
						print an, "Animator village saved"
				except Exception as e:
					print ac, an, e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['Assigned Village save', ac, vc, e])
				try:
					animator = Animator.objects.filter(name = an, gender = gender,district_id= district.district_id , partner_id = partner.id).get()	
					animator_added = JSLPS_Animator.objects.values_list('animator_code', flat=True)
					#animator_added = [i[0] for i in animator_added]
					if ac not in animator_added:
						ja = JSLPS_Animator(animator_code = ac,
											animator = animator)
						ja.save()
						print an, "Animator saved in new"
				except Exception as e:
					print ac, "jslps", e
					if "Duplicate entry" not in str(e):
						jslps.other_error_count += 1
						wtr.writerow(['jslps AKM', ac, e])

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
		for c in root.findall('CameraOperatorMasterData'):
			ac = c.find('CameraOperatorID').text
			an = unicode(c.find('CameraOperatorName').text)
			gender = 'F'
			dc = c.find('DistrictCode').text
			
			try:
				district = JSLPS_District.objects.get(district_code = dc)
				animator_set = Animator.objects.filter(name = an, gender = gender, partner_id = partner.id)
				if not animator_set.exists():
					anim = Animator(name = an,
									gender = gender,
									partner = partner,
									district = district.district
									)
					anim.save()
					jslps.new_count += 1
			except Exception as e:
				if "Duplicate entry" in str(e):
					jslps.duplicate_count += 1
				else:
					jslps.other_error_count += 1
					wtrr.writerow(['camera operator',ac, e])
				print ac, "Camera operator saved"

			try:
				animator = Animator.objects.filter(name = an, gender = gender, district_id= district.district_id, partner_id = partner.id).get()	
				animator_added = JSLPS_Animator.objects.values_list('animator_code', flat = True)
				#animator_added = [i[0] for i in animator_added]
				if ac not in animator_added:
					ja = JSLPS_Animator(animator_code = ac,
										animator = animator)
					ja.save()
					print an, "Camera operator saved in new"
			except Exception as e:
				print ac, "jslps", e
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtrr.writerow(['JSLPS camera operator',ac, e])
