from django.core.management.base import BaseCommand
import os, sys
from os import path
import django
from django.db.models import Count
from django.db import IntegrityError
from activities.models import *
from people.models import *
from raw_data_analytics.utils.data_library import data_lib


class Command(BaseCommand):
    def handle(self,*args,**options):

        # Query to find VRP - Ids whose role is set as 1 instead of 0 : 792

        query1 = '''
                    SELECT 
                        pa.id
                    FROM
                        people_animator pa
                    WHERE
                        pa.id NOT IN (SELECT 
                                pa.id
                            FROM
                                people_animator pa
                                    JOIN
                                (SELECT 
                                    *
                                FROM
                                    people_animator pa
                                WHERE
                                    pa.role = 0
                                GROUP BY pa.name , pa.gender , pa.partner_id , pa.district_id) T ON T.name = pa.name
                                    AND T.gender = pa.gender
                                    AND T.partner_id = pa.partner_id
                                    AND T.district_id = pa.district_id
                                    AND (DATE(pa.time_created) != 20160714
                                    OR pa.district_id NOT IN (114 , 46))
                                    AND pa.role = 1)
                            AND pa.role = 1
                            AND (DATE(pa.time_created) != 20160714
                            OR pa.district_id NOT IN (114 , 46));
                '''

        # Query to find corresponding VRP - Ids and MRP - Ids having similar data [name, gender, partner_id, district_id] and having screening : 89
        query2 = '''
                    SELECT 
                        paa.id,
                        GROUP_CONCAT(DISTINCT paa.id) AS MID_VID
                    FROM
                        people_animator paa
                            JOIN
                        (SELECT 
                            pa.name, pa.gender, pa.PARTNER_ID, pa.district_id
                        FROM
                            people_animator pa
                        JOIN (SELECT 
                            *
                        FROM
                            people_animator pa
                        WHERE
                            pa.role = 0
                        GROUP BY pa.name , pa.gender , pa.partner_id , pa.district_id) T ON T.name = pa.name
                            AND T.gender = pa.gender
                            AND T.partner_id = pa.partner_id
                            AND T.district_id = pa.district_id
                            AND (DATE(pa.time_created) != 20160714
                            OR pa.district_id NOT IN (114 , 46))
                            AND pa.role = 1) U ON paa.name = U.name
                            AND paa.district_id = U.district_id
                            AND paa.partner_id = U.partner_id
                            AND paa.gender = U.gender
                            LEFT JOIN
                        activities_screening scr ON scr.animator_id = paa.id
                    GROUP BY paa.name , paa.gender , paa.PARTNER_ID , paa.district_id
                    HAVING COUNT(scr.id) > 0
                    ;
                '''

        # Query to find corresponding VRP - Ids and MRP - Ids having similar data [name, gender, partner_id, district_id] and having no screening : 89
        query3 = '''
                    SELECT 
                                pa.id
                            FROM
                                people_animator pa
                                    JOIN
                                (SELECT 
                                    *
                                FROM
                                    people_animator pa
                                WHERE
                                    pa.role = 0
                                GROUP BY pa.name , pa.gender , pa.partner_id , pa.district_id) T ON T.name = pa.name
                                    AND T.gender = pa.gender
                                    AND T.partner_id = pa.partner_id
                                    AND T.district_id = pa.district_id
                                    AND (DATE(pa.time_created) != 20160714
                                    OR pa.district_id NOT IN (114 , 46))
                                    AND pa.role = 1
                '''


        # Updating VRPs who have assignment is 1 instead of 0

        data_list_frame1 = data_lib.runQuery(data_lib(), query1)
        print "Actual VRPs with incorrenct assignment of role before Updation"
        print len(data_list_frame1)
        vrp_id_list = data_list_frame1.values.T.tolist()
        for index, row in data_list_frame1.iterrows():
            Animator.objects.filter(id = row['id']).update(role = 0)

        data_list_frame1 = data_lib.runQuery(data_lib(), query1)
        print "Actual VRPs with incorrenct assignment of role after Updation"
        print len(data_list_frame1)



        # Updating Screening data with Old VRPID where VRP entered more than one time with different role i.e. as MRP.

        data_list_frame2 = data_lib.runQuery(data_lib(), query2)
        print "Animators having More than one count with same name, gender, partner, district with different role before"
        print data_list_frame2.count()
        mrp_obj = Animator.objects.filter(role = 1).values_list('id', flat  = True)
        screening_obj = Screening.objects.all()
        print type(screening_obj)
        mrp_list = map(int, list(mrp_obj))

        print mrp_list

        for index, row in data_list_frame2.iterrows():
            
            ids = row['MID_VID'].split(",")
            if (int(ids[0]) not in mrp_list) :
                mrpid = int(ids[1])
                vrpid = int(ids[0])
            else :
                mrpid = int(ids[0])
                vrpid = int(ids[1])
            print str(vrpid) + " -> " + str(mrpid)

            mrp_village_obj = AnimatorAssignedVillage.objects.filter(animator_id = mrpid).values_list('village_id', flat = True)
            vrp_village_obj = AnimatorAssignedVillage.objects.filter(animator_id = vrpid).values_list('village_id', flat = True)
            
            mrp_obj = Animator.objects.filter(id = mrpid).get()
            vrp_obj = Animator.objects.filter(id = vrpid).get()

            # Assigning new villages to the corresponding VRP
            for o in mrp_village_obj:
                if( o not in vrp_village_obj):
                    # add villages
                    
                    vobj = Village.objects.filter(id = o).get()
                    try :
                       q = AnimatorAssignedVillage(animator = vrp_obj, village = vobj)
                       q.save()
                       print 'saved!'
                    except Exception as e :
                       print e

            # Update Screening Data : Replace mrpid to vrpid;
            filtered_screening_obj = Screening.objects.filter(animator_id = mrpid)
            filtered_screening_obj.update(animator_id = vrpid)
            # Deleting Animator with role = 1, which is already in DB as Role = 0
            mrp_obj.delete()
            


        data_list_frame2 = data_lib.runQuery(data_lib(), query2)
        print "Animators having More than one count with same name, gender, partner, district with different role after"
        print data_list_frame2.count()


        data_list_frame3 = data_lib.runQuery(data_lib(), query3)
        print "List of Animators having no screening but having entries as role = 1 and 0 before deleting"
        print len(data_list_frame3)

        for index, row in data_list_frame3.iterrows():
            print 'deleting -> ' + str(row['id'])
            mrpid = int(row['id'])
            mrp_obj = Animator.objects.filter(id = mrpid).get()
            mrp_obj.delete()

        data_list_frame3 = data_lib.runQuery(data_lib(), query3)
        print "List of Animators having no screening but having entries as role = 1 and 0 after deleting"
        print len(data_list_frame3)
