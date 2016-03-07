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
		xml_file = open("/home/ubuntu/code/dg_git/activities/management/group.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		csv_file = open('/home/ubuntu/code/dg_git/activities/management/group_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('/home/ubuntu/code/dg_git/activities/management/group.xml')
		root = tree.getroot()

		for c in root.findall('GroupData'):
			gc = c.find('GroupCode').text
			gn = unicode(c.find('Group_Name').text)
			vc = c.find('VillageCode').text
			
			error = 0
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
				group_set = dict(PersonGroup.objects.filter(village_id = village.Village.id).values_list('id','group_name'))
			except Village.DoesNotExist as e:
				error = 1
				wtr.writerow(['group',vc, e])

			if(error == 0):
				if gn not in group_set.values():
					try:
						gp = PersonGroup(group_name = gn,
									village = village.Village,
									partner = partner)
						gp.save()
						print "Group saved in old"
					except Exception as e:
						wtr.writerow(['group', gc, e])
				try:			
					group = PersonGroup.objects.filter(group_name = gn, village_id = village.Village.id).get()
				except PersonGroup.DoesNotExist as e:
					wtr.writerow(['group', gc, e])

				try:
					group_added = list(JSLPS_Persongroup.objects.values_list('group_code'))
					group_added = [i[0] for i in group_added]
					if gc not in group_added:
						jg = JSLPS_Persongroup(group_code = gc,
											group = group)
						jg.save()
				except Exception as e:
					print gc, e
			
