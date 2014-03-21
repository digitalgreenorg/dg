from output.database.utility import *
import datetime


def old_attach_geog_date(sql_ds,par_table_id,date_filter_field,geog,id,from_date,to_date):
    if(from_date and to_date):
        sql_ds['where'].append(date_filter_field +" BETWEEN '"+from_date+"' AND '"+to_date+"'")
    geog_list = ["VILLAGE","BLOCK","DISTRICT","STATE", "COUNTRY"];
    if(geog is None or geog not in geog_list):
        return

    if(geog=="VILLAGE"):
        sql_ds['where'].append(par_table_id+".village_id = "+str(id))
        return

    sql_ds['lojoin'].append(["VILLAGE V","V.id = "+par_table_id+".village_id"])
    for g in geog_list[1:]:
        prev_geog = geog_list[geog_list.index(g)-1];
        if(geog == g):
            if(type(id) == types.ListType):
                sql_ds['where'].append(prev_geog[0]+"."+geog.lower()+"_id in ("+','.join(id)+")")
            else:
                sql_ds['where'].append(prev_geog[0]+"."+geog.lower()+"_id = "+str(id))
            break;
        sql_ds['lojoin'].append([g+" "+g[0],prev_geog[0]+"."+g.lower()+"_id = "+g[0]+".id"])



def old_filter_partner_geog_date(sql_ds,par_table_id,date_filter_field,geog,id,from_date,to_date,partner_id):
    if(partner_id):
        if(geog == None):
            partner_sql = ["SELECT id FROM geographies_DISTRICT WHERE partner_id in ("+','.join(partner_id)+")"]
            attach_geog_date(sql_ds,par_table_id,date_filter_field,'DISTRICT',partner_sql,from_date,to_date)
            return
        elif(geog=="STATE"  or geog=="COUNTRY"):
            dist_part = []
            if geog=="COUNTRY":
                dist_part = run_query_raw("SELECT DISTINCT partner_id FROM geographies_DISTRICT D JOIN geographies_STATE S ON S.id = D.state_id WHERE country_id = "+str(id))
            else:
                dist_part = run_query_raw("SELECT DISTINCT partner_id FROM geographies_DISTRICT WHERE state_id = "+str(id))
            dist_part_list = [str(x[0]) for x in dist_part if str(x[0]) in partner_id]
            if(dist_part_list):
                partner_sql = ["SELECT id FROM geographies_DISTRICT WHERE partner_id in ("+','.join(dist_part_list)+")"]
                sql_ds['where'].append("district_id in ("+partner_sql[0]+")")

    old_attach_geog_date(sql_ds,par_table_id,date_filter_field,geog,id,from_date,to_date)

def get_csp_identified(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(AAV.animator_id) as count')
    sql_ds['from'].append("people_animatorassignedvillage AAV")
    old_filter_partner_geog_date(sql_ds,"AAV","AAV.START_DATE",geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);

def get_village_operational(geog, id, date_var, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(DISTINCT village_id) as count")
    sql_ds['from'].append("screening_myisam SCM")
    sql_ds['force index'].append('(screening_myisam_village_id)')
    prev_date = str(datetime.date(*[int(i) for i in str(date_var).split('-')]) - datetime.timedelta(days=60))
    filter_partner_geog_date(sql_ds,"SCM","SCM.date",geog,id,prev_date,date_var,partners)
    return join_sql_ds(sql_ds);

def get_storyboard_prepared(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(DISTINCT VID.ID) as count')
    sql_ds['from'].append('videos_video VID')
    sql_ds['where'].append("STORYBOARD_FILENAME != ''")
    old_filter_partner_geog_date(sql_ds,"VID","VID.VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);

def get_video_edited(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(DISTINCT VID.ID) as count')
    sql_ds['from'].append('videos_video VID')
    old_filter_partner_geog_date(sql_ds,"VID","VID.EDIT_FINISH_DATE",geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);

def get_quality_check(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(DISTINCT VID.ID) as count')
    sql_ds['from'].append("videos_video VID")
    old_filter_partner_geog_date(sql_ds,"VID","VID.APPROVAL_DATE",geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);

def get_interest_per_dissemination(geog, id, from_date, to_date, partners):
    inner_sql = get_init_sql_ds();
    inner_sql['select'].append('SUM(PMA.interested) AS interest')
    inner_sql['from'].append("activities_personmeetingattendance PMA")
    inner_sql['join'].append(["activities_screening SC", "SC.id = PMA.screening_id"])
    inner_sql['group by'].append("SC.id")
    old_filter_partner_geog_date(inner_sql,"SC","SC.DATE",geog,id,from_date,to_date,partners)
    
    return "SELECT AVG(interest) as count from ("+join_sql_ds(inner_sql)+") T";

def get_village_identified(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(VIL.ID) as count")
    sql_ds['from'].append("geographies_VILLAGE VIL")
    if(from_date and to_date):
        sql_ds['where'].append("VIL.START_DATE BETWEEN '"+from_date+"' AND '"+to_date+"'")
        
    if(geog=="COUNTRY"):
        sql_ds['join'].append(["geographies_BLOCK B", "B.id = VIL.block_id"])
        sql_ds['join'].append(["geographies_DISTRICT D", "D.id = B.district_id"])
        sql_ds['join'].append(["geographies_STATE S", "S.id = D.state_id"])
        sql_ds['where'].append("S.country_id = "+str(id))
    elif(geog=="STATE"):
        sql_ds['join'].append(["geographies_BLOCK B", "B.id = VIL.block_id"])
        sql_ds['join'].append(["geographies_DISTRICT D", "D.id = B.district_id"])
        sql_ds['where'].append("D.state_id = "+str(id))
    elif(geog=='DISTRICT'):
        sql_ds['join'].append(["geographies_BLOCK B", "B.id = VIL.block_id"])
        sql_ds['where'].append("B.district_id = "+str(id))

    if(partners):
        partner_sql = "SELECT id FROM geographies_DISTRICT WHERE partner_id IN ("+','.join(partners)+")"
        if(geog is None or geog == "COUNTRY"):
            sql_ds['join'].append(["geographies_BLOCK B", "B.id = VIL.block_id"])
            sql_ds['where'].append("B.district_id IN ("+partner_sql+")")
        elif(geog == 'STATE'):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM geographies_DISTRICT WHERE state_id = "+str(id))
            dist_part_list = [str(x[0]) for x in dist_part if str(x[0]) in partners]
            if(dist_part_list):
                partner_sql = "SELECT id FROM geographies_DISTRICT WHERE partner_id in ("+','.join(dist_part_list)+")"
                sql_ds['where'].append("D.id in ("+partner_sql+")")
                
    return join_sql_ds(sql_ds);

def get_videos_uploaded(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(VID.id) as count")
    sql_ds['from'].append("videos_video VID")
    sql_ds['where'].append("YOUTUBEID != ''")
    old_filter_partner_geog_date(sql_ds,"VID","VID.VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partners)
    
    return join_sql_ds(sql_ds)

    