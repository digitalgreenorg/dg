from coco.base_models import CocoModel
from geographies.models import *
from programs.models import Partner
from people.models import Animator, Person, PersonGroup
from videos.models import Video
from coco.base_models import ADOPTION_VERIFICATION, SCREENING_OBSERVATION, SCREENING_GRADE, VERIFIED_BY
from activities.models import PersonAdoptPractice,Screening, PersonMeetingAttendance
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

class Command(BaseCommand):
    def handle(self,*args,**options):
        pap_query=Paginator(PersonAdoptPractice.objects.filter(animator_id__isnull=True),500)
        print pap_query.num_pages
        for page in range(1, 2):
#        for page in range(1, pap_query.num_pages + 1):
            # print "----------------------------------------------------------------------------------------------------"
            for row in pap_query.page(page).object_list:
                print row.video
                try:
                    screenings_list = PersonMeetingAttendance.objects.filter(person = row.person).values_list('screening', flat=True)
                    screening = Screening.objects.filter(date__lte=row.date_of_adoption, id__in=screenings_list, videoes_screened = row.video ).order_by('-date')[0]
                    print str(screening.animator) + str(screening.date) + str(screening.village)
                    row.animator = screening.animator
                    print str(row.id) + '##' + str(row.person.id) + "##" + str(row.person) + str(row.date_of_adoption)
                    row.save()
                except Exception as e:
                    print "Exception" + str(e)
                    print '##################################################################################################'
