import urllib2
import unicodecsv as csv
from datetime import * 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.conf import settings
from geographies.models import *
from people.models import *
from programs.models import *
from videos.models import *
import jslps_data_integration as jslps

class Command(BaseCommand):
	def handle(self, *args, **options):
		#saving videos
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportVedioMasterData'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/video.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		csv_file = open('jslps_data_integration_files/videos_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/video.xml')
		root = tree.getroot()
		for c in root.findall('VedioMasterData'):
			vdc = c.find('VideoID').text
			vn = c.find('VideoTitle').text
			vt = int(c.find('VideoType').text)
			if c.find('Category') is not None: 
				cg = int(c.find('Category').text)
			else:
				cg = None
				jslps.other_error_count += 1
				wtr.writerow(['Can not save video without category',vdc,'title', vn, e])
				continue
			if c.find('SubCategory') is not None: 
				scg = int(c.find('SubCategory').text)
			else:
				scg = None
				jslps.other_error_count += 1
				wtr.writerow(['Can not save video without category',vdc,'title', vn, e])
				continue
			if c.find('Practice') is not None: 
				vp = int(c.find('Practice').text)
			else:
				vp = None
				jslps.other_error_count += 1
				wtr.writerow(['Can not save video without category',vdc,'title', vn, e])
				continue
			if c.find('YouTubeID') is not None: 
				yid = c.find('YouTubeID').text
			else:
				yid = ''
			pd = datetime.strptime(c.find('ProductionDate').text, '%d/%m/%Y')
			if c.find('ApprovalDt') is not None:
				ad = datetime.strptime(c.find('ApprovalDt').text, '%d/%m/%Y')
			else:
				ad = None
			#sd = datetime.strptime(c.find('StartDt').text, '%d/%m/%Y')
			#ed = datetime.strptime(c.find('EndDt').text, '%d/%m/%Y')
			ln = int(c.find('Video_Language').text)
			if (ln == 2):
				ln = 18
			elif (ln ==3):
				ln =10
			if c.find('Benefit') is not None:
				benefit = unicode(c.find('Benefit').text)
			else:
				benefit = ''
			vc = c.find('VillageCode').text
			pro_team = c.find('ProductionTeam').text.split(',')
			
			error = 0
			try:
				village = JSLPS_Village.objects.get(village_code = vc)
				language = Language.objects.get(id = ln)
				try:
					facililator = JSLPS_Animator.objects.get(animator_code = pro_team[0])
				except JSLPS_Animator.DoesNotExist as e:
					facililator = JSLPS_Animator.objects.get(animator_code = str(4))
				try:
					camera_operator = JSLPS_Animator.objects.get(animator_code = pro_team[1])
				except JSLPS_Animator.DoesNotExist as e:
					camera_operator = JSLPS_Animator.objects.get(animator_code = str(4))
				try:
					category = Category.objects.get(id = cg)
				except Category.DoesNotExist as e:
					category = None
					jslps.other_error_count += 1
					wtr.writerow(['Can not save video without category',vdc,'title', vn, e])
					continue
				try:
					subcategory = SubCategory.objects.get(id = scg)
				except SubCategory.DoesNotExist as e:
					subcategory = None
					jslps.other_error_count += 1
					wtr.writerow(['Can not save video without subcategory',vdc,'title', vn, e])
					continue
				try:
					videopractice = VideoPractice.objects.get(id = vp)
				except VideoPractice.DoesNotExist as e:
					videopractice = None
					jslps.other_error_count += 1
					wtr.writerow(['Can not save video without practice',vdc,'title', vn, e])
					continue

			except (JSLPS_Village.DoesNotExist, Language.DoesNotExist) as e:
				print e
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['village',vc,'title', vn, e])
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
									benefit = benefit,
									production_date = pd,
									village_id = village.Village.id,
									partner = partner,
									approval_date=ad,
									youtubeid=yid,
									category=category,
									subcategory=subcategory,
									videopractice=videopractice
									)
						vid.save()
						jslps.new_count += 1
						print "video saved"
					except Exception as e:
						print vdc, e
						if "Duplicate entry" in str(e):
							jslps.duplicate_count += 1
						else:
							jslps.other_error_count += 1
							wtr.writerow(['video save', vdc, e])

					
					try:
						vid = Video.objects.get(title = vn, village_id=village.Village.id, partner_id=partner.id)
						vid.production_team.add(facililator.animator)
						vid.save()
						jslps.new_count += 1
						vid.production_team.add(camera_operator.animator)
						vid.save()
						jslps.new_count += 1
						print "farmer shown saved"
					except Exception as e:
						if "Duplicate entry" in str(e):
							jslps.duplicate_count += 1
						else:
							jslps.other_error_count += 1
							wtr.writerow(['production team save', e])

					video_added = []
					video = None
					try:
						video = Video.objects.filter(title = vn, village_id = village.Village.id, partner_id=partner.id).get()
						video_added = JSLPS_Video.objects.values_list('vc', flat= True)
						#video_added = [i[0] for i in video_added]
					except Exception as e:
						print e
					try:	
						if vdc not in video_added:
							vj = JSLPS_Video(vc = vdc,
										video = video)
							vj.save()
					except Exception as e:
						print vdc, e
						if "Duplicate entry" not in str(e):
							jslps.other_error_count += 1
							wtr.writerow(['JSLPS Video save', vdc, e])

		#saving non-negotiables
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportVedioNon_NegotiableMasterData'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/nn.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		partner = Partner.objects.get(id = 24)
		tree = ET.parse('jslps_data_integration_files/nn.xml')
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
			if error == 0:
				try:
					nonnego_already_exist = NonNegotiable.objects.filter(video_id = video.video_id,
									non_negotiable = nn_n,
									physically_verifiable = vr)
					if len(nonnego_already_exist) == 0:
						nn = NonNegotiable(video_id = video.video_id,
									non_negotiable = nn_n,
									physically_verifiable = vr)
						nn.save()
						jslps.new_count += 1
				except Exception as e:
					print e
					if "Duplicate entry" in str(e):
						jslps.duplicate_count += 1
					else:
						jslps.other_error_count += 1
						wtr.writerow(['Non nego', nn_c,'video',vdc, e])
