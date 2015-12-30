import urllib2
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
		xml_file = open("C:\Users\Abhishek\Desktop\group.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		#ADD MEDIATORS - UT(name, gender, district.id)
		tree = ET.parse('C:\Users\Abhishek\Desktop\group.xml')
		root = tree.getroot()

		for c in root.findall('GroupData'):
			gc = c.find('GroupCode').text
			gn = unicode(c.find('Group_Name').text)
			vc = c.find('VillageCode').text
			
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
				group_set = dict(PersonGroup.objects.filter(village_id = village.Village.id).values_list('id','group_name'))
				if gn not in group_set.values():
					gp = PersonGroup(group_name = gn,
									village = village.Village,
									partner = partner
									)
					gp.save()
					print "Group saved in old"
				group = PersonGroup.objects.filter(group_name = gn, village_id = village.Village.id).get()
				group_added = list(JSLPS_Persongroup.objects.values_list('group_id'))
				group_added = [i[0] for i in group_added]
				if group.id not in group_added:
					jg = JSLPS_Persongroup(group_code = gc,
										group = group)
					jg.save()
			except Exception as e:
				print gc, "jslps", e

				
