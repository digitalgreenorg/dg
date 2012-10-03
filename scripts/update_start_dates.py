import site, sys
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')

from django.core.management import setup_environ
import settings

setup_environ(settings)

from django.db.models import Min, F
from dashboard.models import *

#Village Start Dates
vils = Village.objects.annotate(min_sc = Min("screening__date"))
update_blocks = []
for vil in vils:
    if type(vil.start_date) != type(vil.min_sc) or vil.start_date != vil.min_sc:
        vil.start_date = vil.min_sc
        vil.save()
        update_blocks.append(vil.block.id)
        
if not update_blocks:
    exit()

def update_start_date(qs):
    for obj in qs:
        obj.start_date = obj.min_date
        obj.save()

update_start_date(Block.objects.filter(id__in = update_blocks).annotate(min_date = Min("village__start_date")))
update_start_date(District.objects.filter(block__id__in = update_blocks).annotate(min_date = Min("block__start_date")))
update_start_date(State.objects.filter(district__block__id__in = update_blocks).annotate(min_date = Min("district__start_date")))
update_start_date(Country.objects.filter(state__district__block__id__in = update_blocks).annotate(min_date = Min("state__start_date")))
    
