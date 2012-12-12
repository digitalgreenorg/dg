from output.database.utility import *

# query constructor for malefeamle ratio pie chaart
def video_malefemale_ratio(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["gender as pie_key", "COUNT(DISTINCT actor_id) as count"])
    sql_ds['from'].append('video_myisam VIDM')
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_end_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("VIDM.gender")

    return join_sql_ds(sql_ds);

# query constructor for month wise production of videos bar graph.
def video_month_bar(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["COUNT(DISTINCT VIDM.video_id) AS count", "MONTH(VIDM.video_production_end_date) AS MONTH","YEAR(VIDM.video_production_end_date) AS YEAR"])
    sql_ds['from'].append("video_myisam VIDM");
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_end_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].extend(["YEAR","MONTH"])
    sql_ds['order by'].extend(["YEAR","MONTH"])
    return join_sql_ds(sql_ds)

def video_actor_wise_pie(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["actor_type as pie_key", "COUNT(DISTINCT video_id) as count"])
    sql_ds['from'].append("video_myisam VIDM");
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_end_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("actor_type")

    return join_sql_ds(sql_ds)

def video_language_wise_scatter(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["L.language_name as name", "COUNT(DISTINCT video_id) as count"])
    sql_ds['from'].append("LANGUAGE L");
    sql_ds['join'].append(["video_myisam VIDM", "VIDM.language_id = L.id"])
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_end_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("language_id")

    return join_sql_ds(sql_ds)

# Query constructor for generating total distinct videos screened.
#arguments (geod, id) and (from_date, to_date) optional
def video_tot_scr(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT SCM.video_id) AS count")
    sql_ds['from'].append("screening_myisam SCM");
    sql_ds['force index'].append('(screening_myisam_village_id)')
    filter_partner_geog_date(sql_ds,'SCM','SCM.date',geog,id,from_date,to_date,partners)

    return join_sql_ds(sql_ds)

# Query constructor for generating average time taken to produce video
#arguments (geod, id) and (from_date, to_date) optional
def video_prod_duration(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("prod_duration")
    sql_ds['from'].append("video_myisam VIDM");
    sql_ds['group by'].append("video_id")
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_end_date',geog,id,from_date,to_date,partners)

    return join_sql_ds(sql_ds)

def video_type_wise_pie(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["video_type as pie_key", "COUNT(DISTINCT video_id) as count"])
    sql_ds['from'].append("video_myisam VIDM");
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_end_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append('video_type')

    return join_sql_ds(sql_ds)

def video_practice_wise_scatter(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["PRACTICE_NAME as name","sec.name as sec","subsec.name as subsec","top.name as top","subtop.name as subtop","sub.name as sub", "COUNT(DISTINCT VIDM.video_id) as count"])
    sql_ds['from'].append("video_myisam VIDM");
    sql_ds['join'].append(["PRACTICES P","VIDM.practice_id = P.id"])
    sql_ds['lojoin'].append(["practice_sector sec","sec.id = P.practice_sector_id"])
    sql_ds['lojoin'].append(["practice_subsector subsec","subsec.id = P.practice_subsector_id"])
    sql_ds['lojoin'].append(["practice_topic top","top.id = P.practice_topic_id"])
    sql_ds['lojoin'].append(["practice_subtopic subtop","subtop.id = P.practice_subtopic_id"])
    sql_ds['lojoin'].append(["practice_subject sub","sub.id = P.practice_subject_id"])
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_end_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("VIDM.practice_id")
    sql_ds['order by'].append("count")
    return join_sql_ds(sql_ds)

#####################################
###  SQLs for VIDEO profile page ####
#####################################


def get_screening_month_bar_for_video(id):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["COUNT( DISTINCT SC.ID ) AS count", "MONTH( SC.DATE ) AS MONTH","YEAR( SC.DATE ) AS YEAR"])
    sql_ds['from'].append("SCREENING_videoes_screened SVS");
    sql_ds['join'].append(["SCREENING SC", "SC.id = SVS.screening_id"])
    sql_ds['where'].append("SVS.video_id = "+str(id))
    sql_ds['group by'].extend(["YEAR","MONTH"])
    sql_ds['order by'].extend(["YEAR","MONTH"])
    return join_sql_ds(sql_ds)


