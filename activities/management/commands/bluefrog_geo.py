import urllib2
import json
import requests
import datetime
import unicodecsv as csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from geographies.models import *
import xml.etree.ElementTree as ET
import ap_data_integration as ap


class Command(BaseCommand):
	def handle(self, *args, **options):	

		#GEOGRAPHIES ADD
		req = requests.get('http://45.127.101.204/DG_API/AP_MIS.svc/GetGeographyDetails', auth=(settings.BLUEFROG_API_USERNAME, settings.BLUEFROG_API_PASSWORD))
		xml_file = open("ap/geo.xml", 'w')
		xml_file.write(req.content)
		xml_file.close()

		csv_file = open('ap/geo_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('ap/geo.xml')
		root = tree.getroot()
		data = json.loads(root.text)
		state = State.objects.get(id=6)
		user_obj = User.objects.get(username="apvideo")
		district_data_list = []
		for data_iterable in data:
			district_name = data_iterable.get('District Name')
			district_code = data_iterable.get('District ID')
			village_name = data_iterable.get('Village Name')
			village_code = data_iterable.get('Village ID')
			mandal = data_iterable.get('Mandal Name')
			mandal_code = data_iterable.get('Mandal ID')
			habitation_name = data_iterable.get('Habitation Name')
			habitation_code = data_iterable.get('Habitation ID')
			#District
			district_set = dict(District.objects.filter(state_id=6).values_list('id','district_name'))
			if district_name not in district_set.values():
				try:
					dist, created = \
						District.objects.get_or_create(district_name=district_name,
													   state=state,
													   user_created_id=user_obj.id,
													   start_date=datetime.datetime.now().today())
					ap.new_count += 1
					print district_name, "District Saved in DG District Table"
				except Exception as e:
					print district_name, e
					if "Duplicate entry" in str(e):
						ap.duplicate_count += 1
					else:
						ap.other_error_count += 1
						wtr.writerow(['district',district_name, e])
			try:
				district = District.objects.filter(state_id=6).get(district_name=district_name)
				
				district_obj, created = \
					AP_District.objects.get_or_create(district_name=district_name,
													  district_code=district_code,
									                  district = district,
									                  user_created_id=user_obj.id)
				print district_obj, "District Saved in AP_District Table"
			except Exception as e:
				if "Duplicate entry" not in str(e):
					ap.other_error_count += 1
					wtr.writerow(['AP district',district_name, e])

			#Block
			block_set = dict(Block.objects.filter(district_id=district.id).values_list('id','block_name'))
			if mandal not in block_set.values():
				try:
					blck, created = Block.objects.get_or_create(block_name=mandal,
																district=district)
					ap.new_count += 1
					print blck, "block saved in DG table"
				except Exception as e:
					print mandal, e
					if "Duplicate entry" in str(e):
						ap.duplicate_count += 1
					else:
						ap.other_error_count += 1
						wtr.writerow(['block', e, c])
			
			try:
				block = Block.objects.get(block_name=mandal)
				block_added = AP_Mandal.objects.values_list('mandal_name',flat=True)
				#block_added = [i[0] for i in block_added]
				mandal_obj, created = \
					AP_Mandal.objects.get_or_create(mandal_code=mandal_code,
												    mandal_name=mandal,
												    block=block,
												    ap_district=district_obj,
												    user_created_id=user_obj.id)

				print mandal_obj, "block saved in AP_block table"

			except Exception as e:
				print mandal, e
				if "Duplicate entry" not in str(e):
					ap.other_error_count += 1
					wtr.writerow(['AP block',mandal, e])

			#village
			village_set = dict(Village.objects.filter(block_id = block.id).values_list('id', 'village_name'))
			if village_name not in village_set.values():
				try:
					vil, created = Village.objects.get_or_create(village_name=village_name,
																 block=block)
					ap.new_count += 1
					print vil, "village saved in geaography_village table"
				except Exception as e:
					if "Duplicate entry" in str(e):
						ap.duplicate_count += 1
					else:
						ap.other_error_count += 1
						wtr.writerow(['village',village_name, e])

			try:
				village_q = Village.objects.filter(block_id=block.id).get(village_name=village_name)
				village_added = AP_Village.objects.values_list('village_name',flat=True)
				#village_added = [i[0] for i in village_added]

				village_obj, created = \
					AP_Village.objects.get_or_create(village_code = village_code,
													 village_name = village_name,
													 village = village_q,
													 user_created_id=user_obj.id,
													 ap_mandal=mandal_obj,
													 )

				print village_obj, "village saved in AP_VILLAGE Table"
			except Exception as e:
				if "Duplicate entry" not in str(e):
					ap.other_error_count += 1
					wtr.writerow(['AP village', e])
			# habitation
			try:
				habitation_obj, created = \
					AP_Habitation.objects.get_or_create(habitation_code = village_code,
													    habitation_name = village_name,
													    ap_village = village_obj,
													    user_created_id=user_obj.id,
													    )

				print habitation_obj, "Habitation saved in AP_Habitation Table"
			except Exception as e:
				if "Duplicate entry" not in str(e):
					ap.other_error_count += 1
					wtr.writerow(['AP Habitation', e])
		csv_file.close()



