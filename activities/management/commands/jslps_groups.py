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
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportGroupData'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/group.xml", 'w')
		xml_file.write(contents)
		xml_file.close()
		partner = Partner.objects.get(id=24)
		csv_file = open('jslps_data_integration_files/group_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/group.xml')
		root = tree.getroot()
		user_obj = User.objects.get(username="jslps_bot")

		for c in root.findall('GroupData'):
			gc = c.find('GroupCode').text
			gn = unicode(c.find('Group_Name').text)
			vc = c.find('VillageCode').text
			try:
				village = JSLPS_Village.objects.get(village_code=vc)
				group_set = dict(PersonGroup.objects.filter(village_id = village.Village.id).values_list('id','group_name'))
				if gn not in group_set.values():
					try:
						gp, created = PersonGroup.objects.get_or_create(group_name = gn,
															   village = village.Village,
															   partner = partner,
															   user_created_id=user_obj.id)
						jslps.new_count += 1
						print "Group saved in old"
					except Exception as e:
						if "Duplicate entry" in str(e):
							jslps.duplicate_count += 1
						else:
							jslps.other_error_count += 1
							wtr.writerow(['group save', gc, e])
				try:			
					group = \
						PersonGroup.objects.filter(group_name=gn,
												   village_id=village.Village.id).get()
				except PersonGroup.DoesNotExist as e:
					jslps.other_error_count += 1
					wtr.writerow(['group exist', gc, e])

				try:
					group_added = JSLPS_Persongroup.objects.values_list('group_code',flat=True)
					#group_added = [i[0] for i in group_added]
					if gc not in group_added:
						jg, created = JSLPS_Persongroup.objects.get_or_create(group_code = gc,
																	          group = group,
																	          user_created_id=user_obj.id,
																	          activity="LIVELIHOOD")
				except Exception as e:
					print gc, e
					if "Duplicate entry" not in str(e):
						jslps.other_error_count += 1
						wtr.writerow(['JSLPS group', gc, e])
			except village.DoesNotExist as e:
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['village',vc, e])

		csv_file.close()

