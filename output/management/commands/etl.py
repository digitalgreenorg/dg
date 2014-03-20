import datetime
import os
import site
import sys
import time

from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min, Count

from people.models import Person
from activities.models import PersonAdoptPractice, PersonMeetingAttendance, Screening
from geographies.models import Village
from videos.models import Video
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
        #Create schema
        ret_val = subprocess.call("mysql -u%s -p%s %s < %s" % (self.db_root_user, self.db_root_pass, 'digitalgreen', os.path.join(DIR_PATH,'create_schema.sql')), shell=True)
        if ret_val != 0:
            raise Exception("Could not recreate schema")
        print "Recreated schema"
        
        #Fill Data
        try:
            #screening_myisam
            self.db_cursor.execute("""INSERT INTO screening_myisam (screening_id, date, video_id, practice_id, group_id,
                                        village_id, block_id, district_id, state_id, country_id)
                                        SELECT sc.id, date, svs.video_id, vid.related_practice_id, persongroups_id, sc.village_id, block_id,
                                        district_id, state_id, country_id
                                        FROM activities_screening sc
                                        JOIN activities_screening_videoes_screened svs on svs.screening_id = sc.id
                                        JOIN activities_screening_farmer_groups_targeted sfgt on sfgt.screening_id = sc.id
                                        JOIN videos_video vid on vid.id = svs.video_id
                                        JOIN geographies_village v on v.id = sc.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id""")
            print "Finished insert into Screening_myisam"
            #video_myisam
            self.db_cursor.execute("""INSERT INTO video_myisam (video_id, video_production_end_date, prod_duration, practice_id, video_type,
                                        language_id, actor_id, gender, actor_type, village_id, block_id, district_id, state_id, country_id)
                                        select vid.id, VIDEO_PRODUCTION_END_DATE, datediff(VIDEO_PRODUCTION_END_DATE, VIDEO_PRODUCTION_START_DATE) + 1,
                                        related_practice_id, VIDEO_TYPE, language_id, person_id, gender, actors, vid.village_id, block_id, district_id,
                                        state_id, country_id
                                        FROM videos_video vid
                                        JOIN videos_video_farmers_shown vfs on vfs.video_id = vid.id
                                        JOIN people_person p on p.id = vfs.person_id
                                        JOIN geographies_village v on v.id = vid.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id
                                        WHERE vid.VIDEO_SUITABLE_FOR = 1""")
            print "Finished insert into Video_myisam"
                                        
            #person_meeting_attendance_myisam
            self.db_cursor.execute("""INSERT INTO person_meeting_attendance_myisam (pma_id, person_id, screening_id, gender, date, 
                                        village_id, block_id, district_id, state_id, country_id)
                                        SELECT pma.id, pma.person_id, sc.id, GENDER, date, p.village_id, block_id,
                                        district_id, state_id, country_id
                                        FROM activities_personmeetingattendance pma 
                                        JOIN activities_screening sc on sc.id = pma.screening_id
                                        JOIN people_person p on p.id = pma.person_id
                                        JOIN geographies_village v on v.id = p.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id""")
            print "Finished insert into person_meeting_attendance_myisam"
                                        
            #person_adopt_practice_myisam
            self.db_cursor.execute("""INSERT INTO person_adopt_practice_myisam (adoption_id, person_id, video_id, gender, date_of_adoption, 
                                        village_id, block_id, district_id, state_id, country_id)
                                        SELECT pap.id, pap.person_id, video_id, GENDER, date_of_adoption, p.village_id, block_id,
                                        district_id, state_id, country_id
                                        FROM activities_personadoptpractice pap 
                                        JOIN people_person p on p.id = pap.person_id
                                        JOIN geographies_village v on v.id = p.village_id
                                        JOIN geographies_block b on b.id = v.block_id
                                        JOIN geographies_district d on d.id = b.district_id
                                        JOIN geographies_state s on s.id = d.state_id""")
            print "Finished insert into person_adopt_practice_myisam"

            # main_data_dst stores all the counts for every date and every village                                        
            main_data_dst = defaultdict(lambda: defaultdict(lambda: dict(tot_sc = 0, tot_vid = 0, tot_male_act = 0,
                tot_fem_act = 0, tot_ado=0, tot_male_ado=0, tot_fem_ado=0, tot_att=0, tot_male_att=0, tot_fem_att=0, 
                tot_exp_att=0, tot_int=0, tot_exp_ado = 0, tot_ques=0, tot_adopted_att=0, tot_active=0, tot_ado_by_act=0,
                tot_active_vid_seen=0)))

            sixty_days = datetime.timedelta(days=60)

            person_village_qs = Person.objects.values_list('id','village')
            person_village = {}
            for id, village in person_village_qs:
                person_village[id] = village

            pmas = PersonMeetingAttendance.objects.values('id', 'person','screening__date', 'person__gender', 'interested', 'expressed_question', 
            'expressed_adoption_video').order_by('person', 'screening__date')
            person_att_dict = defaultdict(list) #Stores the active period of farmers in tuples (from_date, to_date)
            person_video_seen_date_dict = defaultdict(list) # For calculating total videos seen
            max_date = min_date = cur_person = prev_pma_id = None
            for pma in pmas:
                per = pma['person']
                dt = pma['screening__date']
                person_video_seen_date_dict[per].append(dt)
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
                counts = main_data_dst[dt][person_village[per]]
                counts['tot_att'] = counts['tot_att'] + 1
                if pma['person__gender'] == 'M':
                    counts['tot_male_att'] = counts['tot_male_att'] + 1
                else:
                    counts['tot_fem_att'] = counts['tot_fem_att'] + 1
                if pma['interested']:
                    counts['tot_int'] = counts['tot_int'] + 1
                if pma['expressed_question']:
                    counts['tot_ques'] = counts['tot_ques'] + 1
                if pma['expressed_adoption_video']:
                    counts['tot_exp_ado'] = counts['tot_exp_ado'] + 1
                    
            if min_date and max_date and cur_person:
                person_att_dict[cur_person].append((min_date, max_date))
                
            del pmas #Free memory
            print "Finished date calculations"

            
            #Total adoption calculation and gender wise adoption totals    
            paps = PersonAdoptPractice.objects.values_list('person', 'date_of_adoption', 'person__village', 'person__gender').order_by('person', 'date_of_adoption')
            pap_dict = defaultdict(list) #For counting total adoption by active attendees
            for person_id, dt, vil, gender in paps:
                pap_dict[person_id].append(dt)
                main_data_dst[dt][vil]['tot_ado'] = main_data_dst[dt][vil]['tot_ado'] + 1
                if gender=='M':
                    main_data_dst[dt][vil]['tot_male_ado'] = main_data_dst[dt][vil]['tot_male_ado'] + 1
                else:
                    main_data_dst[dt][vil]['tot_fem_ado'] = main_data_dst[dt][vil]['tot_fem_ado'] + 1
            
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
                        counts = main_data_dst[cur_date][person_village[per]]
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
            scs = Screening.objects.annotate(gr_size=Count('farmer_groups_targeted__person')).values_list('date', 'village', 'gr_size')
            for dt, vil, gr_size in scs:
                main_data_dst[dt][vil]['tot_sc'] = main_data_dst[dt][vil]['tot_sc'] + 1
                main_data_dst[dt][vil]['tot_exp_att'] = main_data_dst[dt][vil]['tot_exp_att'] + gr_size
            del scs
                
            vids = Video.objects.filter(video_suitable_for=1).values_list('id','video_production_end_date', 'village', 'farmers_shown__gender').order_by('id')
            cur_id = None
            for id, dt, vil, gender in vids:
                counts = main_data_dst[dt][vil]
                if cur_id is None or cur_id != id:
                    cur_id = id
                    counts['tot_vid'] = counts['tot_vid'] + 1
                if gender == 'M':
                    counts['tot_male_act'] = counts['tot_male_act'] + 1
                else:
                    counts['tot_fem_act'] = counts['tot_fem_act'] + 1
            del vids        
            
            
            vils = Village.objects.values_list('id', 'block', 'block__district' , 'block__district__state', 'block__district__state__country')
            vil_dict = dict()
            for vil in vils:
                vil_dict[vil[0]] = vil

            values_list= []
            for dt, village_dict in main_data_dst.iteritems():
                for vil_id, counts in village_dict.iteritems():
                    values_list.append(("('%s',"+','.join(["%d"] * 23)+ ")" )% 
                    (str(dt),counts['tot_sc'],counts['tot_vid'],counts['tot_male_act'],counts['tot_fem_act'],
                   counts['tot_ado'],counts['tot_male_ado'],counts['tot_fem_ado'],counts['tot_att'],counts['tot_male_att'],
                   counts['tot_fem_att'],counts['tot_exp_att'], counts['tot_exp_ado'],counts['tot_int'],counts['tot_ques'],
                   counts['tot_adopted_att'], counts['tot_active'],counts['tot_ado_by_act'],counts['tot_active_vid_seen'],
                   vil_id,vil_dict[vil_id][1],vil_dict[vil_id][2],vil_dict[vil_id][3],vil_dict[vil_id][4]))
                   
            print "To insert", str(len(values_list)), "rows"
            for i in range(1, (len(values_list)/5000) + 2):
                self.db_cursor.execute("INSERT INTO village_precalculation_copy(date, total_screening, total_videos_produced, total_male_actors,\
                total_female_actors, total_adoption, total_male_adoptions, total_female_adoptions, total_attendance, total_male_attendance,\
                total_female_attendance, total_expected_attendance, total_expressed_adoption, total_interested, total_questions_asked,\
                total_adopted_attendees, total_active_attendees, total_adoption_by_active,total_video_seen_by_active,\
                VILLAGE_ID, BLOCK_ID, DISTRICT_ID, STATE_ID, COUNTRY_ID)\
                VALUES "+','.join(values_list[(i-1)*5000:i*5000]))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        
        print "Total Time = ", time.time() - start_time

class Command(BaseCommand):
    help = '''This command updates statistics displayed on Analytics dashboards.
    arguments: mysql_root_username mysql_root_password
    '''
    
    def handle(self, *args, **options):
        print("Log")
        print(datetime.date.today())
        mysql_root_username = args[0]
        mysql_root_password = args[1]
        an_sync_obj = AnalyticsSync(mysql_root_username, mysql_root_password)
        an_sync_obj.refresh_build()
