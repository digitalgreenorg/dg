import datetime
import os
import site
import sys
import time

from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min, Count
from dg.settings import DATABASES
from pandas import DataFrame

from people.models import Person, Animator, AnimatorAssignedVillage
from activities.models import PersonAdoptPractice, PersonMeetingAttendance, Screening
from geographies.models import Village,Block,District,State,Country
from videos.models import Video
from programs.models import Partner

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

class AnalyticsSync():
    def __init__(self, db_root_user, db_root_pass):
        from django.db import connection
        self.db_cursor = connection.cursor()
        self.db_root_user = db_root_user
        self.db_root_pass = db_root_pass
        self.video_date_changes = None
        self.person_gender_changes = None
        self.screening_date_changes = None

    def _get_flat_query_result(self, query):
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()
        return [i[0] for i in result]
        
    def refresh_build(self):
        start_time = time.time()
        import subprocess
        import MySQLdb
        database = DATABASES['default']['NAME']
        print "Database:", database

        #Create schema
        ret_val = subprocess.call("mysql -u%s -p%s %s < %s" % (self.db_root_user, self.db_root_pass, database, os.path.join(DIR_PATH,'create_schema.sql')), shell=True)
        if ret_val != 0:
            raise Exception("Could not recreate schema")
        print "Recreated schema"
        
        #Fill Data
        try:
            #village_partner_myisam
            self.db_cursor.execute("""INSERT INTO village_partner_myisam (partner_id,village_id,block_id,district_id,state_id,country_id)
                                        SELECT distinct pp.partner_id, gv.id ,gb.id ,gd.id ,gs.id ,gc.id
                                        FROM people_person pp INNER JOIN programs_partner ppa ON pp.partner_id = ppa.id INNER JOIN geographies_village gv ON pp.village_id = gv.id INNER JOIN geographies_block gb on gv.block_id = gb.id INNER JOIN geographies_district gd on gb.district_id=gd.id INNER JOIN geographies_state gs on gd.state_id =  gs.id INNER JOIN geographies_country gc on gs.country_id=gc.id""")
            print "Finished insert into village_partner_myisam"

            #screening_myisam
            self.db_cursor.execute("""INSERT INTO screening_myisam (screening_id, date, video_id, practice_id, group_id,
                                        village_id, block_id, district_id, state_id, country_id, partner_id)
                                        SELECT sc.id, date, svs.video_id, vid.related_practice_id, persongroup_id, sc.village_id, block_id,
                                        district_id, state_id, country_id, sc.partner_id
                                        FROM activities_screening sc
                                        JOIN activities_screening_videoes_screened svs on svs.screening_id = sc.id
                                        JOIN activities_screening_farmer_groups_targeted sfgt on sfgt.screening_id = sc.id
                                        JOIN videos_video vid on vid.id = svs.video_id
                                        JOIN geographies_village v on v.id = sc.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id""")
            print "Finished insert into screening_myisam"
            #video_myisam
            self.db_cursor.execute("""INSERT INTO video_myisam (video_id, video_production_date, practice_id, video_type,
                                        language_id, village_id, block_id, district_id, state_id, country_id, partner_id)
                                        select vid.id, production_date, related_practice_id, video_type, 
                                        language_id, vid.village_id, block_id, district_id,
                                        state_id, country_id, vid.partner_id
                                        FROM videos_video vid
                                        JOIN geographies_village v on v.id = vid.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id
                                        WHERE vid.video_type = 1""")
            print "Finished insert into video_myisam"
                                          
            #person_meeting_attendance_myisam
            self.db_cursor.execute("""INSERT INTO person_meeting_attendance_myisam (pma_id, person_id, screening_id, gender, date, 
                                        village_id, block_id, district_id, state_id, country_id, partner_id)
                                        SELECT pma.id, pma.person_id, sc.id, GENDER, date, sc.village_id, block_id,
                                        district_id, state_id, country_id, sc.partner_id
                                        FROM activities_personmeetingattendance pma 
                                        JOIN activities_screening sc on sc.id = pma.screening_id
                                        JOIN people_person p on p.id = pma.person_id
                                        JOIN geographies_village v on v.id = sc.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id""")
            print "Finished insert into person_meeting_attendance_myisam"
                                          
            #person_adopt_practice_myisam
            self.db_cursor.execute("""INSERT INTO person_adopt_practice_myisam (adoption_id, person_id, video_id, gender, date_of_adoption, 
                                        village_id, block_id, district_id, state_id, country_id, partner_id)
                                        SELECT pap.id, pap.person_id, video_id, GENDER, date_of_adoption, p.village_id, block_id,
                                        district_id, state_id, country_id, pap.partner_id
                                        FROM activities_personadoptpractice pap 
                                        JOIN people_person p on p.id = pap.person_id
                                        JOIN geographies_village v on v.id = p.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id""")
            print "Finished insert into person_adopt_practice_myisam"

            #activities_screeningwisedata
            self.db_cursor.execute("""INSERT INTO activities_screeningwisedata (user_created_id, time_created, user_modified_id, time_modified,
                                        screening_id, old_coco_id, screening_date, start_time, location, village_id, animator_id, 
                                        partner_id, video_id, video_title, persongroup_id,video_youtubeid) 
                                        SELECT  A.user_created_id, A.time_created, A.user_modified_id, A.time_modified,  A.id, 
                                        A.old_coco_id, A.date, A.start_time, A.location, A.village_id, A.animator_id, A.partner_id, B.video_id, D.title, C.PERSONGROUP_ID,D.youtubeid
                                        from activities_screening A join activities_screening_videoes_screened B on B.screening_id=A.id join videos_video D on B.video_id=D.id 
                                        join activities_screening_farmer_groups_targeted C on C.SCREENING_ID = A.id""")
            print "Finished insert into activities_screeningwisedata"

            #people_animatorwisedata
            self.db_cursor.execute("""INSERT INTO people_animatorwisedata (user_created_id, time_created, user_modified_id, time_modified, 
                                        animator_id, old_coco_id, animator_name, gender, phone_no, partner_id, district_id, total_adoptions, 
                                        assignedvillage_id, start_date )
                                        SELECT A.user_created_id, A.time_created, A.user_modified_id, A.time_modified, A.id, A.old_coco_id, A.name,
                                        A.gender, A.phone_no, A.partner_id, A.district_id, A.total_adoptions, B.village_id, B.start_date 
                                        from people_animator A 
                                        join people_animatorassignedvillage B on A.id=B.animator_id""")
            print "Finished insert into people_animatorwisedata"
            
            

            # main_data_dst stores all the counts for every date , every village and every partner                                        
            main_data_dst = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: dict(tot_sc = 0, tot_vid = 0,
                tot_ado=0, tot_male_ado=0, tot_fem_ado=0, tot_att=0, tot_male_att=0, tot_fem_att=0, 
                tot_exp_att=0, tot_ques=0, tot_adopted_att=0, tot_active=0, tot_ado_by_act=0,
                tot_active_vid_seen=0))))
            sixty_days = datetime.timedelta(days=60)
 
            person_village_qs = Person.objects.values_list('id','village','partner')
            person_village = {}
            person_partner ={}
            for id, village, partner in person_village_qs:
                person_village[id] = village
                person_partner[id] = partner
            
            pmas_df = DataFrame.from_records(PersonMeetingAttendance.objects.values('id', 'person','screening__date', 'person__gender', 'screening__questions_asked', 
            'screening__village__id', 'screening__partner__id').order_by('person', 'screening__date').iterator())
            
            person_att_dict = defaultdict(list) #Stores the active period of farmers in tuples (from_date, to_date)
            person_video_seen_date_dict = defaultdict(list) # For calculating total videos seen
            max_date = min_date = cur_person = prev_pma_id = None
            curr_count = 0
            for index, pma in pmas_df.iterrows():
                per = pma['person']
                dt = pma['screening__date']
                person_video_seen_date_dict[per].append(dt)
                curr_count += 1
                #Screening videos is many-to-many. Don't repeat calculation for 2 videos but same attendance
                if prev_pma_id is not None and prev_pma_id == pma['id']:
                    continue
                else:
                    prev_pma_id = pma['id']
                if cur_person and cur_person == per:
                    if dt <= (max_date + datetime.timedelta(days=1)):
                        max_date = dt + sixty_days
                    else:
                        person_att_dict[cur_person].append((min_date, max_date))
                        min_date = dt
                        max_date = dt + sixty_days
                else:
                    if min_date and max_date and cur_person:
                        person_att_dict[cur_person].append((min_date, max_date))
                    min_date = dt
                    max_date = dt + sixty_days
                    cur_person = per
                counts = main_data_dst[dt][pma['screening__village__id']][pma['screening__partner__id']]
                counts['tot_att'] = counts['tot_att'] + 1
                if pma['person__gender'] == 'M':
                    counts['tot_male_att'] = counts['tot_male_att'] + 1
                else:
                    counts['tot_fem_att'] = counts['tot_fem_att'] + 1

            scr = Screening.objects.values('questions_asked')
            for s in scr:
                counts['tot_ques'] = counts['tot_ques'] + 1
                     
            if min_date and max_date and cur_person:
                person_att_dict[cur_person].append((min_date, max_date))
                 
            #del pmas_df
            del pmas_df
            #Free memory
            del scr
            print "Finished date calculations"
 
             
            #Total adoption calculation and gender wise adoption totals    
            paps = PersonAdoptPractice.objects.values_list('person', 'date_of_adoption', 'person__village', 'person__gender', 'partner').order_by('person', 'date_of_adoption')
            pap_dict = defaultdict(list) #For counting total adoption by active attendees
            for person_id, dt, vil, gender, partner in paps:
                pap_dict[person_id].append(dt)
                main_data_dst[dt][vil][partner]['tot_ado'] = main_data_dst[dt][vil][partner]['tot_ado'] + 1
                if gender=='M':
                    main_data_dst[dt][vil][partner]['tot_male_ado'] = main_data_dst[dt][vil][partner]['tot_male_ado'] + 1
                else:
                    main_data_dst[dt][vil][partner]['tot_fem_ado'] = main_data_dst[dt][vil][partner]['tot_fem_ado'] + 1
             
            del paps
            print "Finished adoption counts"
             
            today = datetime.date.today()
            for per, date_list in person_att_dict.iteritems():
                has_adopted = per in pap_dict
                adopt_count = 0
                video_seen_count = 0
                for min_date, max_date in date_list:
                    max_date = min(max_date, today)
                    for i in range((max_date - min_date).days + 1):
                        cur_date = min_date + datetime.timedelta(days=i)
                        counts = main_data_dst[cur_date][person_village[per]][person_partner[per]]
                        if has_adopted:
                            counts['tot_adopted_att'] = counts['tot_adopted_att'] + 1
                            while adopt_count < len(pap_dict[per]) and pap_dict[per][adopt_count] <= cur_date:
                                adopt_count = adopt_count + 1
                            counts['tot_ado_by_act'] = counts['tot_ado_by_act'] + adopt_count
                        while video_seen_count < len(person_video_seen_date_dict[per]) and person_video_seen_date_dict[per][video_seen_count] <= cur_date:
                            video_seen_count = video_seen_count + 1
                        counts['tot_active_vid_seen'] = counts['tot_active_vid_seen'] + video_seen_count
                        counts['tot_active'] = counts['tot_active'] + 1
                     
            del person_att_dict, person_video_seen_date_dict, pap_dict
            print "Finished active attendance counts"
 
            #tot sc calculations
            scs = Screening.objects.annotate(gr_size=Count('farmer_groups_targeted__person')).values_list('date', 'village', 'gr_size', 'partner')
            for dt, vil, gr_size, partner in scs:
                main_data_dst[dt][vil][partner]['tot_sc'] = main_data_dst[dt][vil][partner]['tot_sc'] + 1
                main_data_dst[dt][vil][partner]['tot_exp_att'] = main_data_dst[dt][vil][partner]['tot_exp_att'] + gr_size
            del scs
                 
            vids = Video.objects.filter(video_type=1).values_list('id','production_date', 'village', 'partner').order_by('id')
            cur_id = None
            for id, dt, vil, partner in vids:
                counts = main_data_dst[dt][vil][partner]
                if cur_id is None or cur_id != id:
                    cur_id = id
                    counts['tot_vid'] = counts['tot_vid'] + 1
            del vids
            
            vils = Village.objects.values_list('id', 'block', 'block__district' , 'block__district__state', 'block__district__state__country')
            vil_dict = dict()
            for vil in vils:
                vil_dict[vil[0]] = vil
 
            values_list= []
            for dt, village_dict in main_data_dst.iteritems():
                for vil_id, partner_dict in village_dict.iteritems():
                    for partner_id, counts in partner_dict.iteritems():
                        values_list.append(("('%s',"+','.join(["%d"] * 20)+ ")" )% 
                                           (str(dt), counts['tot_sc'], counts['tot_vid'],
                                            counts['tot_ado'], counts['tot_male_ado'], counts['tot_fem_ado'], counts['tot_att'], counts['tot_male_att'],
                                            counts['tot_fem_att'], counts['tot_exp_att'], counts['tot_ques'],
                                            counts['tot_adopted_att'], counts['tot_active'], counts['tot_ado_by_act'], counts['tot_active_vid_seen'],
                                            vil_id, vil_dict[vil_id][1], vil_dict[vil_id][2], vil_dict[vil_id][3], vil_dict[vil_id][4], partner_id))
                    
            print "To insert", str(len(values_list)), "rows"
            for i in range(1, (len(values_list)/5000) + 2):

                self.db_cursor.execute("INSERT INTO village_precalculation_copy(date, total_screening, total_videos_produced,\
                total_adoption, total_male_adoptions, total_female_adoptions, total_attendance, total_male_attendance,\
                total_female_attendance, total_expected_attendance, total_questions_asked,\
                total_adopted_attendees, total_active_attendees, total_adoption_by_active,total_video_seen_by_active,\
                VILLAGE_ID, BLOCK_ID, DISTRICT_ID, STATE_ID, COUNTRY_ID, partner_id)\
                VALUES "+','.join(values_list[(i-1)*5000:i*5000]))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        
        print "Total Time = ", time.time() - start_time

class Command(BaseCommand):
    help = '''This command updates statistics displayed on Analytics dashboards.
    arguments: mysql_root_username mysql_root_password
    '''
    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')

    def handle(self, *args, **options):
        print("Log")
        print(datetime.date.today())
        mysql_root_username = options['username']
        mysql_root_password = options['password']
        an_sync_obj = AnalyticsSync(mysql_root_username, mysql_root_password)
        an_sync_obj.refresh_build()
