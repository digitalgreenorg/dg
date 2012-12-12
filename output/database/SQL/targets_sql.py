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
            partner_sql = ["SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(partner_id)+")"]
            attach_geog_date(sql_ds,par_table_id,date_filter_field,'DISTRICT',partner_sql,from_date,to_date)
            return
        elif(geog=="STATE"  or geog=="COUNTRY"):
            dist_part = []
            if geog=="COUNTRY":
                dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT D JOIN STATE S ON S.id = D.state_id WHERE country_id = "+str(id))
            else:
                dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            dist_part_list = [str(x[0]) for x in dist_part if str(x[0]) in partner_id]
            if(dist_part_list):
                partner_sql = ["SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(dist_part_list)+")"]
                sql_ds['where'].append("district_id in ("+partner_sql[0]+")")

    old_attach_geog_date(sql_ds,par_table_id,date_filter_field,geog,id,from_date,to_date)

def get_csp_identified(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(AAV.animator_id) as count')
    sql_ds['from'].append("ANIMATOR_ASSIGNED_VILLAGE AAV")
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
    sql_ds['from'].append('VIDEO VID')
    sql_ds['where'].append("STORYBOARD_FILENAME != ''")
    old_filter_partner_geog_date(sql_ds,"VID","VID.VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);

def get_video_edited(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(DISTINCT VID.ID) as count')
    sql_ds['from'].append('VIDEO VID')
    old_filter_partner_geog_date(sql_ds,"VID","VID.EDIT_FINISH_DATE",geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);

def get_quality_check(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(DISTINCT VID.ID) as count')
    sql_ds['from'].append("VIDEO VID")
    old_filter_partner_geog_date(sql_ds,"VID","VID.APPROVAL_DATE",geog,id,from_date,to_date,partners)
    return join_sql_ds(sql_ds);

def get_interest_per_dissemination(geog, id, from_date, to_date, partners):
    inner_sql = get_init_sql_ds();
    inner_sql['select'].append('SUM(PMA.interested) AS interest')
    inner_sql['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    inner_sql['join'].append(["SCREENING SC", "SC.id = PMA.screening_id"])
    inner_sql['group by'].append("SC.id")
    old_filter_partner_geog_date(inner_sql,"SC","SC.DATE",geog,id,from_date,to_date,partners)
    
    return "SELECT AVG(interest) as count from ("+join_sql_ds(inner_sql)+") T";

def get_fresh_csp_tot_training(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('MIN(TRAINING_END_DATE) AS min_date')
    sql_ds['from'].append("TRAINING T")
    sql_ds['join'].append(["TRAINING_animators_trained TAT", "TAT.training_id = T.id"])
    sql_ds['join'].append(["ANIMATOR A", "A.id = TAT.animator_id"])
    sql_ds['where'].append('A.CSP_FLAG = TRUE')
    sql_ds['group by'].append('TAT.animator_id')
    old_filter_partner_geog_date(sql_ds,"T","DUMMY",geog,id,None,None,partners)
    sql_ds['having'].append("min_date BETWEEN '"+from_date+"' AND '"+to_date+"'")
    
    return "SELECT COUNT(*) as count FROM ("+join_sql_ds(sql_ds)+") T"
    
def get_csp_tot_training(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(DISTINCT ANIMATOR_ID) as count')
    sql_ds['from'].append("TRAINING T")
    sql_ds['join'].append(["TRAINING_animators_trained TAT", "TAT.training_id = T.id"])
    sql_ds['join'].append(["ANIMATOR A", "A.id = TAT.animator_id"])
    sql_ds['where'].append("A.CSP_FLAG = TRUE")
    old_filter_partner_geog_date(sql_ds,"T","T.TRAINING_END_DATE",geog,id,from_date,to_date,partners)

    return join_sql_ds(sql_ds);

def get_fresh_crp_tot_training(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('MIN(TRAINING_END_DATE) AS min_date')
    sql_ds['from'].append("TRAINING T")
    sql_ds['join'].append(["TRAINING_animators_trained TAT", "TAT.training_id = T.id"])
    sql_ds['join'].append(["ANIMATOR A", "A.id = TAT.animator_id"])
    sql_ds['where'].append('(A.CAMERA_OPERATOR_FLAG = TRUE OR A.FACILITATOR_FLAG = TRUE)')
    sql_ds['group by'].append('TAT.animator_id')
    old_filter_partner_geog_date(sql_ds,"T","DUMMY",geog,id,None,None,partners)
    sql_ds['having'].append("min_date BETWEEN '"+from_date+"' AND '"+to_date+"'")
    
    return "SELECT COUNT(*) as count FROM ("+join_sql_ds(sql_ds)+") T"
    
def get_crp_tot_training(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('COUNT(DISTINCT ANIMATOR_ID) as count')
    sql_ds['from'].append("TRAINING T")
    sql_ds['join'].append(["TRAINING_animators_trained TAT", "TAT.training_id = T.id"])
    sql_ds['join'].append(["ANIMATOR A", "A.id = TAT.animator_id"])
    sql_ds['where'].append("(A.CAMERA_OPERATOR_FLAG = TRUE OR A.FACILITATOR_FLAG = TRUE)")
    old_filter_partner_geog_date(sql_ds,"T","T.TRAINING_END_DATE",geog,id,from_date,to_date,partners)

    return join_sql_ds(sql_ds);

def get_village_identified(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(VIL.ID) as count")
    sql_ds['from'].append("VILLAGE VIL")
    if(from_date and to_date):
        sql_ds['where'].append("VIL.START_DATE BETWEEN '"+from_date+"' AND '"+to_date+"'")
        
    if(geog=="COUNTRY"):
        sql_ds['join'].append(["BLOCK B", "B.id = VIL.block_id"])
        sql_ds['join'].append(["DISTRICT D", "D.id = B.district_id"])
        sql_ds['join'].append(["STATE S", "S.id = D.state_id"])
        sql_ds['where'].append("S.country_id = "+str(id))
    elif(geog=="STATE"):
        sql_ds['join'].append(["BLOCK B", "B.id = VIL.block_id"])
        sql_ds['join'].append(["DISTRICT D", "D.id = B.district_id"])
        sql_ds['where'].append("D.state_id = "+str(id))
    elif(geog=='DISTRICT'):
        sql_ds['join'].append(["BLOCK B", "B.id = VIL.block_id"])
        sql_ds['where'].append("B.district_id = "+str(id))

    if(partners):
        partner_sql = "SELECT id FROM DISTRICT WHERE partner_id IN ("+','.join(partners)+")"
        if(geog is None or geog == "COUNTRY"):
            sql_ds['join'].append(["BLOCK B", "B.id = VIL.block_id"])
            sql_ds['where'].append("B.district_id IN ("+partner_sql+")")
        elif(geog == 'STATE'):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            dist_part_list = [str(x[0]) for x in dist_part if str(x[0]) in partners]
            if(dist_part_list):
                partner_sql = "SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(dist_part_list)+")"
                sql_ds['where'].append("D.id in ("+partner_sql+")")
                
    return join_sql_ds(sql_ds);

def get_videos_uploaded(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(VID.id) as count")
    sql_ds['from'].append("VIDEO VID")
    sql_ds['where'].append("YOUTUBEID != ''")
    old_filter_partner_geog_date(sql_ds,"VID","VID.VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partners)
    
    return join_sql_ds(sql_ds)

def get_targets(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append('SUM(clusters_identification) AS tot_clusters')
    sql_ds['select'].append('SUM(dg_concept_sharing) AS tot_dg_sharing')
    sql_ds['select'].append('SUM(csp_identification) AS tot_csp_identified')
    sql_ds['select'].append('SUM(dissemination_set_deployment) AS tot_deployment')
    sql_ds['select'].append('SUM(village_operationalization) AS tot_vil_op')
    sql_ds['select'].append('SUM(video_uploading) AS tot_vid_upl')
    sql_ds['select'].append('SUM(video_production) AS tot_vid_pro')
    sql_ds['select'].append('SUM(storyboard_preparation) AS tot_story')
    sql_ds['select'].append('SUM(video_shooting) AS tot_vid_shoot')
    sql_ds['select'].append('SUM(video_editing) AS tot_vid_edit')
    sql_ds['select'].append('SUM(video_quality_checking) AS tot_vid_qual')
    sql_ds['select'].append('SUM(disseminations) AS tot_diss')
    sql_ds['select'].append('AVG(avg_attendance_per_dissemination) AS avg_att')
    sql_ds['select'].append('AVG(exp_interest_per_dissemination) AS exp_int')
    sql_ds['select'].append('AVG(adoption_per_dissemination) AS ado_dis')
    sql_ds['select'].append('SUM(crp_training) AS tot_crp')
    sql_ds['select'].append('SUM(crp_refresher_training) AS tot_crp_ref')
    sql_ds['select'].append('SUM(csp_training) AS tot_csp')
    sql_ds['select'].append('SUM(csp_refresher_training) AS tot_csp_ref')
    sql_ds['select'].append('SUM(editor_training) AS tot_editor')
    sql_ds['select'].append('SUM(editor_refresher_training) AS tot_editor_ref')
    sql_ds['select'].append('SUM(villages_certification) AS tot_vil_cert')
    sql_ds['from'].append('dashboard_target DT')
    
    if(from_date and to_date):
        sql_ds['where'].append("month_year BETWEEN '"+from_date+"' AND '"+to_date+"'")
        
    if(geog == 'COUNTRY'):
        sql_ds['join'].append(['DISTRICT D', "D.id = DT.district_id"])
        sql_ds['join'].append(['STATE S', 'S.id = D.state_id'])
        sql_ds['where'].append('S.country_id = '+str(id))        
    elif(geog == 'STATE'):
        sql_ds['join'].append(['DISTRICT D', "D.id = DT.district_id"])
        sql_ds['where'].append('D.state_id = '+str(id))
    elif(geog == 'DISTRICT'):
        sql_ds['where'].append('DT.district_id = '+str(id))
    elif(geog is not None):
        return ""
    
    if(partners):
        partner_sql = "SELECT id FROM DISTRICT WHERE partner_id IN ("+','.join(partners)+")"
        if(geog is None or geog == "COUNTRY"):
            sql_ds['where'].append("DT.district_id IN ("+partner_sql+")")
        elif(geog == 'STATE'):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            dist_part_list = [str(x[0]) for x in dist_part if str(x[0]) in partners]
            if(dist_part_list):
                partner_sql = ["SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(dist_part_list)+")"]
                sql_ds['where'].append("DT.district_id in ("+partner_sql[0]+")")
    
    return join_sql_ds(sql_ds)
            
    

    
    
    