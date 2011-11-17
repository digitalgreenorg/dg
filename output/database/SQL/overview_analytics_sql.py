from output.database.utility import *

#Query for extra data for country in Overview page
def overview_tot_pg(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("COUNT(DISTINCT persongroups_id) AS tot_pg")
    sql_ds['from'].append("SCREENING_farmer_groups_targeted SFGT")
    sql_ds['join'].append(["SCREENING SC","SC.id = SFGT.screening_id"])
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    
    return join_sql_ds(sql_ds)
          
def overview_min_date(geog, id, from_date, to_date, partner_id):
    sql_ds_vid = get_init_sql_ds();
    sql_ds_sc = get_init_sql_ds();
    sql_ds_ado = get_init_sql_ds();

    sql_ds_vid['select'].append("MIN(VIDEO_PRODUCTION_END_DATE) AS DATE")
    sql_ds_vid['from'].append("VIDEO VID")
    sql_ds_vid['where'].append('VID.VIDEO_SUITABLE_FOR = 1')
    filter_partner_geog_date(sql_ds_vid,"VID","VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partner_id);

    sql_ds_sc['select'].append("MIN(DATE) AS DATE")
    sql_ds_sc['from'].append("SCREENING SC")
    filter_partner_geog_date(sql_ds_sc,"SC","SC.DATE",geog,id,from_date,to_date,partner_id);

    sql_ds_ado['select'].append("MIN(DATE_OF_ADOPTION) AS DATE")
    sql_ds_ado['from'].append("PERSON_ADOPT_PRACTICE PAP")
    if(geog!='COUNTRY' or partner_id):
        sql_ds_ado['join'].append(["PERSON P","PAP.person_id = P.id"])
        filter_partner_geog_date(sql_ds_ado,"P","DATE_OF_ADOPTION",geog,id,from_date,to_date,partner_id);


    return """ SELECT MIN(DATE) AS date
    FROM ("""+join_sql_ds(sql_ds_vid)+"\nUNION\n" + \
    join_sql_ds(sql_ds_sc)+"\nUNION\n" + \
    join_sql_ds(sql_ds_ado)+") AS T1"

