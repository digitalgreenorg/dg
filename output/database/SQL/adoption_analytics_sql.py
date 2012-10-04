from output.database.utility import *


def adoption_tot_ado(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT PAP.id) AS tot_ado")
    sql_ds['select'].append("COUNT(DISTINCT person_id) as tot_farmers")
    sql_ds['select'].append("COUNT(DISTINCT video_id) as tot_prac")
    sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP")
    if(geog != "COUNTRY" or partners):
        sql_ds['lojoin'].append(["PERSON P", "P.id = PAP.person_id"]);
        filter_partner_geog_date(sql_ds,'P','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)
    else:
        filter_partner_geog_date(sql_ds,'PAP','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)
        
    return join_sql_ds(sql_ds)

def adoption_month_bar(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["COUNT(*) AS count","MONTH(DATE_OF_ADOPTION) AS MONTH", "YEAR(DATE_OF_ADOPTION) AS YEAR"])
    sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP")
    sql_ds['join'].append(["PERSON P", "P.id = PAP.person_id"])
    filter_partner_geog_date(sql_ds,"P","PAP.DATE_OF_ADOPTION",geog,id,from_date,to_date,partners);
    sql_ds['group by'].extend([ "YEAR", "MONTH"])
    return join_sql_ds(sql_ds);

def adoption_malefemale_ratio(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["P.GENDER as pie_key", "COUNT(*) as count"])
    sql_ds['from'].append('PERSON P')
    sql_ds['join'].append(["PERSON_ADOPT_PRACTICE PAP", "P.id = PAP.person_id"])
    filter_partner_geog_date(sql_ds,'P','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)

    sql_ds['group by'].append("P.GENDER")

    return join_sql_ds(sql_ds);

def adoption_practice_wise_scatter(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["PRACTICE_NAME as name","sec.name as sec","subsec.name as subsec","top.name as top","subtop.name as subtop","sub.name as sub", "COUNT(PAP.id) as count"])
#    sql_ds['select'].extend(["PRACTICE_NAME as name", "COUNT(PAP.id) as count"])
    sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP");
    sql_ds['join'].append(["VIDEO vid","PAP.video_id = vid.id"])
    sql_ds['join'].append(["PRACTICES P","vid.related_practice_id = P.id"])
    ##Change
    sql_ds['lojoin'].append(["practice_sector sec","sec.id = P.practice_sector_id"])
    sql_ds['lojoin'].append(["practice_subsector subsec","subsec.id = P.practice_subsector_id"])
    sql_ds['lojoin'].append(["practice_topic top","top.id = P.practice_topic_id"])
    sql_ds['lojoin'].append(["practice_subtopic subtop","subtop.id = P.practice_subtopic_id"])
    sql_ds['lojoin'].append(["practice_subject sub","sub.id = P.practice_subject_id"])
    sql_ds['join'].append(["PERSON Pe", "Pe.id = PAP.person_id"])
    filter_partner_geog_date(sql_ds,'Pe','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("PRACTICE_NAME")
    sql_ds['order by'].append("count")
    return join_sql_ds(sql_ds)

def adoption_min_date(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("MIN(DATE_OF_ADOPTION) as date")
    sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP");
    if(geog != "COUNTRY" or partners):
        sql_ds['lojoin'].append(["PERSON P", "P.id = PAP.person_id"]);
        filter_partner_geog_date(sql_ds,'P','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)
    else:
        filter_partner_geog_date(sql_ds,'PAP','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds)

def adoption_repeat_adoption_practice_count(geog, id, from_date, to_date, partners):
    inner_sql_ds = get_init_sql_ds();
    inner_sql_ds['select'].append("DISTINCT person_id")
    inner_sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP")
    if(geog != "COUNTRY" or partners):
        inner_sql_ds['lojoin'].append(["PERSON P", "P.id = PAP.person_id"]);
        filter_partner_geog_date(inner_sql_ds,'P','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)
    else:
        filter_partner_geog_date(inner_sql_ds,'PAP','PAP.DATE_OF_ADOPTION',geog,id,from_date,to_date,partners)
        
    inner_sql_ds['group by'].append("PAP.person_id")
    inner_sql_ds['group by'].append("video_id")
    inner_sql_ds['having'].append("COUNT(*) > 1")
    
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(*) as count")
    sql_ds['from'].append('(' + join_sql_ds(inner_sql_ds) + ') TAB')
    
    return join_sql_ds(sql_ds)

def adoption_rate_line(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(['date', 'SUM(total_adopted_attendees)', 'SUM(total_active_attendees)'])
    sql_ds['from'].append("village_precalculation VP")
    sql_ds['group by'].append('date')
    sql_ds['order by'].append('date')
    filter_partner_geog_date(sql_ds,'VP','VP.date',geog,id,from_date,to_date,partners)
    
    return join_sql_ds(sql_ds)
    