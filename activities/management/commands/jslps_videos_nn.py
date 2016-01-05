import urllib2
from datetime import * 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from geographies.models import *
from people.models import *
from programs.models import *
from videos.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		upload_video()
		upload_nn()

		def upload_video():
			#read xml from url
			url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioMasterData?pUsername=admin&pPassword=JSLPSSRI')
			contents = url.read()
			xml_file = open("C:\Users\Abhishek\Desktop\\video.xml", 'w')
			xml_file.write(contents)
			xml_file.close()

			partner = Partner.objects.get(id = 24)
			#ADD MEDIATORS - UT(name, gender, district.id)
			tree = ET.parse('C:\Users\Abhishek\Desktop\\video.xml')
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
				sm = unicode(c.find('Summary').text)
				dc = c.find('DistrictCode').text
				bc = c.find('BlockCode').text
				vc = c.find('VillageCode').text
				fc = int(c.find('Facililator').text)
				co = int(c.find('Camera_Operator').text)
				fr = map(int, c.find('MemberIDList').text.split(','))
				act= c.find('Actors').text
				sf = int(c.find('Suitable_For').text)
				if c.find('ApprovalDt') is not None:
					ad = datetime.strptime(c.find('ApprovalDt').text, '%d/%m/%Y')
				else:
					ad = ''
				if c.find('YouTubeID') is not None:
					yt = c.find('YouTubeID').text
				else:
					yt = ''

				error = 0
				try:
					village = JSLPS_Village.objects.get(village_code = vc)
					language = Language.objects.get(id = ln)
					facililator = JSLPS_Animator.objects.get(animator_code = fc)
					camera_operator = JSLPS_Animator.objects.get(animator_code = co)
					farmer_list = []
					for i in fr:
						fr = JSLPS_Person.objects.get(person_code = i)
						farmer_list.append(fr)
				except (JSLPS_Village.DoesNotExist, JSLPS_Animator.DoesNotExist, JSLPS_Person.DoesNotExist, Language.DoesNotExist) as e:
					print e
					error = 1

				if(error == 0):
					video_xml = vn+' '+str(village.Village.id)
					video_set = dict(Video.objects.filter(village_id = village.Village.id).values_list('title','village'))
					video_db = []
					for key, value in video_set.iteritems():
						name = key+ ' ' +str(value)
						video_db.append(name)
					if video_xml not in video_db:
						try:
							vid = Video(title = vn,
										video_type = vt,
										language = language,
										video_production_start_date = sd,
										video_production_end_date = ed,
										village = village,
										facilitator = facililator,
										cameraoperator = camera_operator,
										approval_date = ad,
										video_suitable_for = sf,
										actors = act,
										youtubeid = yt,
										partner = partner)
							vid.save()
						except Exception as e:
							print vdc, e
						try:
							video = Video.objects.filter(title = vn, village = village.Village.id).get()
							video_added = list(JSLPS_Video.objects.values_list('video_code'))
							video_added = [i[0] for i in video_added]
						except Exception as e:
							print e
						if vdc not in video_added:
							try:
								vj = JSLPS_Video(video_code = vdc,
											video = video)
								vj.save()
								vid = JSLPS_Video.objects.get(video_code = vdc)
								for i in farmer_list:
									vid.video.farmers_shown.add(i)
									vid.save()
							except Exception as e:
								print vdc, e

		def upload_nn():
			#read xml from url
			url = urllib2.urlopen('http://webservicesri.swalekha.in/Service.asmx/GetExportVedioNon_NegotiableMasterData?pUsername=admin&pPassword=JSLPSSRI')
			contents = url.read()
			xml_file = open("C:\Users\Abhishek\Desktop\\nn.xml", 'w')
			xml_file.write(contents)
			xml_file.close()

			partner = Partner.objects.get(id = 24)
			#ADD MEDIATORS - UT(name, gender, district.id)
			tree = ET.parse('C:\Users\Abhishek\Desktop\\nn.xml')
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
					video = JSLPS_Video.objects.get(video_code = vdc)
				except Video.DoesNotExist as e:
					error = 1
				if (error == 0):
					try:
						nn = NonNegotiable(video = video.video,
										non_negotiable = nn_n,
										physically_verifiable = vr)
						nn.save()
					except Exception as e:
						print e