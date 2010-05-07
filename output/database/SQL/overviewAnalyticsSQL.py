from dg.output.database.utility import *

#Query for extra data for country in Overview page
def overview_nation_pg_vil_total():
    return """SELECT * FROM
          (SELECT COUNT(*) AS tot_vil FROM VILLAGE) t1,
          (SELECT COUNT(*) AS tot_pg FROM PERSON_GROUPS) t2"""
          
def overview_sum_geog(request,geog,id):
    from_date,to_date,partner_id = getDatesPartners(request)
    geog_list = [None,"COUNTRY","STATE","DISTRICT","BLOCK","VILLAGE"]
    geog_par = geog_list[geog_list.index(geog.upper())-1]

    sc_sql = getInitSQLds()
    sc_sql['select'].append("COUNT(SC.id) as tot_scr");
    sc_sql['from'].append("SCREENING SC");    
    filterPartnerGeogDate(sc_sql,"SC","SC.DATE",geog,id,from_date,to_date,partner_id);
    
    vid_sql = getInitSQLds()
    vid_sql['select'].append("COUNT(VID.id) as tot_vid");
    vid_sql['from'].append("VIDEO VID");    
    filterPartnerGeogDate(vid_sql,"VID","VID.VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partner_id);
    
    ado_sql = getInitSQLds()
    ado_sql['select'].append("COUNT(PAP.id) as tot_ado");
    ado_sql['from'].append("PERSON P");
    ado_sql['join'].append(["PERSON_ADOPT_PRACTICE PAP", "PAP.person_id = P.id"])    
    filterPartnerGeogDate(ado_sql,"P","PAP.DATE_OF_ADOPTION",geog,id,from_date,to_date,partner_id);
    
    pra_sql = getInitSQLds()
    pra_sql['select'].append("COUNT(DISTINCT VRAP.practices_id) as tot_pra");
    pra_sql['from'].append("VIDEO VID");
    pra_sql['join'].append(["VIDEO_related_agricultural_practices VRAP", "VRAP.video_id = VID.id"])    
    filterPartnerGeogDate(pra_sql,"VID","VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partner_id);
    
    per_sql = getInitSQLds()
    per_sql['select'].append('COUNT(DISTINCT P.id) as tot_per')
    per_sql['from'].append('PERSON P')
    if(from_date is not None and to_date is not None):
        per_sql['join'].append(["""(
        SELECT person_id, min(date) as DATE
        FROM (
            SELECT  vs.person_id, VIDEO_PRODUCTION_END_DATE AS date
            FROM VIDEO_farmers_shown vs, VIDEO vid
            WHERE vs.video_id = vid.id
    
            UNION
    
            SELECT  person_id , DATE_OF_ADOPTION AS date
            FROM PERSON_ADOPT_PRACTICE pa
    
            UNION
    
            SELECT  pa.person_id, DATE
            FROM PERSON_MEETING_ATTENDANCE pa, SCREENING sc
            WHERE pa.screening_id = sc.id ) TMP
            GROUP BY person_id
        )AS TAB""", "TAB.person_id = P.id"])
        date_field = "TAB.DATE"
        
    filterPartnerGeogDate(per_sql,"P","TAB.DATE",geog,id,from_date,to_date,partner_id);
    
    combined_sql =  [joinSQLds(sc_sql), joinSQLds(vid_sql), joinSQLds(ado_sql), joinSQLds(pra_sql), joinSQLds(per_sql)]
    combined_sql = ['('+combined_sql[i]+') t'+str(i) for i in range(0,5)]
    if(geog.upper()=='COUNTRY'):
        combined_sql.append("(SELECT 'India' as name) t5")
    elif(geog.upper()=='STATE'):
        combined_sql.append("(SELECT " + geog.upper() + "_NAME as name, 1 as id FROM " + geog.upper() + " WHERE id = " +str(id) + ") t5")
    else:
        combined_sql.append("(SELECT " + geog.upper() + "_NAME as name, "+geog_par.lower()+"_id as id FROM " + geog.upper() + " WHERE id = " +str(id) + ") t5")
    combined_sql = ',\n'.join(combined_sql)
    
    return 'SELECT * FROM ( '+combined_sql+')'
    
def overview_min_date(request, geog, id):
    from_date, to_date, partner_id = getDatesPartners(request)    

    sql_ds_vid = getInitSQLds();
    sql_ds_sc = getInitSQLds();
    sql_ds_ado = getInitSQLds();
    
    sql_ds_vid['select'].append("MIN(VIDEO_PRODUCTION_END_DATE) AS DATE")
    sql_ds_vid['from'].append("VIDEO VID")
    filterPartnerGeogDate(sql_ds_vid,"VID","VIDEO_PRODUCTION_END_DATE",geog,id,from_date,to_date,partner_id);
    
    sql_ds_sc['select'].append("MIN(DATE) AS DATE")
    sql_ds_sc['from'].append("SCREENING SC")
    filterPartnerGeogDate(sql_ds_sc,"SC","SC.DATE",geog,id,from_date,to_date,partner_id);
    
    sql_ds_ado['select'].append("MIN(DATE_OF_ADOPTION) AS DATE")
    sql_ds_ado['from'].append("PERSON_ADOPT_PRACTICE PAP")
    if(geog.upper()!='COUNTRY' or partner_id):
        sql_ds_ado['join'].append(["PERSON P","PAP.person_id = P.id"])
        filterPartnerGeogDate(sql_ds_ado,"P","DATE_OF_ADOPTION",geog,id,from_date,to_date,partner_id);
        

    return """ SELECT MIN(DATE) AS date
    from ("""+joinSQLds(sql_ds_vid)+"\nUNION\n" + \
    joinSQLds(sql_ds_sc)+"\nUNION\n" + \
    joinSQLds(sql_ds_ado)+") AS T1"
    
#Returns parent level region id
def overview_parent_id(arg_dict):
    sql = []
    if 'geog' in arg_dict:
        if arg_dict['geog'] == 'district':
            sql.append(r"""SELECT state_id as id FROM DISTRICT d WHERE d.id =  """+str(arg_dict['id']) )
        
        elif arg_dict['geog'] == 'block':
            sql.append(r""" SELECT district_id as id FROM BLOCK b WHERE b.id =  """+str(arg_dict['id']) )
        
        elif arg_dict['geog'] == 'village':
            sql.append(r""" SELECT vil.block_id as id, b.BLOCK_NAME AS name FROM VILLAGE vil, BLOCK b WHERE vil.block_id = b.id and vil.id =  """+str(arg_dict['id']) )
        elif arg_dict['geog'] == 'country':
            sql.append(r'SELECT 1 AS id ')
        elif arg_dict['geog'] == 'state':
            sql.append(r'SELECT 1 AS id ')
    
        
    return ''.join(sql)