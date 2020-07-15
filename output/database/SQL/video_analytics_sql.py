from output.database.utility import *

# query constructor for month wise production of videos bar graph.
def video_month_bar(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["COUNT(DISTINCT VIDM.video_id) AS count", "MONTH(VIDM.video_production_date) AS MONTH","YEAR(VIDM.video_production_date) AS YEAR"])
    sql_ds['from'].append("video_myisam VIDM");
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].extend(["YEAR","MONTH"])
    sql_ds['order by'].extend(["YEAR","MONTH"])
    return join_sql_ds(sql_ds)

def video_language_wise_scatter(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["L.language_name as name", "COUNT(DISTINCT video_id) as count"])
    sql_ds['from'].append("videos_language L");
    sql_ds['join'].append(["video_myisam VIDM", "VIDM.language_id = L.id"])
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("language_id")

    return join_sql_ds(sql_ds)

# Query constructor for generating total distinct videos screened.
# arguments (geod, id) and (from_date, to_date) optional
def video_tot_scr(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT svs.video_id) AS count")
    sql_ds['from'].append("activities_screening scr");
    sql_ds['join'].append(["activities_screening_videoes_screened svs","svs.screening_id=scr.id"])
    sql_ds['join'].append(["geographies_village gv","gv.id=scr.village_id"])

    filter_partner_geog_date(sql_ds,'scr','scr.date',geog,id,from_date,to_date,partners)

    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "])
    
    return join_sql_ds(sql_ds)

def video_practice_wise_scatter(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["PRACTICE_NAME as name","sec.name as sec","subsec.name as subsec","top.name as top","subtop.name as subtop","sub.name as sub", "COUNT(DISTINCT VIDM.video_id) as count"])
    sql_ds['from'].append("video_myisam VIDM");
    sql_ds['join'].append(["videos_practice P","VIDM.practice_id = P.id"])
    sql_ds['lojoin'].append(["videos_practicesector sec","sec.id = P.practice_sector_id"])
    sql_ds['lojoin'].append(["videos_practicesubsector subsec","subsec.id = P.practice_subsector_id"])
    sql_ds['lojoin'].append(["videos_practicetopic top","top.id = P.practice_topic_id"])
    sql_ds['lojoin'].append(["videos_practicesubtopic subtop","subtop.id = P.practice_subtopic_id"])
    sql_ds['lojoin'].append(["videos_practicesubject sub","sub.id = P.practice_subject_id"])
    filter_partner_geog_date(sql_ds,'VIDM','VIDM.video_production_date',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("VIDM.practice_id")
    sql_ds['order by'].append("count")
    return join_sql_ds(sql_ds)

#####################################
###  SQLs for VIDEO profile page ####
#####################################


def get_screening_month_bar_for_video(id):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["COUNT( DISTINCT SC.ID ) AS count", "MONTH( SC.DATE ) AS MONTH","YEAR( SC.DATE ) AS YEAR"])
    sql_ds['from'].append("activities_screening_videoes_screened SVS");
    sql_ds['join'].append(["activities_screening SC", "SC.id = SVS.screening_id"])
    sql_ds['where'].append("SVS.video_id = "+str(id))
    sql_ds['group by'].extend(["YEAR","MONTH"])
    sql_ds['order by'].extend(["YEAR","MONTH"])
    return join_sql_ds(sql_ds)

