import site, sys
import datetime, time
import argparse
import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))


from django.core.management import setup_environ
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')

import settings
setup_environ(settings)

from django.db.models import Min, Count
from dashboard.models import *
from collections import defaultdict

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
                                        SELECT sc.id, date, svs.video_id, practices_id, persongroups_id, sc.village_id, block_id,
                                        district_id, state_id, country_id
                                        FROM SCREENING sc
                                        JOIN SCREENING_videoes_screened svs on svs.screening_id = sc.id
                                        JOIN SCREENING_farmer_groups_targeted sfgt on sfgt.screening_id = sc.id
                                        JOIN VIDEO_related_agricultural_practices vrap on vrap.video_id = svs.video_id
                                        JOIN VILLAGE v on v.id = sc.village_id
                                        JOIN BLOCK b on b.id = v.block_id
                                        JOIN DISTRICT d on d.id = b.district_id
                                        JOIN STATE s on s.id = d.state_id""")
            print "Finished insert into Screening_myisam"
            #video_myisam
            self.db_cursor.execute("""INSERT INTO video_myisam (video_id, video_production_end_date, prod_duration, practice_id, video_type,
                                        language_id, actor_id, gender, actor_type, village_id, block_id, district_id, state_id, country_id)
                                        select vid.id, VIDEO_PRODUCTION_END_DATE, datediff(VIDEO_PRODUCTION_END_DATE, VIDEO_PRODUCTION_START_DATE) + 1,
                                        practices_id, VIDEO_TYPE, language_id, person_id, gender, actors, vid.village_id, block_id, district_id,
                                        state_id, country_id
                                        FROM VIDEO vid
                                        JOIN VIDEO_farmers_shown vfs on vfs.video_id = vid.id
                                        JOIN PERSON p on p.id = vfs.person_id
                                        JOIN VIDEO_related_agricultural_practices vrap on vrap.video_id = vid.id
                                        JOIN VILLAGE v on v.id = vid.village_id
                                        JOIN BLOCK b on b.id = v.block_id
                                        JOIN DISTRICT d on d.id = b.district_id
                                        JOIN STATE s on s.id = d.state_id
                                        WHERE vid.VIDEO_SUITABLE_FOR = 1""")
            print "Finished insert into Video_myisam"
                                        
            #person_meeting_attendance_myisam
            self.db_cursor.execute("""INSERT INTO person_meeting_attendance_myisam (pma_id, person_id, screening_id, gender, date, 
                                        village_id, block_id, district_id, state_id, country_id)
                                        SELECT pma.id, pma.person_id, sc.id, GENDER, date, p.village_id, block_id,
                                        district_id, state_id, country_id
                                        FROM PERSON_MEETING_ATTENDANCE pma 
                                        JOIN SCREENING sc on sc.id = pma.screening_id
                                        JOIN PERSON p on p.id = pma.person_id
                                        JOIN VILLAGE v on v.id = p.village_id
                                        JOIN BLOCK b on b.id = v.block_id
                                        JOIN DISTRICT d on d.id = b.district_id
                                        JOIN STATE s on s.id = d.state_id""")
            print "Finished insert into person_meeting_attendance_myisam"
                                        
            #person_adopt_practice_myisam
            self.db_cursor.execute("""INSERT INTO person_adopt_practice_myisam (adoption_id, person_id, video_id, practice_id, gender, date_of_adoption, 
                                        village_id, block_id, district_id, state_id, country_id)
                                        SELECT pap.id, pap.person_id, video_id, practice_id, GENDER, date_of_adoption, p.village_id, block_id,
                                        district_id, state_id, country_id
                                        FROM PERSON_ADOPT_PRACTICE pap 
                                        JOIN PERSON p on p.id = pap.person_id
                                        JOIN VILLAGE v on v.id = p.village_id
                                        JOIN BLOCK b on b.id = v.block_id
                                        JOIN DISTRICT d on d.id = b.district_id
                                        JOIN STATE s on s.id = d.state_id""")
            print "Finished insert into person_adopt_practice_myisam"

            # main_data_dst stores all the coutns for every date and every village                                        
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
            'expressed_adoption_video', 'screening__videoes_screened').order_by('person', 'screening__date')
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
                
            del pma #Free memory
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
    
    def _calculate_date_changes(self, sql):
        return_list = []
        self.db_cursor.execute(sql)
        rs = self.db_cursor.fetchall()
        if len(rs) > 0:
            for i in range(1, len(rs)):
                # Delete followed by insert with date changed.
                if rs[i-1][1] == rs[i][1] and rs[i-1][0] == -1 and rs[i][0] == 1 and rs[i-1][2] != rs[i][2]:
                    return_list.append((rs[i][1], rs[i-1][2], rs[i][2]))
        return_list.sort(key=lambda x: x[0])
        # Merge multiple changes for same video/screening
        if len(return_list) > 0:
            i = 1
            while i < len(return_list):
                if return_list[i-1][0] == return_list[i][0] and return_list[i-1][2] == return_list[i][1]:
                    return_list[i-1][2] = return_list[i][2]
                    return_list.pop(i)
                else:
                    i = i + 1
        return return_list
    
    def get_video_date_changes(self):
        if self.video_date_changes is None:
            sql = """SELECT dml_type, ID, VIDEO_PRODUCTION_END_DATE FROM flexviews.digitalgreen_VIDEO"""
            self.video_date_changes = _calculate_date_changes(sql)
        return self.video_date_changes
        
    def get_screening_date_changes(self):
        if self.screening_date_changes is None:
            sql = """SELECT dml_type, ID, DATE FROM flexviews.digitalgreen_SCREENING"""
            self.screening_date_changes = _calculate_date_changes(sql)
        return self.screening_date_changes
                    
    def get_person_gender_changes(self):
        if self.person_gender_changes is not None:
            self.person_gender_changes = []
            self.db_cursor.execute("""SELECT dml_type, ID, gender FROM flexviews.digitalgreen_PERSON""")
            rs = self.db_cursor.fetchall()
            if len(rs) > 0:
                for i in range(1, len(rs)):
                    #delete followed by insert with gender changed.
                    if rs[i-1][1] == rs[i][1] and rs[i-1][0] == -1 and rs[i][0] == 1 and rs[i-1][2] != rs[i][2]:
                        self.person_gender_changes.append((rs[i][1], rs[i-1][2], rs[i][2]))
            self.person_gender_changes.sort(key=lambda x: x[0])
            # Remove gender changed twice (e.g. M->F and F->M)
            if len(return_list) > 0:
                i = 1
                while i < len(return_list):
                    if return_list[i-1][0] == return_list[i][0] and return_list[i-1][2] == return_list[i][1]:
                        return_list.pop(i)
                    else:
                        i = i + 1
        
        return self.person_gender_changes
                
        
    
    def update_screening_myisam(self):
        changed_sc_ids = set(self._get_flat_query_result("SELECT DISTINCT ID FROM flexviews.digitalgreen_SCREENING"))
        changed_sc_ids.udpate(set(self._get_flat_query_result("SELECT DISTINCT SCREENING_ID FROM flexviews.digitalgreen_SCREENING_videoes_screened")))
        changed_sc_ids.udpate(set(self._get_flat_query_result("SELECT DISTINCT SCREENING_ID FROM flexviews.digitalgreen_SCREENING_farmer_groups_targeted")))
        changed_sc_ids.update(set(self._get_flat_query_result("""SELECT DISTINCT screening_id FROM screening_myisam SCM 
                                                                JOIN flexviews.digitalgreen_VIDEO_related_agricultural_practices F_VRAP ON F_VRAP.VIDEO_ID = SCM.video_id""")))
        #Delete all changed from myisam
        id_str = ','.join(map(str, list(changed_sc_ids)))
        self.db_cursor.execute("DELETE FROM screening_myisam where screening_id in (%s)" % (id_str))
        #Refill them up
        self.db_cursor.execute("""INSERT INTO screening_myisam (screening_id, date, video_id, practice_id, group_id,
                                village_id, block_id, district_id, state_id, country_id)
                                SELECT sc.id, date, svs.video_id, practices_id, persongroups_id, sc.village_id, block_id,
                                district_id, state_id, country_id
                                FROM SCREENING sc
                                JOIN SCREENING_videoes_screened svs on svs.screening_id = sc.id
                                JOIN SCREENING_farmer_groups_targeted sfgt on sfgt.screening_id = sc.id
                                JOIN VIDEO_related_agricultural_practices vrap on vrap.video_id = svs.video_id
                                JOIN VILLAGE v on v.id = sc.village_id
                                JOIN BLOCK b on b.id = v.block_id
                                JOIN DISTRICT d on d.id = b.district_id
                                JOIN STATE s on s.id = d.state_id
                                WHERE sc.id in (%s)""" %(id_str))
                                
    def update_video_myisam(self):
        changed_vid_ids = set(self._get_flat_query_results("SELECT DISTINCT ID FROM flexviews.digitalgreen_VIDEO"))
        changed_vid_ids.update(set(self._get_flat_query_results("SELECT DISTINCT VIDEO_ID FROM flexviews.digitalgreen_VIDEO_farmers_shown")))
        changed_vid_ids.update(set(self._get_flat_query_results("SELECT DISTINCT VIDEO_ID FROM flexviews.digitalgreen_VIDEO_related_agricultural_practices")))
        changed_vid_ids.update(set(self._get_flat_query_results("""SELECT DISTINCT video_id FROM video_myisam VIDM
                                                    JOIN flexviews.digitalgreen_PERSON F_P ON VIDM.person_id = F_P.ID""")))
        #Delete all changed from myisam
        id_str = ','.join(map(str, list(changed_vid_ids)))
        self.db_cursor.execute("DELETE FROM video_myisam where video_id in (%s)" % (id_str))
        #Refill them up
        self.db_cursor.execute("""INSERT INTO video_myisam (video_id, video_production_end_date, prod_duration, practice_id, video_type,
                                language_id, actor_id, gender, actor_type, village_id, block_id, district_id, state_id, country_id)
                                select vid.id, VIDEO_PRODUCTION_END_DATE, datediff(VIDEO_PRODUCTION_END_DATE, VIDEO_PRODUCTION_START_DATE) + 1,
                                practices_id, VIDEO_TYPE, language_id, person_id, gender, actors, vid.village_id, block_id, district_id,
                                state_id, country_id
                                FROM VIDEO vid
                                JOIN VIDEO_farmers_shown vfs on vfs.video_id = vid.id
                                JOIN PERSON p on p.id = vfs.person_id
                                JOIN VIDEO_related_agricultural_practices vrap on vrap.video_id = vid.id
                                JOIN VILLAGE v on v.id = vid.village_id
                                JOIN BLOCK b on b.id = v.block_id
                                JOIN DISTRICT d on d.id = b.district_id
                                JOIN STATE s on s.id = d.state_id
                                WHERE vid.id in (%s)""" %(id_str))
        
    def udpate_person_meeting_attendance_myisam(self):
        changed_pma_ids = set(self._get_flat_query_results("SELECT DISTINCT ID FROM flexviews.digitalgreen_PERSON_MEETING_ATTENDANCE"))
        changed_pma_ids.update(set(self._get_flat_query_results("""SELECT DISTINCT pma_id FROM person_meeting_attendance_myisam PMAM
                                                        JOIN flexviews.digitalgreen_SCREENING F_SC ON F_SC.ID = PMAM.screening_id""")))
        changed_pma_ids.update(set(self._get_flat_query_results("""SELECT DISTINCT pma_id FROM person_meeting_attendance_myisam PMAM
                                                        JOIN flexviews.digitalgreen_PERSON F_P ON F_P.ID = PMAM.person_id""")))

        #Delete all changed from myisam
        id_str = ','.join(map(str, list(changed_pma_ids)))
        self.db_cursor.execute("DELETE FROM person_meeting_attendance_myisam where pma_id in (%s)" % (id_str))
        
        #Refill them up
        self.db_cursor.execute("""INSERT INTO person_meeting_attendance_myisam (pma_id, person_id, screening_id, gender, date, 
                                village_id, block_id, district_id, state_id, country_id)
                                SELECT pma.id, pma.person_id, sc.id, GENDER, date, p.village_id, block_id,
                                district_id, state_id, country_id
                                FROM PERSON_MEETING_ATTENDANCE pma 
                                JOIN SCREENING sc on sc.id = pma.screening_id
                                JOIN PERSON p on p.id = pma.person_id
                                JOIN VILLAGE v on v.id = p.village_id
                                JOIN BLOCK b on b.id = v.block_id
                                JOIN DISTRICT d on d.id = b.district_id
                                JOIN STATE s on s.id = d.state_id
                                WHERE pma.id in (%s)""" %(id_str))
        
    def update_person_adopt_practice_myisam(self):
        changed_pap_ids = set(self._get_flat_query_results("SELECT DISTINCT ID FROM flexviews.digitalgreen_PERSON_ADOPT_PRACTICE"))
        changed_pap_ids.update(set(self._get_flat_query_results("""SELECT DISTINCT adoption_id FROM person_adopt_practice_myisam PAPM
                                                        JOIN flexviews.digitalgreen_PERSON F_P ON F_P.ID = PAPM.person_id""")))
        
        #Delete all changed from myisam
        id_str = ','.join(map(str, list(changed_pap_ids)))
        self.db_cursor.execute("DELETE FROM person_adopt_practice_myisam where adoption_id in (%s)" % (id_str))
        
        #Refill them up
        self.db_cursor.execute("""INSERT INTO person_adopt_practice_myisam (adoption_id, person_id, video_id, practice_id, gender, date_of_adoption, 
                                village_id, block_id, district_id, state_id, country_id)
                                SELECT pap.id, pap.person_id, video_id, practice_id, GENDER, date_of_adoption, p.village_id, block_id,
                                district_id, state_id, country_id
                                FROM PERSON_ADOPT_PRACTICE pap 
                                JOIN PERSON p on p.id = pap.person_id
                                JOIN VILLAGE v on v.id = p.village_id
                                JOIN BLOCK b on b.id = v.block_id
                                JOIN DISTRICT d on d.id = b.district_id
                                JOIN STATE s on s.id = d.state_id
                                WHERE pap.id in (%s)""" %(id_str))
                                
    def update_village_precalculation_copy(self):
        changed_vals = defaultdict(lambda: defaultdict(lambda: dict(tot_sc = 0, tot_vid = 0, tot_male_act = 0,
            tot_fem_act = 0, tot_ado=0, tot_male_ado=0, tot_fem_ado=0, tot_att=0, tot_male_att=0, tot_fem_att=0, 
            tot_exp_att=0, tot_int=0, tot_exp_ado = 0, tot_ques=0, tot_adopted_att=0, tot_active=0, tot_ado_by_act=0)))
        
    def calculate_total_screening_change(self, changed_vals):
        # total_screening change
        self.db_cursor.execute("""SELECT dml_type, DATE, VILLAGE_ID, COUNT(*) as COUNT FROM flexviews.digitalgreen_SCREENING F_SC 
                    GROUP BY dml_type, DATE, VILLAGE_ID""")
        for dml_type, date, village_id, count in self.db_cursor.fetchall():
            if dml_type == -1:
                changed_vals[date][village_id]['tot_sc'] = changed_vals[date][village_id]['tot_sc'] - count
            elif dml_type == 1:
                changed_vals[date][village_id]['tot_sc'] = changed_vals[date][village_id]['tot_sc'] + count
        
    def calculate_total_video_change(self, changed_vals):        
        # total_video change
        self.db_cursor.execute("""SELECT dml_type, VIDEO_PRODUCTION_END_DATE, VILLAGE_ID, COUNT(*) as COUNT FROM flexviews.digitalgreen_VIDEO F_VID
                    GROUP BY dml_type, VIDEO_PRODUCTION_END_DATE, VILLAGE_ID""")
        for dml_type, date, village_id, count in self.db_cursor.fetchall():
            if dml_type == -1:
                changed_vals[date][village_id]['tot_vid'] = changed_vals[date][village_id]['tot_vid'] - count
            elif dml_type == 1:
                changed_vals[date][village_id]['tot_vid'] = changed_vals[date][village_id]['tot_vid'] + count
        
    def calculate_total_actor_change(self, changed_vals):
        # Decrement for the all deleted video-actor association considering earlier video dates
        self.db_cursor.execute("""SELECT video_production_end_date, village_id, gender, COUNT(*) as COUNT 
                    FROM flexviews.VIDEO_farmers_shown F_VFS
                    JOIN video_myisam VIDM ON VIDM.video_id = F_VFS.video_id and VIDM.actor_id = F_VFS.actor_id
                    GROUP BY video_production_end_date, village_id, F_VFS.gender
                    WHERE dml_type = -1""")
        
        for date, village_id, gender, count in self.db_cursor.fetchall():
            if gender == 'M':
                key = 'tot_male_act'
            elif gender == 'F':
                key = 'tot_fem_act'
            changed_vals[date][village_id][key] = changed_vals[date][village_id][key] - count
        
        # Increment for the inserts for the new video dates
        self.db_cursor.execute("""SELECT VIDEO_PRODUCTION_END_DATE, VILLAGE_ID, gender, COUNT(*) as COUNT 
                    FROM flexviews.VIDEO_farmers_shown F_VFS
                    JOIN VIDEO VID ON VID.ID = F_VFS.video_id
                    JOIN PERSON P ON P.ID = F_VFS.person_id
                    GROUP BY VIDEO_PRODUCTION_END_DATE, VILLAGE_ID, F_VFS.gender
                    WHERE dml_type = 1""")
        
        for date, village_id, gender, count in self.db_cursor.fetchall():
            if gender == 'M':
                key = 'tot_male_act'
            elif gender == 'F':
                key = 'tot_fem_act'
            changed_vals[date][village_id][key] = changed_vals[date][village_id][key] + count
        
        # Only gender changes
        person_gender_changes = self.get_person_gender_changes()
        self.db_cursor.execute("""SELECT DISTINCT PERSON_ID FROM flexviews.VIDEO_farmers_shown F_VFS""")
        person_accounted = set([i[0] for i in self.db_cursor.fetchall()])
       
        # Fetch the video dates for these actors (one actor can be in multiple videos). Discounting the actors which
        # have been accounted in above.
        final_person_set = set([i[0] for i in person_gender_changes]) - person_accounted 
        self.db_cursor.execute("""SELECT PERSON_ID, VIDEO_PRODUCTION_END_DATE, VID.VILLAGE_ID
                    FROM VIDEO_farmers_shown VFS
                    JOIN VIDEO VID VID.ID = VFS.VIDEO_ID
                    WHERE PERSON_ID IN (%s)""" % (', '.join(map(str, final_person_set))))
        person_date_dict = defaultdict(list)
        for person_id, dt, village_id in self.db_cursor.fetchall():
            person_date_dict[person_id].append((dt, village_id))
        
        for person_id, prev_gender, cur_gender in person_gender_changes:
            if person_id not in final_person_set:
                continue
            for dt, vil_id in person_date_dict[person_id]:
                if prev_gender == 'M':
                    changed_vals[dt][vil_id]['tot_male_act'] = changed_vals[dt][vil_id]['tot_male_act'] - 1
                    changed_vals[dt][vil_id]['tot_fem_act'] = changed_vals[dt][vil_id]['tot_fem_act'] + 1
                elif prev_gender == 'F':
                    changed_vals[dt][vil_id]['tot_fem_act'] = changed_vals[dt][vil_id]['tot_fem_act'] - 1
                    changed_vals[dt][vil_id]['tot_male_act'] = changed_vals[dt][vil_id]['tot_male_act'] + 1
        # Not accounting for date or village change in video. Saving video in COCO/Admin causes reinsertion in VIDEO_farmers_show.
    
       
    #includes gender-wise total_adoption change also - tot_ado, tot_male_ado, tot_fem_ado
    def calculate_total_adoption_change(self, changed_vals):
        # 1. Substract for all deleted adoptions considering previous gender & village
        # 2. Increment for new adoptions considering current person gender & village
        # 3. Discount 1 & 2 and change for the remaining gender & village changes
        self.db_cursor.execute("""SELECT DATE_OF_ADOPTION, VILLAGE_ID, gender, COUNT(*) as COUNT FROM flexviews.digitalgreen_PERSON_ADOPT_PRACTICE F_PAP
                    JOIN person_adopt_practice_myisam PAPM on PAPM.adoption_id = F_PAP.ID
                    WHERE dml_type = -1
                    GROUP BY DATE_OF_ADOPTION, VILLAGE_ID, gender""")
        for dt, vil_id, gender, count in self.db_cursor.fetchall():
            if gender == 'M':
                key = 'tot_male_ado'
            elif gender == 'F':
                key = 'tot_fem_ado'
            changed_vals[dt][vil_id][key] = changed_vals[dt][vil_id][key] - count
            changed_vals[dt][vil_id]['tot_ado'] = changed_vals[dt][vil_id]['tot_ado'] - count
            
        self.db_cursor.execute("""SELECT DATE_OF_ADOPTION, VILLAGE_ID, gender, COUNT(*) as COUNT FROM flexviews.digitalgreen_PERSON_ADOPT_PRACTICE F_PAP
                    JOIN PERSON P on P.ID = F_PAP.person_id
                    WHERE dml_type = 1
                    GROUP BY DATE_OF_ADOPTION, VILLAGE_ID, gender""")
        
        for dt, vil_id, gender, count in self.db_cursor.fetchall():
            if gender == 'M':
                key = 'tot_male_ado'
            elif gender == 'F':
                key = 'tot_fem_ado'
            changed_vals[dt][vil_id][key] = changed_vals[dt][vil_id][key] + count
            changed_vals[dt][vil_id]['tot_ado'] = changed_vals[dt][vil_id]['tot_ado'] + count
        
        self.db_cursor.execute("""SELECT DISTINCT PERSON_ID FROM flexviews.digitalgreen_PERSON_ADOPT_PRACTICE F_PAP""")
        person_accounted = set([i[0] for i in self.db_cursor.fetchall()])
            
        # TODO: Gender change of person - Discount above. Fetch date & village of adoptions and update counts 
        person_gender_changes = self.get_person_gender_changes()
        final_person_set = set([i[0] for i in person_gender_changes]) - person_accounted 
        
        #TODO: Village change of person - Discount above. Fetch gender of Person, date of adoptions and update counts
        
                
    def handle_geography_changes(self):
        pass
    def clean_tables_and_binlogs(self):
        pass
    def run_flexcdc(self):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mysql_root_username", help="MySQL Root User")
    parser.add_argument("mysql_root_password", help="MySQL Root Password")
    parser.add_argument("action", help="Task to run. Currently only referesh. Can include add.",  choices=['refresh_schema'])
    args = parser.parse_args()
    if args.action == "refresh_schema":
        an_sync_obj = AnalyticsSync(args.mysql_root_username, args.mysql_root_password)
        an_sync_obj.refresh_build()