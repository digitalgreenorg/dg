from output.database.utility import *

def distinct_attendees(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();

    sql_ds["select"].append("COUNT(DISTINCT pma.person_id) as tot_per")
    sql_ds["from"].append("activities_personmeetingattendance pma")
    sql_ds["join"].append(["activities_screening scr", "scr.id=pma.screening_id "])
    sql_ds["join"].append(["people_person pp", "pp.id = pma.person_id "])
    sql_ds["join"].append(["geographies_village gv", "gv.id=pp.village_id "])
    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "])
    par_table = "scr"
    date_field = "scr.date"
    filter_partner_geog_date(sql_ds, par_table, date_field,geog,id,from_date,to_date,partners)
    
    return join_sql_ds(sql_ds);

def average_video_by_active_data(geog, id, from_date, to_date, partners):
    """ This function returns total number of videos seen by unique viewers who are active. 
        We say a person is active if she/he has attended atleast one screening in last 60 days."""
    
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('COUNT(svs.video_id) as tot_vid_by_active')
    sql_ds['from'].append('activities_personmeetingattendance pma ')
    sql_ds['join'].append(["activities_screening scr", "scr.id=pma.screening_id "])
    sql_ds['join'].append(["activities_screening_videoes_screened svs", "svs.screening_id=scr.id "])
    sql_ds['join'].append(["geographies_village gv", "gv.id=scr.village_id "])
    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "]) 
    sql_ds['where'].append("scr.date between date_sub('"+str(to_date)+"', INTERVAL 60 DAY) AND '"+str(to_date)+"'")

    par_table = "pap"
    date_field = "DUMMY"
    filter_partner_geog_date(sql_ds, par_table, date_field, geog, id, None, None, partners)
    
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
    sql_ds['join'].append(["videos_practice P", "P.id = SCM.practice_id"])
    sql_ds['lojoin'].append(["videos_practicesector sec","sec.id = P.practice_sector_id"])
    sql_ds['lojoin'].append(["videos_practicesubsector subsec","subsec.id = P.practice_subsector_id"])
    sql_ds['lojoin'].append(["videos_practicetopic top","top.id = P.practice_topic_id"])
    sql_ds['lojoin'].append(["videos_practicesubtopic subtop","subtop.id = P.practice_subtopic_id"])
    sql_ds['lojoin'].append(["videos_practicesubject sub","sub.id = P.practice_subject_id"])
    filter_partner_geog_date(sql_ds,"SCM","SCM.date",geog,id,from_date,to_date, partners);
    sql_ds['group by'].append("practice_id")
    return join_sql_ds(sql_ds);

def screening_raw_attendance(geog,id,from_date,to_date,partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["date", "SUM(total_attendance) AS tot_per", "SUM(total_questions_asked) as tot_que", 
                             "SUM(total_screening) as tot_scr"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append("(village_precalculation_copy_village_id)")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("date")
    sql_ds['order by'].append("date")

    return join_sql_ds(sql_ds);

def screening_percent_attendance(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["date", "SUM(total_attendance) AS tot_per", "SUM(total_questions_asked) as tot_que", 
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
