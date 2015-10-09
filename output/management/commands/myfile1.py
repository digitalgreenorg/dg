from django.core.management.base import BaseCommand
import datetime
from people.models import *
from activities.models import *
from geographies.models import *
from programs.models import *
from videos.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        person_data = Person.objects.filter(village__block__district__id__in=[26,22])
        count=0
        for i in person_data:
            if i.partner_id==11:
                i.partner_id=6
                i.save()
            #print i.village, i.partner_id
            count+=1
        print count

        group_data = PersonGroup.objects.filter(village__block__district__id__in=[26,22])
        count=0
        for i in group_data:
            if i.partner_id==11:
                i.partner_id=6
                i.save()
            #print i.village, i.partner_id
            count+=1
        print count

        animator_data = Animator.objects.filter(district__id__in=[26,22])
        count=0
        for i in animator_data:
            if i.partner_id==11:
                i.partner_id=6
                i.save()
            #print i.district, i.partner_id
            count+=1
        print count

        adoption_data = PersonAdoptPractice.objects.filter(person__village__block__district__id__in=[26,22])
        count=0
        for i in adoption_data:
            if i.partner_id==11:
                i.partner_id=6
                i.save()
            #print i.id, i.partner_id
            count+=1
        print count

        screening_data = Screening.objects.filter(village__block__district__id__in=[26,22])
        count=0
        for i in screening_data:
            if i.partner_id==11:
                i.partner_id=6
                i.save()
            #print i.village, i.partner_id
            count+=1
        print count

        video_data = Video.objects.filter(village__block__district__id__in=[26,22])
        count=0
        for i in video_data:
            if i.partner_id==11:
                i.partner_id=6
                i.save()
            #print i.village, i.partner_id
            count+=1
        print count