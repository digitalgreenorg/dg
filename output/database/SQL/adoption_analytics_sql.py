from output.database.utility import *


def adoption_tot_ado(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();

    sql_ds['select'].extend(["COUNT(DISTINCT pap.person_id) as tot_farmers", "COUNT(DISTINCT pap.video_id) as tot_prac "])
    sql_ds['from'].append("activities_personadoptpractice pap")
    sql_ds['join'].append(["people_person pp", "pp.id=pap.person_id "])
    sql_ds['join'].append(["geographies_village gv", "gv.id=pp.village_id "])
    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "]) 

    filter_partner_geog_date(sql_ds,'pap','pap.date_of_adoption', geog, id, from_date, to_date, partners)
    
    return join_sql_ds(sql_ds)

def adoption_month_bar(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["SUM(total_adoption) AS count","MONTH(date) AS MONTH", "YEAR(date) AS YEAR"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append("(village_precalculation_copy_village_id)")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].extend([ "YEAR", "MONTH"])
    return join_sql_ds(sql_ds);

def adoption_malefemale_ratio(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["PAPM.gender as pie_key", "COUNT(*) as count"])
    sql_ds['from'].append("person_adopt_practice_myisam PAPM")
    sql_ds['force index'].append("(person_adopt_practice_myisam_village_id)")
    filter_partner_geog_date(sql_ds,'PAPM','PAPM.date_of_adoption',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("PAPM.gender")
    return join_sql_ds(sql_ds);

def adoption_practice_wise_scatter(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["PRACTICE_NAME as name","sec.name as sec","subsec.name as subsec","top.name as top","subtop.name as subtop","sub.name as sub", "COUNT(PAPM.adoption_id) as count"])
    sql_ds['from'].append("person_adopt_practice_myisam PAPM")
    sql_ds['force index'].append("(person_adopt_practice_myisam_village_id)")
    sql_ds['join'].append(["videos_video vid","PAPM.video_id = vid.id"])
    sql_ds['join'].append(["videos_practice PR","vid.related_practice_id = PR.id"])
    sql_ds['lojoin'].append(["videos_practicesector sec","sec.id = PR.practice_sector_id"])
    sql_ds['lojoin'].append(["videos_practicesubsector subsec","subsec.id = PR.practice_subsector_id"])
    sql_ds['lojoin'].append(["videos_practicetopic top","top.id = PR.practice_topic_id"])
    sql_ds['lojoin'].append(["videos_practicesubtopic subtop","subtop.id = PR.practice_subtopic_id"])
    sql_ds['lojoin'].append(["videos_practicesubject sub","sub.id = PR.practice_subject_id"])
    filter_partner_geog_date(sql_ds,'PAPM','PAPM.date_of_adoption',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("PR.id")
    sql_ds['order by'].append("count")
    return join_sql_ds(sql_ds)

# def adoption_repeat_adoption_practice_count(geog, id, from_date, to_date, partners):
#     inner_sql_ds = get_init_sql_ds();
#     inner_sql_ds['select'].append("DISTINCT person_id")
#     inner_sql_ds['from'].append("person_adopt_practice_myisam PAPM")
#     inner_sql_ds['force index'].append("(person_adopt_practice_myisam_village_id)")
#     filter_partner_geog_date(inner_sql_ds,'PAPM','PAPM.date_of_adoption',geog,id,from_date,to_date,partners)
#     inner_sql_ds['group by'].append("PAPM.person_id")
#     inner_sql_ds['group by'].append("PAPM.video_id")
#     inner_sql_ds['having'].append("COUNT(*) > 1")
    
#     sql_ds = get_init_sql_ds();
#     sql_ds['select'].append("COUNT(*) as count")
#     sql_ds['from'].append('(' + join_sql_ds(inner_sql_ds) + ') TAB')
    
#     return join_sql_ds(sql_ds)

def adoption_repeat_adoption_practice_count(geog, id, from_date, to_date, partners):
    inner_sql_ds = get_init_sql_ds();

    inner_sql_ds['select'].append("pap.person_id as person_id")
    inner_sql_ds['from'].append("activities_personadoptpractice pap")
    inner_sql_ds['join'].append(["people_person pp", "pp.id=pap.person_id  "])
    inner_sql_ds['join'].append(["geographies_village gv", "gv.id=pp.village_id "])
    inner_sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    inner_sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    inner_sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    inner_sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "]) 

    
    filter_partner_geog_date(inner_sql_ds,'pap','pap.date_of_adoption',geog,id,from_date,to_date,partners)
    inner_sql_ds['group by'].append("pap.person_id")
    inner_sql_ds['group by'].append("pap.video_id")
    inner_sql_ds['having'].append("COUNT(*) > 1")
    
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT T.person_id) as count")
    sql_ds['from'].append('(' + join_sql_ds(inner_sql_ds) + ')T')
    
    return join_sql_ds(sql_ds)

def adoption_rate_line(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(['date', 'SUM(total_adopted_attendees)', 'SUM(total_active_attendees)'])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append("(village_precalculation_copy_village_id)")
    sql_ds['group by'].append('date')
    sql_ds['order by'].append('date')
    filter_partner_geog_date(sql_ds,'VPC','VPC.date',geog,id,from_date,to_date,partners)
    
    return join_sql_ds(sql_ds)
    