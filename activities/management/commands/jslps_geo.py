import urllib2
import unicodecsv as csv
from django.core.management.base import BaseCommand
from geographies.models import *
import xml.etree.ElementTree as ET

class Command(BaseCommand):
	def handle(self, *args, **options):	

		#GEOGRAPHIES ADD

		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportMasterData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Abhishek\Desktop\\geo.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		csv_file = open('/home/ubuntu/code/dg_test/activities/management/geo_error.csv', 'wb')
		#csv_file = open('C:\Users\Abhishek\Desktop\geo_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('C:\Users\Abhishek\Desktop\geo.xml')
		root = tree.getroot()
		state = State.objects.get(id = 2)
		for c in root.findall('MasterData'):
			dc = c.find('DistrictCode').text
			dn = unicode(c.find('DistrictName').text)
			bc = c.find('BlockCode').text
			bn = unicode(c.find('BlockName').text)
			vc = c.find('VillageCode').text
			vn = unicode(c.find('VillageName').text)
			
			#District
			district_set = dict(District.objects.filter(state_id = 2).values_list('id','district_name'))
			if dn not in district_set.values():
				try:
					dist = District(district_name = dn,
									state = state)
					dist.save()
					print dc, " District saved in old"
				except Exception as e:
					print dc, e
					wtr.writerow(['district',dc, e])
			try:
				district = District.objects.filter(state_id = 2).get(district_name = dn)
				'''d_n = JSLPS_District.objects.get(district_code = dc)
				d_n.district = district
				d_n.save()
				print dc, "distict-foreign key saved in new"'''
				district_added = list(JSLPS_District.objects.values_list('district_code'))
				district_added = [i[0] for i in district_added]
				
				if dc not in district_added:
					jd = JSLPS_District(district_code = dc,
										district_name = dn,
										district = district)
					jd.save()
					print dc, "District Saved in new"
			except Exception as e:
				print dc, e
				wtr.writerow(['district',dc, e])

			#Block
			block_set = dict(Block.objects.filter(district_id = district.id).values_list('id','block_name'))
			if bn not in block_set.values():
				try:
					blck = Block(block_name = bn,
								district = district)
					blck.save()
					print bc, "block saved in old"
				except Exception as e:
					print bc, e
					wtr.writerow(['block',bc, e])
			
			try:
				block = Block.objects.get(block_name = bn)
				block_added = list(JSLPS_Block.objects.values_list('block_code'))
				block_added = [i[0] for i in block_added]

				if bc not in block_added:
					jb = JSLPS_Block(block_code = bc,
									block_name = bn,
									block = block)
					jb.save()
					print bc, "block saved in new"
			except Exception as e:
				print bc, e

			#village
			village_set = dict(Village.objects.filter(block_id = block.id).values_list('id', 'village_name'))
			if vn not in village_set.values():
				try:
					vil = Village(village_name = vn,
								block = block)
					vil.save()
					print vc, "village saved in old"
				except Exception as e:
					print vc, e
					wtr.writerow(['village',vc, e])

			try:
				village = Village.objects.filter(block_id = block.id).get(village_name = vn)
				'''v_n = JSLPS_Village.objects.get(village_code = vc)
				v_n.Village = village
				v_n.save()
				print vc, "village-foreign key saved in new"'''
				village_added = list(JSLPS_Village.objects.values_list('village_code'))
				village_added = [i[0] for i in village_added]

				if vc not in village_added:
					jv = JSLPS_Village(village_code = vc,
									village_name = vn,
									Village = village)
					jv.save()
					print vc, "village saved in new"
			except Exception as e:
				print vc, e
