from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from geographies.models import *
from activities.models import *
import csv

class Command(BaseCommand):

    def handle(self, *args, **options):
        prod = 'default'
        rds = 'user'
        pap_list = []

        '''
        pap_query = Paginator(PersonAdoptPractice.objects.using(rds).all(), 20000)
        print "No. of Pages: ",pap_query.num_pages
        filename = 'activities/management/db_fix.csv'
        count = 0
        return
        for page in range(1, pap_query.num_pages + 1):
            count = 0
            new_pap_in_rds = pap_query.page(page).object_list
            print "No. of Adoption objects in this page: ",len(new_pap_in_rds)
            for pap in new_pap_in_rds:
                print count
                count += 1
                new_pap = PersonAdoptPractice(id=pap.id,
                                              old_coco_id=pap.old_coco_id,
                                              person = pap.person,
                                              video = pap.video,
                                              animator=pap.animator,
                                              date_of_verification= pap.date_of_verification,
                                              verification_status = pap.verification_status,
                                              non_negotiable_check = pap.non_negotiable_check,
                                              verified_by = pap.verified_by,
                                              date_of_adoption = pap.date_of_adoption,
                                              partner = pap.partner,
                                              time_created=pap.time_created,
                                              time_modified=pap.time_modified,
                                              user_created=pap.user_created,
                                              user_modified=pap.user_modified)

                pap_list.append(new_pap)
            try:
                PersonAdoptPractice.objects.using(prod).bulk_create(pap_list)
            except Exception as e:
                print "This is the bad case man :D"
                with open(filename, 'ab') as csvfile:
                    fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                    fileWrite.writerow(['ID (No Screening,No Animator)', row.id])

        #pma1 = PersonMeetingAttendance.objects.using(prod).values_list('id',flat=True)
        #pma2 = PersonMeetingAttendance.objects.using(rds).values_list('id',flat=True)
        #print len(set(pma1)-set(pma2))
        #return
        '''
        pap_in_prod = PersonAdoptPractice.objects.using(prod).values_list('id',flat=True)
        pap_in_rds = PersonAdoptPractice.objects.using(rds).values_list('id',flat=True)
        pap_in_prod =  list(set(pap_in_rds)-set(pap_in_prod))
        pap_query = Paginator(PersonAdoptPractice.objects.using(rds).filter(id__in=pap_in_prod), 20000)
        print "No. of Pages: ",pap_query.num_pages
        filename = 'activities/management/db_fix_pap.csv'
        count = 0
        for page in range(1, pap_query.num_pages + 1):
            count = 0
            new_pap_in_rds = pap_query.page(page).object_list
            print "No. of Adoption objects in this page: ",len(new_pap_in_rds)
            for pap in new_pap_in_rds:
                print count
                count += 1
                new_pap = PersonAdoptPractice(id=pap.id,
                                              old_coco_id=pap.old_coco_id,
                                              person = pap.person,
                                              video = pap.video,
                                              animator=pap.animator,
                                              date_of_verification= pap.date_of_verification,
                                              verification_status = pap.verification_status,
                                              non_negotiable_check = pap.non_negotiable_check,
                                              verified_by = pap.verified_by,
                                              date_of_adoption = pap.date_of_adoption,
                                              partner = pap.partner,
                                              time_created=pap.time_created,
                                              time_modified=pap.time_modified,
                                              user_created=pap.user_created,
                                              user_modified=pap.user_modified)

                pap_list.append(new_pap)
            try:
                PersonAdoptPractice.objects.using(prod).bulk_create(pap_list)
            except Exception as e:
                print "This is the bad case man :D"
                with open(filename, 'ab') as csvfile:
                    fileWrite = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                    fileWrite.writerow(['ID (No Screening,No Animator)',e])
                 
