from output.database.utility import *


def adoption_tot_ado(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT person_id) as tot_farmers")
    sql_ds['select'].append("COUNT(DISTINCT practice_id) as tot_prac")
    sql_ds['from'].append("person_adopt_practice_myisam PAPM")
    filter_partner_geog_date(sql_ds,'PAPM','PAPM.date_of_adoption',geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds)

def adoption_month_bar(geog,id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["SUM(total_adoption) AS count","MONTH(date) AS MONTH", "YEAR(date) AS YEAR"])
    sql_ds['from'].append("village_precalculation_copy VPC")
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners);
    sql_ds['group by'].extend([ "YEAR", "MONTH"])
    return join_sql_ds(sql_ds);

def adoption_malefemale_ratio(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["PAPM.gender as pie_key", "COUNT(*) as count"])
    sql_ds['from'].append("person_adopt_practice_myisam PAPM")
    filter_partner_geog_date(sql_ds,'PAPM','PAPM.date_of_adoption',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("PAPM.gender")
    return join_sql_ds(sql_ds);

def adoption_practice_wise_scatter(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(["PRACTICE_NAME as name", "COUNT(PAPM.adoption_id) as count"])
    sql_ds['from'].append("person_adopt_practice_myisam PAPM")
    sql_ds['join'].append(["PRACTICES PR","PAPM.practice_id = PR.id"])
    filter_partner_geog_date(sql_ds,'PAPM','PAPM.date_of_adoption',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("practice_id")
    sql_ds['order by'].append("count")
    return join_sql_ds(sql_ds)

def adoption_repeat_adoption_practice_count(geog, id, from_date, to_date, partners):
    inner_sql_ds = get_init_sql_ds();
    inner_sql_ds['select'].append("DISTINCT person_id")
    inner_sql_ds['from'].append("person_adopt_practice_myisam PAPM")
    filter_partner_geog_date(inner_sql_ds,'PAPM','PAPM.date_of_adoption',geog,id,from_date,to_date,partners)
    inner_sql_ds['group by'].append("PAPM.person_id")
    inner_sql_ds['group by'].append("PAPM.practice_id")
    inner_sql_ds['having'].append("COUNT(*) > 1")
    
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(*) as count")
    sql_ds['from'].append('(' + join_sql_ds(inner_sql_ds) + ') TAB')
    
    return join_sql_ds(sql_ds)

def adoption_rate_line(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(['date', 'SUM(total_adopted_attendees)', 'SUM(total_active_attendees)'])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['group by'].append('date')
    sql_ds['order by'].append('date')
    filter_partner_geog_date(sql_ds,'VPC','VPC.date',geog,id,from_date,to_date,partners)
    
    return join_sql_ds(sql_ds)
    