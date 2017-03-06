import urllib2
import unicodecsv as csv
from django.core.management.base import BaseCommand
from geographies.models import *
import xml.etree.ElementTree as ET
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):	

		#GEOGRAPHIES ADD
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportMasterData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("jslps_data_integration_files/geo.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		csv_file = open('jslps_data_integration_files/geo_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/geo.xml')
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
					jslps.new_count += 1
					print dc, " District saved in old"
				except Exception as e:
					print dc, e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['district',dc, e])
			try:
				district = District.objects.filter(state_id = 2).get(district_name = dn)
				district_added = JSLPS_District.objects.values_list('district_code',flat=True)
				#district_added = [i[0] for i in district_added]
				
				if dc not in district_added:
					jd = JSLPS_District(district_code = dc,
										district_name = dn,
										district = district)
					jd.save()
					print dc, "District Saved in new"
			except Exception as e:
				print dc, e
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['JSLPS district',dc, e])

			#Block
			block_set = dict(Block.objects.filter(district_id = district.id).values_list('id','block_name'))
			if bn not in block_set.values():
				try:
					blck = Block(block_name = bn,
								district = district)
					blck.save()
					jslps.new_count += 1
					print bc, "block saved in old"
				except Exception as e:
					print bc, e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['block',bc, e])
			
			try:
				block = Block.objects.get(block_name = bn)
				block_added = JSLPS_Block.objects.values_list('block_code',flat=True)
				#block_added = [i[0] for i in block_added]

				if bc not in block_added:
					jb = JSLPS_Block(block_code = bc,
									block_name = bn,
									block = block)
					jb.save()
					print bc, "block saved in new"
			except Exception as e:
				print bc, e
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['JSLPS block',bc, e])

			#village
			village_set = dict(Village.objects.filter(block_id = block.id).values_list('id', 'village_name'))
			if vn not in village_set.values():
				try:
					vil = Village(village_name = vn,
								block = block)
					vil.save()
					jslps.new_count += 1
					print vc, "village saved in old"
				except Exception as e:
					print vc, e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['village',vc, e])

			try:
				village = Village.objects.filter(block_id = block.id).get(village_name = vn)
				village_added = JSLPS_Village.objects.values_list('village_code',flat=True)
				#village_added = [i[0] for i in village_added]

				if vc not in village_added:
					jv = JSLPS_Village(village_code = vc,
									village_name = vn,
									Village = village)
					jv.save()
					print vc, "village saved in new"
			except Exception as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['JSLPS village',vc, e])
