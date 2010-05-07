from dg.output.database.utility import *


#Query for the drop down menu in search box
#Context Required: geog can be (state/district/block/village(
#                  id for(district/block/village)
#                  geog_parent (e.g. 'state'->'district'->'block'->'village'
search_drop_down_list = r"""
    SELECT id, {{geog|upper}}_NAME AS name
    FROM {{geog|upper}}
    {% ifnotequal geog 'state' %}
    WHERE {{geog_parent}}_id = {{id}}
    {% endifnotequal %}
    ORDER BY name
"""


#Query for breadcrumbs
#Params: geog - options to be calculated for this geog
#        id - id of 'geog' if is_child = false else it's parent geog's id
#        is_child: flag(0/1) if the options are one level below then selected
#                e.g for district 'x', option for x's blocks must be presented with nothing pre-selected.
def breadcrumbs_options_sql(geog,id, is_child):
    geog_list = ['village','block','district','state'];
    
    if(geog=='state'):
        return 'SELECT id, STATE_NAME as name FROM STATE'
    
    par_geog = geog_list[geog_list.index(geog)+1]; 
    
    if(is_child == 1):
        return construct_query(""" SELECT id, {{geog|upper}}_NAME 
            FROM {{geog|upper}}
            WHERE {{par_geog}}_id = {{id}}
        """,dict(geog=geog,id=id,par_geog=par_geog))
    
    return construct_query("""SELECT {{geog|first}}1.id ,{{geog|first}}1.{{geog|upper}}_NAME, {{geog|first}}1.{{par_geog}}_id
    FROM {{geog|upper}} {{geog|first}}1, {{geog|upper}} {{geog|first}}2
    WHERE {{geog|first}}1.{{par_geog}}_id = {{geog|first}}2.{{par_geog}}_id
        and {{geog|first}}2.id = {{id}}""",dict(geog=geog,par_geog=par_geog,id=id))


#Generates SQL for getting Partner_ID, Partner_name given Geog, id. 
#Returns '' if geography!= country or geography!=state
def get_partners_sql(geog, id):
    geog = geog.upper()
    if geog not in ["COUNTRY", "STATE"]:
        return ''
    
    sql_ds = getInitSQLds()
    sql_ds['select'].extend(["DISTINCT P.id", "P.PARTNER_NAME"])
    sql_ds['from'].append("DISTRICT D")
    sql_ds['join'].append(["PARTNERS P", "P.id = D.partner_id"])
    if (geog=="STATE"):
        sql_ds['where'].append("D.state_id = "+str(id))
    
    return joinSQLds(sql_ds);

def child_geog_list(request, geog, id):
    from_date, to_date, partner_id = getDatesPartners(request)
    geog = geog.upper()
    if(geog == "COUNTRY"):
        sql = "SELECT DISTINCT S.id, STATE_NAME AS name from STATE S"
        if(partner_id):
            sql+=  """ JOIN DISTRICT D ON (D.state_id = S.id)
                  WHERE D.partner_id in ("""+','.join(partner_id)+")"
    elif(geog == "STATE"):
        sql = """SELECT DISTINCT D.id, DISTRICT_NAME AS name from DISTRICT D
                  WHERE state_id = """+str(id)
        if(partner_id):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            filtered_partner_list = [str(x[0]) for x in dist_part if str(x[0]) in partner_id]
            if(filtered_partner_list):
                sql += " AND D.partner_id in ("+','.join(filtered_partner_list)+")"
    elif(geog == 'DISTRICT'):
        sql="SELECT id, BLOCK_NAME as name FROM BLOCK where district_id = "+str(id)
    elif(geog == "BLOCK"):
        sql="SELECT id, VILLAGE_NAME AS name FROM VILLAGE WHERE block_id = "+str(id)
    elif(geog == "VILLAGE"):
        sql="SELECT id, VILLAGE_NAME AS name FROM VILLAGE WHERE id = "+str(id);
    else:
        sql = ''
    
    return sql;

#Query for Total Video Production in Overview module
#Parameter Required:'type' can be (production/screening/adoption/practice/person)
def overview(request, geog,id, type):
    geog = geog.upper();
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    from_date, to_date, partners = getDatesPartners(request)
    
    if(geog == 'VILLAGE'):
        geog_child = 'VILLAGE'
    else:
        geog_child = geog_list[geog_list.index(geog)+1]
    
    date_field = main_tab_abb = ''
    sql_ds = getInitSQLds();
    if(geog=="VILLAGE"):
        sql_ds['select'].append("village_id as id")
    else:
        sql_ds['select'].append(geog_child[0]+".id as id")
    if(type == 'production'):
        sql_ds['select'].append('COUNT(DISTINCT VID.id) as tot_pro')
        sql_ds['from'].append('VIDEO VID')
        main_tab_abb = "VID"
        date_field = "VID.VIDEO_PRODUCTION_END_DATE"
    elif(type=='screening'):
        sql_ds['select'].append('COUNT(DISTINCT SC.id) as tot_scr')
        sql_ds['from'].append('SCREENING SC')
        main_tab_abb = "SC"
        date_field = "SC.DATE"
    elif(type=='adoption'):
        sql_ds['select'].append('COUNT(DISTINCT PAP.id) as tot_ado')
        sql_ds['from'].append('PERSON_ADOPT_PRACTICE PAP')
        sql_ds['lojoin'].append(['PERSON P','P.id = PAP.person_id'])
        main_tab_abb = "P"
        date_field = "PAP.DATE_OF_ADOPTION"
    elif(type=='practice'):
        sql_ds['select'].append('COUNT(DISTINCT VRAP.practices_id) as tot_pra')
        sql_ds['from'].append('VIDEO_related_agricultural_practices VRAP')
        sql_ds['lojoin'].append(['VIDEO VID','VID.id = VRAP.video_id'])
        main_tab_abb = 'VID'
        date_field = "VID.VIDEO_PRODUCTION_END_DATE"
    elif(type=='person'):
        sql_ds['select'].append('COUNT(DISTINCT P.id) as tot_per')
        sql_ds['from'].append('PERSON P')
        main_tab_abb = 'P'
        if(from_date is not None and to_date is not None):
            sql_ds['join'].append(["""(
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
            
    
    if(geog=="COUNTRY"):
        #Hacking attachGeogDate for attaching geography till state in country case.
        attachGeogDate(sql_ds,main_tab_abb,date_field,'state',0, from_date,to_date)
        sql_ds['where'].pop();
        if(partners):
            sql_ds['where'].append("D.id in (SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(partners)+"))")
        sql_ds['lojoin'].append(['STATE S','S.id = D.state_id']);
    else:
        filterPartnerGeogDate(sql_ds,main_tab_abb,date_field,geog,id,from_date,to_date,partners)
    
    sql_ds['group by'].append(geog_child.lower()+"_id")
    sql_ds['order by'].append(geog_child.lower()+"_id")
    
    return joinSQLds(sql_ds);
    
#Query for Line Chart in Overview module. It returns date and count of the metric on that date.
#Context Required:'type' can be (production/screening/adoption/practice/person)
def overview_line_chart(request,geog,id,type):
    sql_ds = getInitSQLds();
    sql_inn_ds = getInitSQLds();
    from_date, to_date, partners = getDatesPartners(request)
    
    if(type=='practice'):
        sql_ds['select'].extend(["date", "COUNT(*)"])
        
        sql_inn_ds = getInitSQLds();
        sql_inn_ds['select'].extend(["VRAP.practices_id" , "MIN(VIDEO_PRODUCTION_END_DATE) AS date"])
        sql_inn_ds['from'].append("VIDEO VID");
        sql_inn_ds['join'].append(["VIDEO_related_agricultural_practices VRAP","VRAP.video_id = VID.id"])
        filterPartnerGeogDate(sql_inn_ds,'VID','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("practices_id");
        
        sql_ds['from'].append('('+joinSQLds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
    elif(type=='person'):
        sql_ds['select'].extend(["date", "COUNT(*)"])
        
        sql_inn_ds = getInitSQLds();
        sql_inn_ds['select'].extend(["person_id", "MIN(date) as date"])
        sql_inn_ds['from'].append("""(
            SELECT  vs.person_id, VIDEO_PRODUCTION_END_DATE AS date
            FROM VIDEO_farmers_shown vs, VIDEO vid
            WHERE vs.video_id = vid.id

            UNION

            SELECT  person_id , DATE_OF_ADOPTION AS date
            FROM PERSON_ADOPT_PRACTICE pa

            UNION

            SELECT  pa.person_id, DATE
            FROM PERSON_MEETING_ATTENDANCE pa, SCREENING sc
            WHERE pa.screening_id = sc.id

        ) as tab""");
        if(geog.upper()!="COUNTRY" or partners):
            sql_inn_ds['join'].append(["PERSON P","P.id = tab.person_id"])
            filterPartnerGeogDate(sql_inn_ds,'P','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("tab.person_id");
        
        sql_ds['from'].append('('+joinSQLds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
    elif(type=='production'):
        sql_ds['select'].extend(["VIDEO_PRODUCTION_END_DATE as date", "count(*)"])
        sql_ds['from'].append("VIDEO VID");
        filterPartnerGeogDate(sql_ds,'VID','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("VIDEO_PRODUCTION_END_DATE");
    elif(type=='screening'):
        sql_ds['select'].extend(["DATE AS date", "count(*)"])
        sql_ds['from'].append("SCREENING SC");
        filterPartnerGeogDate(sql_ds,'SC','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("DATE");
    elif(type=='adoption'):
        sql_ds['select'].extend(["DATE_OF_ADOPTION AS date", "count(*)"])
        sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP");
        if(geog.upper()!="COUNTRY" or partners):
            sql_ds['join'].append(["PERSON P","P.id = PAP.person_id"])
            filterPartnerGeogDate(sql_ds,'P','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("DATE_OF_ADOPTION");
        
    if(from_date is not None and to_date is not None):
        sql_ds['having'].append("date between '"+from_date+"' and '"+to_date+"'")
        
    return joinSQLds(sql_ds)