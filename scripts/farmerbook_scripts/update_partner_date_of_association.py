import glob, os
from django.core.management import setup_environ
import settings
setup_environ(settings)
from dashboard.models import *


partner = Partners.objects.all().values_list('id','date_of_association')

for partner_id,startdate in partner:
    if(startdate == None):
        min_screening_date = Screening.objects.filter(village__block__district__partner = partner_id).aggregate(start=Min('date'))['start']
        Partners.objects.filter(id = partner_id).update(date_of_association = min_screening_date)
        print "Updated start date for " + str(partner_id)
