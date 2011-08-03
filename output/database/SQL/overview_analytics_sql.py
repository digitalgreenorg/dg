from dg.output.database.utility import *

#Query for extra data for country in Overview page
def overview_tot_pg(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("COUNT(DISTINCT persongroups_id) AS tot_pg")
    sql_ds['from'].append("SCREENING_farmer_groups_targeted SFGT")
    sql_ds['join'].append(["SCREENING SC","SC.id = SFGT.screening_id"])
    filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners);
    
    return join_sql_ds(sql_ds)
          
#Type is an list which can have 'production', 'screening','person', 'adoption', 'practice', 'village'
#Type can be None to include all
def overview_sum_geog(geog, id, from_date, to_date, partner_id, type=None):
    geog_list = [None,"COUNTRY","STATE","DISTRICT","BLOCK","VILLAGE"]
    geog_par = geog_list[geog_list.index(geog)-1]

    sc_sql = get_init_sql_ds()
    sc_sql['select'].append("COUNT(SC.id) as tot_scr");
    sc_sql['from'].append("SCREENING SC");
    filter_partner_geog_date(sc_sql,"SC","SC.DATE",geog,id,from_date,to_date,partner_id);

    #Total villages which have had screening in given time period.
    vil_sql = get_init_sql_ds()
    vil_sql['select'].append("COUNT(DISTINCT village_id) as tot_vil");
    vil_sql['from'].append("SCREENING SC");
    filter_partner_geog_date(vil_sql,"SC","SC.DATE",geog,id,from_date,to_date,partner_id);
    
    vid_sql = get_init_sql_ds()
    vid_sql['select'].append("COUNT(VID.id) as tot_vid");
    vid_sql['from'].append("VIDEO VID");
    filter_partner_geog_date(vid_sql,"VID","VID.VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partner_id);

    ado_sql = get_init_sql_ds()
    ado_sql['select'].append("COUNT(PAP.id) as tot_ado");
    ado_sql['from'].append("PERSON P");
    ado_sql['join'].append(["PERSON_ADOPT_PRACTICE PAP", "PAP.person_id = P.id"])
    filter_partner_geog_date(ado_sql,"P","PAP.DATE_OF_ADOPTION",geog,id,from_date,to_date,partner_id);

    pra_sql = get_init_sql_ds()
    pra_sql['select'].append("COUNT(DISTINCT VRAP.practices_id) as tot_pra");
    pra_sql['from'].append("VIDEO VID");
    pra_sql['join'].append(["VIDEO_related_agricultural_practices VRAP", "VRAP.video_id = VID.id"])
    filter_partner_geog_date(pra_sql,"VID","VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partner_id);

    per_sql = get_init_sql_ds()
    per_sql['select'].append('COUNT(P.id) as tot_per')
    per_sql['from'].append('PERSON P')
    per_sql['where'].append('date_of_joining is not NULL')
    filter_partner_geog_date(per_sql,"P","P.date_of_joining",geog,id,from_date,to_date,partner_id);

    if(type):
        combined_sql = []
        if('production' in type):
            combined_sql.append(join_sql_ds(vid_sql))
        if('screening' in type):
            combined_sql.append(join_sql_ds(sc_sql))
        if('adoption' in type):
            combined_sql.append(join_sql_ds(ado_sql))
        if('person' in type):
            combined_sql.append(join_sql_ds(per_sql))
        if('practice' in type):
            combined_sql.append(join_sql_ds(pra_sql))
        if('village' in type):
            combined_sql.append(join_sql_ds(vil_sql))
    else:
        combined_sql =  [join_sql_ds(sc_sql), join_sql_ds(vid_sql), join_sql_ds(ado_sql), join_sql_ds(pra_sql), join_sql_ds(per_sql), join_sql_ds(vil_sql)]
    
    arr_len = len(combined_sql);
    combined_sql = ['('+combined_sql[i]+') t'+str(i) for i in range(0,arr_len)]
    if(geog=='COUNTRY'):
        combined_sql.append("(SELECT 'India' as name) t"+str(arr_len))
    elif(geog=='STATE'):
        combined_sql.append("(SELECT " + geog + "_NAME as name, 1 as id FROM " + geog + " WHERE id = " +str(id) + ") t"+str(arr_len))
    else:
        combined_sql.append("(SELECT " + geog + "_NAME as name, "+geog_par.lower()+"_id as id FROM " + geog + " WHERE id = " +str(id) + ") t"+str(arr_len))
    combined_sql = ',\n'.join(combined_sql)

    return 'SELECT * FROM ( '+combined_sql+')'

def overview_min_date(geog, id, from_date, to_date, partner_id):
    sql_ds_vid = get_init_sql_ds();
    sql_ds_sc = get_init_sql_ds();
    sql_ds_ado = get_init_sql_ds();

    sql_ds_vid['select'].append("MIN(VIDEO_PRODUCTION_END_DATE) AS DATE")
    sql_ds_vid['from'].append("VIDEO VID")
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

