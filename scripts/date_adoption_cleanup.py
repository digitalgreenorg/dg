import os, sys
from os import path
import csv
from django.db.models import F

proj_path = "/home/ubuntu/code/dg_git/dg"
# proj_path = "C:\Users\Server-Tech\Documents\dg_clone"


#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dg.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
from datetime import date, timedelta
from django.db import IntegrityError
# from people.models import *
# from programs.models import Partner
# from geographies.models import District, Village, Block

from activities.models import *

application = get_wsgi_application()

animator = PersonAdoptPractice.objects.filter(date_of_adoption__gt=F('time_created')).values_list('id')
print animator.count()
c = 0
for v in animator :
	try :
		obj = PersonAdoptPractice.objects.filter(id = v[0]).update( date_of_adoption = F('time_created'))
		print 'saved'
	except IntegrityError :
		c += 1
		obj = PersonAdoptPractice.objects.filter(id = v[0]).update( date_of_adoption = (F('time_created') - timedelta(days=c)))
		print 'duplicate changed and saved ! '
print c



# file_path = 'C:\Users\Server-Tech\Documents\dg_clone\scripts/MRP_Database.csv'
# file_path1 = 'C:\Users\Server-Tech\Documents\dg_clone\scripts/mrp_data_2_error.csv'

# file_path = '/home/ubuntu/code/dg_test/scripts/MRP_Database.csv'
# file_path1 = '/home/ubuntu/code/dg_test/scripts/mrp_data_2_error.csv'






# csvfile1 = open(file_path1, 'w')

# a = csv.writer(csvfile1, delimiter = ',')

# try :

# 	fieldnames = ['Mrp_name',
# 				'Assigned_village_name',
# 		 		'Assigned_village_id',
# 		 		'Block_name',
# 		 		'Block_id',
# 		 		'District_name',
# 		 		'District_id',
# 		 		'gender',
# 		 		'Phone_number',
# 		 		'Partner_name'
# 		 		]

# 	writer = csv.DictWriter(csvfile1, fieldnames = fieldnames)
# 	writer.writeheader()
# 	writer.writerow({'Mrp_name' : 'Sujit',
# 	 					'Assigned_village_name' : 'bhatpar rani',
# 	 					'Assigned_village_id' : 12,
# 	 					'Block_name' : 'deoria',
# 	 					'Block_id' : 23,
# 	 					'District_name' : 'Deoria',
# 	 					'District_id' : 32,
# 	 					'gender' : 'M',
# 	 					'Phone_number' : 8960765432,
# 	 					'Partner_name' : 'BRLPS'
# 	 					})
# 	print 'write successfully'
# except Exception as e :
# 	print e, 'bhai'


# with open(file_path, 'rb') as csvfile :
# 	#csv_reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '|')
# 	csv_reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '|')

# for
# 	 row in csv_reader :
# 		#print row['Mrp_name'], row['gender']

# 		if(row['Mrp_name'] == '') :
# 			break

# 		try :

# 			row_data = row
# 			part = Partner.objects.get(partner_name = row['Partner_name'])
# 			dist = District.objects.get(district_name = row['District_name'])
# 			p = Animator(name = row['Mrp_name'],
# 						gender = row['gender'],
# 						phone_no = row['Phone_number'],
# 						partner = part,
# 						district = dist,
# 						role = 1
# 						)
# 			p.save()

# 		except Exception as e :
# 			print e, row['Mrp_name']

# 		try :
# 			v = Village.objects.filter(village_name = row['Assigned_village_name'], block__block_name = row['Block_name']).get()
# 			p = Animator.objects.filter(name = row['Mrp_name'], district__id = dist.id, role = 1).get()

# 			try :
# 				q = AnimatorAssignedVillage(animator = p, village = v)
# 				q.save()
# 				print v, 'saved!'
# 			except Exception as e :
# 				print e
# 		except Village.DoesNotExist as e:
# 			print e
