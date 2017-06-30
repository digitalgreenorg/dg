import os
import csv 
from django.core.management.base import BaseCommand
from django.conf import settings
from openpyxl import load_workbook
from videos.models import *
from people.models import *
from geographies.models import *
from programs.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        upload_file = '/Users/nikhilverma/workspace/DG/dg/data_nsert.csv'
        # path = os.path.abspath(pm_file)
        partner_obj = Partner.objects.get(partner_name="JSNM_HNN")
        partner_id = partner_obj.id
        with open(upload_file, 'rU') as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            for row in reader:
                district_obj = District.objects.get(district_name=row[1])
                block_obj, created = \
                    Block.objects.get_or_create(district_id=district_obj.id,
                                                block_name=row[2])
                print "block", created

                village_obj, created = \
                    Village.objects.get_or_create(village_name=row[3],
                                                  block_id=block_obj.id)
                print "village_obj", created

                person_group_obj, created = \
                    PersonGroup.objects.get_or_create(village_id=village_obj.id,
                                                      group_name=row[4],
                                                      partner_id=partner_id)
                print "person_group_obj", created

                if row[6] == "Female":
                    gender = 'F'
                else:
                    gender = 'M'
                try:
                    mediator_obj, created = \
                        Animator.objects.get_or_create(partner_id=partner_id, name=row[5],
                                                       gender=gender,
                                                       district_id=district_obj.id)
                except:
                    mediator_obj = Animator.objects.filter(partner_id=partner_id, name=row[5],
                                                           gender=gender,
                                                           district_id=district_obj.id)
                    if len(mediator_obj):
                        mediator_obj = mediator_obj.latest('id')

                print "mediator_obj", created
                obj, created = AnimatorAssignedVillage.objects.get_or_create(village_id=village_obj.id, animator=mediator_obj)
                print created, "CREATED"
                # mediator_obj.assigned_villages.add(village_obj)
                # mediator_obj.save()
                # print mediator_obj
                
                if row[9] == "Female":
                    gender = 'F'
                else:
                    gender = 'M'
                person_obj, created = \
                    Person.objects.get_or_create(person_name=row[7],
                                                 father_name=row[8],
                                                 gender=gender,
                                                 village_id=village_obj.id,
                                                 group_id=person_group_obj.id,
                                                 partner_id=partner_id)
                print "person_obj", created
