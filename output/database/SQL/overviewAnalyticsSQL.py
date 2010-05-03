from dg.output.database.utility import *

#Query for extra data for country in Overview page
def overview_nation_pg_vil_total():
    return """SELECT * FROM
          (SELECT COUNT(*) AS tot_vil FROM VILLAGE) t1,
          (SELECT COUNT(*) AS tot_pg FROM PERSON_GROUPS) t2"""
          
def method_overview_sum_geog(request,geog,id):
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
    
    
    
    

# geog can be (country,state,district,block,village)
#id of the geog
#from_date and to_date (optional)
def overview_sum_geog(arg_dict):
    a = ['village','block','district','state','country']
    arg_dict['id'] = str(arg_dict['id'])
    sql = []
    if(arg_dict['geog']!= 'country'):
        for i in range(1,4):
            loc_geog = a[i]
            if(loc_geog == arg_dict['geog']):
                break
            child_geog = a[i-1]
            sql.append("JOIN "+loc_geog.upper() +" "+loc_geog[0]+" on ("+child_geog[0] + "." + loc_geog + "_id = " + loc_geog[0] + ".id)")

        if(arg_dict['geog']!='village'):
            sql.append('WHERE '+ a[a.index(arg_dict['geog'])-1][0] + '.' + arg_dict['geog'] + '_id = '+arg_dict['id']);
            
    sql = '\n'.join(sql)
    return_val = []
    return_val.append("""
    select * from (
    (select count(scr.id) as tot_scr from SCREENING scr """)
    
    if(arg_dict['geog']=='country' and 'from_date' in arg_dict and 'to_date' in arg_dict):
        return_val.append("WHERE scr.DATE between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")
    else:
        if(arg_dict['geog']=='village'):
            return_val.append('WHERE scr.village_id = '+arg_dict['id'])
        else:
            return_val.append("JOIN VILLAGE v on (scr.village_id = v.id)")
            return_val.append(sql);
        if('from_date' in arg_dict and 'to_date' in arg_dict):
            return_val.append("AND scr.DATE between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")

    return_val.append("""
    ) t1
    ,
    (select count(vid.id) as tot_vid from VIDEO vid""")
    if(arg_dict['geog']=='country' and 'from_date' in arg_dict and 'to_date' in arg_dict):
        return_val.append("WHERE VIDEO_PRODUCTION_END_DATE between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")
    else:
        if(arg_dict['geog']=='village'):
            return_val.append('WHERE vid.village_id = '+arg_dict['id'])
        else:
            return_val.append("JOIN VILLAGE v on (vid.village_id = v.id)")
            return_val.append(sql);
        if('from_date' in arg_dict and 'to_date' in arg_dict):
            return_val.append("AND VIDEO_PRODUCTION_END_DATE between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")
            
    return_val.append("""
    ) t2
    ,
    (select count(ado.id) as tot_ado
    from PERSON p
    join PERSON_ADOPT_PRACTICE ado  on (ado.person_id = p.id)""")
    
    if(arg_dict['geog']=='country' and 'from_date' in arg_dict and 'to_date' in arg_dict):
        return_val.append("WHERE ado.DATE_OF_ADOPTION between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")
    else:
        if(arg_dict['geog']=='village'):
            return_val.append('WHERE p.village_id = '+arg_dict['id'])
        else:
            return_val.append("JOIN VILLAGE v on (p.village_id = v.id)")
            return_val.append(sql);
        if('from_date' in arg_dict and 'to_date' in arg_dict):
            return_val.append("AND ado.DATE_OF_ADOPTION between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")
            
    return_val.append("""
    ) t3
    ,
    (select count(distinct vid_pr.practices_id) as tot_pra
    from VIDEO vid
    JOIN VIDEO_related_agricultural_practices vid_pr ON (vid_pr.video_id = vid.id)""")
    
    if(arg_dict['geog']=='country' and 'from_date' in arg_dict and 'to_date' in arg_dict):
        return_val.append("WHERE VIDEO_PRODUCTION_END_DATE between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")
    else:
        if(arg_dict['geog']=='village'):
            return_val.append('WHERE vid.village_id = '+arg_dict['id'])
        else:
            return_val.append("JOIN VILLAGE v on (vid.village_id = v.id)")
            return_val.append(sql);
        if('from_date' in arg_dict and 'to_date' in arg_dict):
            return_val.append("AND VIDEO_PRODUCTION_END_DATE between \'" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']  +"\'")
            
    return_val.append("""
    ) t4
    ,
    (select count(per.id) as tot_per
    from PERSON per""")
    
    if(arg_dict['geog']=='country' and 'from_date' in arg_dict and 'to_date' in arg_dict):
        return_val.append("""WHERE per.id in 
                                (
                                    SELECT vs.person_id
                                    FROM VIDEO_farmers_shown vs, VIDEO v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE between \'""" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']+ """\'
            
                                    UNION
            
                                    SELECT person_id
                                    FROM PERSON_ADOPT_PRACTICE
                                    WHERE DATE_OF_ADOPTION between \'""" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']+ """\'
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM PERSON_MEETING_ATTENDANCE pa, SCREENING sc
                                    WHERE pa.screening_id = sc.id
                                    AND sc.DATE between \'""" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date']+ """\'
                                )""")
    else:
        if(arg_dict['geog']=='village'):
            return_val.append('WHERE per.village_id = '+arg_dict['id'])
        else:
            return_val.append("JOIN VILLAGE v on (per.village_id = v.id)")
            return_val.append(sql);
        if('from_date' in arg_dict and 'to_date' in arg_dict):
            return_val.append("""AND  per.id in 
                                (
                                    SELECT vs.person_id
                                    FROM VIDEO_farmers_shown vs, VIDEO v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE between \'""" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date'] + """\'
            
                                    UNION
            
                                    SELECT person_id
                                    FROM PERSON_ADOPT_PRACTICE
                                    WHERE DATE_OF_ADOPTION between \'""" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date'] + """\'
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM PERSON_MEETING_ATTENDANCE pa, SCREENING sc
                                    WHERE pa.screening_id = sc.id
                                    AND sc.DATE between \'""" + arg_dict['from_date'] + "\' and \'" + arg_dict['to_date'] + """\'
                                )""")
            
            
    return_val.append("""
    ) t5
    """)

    if(arg_dict['geog']!='country'):
        return_val.append(",(SELECT " + arg_dict['geog'].upper() + "_NAME as name from " + arg_dict['geog'].upper() + " where id = " +arg_dict['id'] + ") t6")
        
    return_val.append(')')

    
    return '\n'.join(return_val)


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