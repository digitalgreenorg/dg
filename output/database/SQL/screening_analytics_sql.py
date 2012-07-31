from output.database.utility import *

def distinct_attendees(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT PMAM.person_id) as tot_dist_per")
    sql_ds['from'].append("person_meeting_attendance_myisam PMAM")
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
    filter_partner_geog_date(sql_ds,"PMAM","PMAM.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append('PMAM.gender')
    return join_sql_ds(sql_ds);

def screening_month_bar(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["SUM(total_screening) AS count","MONTH(date) AS MONTH", "YEAR(date) AS YEAR"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].extend(["YEAR", "MONTH"])
    return join_sql_ds(sql_ds);

def screening_practice_scatter(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["practice_name AS name","COUNT(DISTINCT SCM.screening_id) AS count"]);
    sql_ds['from'].append("screening_myisam SCM")
    sql_ds['join'].append(["PRACTICES P", "P.id = SCM.practice_id"])
    filter_partner_geog_date(sql_ds,"SCM","SCM.date",geog,id,from_date,to_date, partners);
    sql_ds['group by'].append("practice_id")
    return join_sql_ds(sql_ds);

def screening_raw_attendance(geog,id,from_date,to_date,partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["date", "SUM(total_attendance) AS tot_per", "SUM(total_interested) AS tot_int", \
                             "SUM(total_expressed_adoption) as tot_ado", "SUM(total_questions_asked) as tot_que", 
                             "SUM(total_screening) as tot_scr"])
    sql_ds['from'].append("village_precalculation_copy VPC")
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
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("date")
    sql_ds['order by'].append("date")

    return join_sql_ds(sql_ds);

def screening_per_day(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["date", "SUM(total_screening) AS count"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("date")
    sql_ds['order by'].append("date")

    return join_sql_ds(sql_ds)
