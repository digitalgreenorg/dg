import urllib2
import unicodecsv as csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import *
from django.db.models.manager import *
from django.db import models
#from activities.models import *
from geographies.models import *
import xml.etree.ElementTree as ET

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('activities/management/commands/Village_list.csv','rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in list(reader)[1:]:
                state_obj, created = State.objects.get_or_create(state_name=row[4].strip(), country_id=9)
                if state_obj or created:
                    district_obj, created =\
                    District.objects.get_or_create(district_name=row[3].strip(),state_id=state_obj.id)
                    if district_obj or created:
                        block_obj, created=\
                        Block.objects.get_or_create(block_name=row[2].strip(),district_id=district_obj.id)
                        if block_obj or created:
                            Village.objects.get_or_create(village_name=row[1].strip(),block_id=block_obj.id)
