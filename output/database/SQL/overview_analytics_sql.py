from output.database.utility import *

#Query for extra data for country in Overview page
def overview_tot_pg(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("COUNT(DISTINCT group_id) AS tot_pg")
    sql_ds['from'].append("screening_myisam SCM")
    filter_partner_geog_date(sql_ds,"SCM","SCM.date",geog,id,from_date,to_date,partners);
    
    return join_sql_ds(sql_ds)