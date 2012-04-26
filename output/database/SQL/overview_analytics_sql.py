from output.database.utility import *

#Query for extra data for country in Overview page
def overview_tot_pg(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("COUNT(DISTINCT persongroups_id) AS tot_pg")
    sql_ds['from'].append("SCREENING_farmer_groups_targeted SFGT")
    sql_ds['join'].append(["SCREENING SC","SC.id = SFGT.screening_id"])
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    
    return join_sql_ds(sql_ds)