from coco.base_models import CocoModel
from geographies.models import *
from programs.models import Partner
from people.models import Animator, Person, PersonGroup
from videos.models import Video
from coco.base_models import ADOPTION_VERIFICATION, SCREENING_OBSERVATION, SCREENING_GRADE, VERIFIED_BY
from activities.models import PersonAdoptPractice,Screening
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self,*args,**options):
        pap_query=PersonAdoptPractice.objects.filter(animator_id__isnull=True)
        print pap_query.count()
        for pap in pap_query:
            print pap['video']
            screening = Screening.objects.filter(date__lte=pap['date_of_adoption'],videoes_screened__contains=pap['video']).order_by('-date')[0]
            print screening['animator']
