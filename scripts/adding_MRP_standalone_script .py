import site, os, sys
from os import path
import csv

proj_path = "/home/ubuntu/code/dg_git/dg"
# proj_path = "C:\Users\Lokesh\Documents\dg_code"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dg.settings")

sys.path.append(proj_path)
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')
# os.chdir(proj_path)

from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from django.core.wsgi import get_wsgi_application
from people.models import *
from programs.models import Partner
from geographies.models import District, Village, Block


application = get_wsgi_application()


# file_path = 'C:\Users\Lokesh\Documents\dg_code\scripts\MRP Database - Master.csv'
# file_path1 = 'C:\Users\Lokesh\Documents\dg_code\scripts\MRP_DATA_error.csv'

file_path = '/home/ubuntu/code/dg_git/dg/scripts/MRP Database - Master.csv'
file_path1 = '/home/ubuntu/code/dg_git/dg/scripts/MRP_DATA_error.csv'

# # ___________________________Setting Header in Error File______________________________

# csvfile1 = open(file_path1, 'w')

# a = csv.writer(csvfile1, delimiter = ',')

# try :
# 	# _______________________Setting Header for Error File______________________________

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
# except Exception as e :
# 	print e

# ________________________________Reading MRP Database___________________________________


with open(file_path, 'rb') as csvfile :
	#csv_reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '|')
	csv_reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '|')

	for row in csv_reader :
		# _______________if No mrp assigned, put it in error file________________________

		if(row['MRP Name'] == ''  or row['MRP Name'] == 'No MRP') :
			pass
			# writer.writerow({'Mrp_name' : row['MRP Name'],
			#  					'Assigned_village_name' : row['Assigned Village Name'],
			#  					'Assigned_village_id' : row['Assigned Village ID'],
			#  					'Block_name' : row['Block Name'],
			#  					'Block_id' : row['Block ID'],
			#  					'District_name' : row['District Name'],
			#  					'District_id' : row['District ID'],
			#  					'gender' : '',
			#  					'Phone_number' : '',
			#  					'Partner_name' : 'BRLPS'
			#  					})
		else :
			# __________________________if MRP found,importing in DB______________________
			try :

				row_data = row
				part = Partner.objects.get(partner_name = row['Partner Name'])
				dist = District.objects.get(district_name = row['District Name'])
				p = Animator(name = row['MRP Name'],
							gender = row['Gender'],
							phone_no = row['Phone Number'],
							partner = part,
							district = dist,
							role = 1
							)
				p.save()

			except Exception as e :
				print e, row['MRP Name']
			# __________________________Inserting Assigned Villages________________________
			try :
				v = Village.objects.filter(village_name = row['Assigned Village Name'], block__block_name = row['Block Name']).get()
				p = Animator.objects.filter(name = row['MRP Name'], district__id = dist.id, role = 1).get()
				try :
					q = AnimatorAssignedVillage(animator = p, village = v)
					q.save()
					print v, 'saved!'
				except Exception as e :
					print e
			except Village.DoesNotExist as e:
				print e
			except Animator.DoesNotExist as e:
				print e, row['MRP Name']