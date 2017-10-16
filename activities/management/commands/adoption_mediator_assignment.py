from activities.models import PersonAdoptPractice, Screening, PersonMeetingAttendance
from people.models import AnimatorAssignedVillage
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from datetime import datetime
from bulk_update.helper import bulk_update
import unicodecsv as csv
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **options):
        animator_villages = AnimatorAssignedVillage.objects.values('village_id','animator_id')
        village_wise_animator = {}
        for entry in animator_villages:
            if entry['village_id'] not in village_wise_animator:
                village_wise_animator[entry['village_id']] = set()
            village_wise_animator[entry['village_id']].add(entry['animator_id'])
        print "Current Time: ",datetime.now()
        pap_query = Paginator(PersonAdoptPractice.objects.filter(animator_id__isnull=True), 20000)
        print "No. of Pages: ",pap_query.num_pages
        #filename = 'C:/Users/Lokesh/Documents/dg_code/activities/management/exception.csv'
        filename = 'activities/management/commands/animator_assign_exceptions.csv'
        count = 0
        for page in range(1, pap_query.num_pages + 1):
            adoption_list = pap_query.page(page).object_list
            print "No. of Adoption objects in this page: ",len(adoption_list)
            person_list = adoption_list.values_list('person_id',flat=True)
            person_list = list(set(person_list))
            pma =  PersonMeetingAttendance.objects.filter(person_id__in=person_list).values('screening_id','person_id')
            person_wise_screening = {}
            for entry in pma:
                if entry['person_id'] not in person_wise_screening:
                    person_wise_screening[entry['person_id']] = set()
                person_wise_screening[entry['person_id']].add(entry['screening_id'])
            for row in adoption_list:
                print count
                count += 1
                try:
                    if row.person.id in person_wise_screening:
                        screenings_list = list(person_wise_screening[row.person.id])
                    else:
                        screenings_list = []
                    try:
                        screening = Screening.objects.filter(date__lte=row.date_of_adoption,id__in=screenings_list, videoes_screened=row.video).order_by('-date')
                        if len(screening) == 0:
                            try:
                                if row.time_created:
                                    screening = Screening.objects.filter(
                                    date__lte=row.time_created.date(),
                                    id__in=screenings_list, videoes_screened=row.video).order_by('-date')
                                if (row.time_modified) and (len(screening) == 0 or not row.time_created):
                                    screening = Screening.objects.filter(date__lte=row.time_modified.date(),
                                    id__in=screenings_list, videoes_screened=row.video).order_by('-date')
                                if len(screening) == 0:
                                    screening = Screening.objects.filter(id__in=screenings_list, videoes_screened=row.video).order_by('-date')
                                if len(screening) == 0:
                                    screening = Screening.objects.filter(id__in=screenings_list).order_by('-date')
                                if len(screening) > 0:
                                    screening = screening[0]
                                    row.animator = screening.animator
                                    continue                 
                                if row.person.village_id in village_wise_animator:
                                    animator_id = Screening.objects.filter(animator_id__in=list(village_wise_animator[row.person.village_id])).order_by('-date')
                                    if len(animator_id) > 0:
                                        animator_id = animator_id[0].animator_id
                                        #animator_id = next(iter(village_wise_animator[row.person.village_id]))
                                        row.animator_id = animator_id 
                                        continue                
                                print "If code is here, then this is the bad case man :D"
                                with open(filename, 'ab') as csvfile:
                                    fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                                    fileWrite.writerow(['ID (No Screening,No Animator)', row.id])
                            except Exception as e:
                                with open(filename, 'ab') as csvfile:
                                    fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                                    fileWrite.writerow(['ID (%s)'%(str(e),), row.id])
                                count += 1
                        else:
                            screening = screening[0]
                            row.animator = screening.animator
                    except Exception as e:
                        # Capture exceptions in csv file
                        count += 1
                        with open(filename, 'ab') as csvfile:
                            fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                            fileWrite.writerow(['HELLO', row.id])
                except Exception as e:
                    count += 1
                    with open(filename, 'ab') as csvfile:
                        fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                        fileWrite.writerow(['THIRD', row.id])
            bulk_update(adoption_list)
            print "Done Successful"
            print "Failed : " + str(count)
            print datetime.now()
