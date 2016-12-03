from activities.models import PersonAdoptPractice, Screening, PersonMeetingAttendance
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from datetime import datetime
from bulk_update.helper import bulk_update
import unicodecsv as csv
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        print datetime.now()
        pap_query = Paginator(PersonAdoptPractice.objects.filter(animator_id__isnull=True), 20000)
        print pap_query.num_pages
#        filename = 'C:/Users/Lokesh/Documents/dg_code/activities/management/exception.csv'
        filename = '/home/ubuntu/code/dg_git/activities/management/exceptions.csv'
        for page in range(1, pap_query.num_pages + 1):
            count = 0
            adoption_list = pap_query.page(page).object_list
            print len(adoption_list)
            # for page in range(1, pap_query.num_pages + 1):
            # print "----------------------------------------------------------------------------------------------------"
            for row in adoption_list:
#                print row.id #273164
                try:
                    screenings_list = PersonMeetingAttendance.objects.filter(person=row.person).values_list('screening',
                                                                                                            flat=True)
                    try:
                        screening = Screening.objects.filter(
                            date__lte=row.date_of_adoption,
                            id__in=screenings_list, videoes_screened=row.video).order_by('-date')
                        if len(screening) == 0:
                            try:
                                if row.time_created:
                                    screening = Screening.objects.filter(
                                    date__lte=row.time_created.date(),
                                    id__in=screenings_list, videoes_screened=row.video).order_by('-date')
                                if len(screening) == 0 or not row.time_created:
                                    screening = Screening.objects.filter(date__lte=row.time_modified.date(),
                                    id__in=screenings_list, videoes_screened=row.video).order_by('-date')
#                                print "working>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                                screening = screening[0]
#                                print "CC@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                                row.animator = screening.animator
                            except Exception as e:
#                                print "Main Exception" + str(e)
                                with open(filename, 'ab') as csvfile:
                                    fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                                    fileWrite.writerow(['ID', row.id])
                                count += 1
                        else:
                            screening = screening[0]
                            row.animator = screening.animator
                    except Exception as e:
                        count += 1
                        with open(filename, 'ab') as csvfile:
                            fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                            fileWrite.writerow(['HELLO', row.id])
#                        print "Internal Exception" + str(e)
                except Exception as e:
                    count += 1
#                    print "Exception" + str(e)
                    with open(filename, 'ab') as csvfile:
                        fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                        fileWrite.writerow(['THIRD', row.id])
#                    print row.id
            #                    print '##################################################################################################'
            bulk_update(adoption_list)
            print "Done Successful"
            print "Failed : " + str(count)
            print datetime.now()