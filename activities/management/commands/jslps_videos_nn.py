import urllib2
import unicodecsv as csv
from datetime import * 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from geographies.models import *
from people.models import *
from programs.models import *
from videos.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		#saving videos
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioMasterData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Server-Tech\Desktop\\video.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		#ADD MEDIATORS - UT(name, gender, district.id)
		csv_file = open('/home/ubuntu/code/dg_test/activities/management/videos_error.csv', 'wb')
		#csv_file = open('C:\Users\Abhishek\Desktop\\videos_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('C:\Users\Server-Tech\Desktop\\video.xml')
		root = tree.getroot()
		for c in root.findall('VedioMasterData'):
			vdc = c.find('VideoID').text
			vn = c.find('VideoTitle').text
			vt = int(c.find('VideoType').text)
			sd = datetime.strptime(c.find('StartDt').text, '%d/%m/%Y')
			ed = datetime.strptime(c.find('EndDt').text, '%d/%m/%Y')
			ln = int(c.find('Video_Language').text)
			if (ln == 2):
				ln = 18
			elif (ln ==3):
				ln =10
			if unicode(c.find('Summary').text) is not None:
				sm = unicode(c.find('Summary').text)
			else:
				sm = ''
			dc = c.find('DistrictCode').text
			bc = c.find('BlockCode').text
			vc = c.find('VillageCode').text
			fc = int(c.find('Facililator').text)
			co = int(c.find('Camera_Operator').text)
			fr = map(int, c.find('MemberIDList').text.split(','))
			act= c.find('Actors').text
			sf = int(c.find('Suitable_For').text)
			
			error = 0
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
				language = Language.objects.get(id = ln)
				facililator = JSLPS_Animator.objects.get(animator_code = fc)
				camera_operator = JSLPS_Animator.objects.get(animator_code = co)
				farmer_list = []
				for i in fr:
					try:
						fr = JSLPS_Person.objects.get(person_code = str(i))
						farmer_list.append(fr.person)
					except JSLPS_Person.DoesNotExist as e:
						fr = JSLPS_Person.objects.get(person_code = str(630))
						farmer_list.append(fr.person)

			except (JSLPS_Village.DoesNotExist, JSLPS_Animator.DoesNotExist, Language.DoesNotExist) as e:
				print e
				wtr(['village',vc,'facililator', ac, 'cameraoperator', co, e])
				error = 1

			if(error == 0):
				video_set = dict(Video.objects.filter(village_id = village.Village.id).values_list('title','village'))
				video_db = []
				video_xml = str(vn)+str(village.Village.id)
				for key, value in video_set.iteritems():
					name = str(key)+str(value)
					video_db.append(name)
				if video_xml not in video_db:
					try:
						vid = Video(title = vn,
									video_type = vt,
									language = language,
									summary = sm,
									video_production_start_date = sd,
									video_production_end_date = ed,
									village = village.Village,
									facilitator = facililator.animator,
									cameraoperator = camera_operator.animator,
									video_suitable_for = sf,
									actors = act,
									partner = partner)
						vid.save()
						print "video saved"
					except Exception as e:
						print vdc, e
						wtr(['video', vdc, e])
					try:
						vid = Video.objects.get(title = vn, village_id=village.Village.id, partner_id=partner.id)
						for i in farmer_list:
							vid.farmers_shown.add(i)
							vid.save()
							print "farmer shown saved"
					except Exception as e:
						wtr(['farmers shown', e])

					try:
						video = Video.objects.filter(title = vn, village_id = village.Village.id).get()
						video_added = list(JSLPS_Video.objects.values_list('vc'))
						video_added = [i[0] for i in video_added]
					except Exception as e:
						print e
					try:	
						if vdc not in video_added:
							vj = JSLPS_Video(vc = vdc,
										video = video)
							vj.save()
					except Exception as e:
						print vdc, e

		#saving non-negotiables
		url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioNon_NegotiableMasterData?pUsername=admin&pPassword=JSLPSSRI')
		contents = url.read()
		xml_file = open("C:\Users\Server-Tech\Desktop\\nn.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		#ADD MEDIATORS - UT(name, gender, district.id)
		tree = ET.parse('C:\Users\Server-Tech\Desktop\\nn.xml')
		root = tree.getroot()

		for c in root.findall('VedioNon_NegotiableMasterData'):
			nn_c = c.find('Non_NegotiablesID').text
			vdc = int(c.find('VideoId').text)
			nn_n = c.find('Non_NegotiablesName').text
			vr = c.find('Verification').text
			if vr == 'false':
				vr = False
			else:
				vr = True
			error = 0
			try:
				video = JSLPS_Video.objects.get(vc = vdc)
			except JSLPS_Video.DoesNotExist as e:
				error = 1
			if (error == 0):
				try:
					nn = NonNegotiable(video = video.video,
									non_negotiable = nn_n,
									physically_verifiable = vr)
					nn.save()
				except Exception as e:
					print e