import site, sys
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')

from django.core.management import setup_environ
import settings

setup_environ(settings)
from django.db.models import Min, Max
from dashboard.models import *
from collections import defaultdict
import datetime

start = datetime.datetime.now()
sixty_days = datetime.timedelta(days=60)

last_calculated_date = VillagePrecalculation.objects.aggregate(Max('date')).values()[0] + datetime.timedelta(days=1)
today = datetime.date.today()
if last_calculated_date > today:
    exit() 
pmas = PersonMeetingAttendance.objects.filter(screening__date__gte = last_calculated_date - sixty_days).values_list('person','screening__date').order_by('person', 'screening__date')
person_att_dict = defaultdict(list)
max_date = min_date = cur_person = None
for per, dt in pmas:
    if cur_person and cur_person == per:
        if dt <= (max_date + datetime.timedelta(days=1)):
            max_date = dt + sixty_days
        else:
            person_att_dict[cur_person].append((min_date, max_date))
            min_date = dt
            max_date = dt + sixty_days
    else:
        if min_date and max_date and cur_person:
            person_att_dict[cur_person].append((min_date, max_date))
        min_date = dt
        max_date = dt + sixty_days
        cur_person = per        

person_village_qs = Person.objects.filter(id__in = person_att_dict.keys()).values_list('id','village')
person_village = {}
for id, village in person_village_qs:
    person_village[id] = village


paps = PersonAdoptPractice.objects.filter(person__in = person_att_dict.keys()).values_list('person', 'date_of_adoption').order_by('person', 'date_of_adoption')
pap_dict = defaultdict(list)
for person_id, date in paps:
    pap_dict[person_id].append(date)
adopting_persons = set(PersonAdoptPractice.objects.filter(person__in = person_att_dict.keys()).values_list('person',flat=True))
main_data_dst = defaultdict(lambda: defaultdict(lambda: [0,0,0]))
for per, date_list in person_att_dict.iteritems():
    has_adopted = per in adopting_persons
    adopt_count = 0
    for min_date, max_date in date_list:
        min_date = max(last_calculated_date, min_date)
        max_date = min(max_date, today)
        for i in range((max_date - min_date).days + 1):
            cur_date = min_date + datetime.timedelta(days=i)
            counts = main_data_dst[cur_date][person_village[per]]
            if has_adopted:
                counts[0] = counts[0] + 1
                while adopt_count < len(pap_dict[per]) and pap_dict[per][adopt_count] <= cur_date:
                    adopt_count = adopt_count + 1
                counts[2] = counts[2] + adopt_count
            counts[1] = counts[1] + 1

village_precalc = VillagePrecalculation.objects.filter(date__gte = min(main_data_dst.keys()))
cur_db_values = defaultdict(dict)
for vp in village_precalc:
    cur_db_values[vp.date][vp.village.id] = vp

for dt, vill_dict in main_data_dst.iteritems():
    for village_id, (adopt_active_att, active_att, active_adopt_count) in vill_dict.iteritems():
        if dt in cur_db_values and village_id in cur_db_values[dt]:
            vp = cur_db_values[dt][village_id]
            if vp.total_adopted_attendees != adopt_active_att or vp.total_active_attendees != active_att:
                vp.total_adopted_attendees = adopt_active_att
                vp.total_active_attendees = active_att
                vp.save()
        else:
            VillagePrecalculation.objects.create(village=Village.objects.get(pk=village_id), date=dt, total_adopted_attendees=adopt_active_att, total_active_attendees=active_att, total_adoption_by_active=active_adopt_count)
