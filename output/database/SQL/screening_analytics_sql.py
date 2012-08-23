from output.database.utility import *

def screening_min_date(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("MIN(DATE) as date")
    sql_ds['from'].append("SCREENING SC")
    filter_partner_geog_date(sql_ds,'SC','SC.DATE',geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);


#values_to_fetch is for restricting calculated values.
#values_to_fetch is a list of combination of 'tot_dist_per', 'tot_per', 'tot_scr', 'dates'
def totAttendees_totScreening_datediff(geog, id, from_date, to_date, partners, values_to_fetch=None):
    sql_ds = get_init_sql_ds();
    if(values_to_fetch==None or 'tot_dist_per' in values_to_fetch):
        sql_ds['select'].append("COUNT(DISTINCT PMA.person_id) as tot_dist_per");
    if(values_to_fetch==None or 'tot_per' in values_to_fetch):
        sql_ds['select'].append("COUNT(PMA.person_id) as tot_per");
    if(values_to_fetch==None or 'tot_scr' in values_to_fetch):
        sql_ds['select'].append("COUNT(DISTINCT SC.id) as tot_scr");
    if(values_to_fetch==None or 'dates' in values_to_fetch):
        sql_ds['select'].append("DATEDIFF(MAX(SC.DATE),MIN(SC.DATE))+1 as tot_days");
    if(values_to_fetch==None or 'tot_scr' in values_to_fetch or 'dates' in values_to_fetch or geog!="COUNTRY" or from_date or to_date or partners):
        sql_ds['from'].append("SCREENING SC");
    if(values_to_fetch==None or 'tot_dist_per' in values_to_fetch or 'tot_per' in values_to_fetch):
        if sql_ds['from']:
            sql_ds['lojoin'].append(["PERSON_MEETING_ATTENDANCE PMA", "PMA.screening_id = SC.id"]);
        else:
            sql_ds['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);

    return join_sql_ds(sql_ds);

def screening_attendees_malefemaleratio(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["P.GENDER AS pie_key", "COUNT(DISTINCT P.id) AS count"]);
    sql_ds['from'].append("PERSON_MEETING_ATTENDANCE PMA");
    sql_ds['join'].append(["PERSON P", "P.id = PMA.person_id"]);
    if(from_date is not None and to_date is not None):
        sql_ds['join'].append(["SCREENING SC", "SC.id = PMA.screening_id"]);

    filter_partner_geog_date(sql_ds,"P","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append('P.GENDER')
    return join_sql_ds(sql_ds);

def screening_month_bar(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["COUNT(*) AS count","MONTH(DATE) AS MONTH", "YEAR(DATE) AS YEAR"])
    sql_ds['from'].append("SCREENING SC")
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds['group by'].extend([ "YEAR", "MONTH"])
    return join_sql_ds(sql_ds);

def screening_practice_scatter(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["practice_name AS name","sec.name as sec","subsec.name as subsec","top.name as top","subtop.name as subtop","sub.name as sub","COUNT(DISTINCT SVS.screening_id) AS count"]);
    sql_ds['from'].append("SCREENING_videoes_screened SVS")
    sql_ds['join'].append(["VIDEO v","v.id = SVS.video_id"])
    sql_ds['join'].append(["PRACTICES P", "P.id = v.related_practice_id"])
    sql_ds['lojoin'].append(["practice_sector sec","sec.id = P.practice_sector_id"])
    sql_ds['lojoin'].append(["practice_subsector subsec","subsec.id = P.practice_subsector_id"])
    sql_ds['lojoin'].append(["practice_topic top","top.id = P.practice_topic_id"])
    sql_ds['lojoin'].append(["practice_subtopic subtop","subtop.id = P.practice_subtopic_id"])
    sql_ds['lojoin'].append(["practice_subject sub","sub.id = P.practice_subject_id"])
    if((from_date and to_date) or geog.lower()!='country' or partners):
        sql_ds['join'].append(["SCREENING SC","SVS.screening_id = SC.id"])
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date, partners);
    sql_ds['group by'].append("practice_name")
    return join_sql_ds(sql_ds);

def screening_raw_attendance(geog,id,from_date,to_date,partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["DATE","COUNT(person_id) AS tot_per", "SUM(interested) AS tot_int", \
                             "COUNT(expressed_adoption_video) as tot_ado, SUM(if(expressed_question = '', 0, 1)) as tot_que"])
    sql_ds['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    sql_ds['join'].append(["SCREENING SC","SC.id = PMA.screening_id"])
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("screening_id")


    return_sql_ds = get_init_sql_ds();
    return_sql_ds['select'].extend(["DATE","AVG(tot_per) AS tot_per", "AVG(tot_int) AS tot_int", \
                             "AVG(tot_ado) as tot_ado, AVG(tot_que) as tot_que"])
    return_sql_ds['from'].append('('+join_sql_ds(sql_ds)+') T')
    return_sql_ds['group by'].append("DATE")
    return_sql_ds['order by'].append("DATE")

    return join_sql_ds(return_sql_ds);

def screening_percent_attendance(geog, id, from_date, to_date, partners):
    sql_ds_att = get_init_sql_ds(); #sql for selecting count(person) and count(interests)
    sql_ds_group = get_init_sql_ds(); #sql for person group_id and total strength
    sql_ds_main = get_init_sql_ds(); #sql joining above two sqls

    sql_ds_att['select'].extend(['DATE', 'group_id', 'COUNT(person_id) as tot_per', 'SUM(interested) as tot_int', \
                                 'SUM(if(expressed_question = "", 0, 1)) AS tot_que', 'COUNT(expressed_adoption_video) AS tot_ado']);

    sql_ds_att['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    sql_ds_att['join'].append(["PERSON P", "P.id = PMA.person_id"])
    sql_ds_att['join'].append(["SCREENING SC", "SC.id = PMA.screening_id"])

    filter_partner_geog_date(sql_ds_att,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds_att['group by'].extend(["screening_id", "group_id"])

    sql_ds_group['select'].extend(["group_id","COUNT(*) AS tot_pg_per"])
    sql_ds_group['from'].append("PERSON P")
    sql_ds_group['group by'].append("group_id");

    sql_ds_main['select'].extend(['DATE', 'ROUND(AVG(tot_per * 100/tot_pg_per),3) AS perc_per', \
                                   'ROUND(AVG(tot_int * 100/tot_per),3) AS perc_int', \
                                   'ROUND(AVG(tot_ado * 100/tot_pg_per),3) AS perc_ado', \
                                   'ROUND(AVG(tot_que * 100/tot_per),3) AS perc_ado'])
    sql_ds_main['from'].append("( "+join_sql_ds(sql_ds_att)+") t1")
    sql_ds_main['join'].append(["( "+join_sql_ds(sql_ds_group)+") t2", "t1.group_id = t2.group_id"])
    sql_ds_main['group by'].append("DATE")
    sql_ds_main['order by'].append("DATE")

    return join_sql_ds(sql_ds_main)


def screening_per_day(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["DATE as date", "COUNT(SC.id) as count"]);
    sql_ds['from'].append("SCREENING SC");
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("DATE")
    sql_ds['order by'].append("DATE")

    return join_sql_ds(sql_ds)
