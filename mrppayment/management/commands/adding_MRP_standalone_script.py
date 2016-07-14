from activities.models import PersonAdoptPractice
from django.core.management.base import BaseCommand
from people.models import *
import csv
from programs.models import Partner
from geographies.models import District, Village, Block



# file_path = 'C:\Users\Lokesh\Documents\dg_code\scripts\MRP Database - Master.csv'
# file_path1 = 'C:\Users\Lokesh\Documents\dg_code\scripts\MRP_DATA_error.csv'



class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = 'MRP Database - Master.csv'
        file_path1 = 'MRP_DATA_error.csv'
        with open(file_path, 'rb') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')

            for row in csv_reader:
                # _______________if No mrp assigned, put it in error file________________________

                if (row['MRP Name'] == '' or row['MRP Name'] == 'No MRP'):
                    pass
                    # writer.writerow({'Mrp_name' : row['MRP Name'],
                    # 'Assigned_village_name' : row['Assigned Village Name'],
                    #  					'Assigned_village_id' : row['Assigned Village ID'],
                    #  					'Block_name' : row['Block Name'],
                    #  					'Block_id' : row['Block ID'],
                    #  					'District_name' : row['District Name'],
                    #  					'District_id' : row['District ID'],
                    #  					'gender' : '',
                    #  					'Phone_number' : '',
                    #  					'Partner_name' : 'BRLPS'
                    #  					})
                else:
                    # __________________________if MRP found,importing in DB______________________
                    try:

                        row_data = row
                        part = Partner.objects.get(partner_name=row['Partner Name'])
                        dist = District.objects.get(district_name=row['District Name'])
                        p = Animator(name=row['MRP Name'],
                                     gender=row['Gender'],
                                     phone_no=row['Phone Number'],
                                     partner=part,
                                     district=dist,
                                     role=1
                        )
                        p.save()

                    except Exception as e:
                        print e, row['MRP Name']
                    # __________________________Inserting Assigned Villages________________________
                    try:
                        v = Village.objects.filter(village_name=row['Assigned Village Name'],
                                                   block__block_name=row['Block Name']).get()
                        p = Animator.objects.filter(name=row['MRP Name'], district__id=dist.id, role=1).get()
                        try:
                            q = AnimatorAssignedVillage(animator=p, village=v)
                            q.save()
                            print v, 'saved!'
                        except Exception as e:
                            print e
                    except Village.DoesNotExist as e:
                        print e
                    except Animator.DoesNotExist as e:
                        print e, row['MRP Name']
