import glob, os
from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
from activities.models import *
from coco.models import *
from geographies.models import *
from programs.models import *
from people.models import *
from videos.models import *


partner = Partner.objects.all().values_list('id','date_of_association')

for partner_id,startdate in partner:
    if(startdate == None):
        min_screening_date = Screening.objects.filter(village__block__district__partner = partner_id).aggregate(start=Min('date'))['start']
        Partner.objects.filter(id = partner_id).update(date_of_association = min_screening_date)
        print "Updated start date for " + str(partner_id)
