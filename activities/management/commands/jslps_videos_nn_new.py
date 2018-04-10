import urllib2
import unicodecsv as csv
from datetime import * 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
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

		partner = Partner.objects.get(id=24)
		csv_file = open('jslps_data_integration_files/videos_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/video.xml')
		root = tree.getroot()
		user_obj = User.objects.get(username="jslps_bot")
		data_list = []
		for c in root.findall('VedioMasterData'):
			vdc = c.find('VideoID').text
			data_list.append(vdc)
			vn = c.find('VideoTitle').text
			vt = int(c.find('VideoType').text)
			if c.find('Category') is not None: 
				cg = int(c.find('Category').text)
			else:
				cg = None
				wtr.writerow(['Can not save video without category',vdc,'title', vn])
				continue
			if c.find('SubCategory') is not None: 
				scg = int(c.find('SubCategory').text)
			else:
				scg = None
				wtr.writerow(['Can not save video without SubCategory',vdc,'title', vn])
				continue
			if c.find('Practice') is not None: 
				vp = int(c.find('Practice').text)
			else:
				vp = None
				wtr.writerow(['Can not save video without Practice',vdc,'title', vn])
				continue
			if c.find('YouTubeID') is not None: 
				yid = c.find('YouTubeID').text
			else:
				yid = ''
			if c.find('ProductionDate') is not None:
				pd = datetime.strptime(c.find('ProductionDate').text, '%d/%m/%Y')
			else:
				pd = None
			if c.find('ApprovalDt') is not None:
				ad = datetime.strptime(c.find('ApprovalDt').text, '%d/%m/%Y')
			else:
				ad = None
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

			try:
				village = JSLPS_Village.objects.get(village_code=vc)
			except Exception as e:
				wtr.writerow(['Can not save video without village',vdc,'title', vn, e])
				continue

			try:
				language = Language.objects.get(id=ln)
			except Exception as e:
				wtr.writerow(['Can not save video without language',vdc,'title', vn, e])
				continue

			try:
				facililator = JSLPS_Animator.objects.get(animator_code=pro_team[0])
			except Exception as e:
				facililator = JSLPS_Animator.objects.get(animator_code = str(4))
			try:
				camera_operator = JSLPS_Animator.objects.get(animator_code = pro_team[1])
			except Exception as e:
				camera_operator = JSLPS_Animator.objects.get(animator_code = str(4))

			try:
				category = Category.objects.get(id = cg)
			except Category.DoesNotExist as e:
				category = None
				wtr.writerow(['Can not save video without category',vdc,'title', vn, e])
				continue

			try:
				subcategory = SubCategory.objects.get(id = scg)
			except SubCategory.DoesNotExist as e:
				subcategory = None
				wtr.writerow(['Can not save video without subcategory',vdc,'title', vn, e])
				continue

			try:
				videopractice = VideoPractice.objects.get(id = vp)
			except VideoPractice.DoesNotExist as e:
				videopractice = None
				wtr.writerow(['Can not save video without practice',vdc,'title', vn, e])
				continue

			try:
				vid, created = \
					Video.objects.get_or_create(title = vn,
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
											   )
				vid.videopractice.add(videopractice)
				jslps.new_count += 1
			except Exception as e:
				vid = None
				if "Duplicate entry" not in str(e):
					jslps.other_error_count += 1
					wtr.writerow(['Video save error', vdc,'title', vn, e])
				else:
					jslps.duplicate_count += 1

			if vid != None:
				vid.production_team.add(facililator.animator)
				vid.save()
				vid.production_team.add(camera_operator.animator)
				vid.save()
				jslps_video_list = JSLPS_Video.objects.filter(vc=vdc, title=vn)
				if jslps_video_list.count() == 0:
					jslps_video, created = \
						JSLPS_Video.objects.get_or_create(title=vn,
														  vc=vdc,
														  video=vid,
														  user_created_id=user_obj.id,
														  activity="LIVELIHOOD")
				else:
					jslps_video_list.update(activity="LIVELIHOOD")
					jslps_video = jslps_video_list[0]
					jslps_video.video = vid
					jslps_video.save()
			else:
				video_list = Video.objects.filter(title = vn, village_id = village.Village.id, language = language, production_date = pd)
				if len(video_list) != 0:	
					vid = video_list[0]
					vid.production_team.add(facililator.animator)
					vid.save()
					vid.production_team.add(camera_operator.animator)
					vid.save()
					jslps_video_list = JSLPS_Video.objects.filter(vc=vdc, title=vn, video=vid)
					if len(jslps_video_list) == 0:
						jslps_video, created = \
						JSLPS_Video.objects.get_or_create(title=vn,
														  vc=vdc,
														  video=vid,
														  user_created_id=user_obj.id,
														  activity="LIVELIHOOD")
					else:
						jslps_video_list.update(activity="LIVELIHOOD")
						jslps_video = jslps_video_list[0]
						if jslps_video.video == None:
							jslps_video.video = vid
							jslps_video.save()
				else:
					wtr.writerow(['Video not saved and duplicate also not exist', vdc,'title', vn, e])		

		JSLPS_Video.objects.filter(vc__in=data_list).update(activity="LIVELIHOOD")

		csv_file.close()

		#saving non-negotiables
		file_url = 'http://webservicesri.swalekha.in/Service.asmx/GetExportVedioNon_NegotiableMasterData'+'?pUsername=%s&pPassword=%s' % (settings.JSLPS_USERNAME, settings.JSLPS_PASSWORD)
		url = urllib2.urlopen(file_url)
		contents = url.read()
		xml_file = open("jslps_data_integration_files/nonnego.xml", 'w')
		xml_file.write(contents)
		xml_file.close()

		csv_file = open('jslps_data_integration_files/nonnego_error.csv', 'wb')
		wtr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
		tree = ET.parse('jslps_data_integration_files/nonnego.xml')
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
			try:
				video = JSLPS_Video.objects.get(vc = vdc)
			except Exception as e:
				wtr.writerow(['Video Not Found',vdc, e])
				continue
			nonnego_already_list = NonNegotiable.objects.filter(video_id = video.video_id,
									non_negotiable__iexact = nn_n)
			if len(nonnego_already_list) == 0:
				try:
					nn, created = \
						NonNegotiable.objects.get_or_create(video_id = video.video_id,
														    non_negotiable = nn_n,
														    physically_verifiable = vr)
					jslps.new_count += 1
				except Exception as e:
					wtr.writerow(['NonNegotiable not saved',nn_c, e])
			else:
				jslps.duplicate_count += 1
				nonnego_already = nonnego_already_list[0]
				nonnego_already.physically_verifiable = vr
				nonnego_already.save()
		
		csv_file.close()


