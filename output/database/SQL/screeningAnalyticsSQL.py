from dg.output.database.utility import *

def getScreeningIDs(request,geog,id):
    from_date, to_date, partners = getDatesPartners(request);
    geog = geog.upper();
    sql_ds = getInitSQLds();
    sql_ds['select'].append("COUNT(SC.id)")
    sql_ds['from'].append("SCREENING SC")
    filterPartnerGeogDate(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners)
    return joinSQLds(sql_ds);

def screening_min_date(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    sql_ds = getInitSQLds();
    sql_ds['select'].append("MIN(DATE) as date")
    sql_ds['from'].append("SCREENING SC")
    filterPartnerGeogDate(sql_ds,'SC','SC.DATE',geog,id,from_date,to_date,partners)
    return joinSQLds(sql_ds);


def totAttendees_totScreening_datediff(request,geog,id):
    from_date, to_date, partners = getDatesPartners(request);
    sql_ds = getInitSQLds();
    sql_ds['select'].append("COUNT(DISTINCT PMA.person_id) as tot_dist_per");
    sql_ds['select'].append("COUNT(PMA.person_id) as tot_per");
    sql_ds['select'].append("COUNT(DISTINCT SC.id) as tot_scr");
    sql_ds['select'].append("DATEDIFF(MAX(SC.DATE),MIN(SC.DATE)) as tot_days");
    sql_ds['from'].append("SCREENING SC");
    sql_ds['join'].append(["PERSON_MEETING_ATTENDANCE PMA", "PMA.screening_id = SC.id"]);
    filterPartnerGeogDate(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);

    return joinSQLds(sql_ds);


def screening_attendees_malefemaleratio(request,geog,id):
    from_date, to_date, partners = getDatesPartners(request);
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["P.GENDER AS pie_key", "COUNT(DISTINCT P.id) AS count"]);
    sql_ds['from'].append("PERSON_MEETING_ATTENDANCE PMA");
    sql_ds['join'].append(["PERSON P", "P.id = PMA.person_id"]);
    if(from_date is not None and to_date is not None):
        sql_ds['join'].append(["SCREENING SC", "SC.id = PMA.screening_id"]);
    
    filterPartnerGeogDate(sql_ds,"P","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append('P.GENDER')
    return joinSQLds(sql_ds);

def screening_month_bar(request,geog,id):
    from_date, to_date, partners = getDatesPartners(request);
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["COUNT(*) AS count","MONTH(DATE) AS MONTH", "YEAR(DATE) AS YEAR"])
    sql_ds['from'].append("SCREENING SC")
    filterPartnerGeogDate(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds['group by'].extend([ "YEAR", "MONTH"])
    return joinSQLds(sql_ds);

def screening_practice_scatter(request,geog,id):
    from_date, to_date, partners = getDatesPartners(request);
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["practice_name AS name","COUNT(SVS.screening_id) AS count"]);
    sql_ds['from'].append("SCREENING_videoes_screened SVS")
    sql_ds['join'].append(["VIDEO_related_agricultural_practices VRP","VRP.video_id = SVS.video_id"])
    sql_ds['join'].append(["PRACTICES P", "P.id = VRP.practices_id"])
    if((from_date and to_date) or geog.lower()!='country' or partners):
        sql_ds['join'].append(["SCREENING SC","SVS.screening_id = SC.id"])
    filterPartnerGeogDate(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date, partners);
    sql_ds['group by'].append("practice_name")
    return joinSQLds(sql_ds);

def screening_raw_attendance(request,geog,id):
    from_date, to_date, partners = getDatesPartners(request);
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["DATE","COUNT(person_id) AS tot_per", "COUNT(expressed_interest_practice_id) AS tot_int", \
                             "COUNT(expressed_adoption_practice_id) as tot_ado, COUNT(expressed_question_practice_id) as tot_que"])
    sql_ds['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    sql_ds['join'].append(["SCREENING SC","SC.id = PMA.screening_id"])
    filterPartnerGeogDate(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds['group by'].append("screening_id")
    
    
    return_sql_ds = getInitSQLds();
    return_sql_ds['select'].extend(["DATE","AVG(tot_per) AS tot_per", "AVG(tot_int) AS tot_int", \
                             "AVG(tot_ado) as tot_ado, AVG(tot_que) as tot_que"])
    return_sql_ds['from'].append('('+joinSQLds(sql_ds)+') T')
    return_sql_ds['group by'].append("DATE")
    return_sql_ds['order by'].append("DATE")
    
    return joinSQLds(return_sql_ds);

def screening_percent_attendance(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request);
    sql_ds_att = getInitSQLds(); #sql for selecting count(person) and count(interests)
    sql_ds_group = getInitSQLds(); #sql for person group_id and total strength
    sql_ds_main = getInitSQLds(); #sql joining above two sqls
    
    sql_ds_att['select'].extend(['DATE', 'group_id', 'COUNT(person_id) as tot_per', 'COUNT(expressed_interest_practice_id) as tot_int', \
                                 'COUNT(expressed_question_practice_id) AS tot_que', 'COUNT(expressed_adoption_practice_id) AS tot_ado']);
    
    sql_ds_att['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    sql_ds_att['join'].append(["PERSON P", "P.id = PMA.person_id"])
    sql_ds_att['join'].append(["SCREENING SC", "SC.id = PMA.screening_id"])
    
    filterPartnerGeogDate(sql_ds_att,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    sql_ds_att['group by'].extend(["screening_id", "group_id"])
    
    sql_ds_group['select'].extend(["group_id","COUNT(*) AS tot_pg_per"])
    sql_ds_group['from'].append("PERSON P")
    sql_ds_group['group by'].append("group_id");
    
    sql_ds_main['select'].extend(['DATE', 'ROUND(AVG(tot_per * 100/tot_pg_per),3) AS perc_per', \
                                   'ROUND(AVG(tot_int * 100/tot_per),3) AS perc_int', \
                                   'ROUND(AVG(tot_ado * 100/tot_pg_per),3) AS perc_ado', \
                                   'ROUND(AVG(tot_que * 100/tot_per),3) AS perc_ado'])
    sql_ds_main['from'].append("( "+joinSQLds(sql_ds_att)+") t1")
    sql_ds_main['join'].append(["( "+joinSQLds(sql_ds_group)+") t2", "t1.group_id = t2.group_id"])
    sql_ds_main['group by'].append("DATE")
    sql_ds_main['order by'].append("DATE")
    
    return joinSQLds(sql_ds_main)
