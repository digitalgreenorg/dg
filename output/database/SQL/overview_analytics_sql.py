from output.database.utility import *

#Query for extra data for country in Overview page
def overview_tot_pg(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("COUNT(DISTINCT sfgt.persongroup_id) AS tot_pg")
    sql_ds['from'].append("activities_screening scr")
    sql_ds["join"].append(["activities_screening_farmer_groups_targeted sfgt", "sfgt.screening_id = scr.id "])
    sql_ds["join"].append(["geographies_village gv", "gv.id=scr.village_id "])

    filter_partner_geog_date(sql_ds,"scr","scr.date",geog,id,from_date,to_date,partners);

    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "])

    return join_sql_ds(sql_ds)