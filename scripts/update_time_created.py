from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from activities.models import PersonAdoptPractice, Screening
from dashboard.models import PersonAdoptPractice as Old_Adoption, Screening as Old_Screening


for adoption in PersonAdoptPractice.objects.exclude(old_coco_id__isnull=True):
    old_adoption = Old_Adoption.objects.get(id=adoption.old_coco_id)
    adoption.time_created = old_adoption.time_created
    adoption.save()

print "Adoption Updated"

for screening in Screening.objects.exclude(old_coco_id__isnull=True):
    old_screening = Old_Screening.objects.get(id=screening.old_coco_id)
    screening.time_created = old_screening.time_created
    screening.save()

print "Screening Updated"
