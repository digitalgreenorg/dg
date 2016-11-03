import urllib2
import unicodecsv as csv
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from geographies.models import *
from people.models import *
from programs.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		#read xml from url
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportGroupData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("jslps_data_integration_files/group.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		csv_file = open('jslps_data_integration_files/group_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/group.xml')
		root = tree.getroot()

		for c in root.findall('GroupData'):
			gc = c.find('GroupCode').text
			gn = unicode(c.find('Group_Name').text)
			vc = c.find('VillageCode').text
		
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
				group_set = dict(PersonGroup.objects.filter(village_id = village.Village.id).values_list('id','group_name'))
				if gn not in group_set.values():
					try:
						gp = PersonGroup(group_name = gn,
									village = village.Village,
									partner = partner)
						gp.save()
						print "Group saved in old"
					except Exception as e:
						wtr.writerow(['group save', gc, e])
				try:			
					group = PersonGroup.objects.filter(group_name = gn, village_id = village.Village.id).get()
				except PersonGroup.DoesNotExist as e:
					wtr.writerow(['group exist', gc, e])

				try:
					group_added = JSLPS_Persongroup.objects.values_list('group_code',flat=True)
					#group_added = [i[0] for i in group_added]
					if gc not in group_added:
						jg = JSLPS_Persongroup(group_code = gc,
											group = group)
						jg.save()
				except Exception as e:
					print gc, e
					wtr.writerow(['JSLPS group', gc, e])
			except Village.DoesNotExist as e:
				wtr.writerow(['village',vc, e])
			
