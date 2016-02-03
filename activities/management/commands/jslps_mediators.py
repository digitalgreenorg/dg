import urllib2
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from geographies.models import *
from people.models import *
from programs.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportAKMData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Abhishek\Desktop\mediator.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		#ADD MEDIATORS - UT(name, gender, district.id)
		tree = ET.parse('C:\Users\Abhishek\Desktop\mediator.xml')
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
			try:
				district = JSLPS_District.objects.get(district_code = dc)
				village = JSLPS_Village.objects.get(village_code = vc)
				animator_set = Animator.objects.filter(name = an, gender = gender, partner_id = partner.id)
				if not animator_set.exists():
					anim = Animator(name = an,
									gender = gender,
									partner = partner,
									district = district.district,
									phone_no = phone)
					anim.save()
					print an, "Animator saved in old"
				animator = Animator.objects.filter(name = an, gender = gender, partner_id = partner.id).get()
				village_list = list(AnimatorAssignedVillage.objects.values_list('village_id'))
				village_list = [i[0] for i in village_list]
				if village.Village.id not in village_list:
					anim_assigned = AnimatorAssignedVillage(animator = animator,
															village = village.Village)
					anim_assigned.save()
					print an, "Animator village saved"
			except Exception as e:
				print ac, an, e

			try:
				animator = Animator.objects.filter(name = an, gender = gender, partner_id = partner.id).get()	
				animator_added = list(JSLPS_Animator.objects.values_list('animator_code'))
				animator_added = [i[0] for i in animator_added]
				if ac not in animator_added:
					ja = JSLPS_Animator(animator_code = ac,
										animator = animator)
					ja.save()
					print an, "Animator saved in new"
			except Exception as e:
				print ac, "jslps", e

		#add camera operator to mediator table
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportCameraOperatorMaster?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Abhishek\Desktop\mediator_co.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		#ADD MEDIATORS - UT(name, gender, district.id)
		tree = ET.parse('C:\Users\Abhishek\Desktop\mediator_co.xml')
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
			except Exception as e:
				print ac, "Camera operator saved"

			try:
				animator = Animator.objects.filter(name = an, gender = gender, partner_id = partner.id).get()	
				animator_added = list(JSLPS_Animator.objects.values_list('animator_code'))
				animator_added = [i[0] for i in animator_added]
				if ac not in animator_added:
					ja = JSLPS_Animator(animator_code = ac,
										animator = animator)
					ja.save()
					print an, "Animator saved in new"
			except Exception as e:
				print ac, "jslps", e