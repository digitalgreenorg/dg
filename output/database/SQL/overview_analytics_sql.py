from dg.output.database.utility import *

#Query for extra data for country in Overview page
def overview_nation_pg_vil_total():
    return """SELECT * FROM
          (SELECT COUNT(*) AS tot_vil FROM VILLAGE) t1,
          (SELECT COUNT(*) AS tot_pg FROM PERSON_GROUPS) t2"""
#Type is an list which can have 'production', 'screening','person', 'adoption', 'practice'
def overview_sum_geog(geog, id, from_date, to_date, partner_id, type=None):
    geog_list = [None,"COUNTRY","STATE","DISTRICT","BLOCK","VILLAGE"]
    geog_par = geog_list[geog_list.index(geog)-1]

    sc_sql = get_init_sql_ds()
    sc_sql['select'].append("COUNT(SC.id) as tot_scr");
    sc_sql['from'].append("SCREENING SC");
    filter_partner_geog_date(sc_sql,"SC","SC.DATE",geog,id,from_date,to_date,partner_id);

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

    filter_partner_geog_date(per_sql,"P","TAB.DATE",geog,id,from_date,to_date,partner_id);

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
    else:
        combined_sql =  [join_sql_ds(sc_sql), join_sql_ds(vid_sql), join_sql_ds(ado_sql), join_sql_ds(pra_sql), join_sql_ds(per_sql)]
    
    
    combined_sql = ['('+combined_sql[i]+') t'+str(i) for i in range(0,len(combined_sql))]
    if(geog=='COUNTRY'):
        combined_sql.append("(SELECT 'India' as name) t5")
    elif(geog=='STATE'):
        combined_sql.append("(SELECT " + geog + "_NAME as name, 1 as id FROM " + geog + " WHERE id = " +str(id) + ") t5")
    else:
        combined_sql.append("(SELECT " + geog + "_NAME as name, "+geog_par.lower()+"_id as id FROM " + geog + " WHERE id = " +str(id) + ") t5")
    combined_sql = ',\n'.join(combined_sql)

    return 'SELECT * FROM ( '+combined_sql+')'

def overview_min_date(request, geog, id):
    from_date, to_date, partner_id = get_dates_partners(request)

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

#Returns parent level region id
def overview_parent_id(arg_dict):
    sql = []
    if 'geog' in arg_dict:
        if arg_dict['geog'] == 'DISTRICT':
            sql.append(r"""SELECT state_id as id FROM DISTRICT d WHERE d.id =  """+str(arg_dict['id']) )

        elif arg_dict['geog'] == 'BLOCK':
            sql.append(r""" SELECT district_id as id FROM BLOCK b WHERE b.id =  """+str(arg_dict['id']) )

        elif arg_dict['geog'] == 'VILLAGE':
            sql.append(r""" SELECT vil.block_id as id, b.BLOCK_NAME AS name FROM VILLAGE vil, BLOCK b WHERE vil.block_id = b.id and vil.id =  """+str(arg_dict['id']) )
        elif arg_dict['geog'] == 'COUNTRY':
            sql.append(r'SELECT 1 AS id ')
        elif arg_dict['geog'] == 'STATE':
            sql.append(r'SELECT 1 AS id ')


    return ''.join(sql)
