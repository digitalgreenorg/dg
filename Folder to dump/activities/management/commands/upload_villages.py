import unicodecsv as csv
from django.core.management.base import BaseCommand
from geographies.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		error_file = open('/home/ubuntu/code/dg_git/activities/management/commands/errors.csv', 'wb')
		wrtr = csv.writer(error_file, delimiter=',', quotechar='"')
		csvfile = open('/home/ubuntu/code/dg_git/activities/management/commands/bangladesh_villages.csv', 'rb')
		rows_file = csv.DictReader(csvfile)
		i = 0
		for row in rows_file:
			i = i + 1
			try:
				state = State.objects.get(state_name=unicode(row['StateName']))
				district = District.objects.filter(district_name=unicode(row['DistrictName']))
				
				if(len(district) == 0):
					print 'Add district', unicode(row['DistrictName'])
					district = District(user_created_id=1,
								state = state,
								district_name = unicode(row['DistrictName']).title()
								)
					district.save()
					print 'District Added'
				
				# print 'District is already in database'
				district = District.objects.get(district_name = unicode(row['DistrictName']))
				blocks = list(Block.objects.values_list('block_name'))
				blocks = [unicode(b[0]) for b in blocks]
				if unicode(row['BlockName']).title() not in blocks:
					block = Block(user_created_id=1,
								district = district,
								block_name = unicode(row['BlockName']).title()
								)
					block.save()
					print unicode(row['BlockName']), "##block saved"
			except Exception as e:
				wrtr.writerow([i, "**block-error**", unicode(row['BlockName']), e])
				print e, "**block-error"
			try:
				villages = list(Village.objects.filter(block__block_name = unicode(row['BlockName'])).values_list('village_name'))
				 
				block = Block.objects.get(block_name = unicode(row['BlockName']))
				if unicode(row['VillageName']).title() not in villages:
					village = Village(user_created_id=1,
									block = block,
									village_name = unicode(row['VillageName']).title()
									)
					village.save()
					print unicode(row['VillageName']), "##village saved"
			except Exception as e:
				wrtr.writerow([i, "**village-error**", unicode(row['VillageName']), e])
				print e, "**village-error"
		
		error_file.close()
		csvfile.close()
