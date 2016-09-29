from activities.models import PersonAdoptPractice,Screening, PersonMeetingAttendance
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from datetime import datetime
from bulk_update.helper import bulk_update

class Command(BaseCommand):
    def handle(self,*args,**options):
        print datetime.now()
        pap_query=Paginator(PersonAdoptPractice.objects.filter(animator_id__isnull=True),5000)
#        print pap_query.num_pages
        for page in range(1, 2):
            count = 0
            print len(pap_query.page(page+11).object_list)
#        for page in range(1, pap_query.num_pages + 1):
            # print "----------------------------------------------------------------------------------------------------"
            for row in pap_query.page(page+10).object_list:
#                print row.video
                try:
                    screenings_list = PersonMeetingAttendance.objects.filter(person = row.person).values_list('screening', flat=True)
                    try:
                        screening = Screening.objects.filter(date__lte=row.date_of_adoption, id__in=screenings_list, videoes_screened = row.video ).order_by('-date')[0]
                    except Exception as e:
                        count+=1
                        print "Internal Exception" + str(e)
#                  print str(screening.animator) + str(screening.date) + str(screening.village)
                    row.animator = screening.animator
#                    print str(row.id) + '##' + str(row.person.id) + "##" + str(row.person) + str(row.date_of_adoption)
#                    row.save()
                except Exception as e:
                    count+=1
                    print "Exception" + str(e)
            bulk_update(pap_query)
#                    print '##################################################################################################'
            print "Done Successful"
            print "Failed : "+str(count)
            print datetime.now()