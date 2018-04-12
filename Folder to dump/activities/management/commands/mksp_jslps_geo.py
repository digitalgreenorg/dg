import urllib2
import unicodecsv as csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from geographies.models import *
import xml.etree.ElementTree as ET
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):	

		#GEOGRAPHIES ADD
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportMasterDataMKSP'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/mksp_geo.xml", 'w')
		xml_file.write(contents)
		xml_file.close()
		village_data_list = []
		block_data_list = []
		district_data_list = []
		csv_file = open('jslps_data_integration_files/mksp_geo_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/mksp_geo.xml')
		root = tree.getroot()
		state = State.objects.get(id=2)
		user_obj = User.objects.get(username="jslps_bot")
		for c in root.findall('MasterDataMKSP'):
			dc = c.find('DistrictCode').text
			dn = unicode(c.find('DistrictName').text)
			bc = c.find('BlockCode').text
			bn = unicode(c.find('BlockName').text)
			vc = c.find('VillageCode').text
			vn = unicode(c.find('VillageName').text)
			village_data_list.append(vc)
			block_data_list.append(bc)
			district_data_list.append(dc)
			#District
			district_set = dict(District.objects.filter(state_id=2).values_list('id','district_name'))
			if dn not in district_set.values():
				try:
					dist, created = \
						District.objects.get_or_create(district_name = dn,
													   state=state)
					jslps.new_count += 1
					print dc, "District Saved in DG Table"
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
					jd, created = \
						JSLPS_District.objects.get_or_create(district_code = dc,
															 district_name = dn,
										                     district = district,
										                     activity='MKSP',
										                     user_created_id=user_obj.id)
					jd.user_created_id=user_obj.id
					jd.save()
					print dc, "District Saved in JSLPS_District Table"
			except Exception as e:
				print dc, e
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['JSLPS district',dc, e, c])

			#Block
			block_set = dict(Block.objects.filter(district_id = district.id).values_list('id','block_name'))
			if bn not in block_set.values():
				try:
					blck, created = Block.objects.get_or_create(block_name=bn,
																district=district)
					jslps.new_count += 1
					print bc, "block saved in DG table"
				except Exception as e:
					print bc, e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['block',bc, e, c])
			
			try:
				block = Block.objects.get(block_name = bn)
				block_added = JSLPS_Block.objects.values_list('block_code',flat=True)
				#block_added = [i[0] for i in block_added]

				if bc not in block_added:
					jb, created = JSLPS_Block.objects.get_or_create(block_code = bc,
														   block_name = bn,
														   block = block,
														   district_code=dc,
														   activity='MKSP',
														   user_created_id=user_obj.id)
					print bc, "block saved in JSLPS_block table"
			except Exception as e:
				print bc, e
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['JSLPS block',bc, e, c])

			#village
			village_set = dict(Village.objects.filter(block_id = block.id).values_list('id', 'village_name'))
			if vn not in village_set.values():
				try:
					vil, created = Village.objects.get_or_create(village_name = vn,
																 block = block)
					jslps.new_count += 1
					print vc, "village saved in geaography_village table", vil.id
				except Exception as e:
					print vc, e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['village',vc, e, c])

			try:
				village = Village.objects.filter(block_id = block.id).get(village_name = vn)
				village_added = JSLPS_Village.objects.values_list('village_code',flat=True)
				#village_added = [i[0] for i in village_added]

				if vc not in village_added:
					jv, created = JSLPS_Village.objects.get_or_create(village_code = vc,
															 village_name = vn,
															 Village = village,
															 user_created_id=user_obj.id,
															 block_code=bc,
															 activity='MKSP'
															)

					print vc, "village saved in JSLPS_VILLAGE Table"
			except Exception as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['JSLPS village',vc, e, c])

		JSLPS_Village.objects.filter(village_code__in=village_data_list).update(activity="MKSP")
		JSLPS_District.objects.filter(district_code__in=district_data_list).update(activity="MKSP")
		JSLPS_Block.objects.filter(block_code__in=block_data_list).update(activity="MKSP")


