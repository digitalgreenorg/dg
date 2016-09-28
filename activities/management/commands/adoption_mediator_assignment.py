from coco.base_models import CocoModel
from geographies.models import *
from programs.models import Partner
from people.models import Animator, Person, PersonGroup
from videos.models import Video
from coco.base_models import ADOPTION_VERIFICATION, SCREENING_OBSERVATION, SCREENING_GRADE, VERIFIED_BY
from activities.models import PersonAdoptPractice,Screening
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

class Command(BaseCommand):
    def handle(self,*args,**options):
        pap_query=Paginator(PersonAdoptPractice.objects.filter(animator_id__isnull=True),1000)
        print pap_query.num_pages
        for page in range(1, pap_query.num_pages + 1):
            # print "----------------------------------------------------------------------------------------------------"
            for row in pap_query.page(page).object_list:
                print row.video
                try:
                    screening = Screening.objects.filter(date__lte=row.date_of_adoption,videoes_screened__in=[row.video]).order_by('-date')[0]
                    print screening.animator
                except Exception as e:
                    print '##################################################################################################'
