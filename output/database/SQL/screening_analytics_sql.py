from output.database.utility import *

def distinct_attendees(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT PMAM.person_id) as tot_dist_per")
    sql_ds['from'].append("person_meeting_attendance_myisam PMAM")
    sql_ds['force index'].append("(person_meeting_attendance_myisam_village_id)")
    filter_partner_geog_date(sql_ds,"PMAM","PMAM.date",geog,id,from_date,to_date,partners);
    return join_sql_ds(sql_ds);

def average_video_by_active_data(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(['SUM(total_video_seen_by_active) AS tot_vid_by_active ', 
                             'SUM(total_active_attendees) AS tot_active_per'])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['where'].append("date = '%s'" % str(to_date))
    filter_partner_geog_date(sql_ds, "VPC", "DUMMY", geog, id, None, None, partners)
    
    return join_sql_ds(sql_ds);

def screening_attendees_malefemaleratio(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["gender AS pie_key", "COUNT(DISTINCT PMAM.person_id) AS count"]);
    sql_ds['from'].append("person_meeting_attendance_myisam PMAM");
    sql_ds['force index'].append("(person_meeting_attendance_myisam_village_id)");
    filter_partner_geog_date(sql_ds,"PMAM","PMAM.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append('PMAM.gender')
    return join_sql_ds(sql_ds);

def screening_month_bar(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["SUM(total_screening) AS count","MONTH(date) AS MONTH", "YEAR(date) AS YEAR"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append("(village_precalculation_copy_village_id)")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].extend(["YEAR", "MONTH"])
    return join_sql_ds(sql_ds);

def screening_practice_scatter(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["practice_name AS name","sec.name as sec","subsec.name as subsec","top.name as top","subtop.name as subtop","sub.name as sub","COUNT(DISTINCT SCM.screening_id) AS count"]);
    sql_ds['from'].append("screening_myisam SCM")
    sql_ds['force index'].append("(screening_myisam_village_id)")
    sql_ds['join'].append(["PRACTICES P", "P.id = SCM.practice_id"])
    sql_ds['lojoin'].append(["practice_sector sec","sec.id = P.practice_sector_id"])
    sql_ds['lojoin'].append(["practice_subsector subsec","subsec.id = P.practice_subsector_id"])
    sql_ds['lojoin'].append(["practice_topic top","top.id = P.practice_topic_id"])
    sql_ds['lojoin'].append(["practice_subtopic subtop","subtop.id = P.practice_subtopic_id"])
    sql_ds['lojoin'].append(["practice_subject sub","sub.id = P.practice_subject_id"])
    filter_partner_geog_date(sql_ds,"SCM","SCM.date",geog,id,from_date,to_date, partners);
    sql_ds['group by'].append("practice_id")
    return join_sql_ds(sql_ds);

def screening_raw_attendance(geog,id,from_date,to_date,partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["date", "SUM(total_attendance) AS tot_per", "SUM(total_interested) AS tot_int", \
                             "SUM(total_expressed_adoption) as tot_ado", "SUM(total_questions_asked) as tot_que", 
                             "SUM(total_screening) as tot_scr"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append("(village_precalculation_copy_village_id)")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("date")
    sql_ds['order by'].append("date")

    return join_sql_ds(sql_ds);

def screening_percent_attendance(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["date", "SUM(total_attendance) AS tot_per", "SUM(total_interested) AS tot_int", \
                             "SUM(total_expressed_adoption) as tot_ado", "SUM(total_questions_asked) as tot_que", 
                             "SUM(total_expected_attendance) as tot_exp_att"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append("(village_precalculation_copy_village_id)")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("date")
    sql_ds['order by'].append("date")

    return join_sql_ds(sql_ds);

def screening_per_day(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["date", "SUM(total_screening) AS count"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append("(village_precalculation_copy_village_id)")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("date")
    sql_ds['order by'].append("date")

    return join_sql_ds(sql_ds)
