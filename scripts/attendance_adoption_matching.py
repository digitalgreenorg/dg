import site, sys
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')

from django.core.management import setup_environ
import settings

setup_environ(settings)
from dashboard.models import *

break_flag = False
for p in Person.objects.all():
    ados = p.personadoptpractice_set.order_by('-date_of_adoption').all()
    if not ados:
        continue
    pmas = list(p.personmeetingattendance_set.values_list('id','screening__date','screening__videoes_screened__id', 'matched_adoption'))
    for ado in ados:
        match = False
        for pma in pmas:
            if pma[1] >= ado.date_of_adoption:
                continue
            if ado.video.id == pma[2]:
                pmas.remove(pma)
                match = True
                if pma[3] == None or pma[3] != ado.id:
                    pma = PersonMeetingAttendance.objects.get(id=pma[0])
                    pma.matched_adoption = ado
                    pma.save()
                break
        if not match:
            for pma in pmas:
                if pma[1] < ado.date_of_adoption:
                    break
                if ado.video.id == pma[2]:
                    pmas.remove(pma)
                    match = True
                    if pma[3] == None or pma[3] != ado.id:
                        pma = PersonMeetingAttendance.objects.get(id=pma[0])
                        pma.matched_adoption = ado
                        pma.save()
                    break

