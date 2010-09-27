from dg.output.database.utility import *


#Query for the drop down menu in search box
def search_drop_down_list(geog, geog_parent, id):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(['id', geog.upper()+'_NAME as name'])
    sql_ds['from'].append(geog.upper())
    if(geog.upper() != "STATE"):
        sql_ds['where'].append(geog_parent.lower()+'_id = '+str(id))
    sql_ds['order by'].append('name')
    
    return join_sql_ds(sql_ds)

#Query for breadcrumbs
#Params: geog - options to be calculated for this geog
#               id - id of 'geog' if is_child = false else it's parent geog's id
#               is_child: flag(0/1) if the options are one level below then selected
#                               e.g for district 'x', option for x's blocks must be presented with nothing pre-selected.
def breadcrumbs_options_sql(geog,id, is_child):
    geog_list = ['VILLAGE','BLOCK','DISTRICT','STATE'];

    if(geog=='STATE'):
        return 'SELECT id, STATE_NAME as name FROM STATE'

    par_geog = geog_list[geog_list.index(geog)+1];

    if(is_child == 1):
        return construct_query(""" SELECT id, {{geog}}_NAME
                FROM {{geog}}
                WHERE {{par_geog|lower}}_id = {{id}}
        """,dict(geog=geog,id=id,par_geog=par_geog))

    return construct_query("""SELECT {{geog|first}}1.id ,{{geog|first}}1.{{geog|upper}}_NAME, {{geog|first}}1.{{par_geog}}_id
    FROM {{geog}} {{geog|first}}1, {{geog}} {{geog|first}}2
    WHERE {{geog|first}}1.{{par_geog|lower}}_id = {{geog|first}}2.{{par_geog|lower}}_id
            and {{geog|first}}2.id = {{id}}""",dict(geog=geog,par_geog=par_geog,id=id))


#Generates SQL for getting Partner_ID, Partner_name given Geog, id.
#Returns '' if geography!= country or geography!=state
def get_partners_sql(geog, id):
    if geog not in ["COUNTRY", "STATE"]:
        return ''

    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(["DISTINCT P.id", "P.PARTNER_NAME"])
    sql_ds['from'].append("DISTRICT D")
    sql_ds['join'].append(["PARTNERS P", "P.id = D.partner_id"])
    if (geog=="STATE"):
        sql_ds['where'].append("D.state_id = "+str(id))

    return join_sql_ds(sql_ds);

def child_geog_list(geog, id, from_date, to_date, partners):
    if(geog == "COUNTRY"):
        sql = "SELECT DISTINCT S.id, STATE_NAME AS name from STATE S"
        if(partners):
            sql+=  """ JOIN DISTRICT D ON (D.state_id = S.id)
                      WHERE D.partner_id in ("""+','.join(partners)+")"
    elif(geog == "STATE"):
        sql = """SELECT DISTINCT D.id, DISTRICT_NAME AS name from DISTRICT D
                          WHERE state_id = """+str(id)
        if(partners):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            filtered_partner_list = [str(x[0]) for x in dist_part if str(x[0]) in partners]
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

#Query for the table in overview module and pie graphs.
#Parameter Required:'type' can be (production/screening/adoption/practice/person/village)
def overview(geog, id, from_date, to_date, partners, type):
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']

    if(geog == 'VILLAGE'):
        geog_child = 'VILLAGE'
    else:
        geog_child = geog_list[geog_list.index(geog)+1]

    date_field = main_tab_abb = ''
    sql_ds = get_init_sql_ds();
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
    elif(type=='village'):
        sql_ds['select'].append('COUNT(DISTINCT SC.village_id) as tot_vil')
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
        sql_ds['select'].append('COUNT(DISTINCT TAB.person_id) as tot_per')
        sql_ds['from'].append("""(
        SELECT person_id, min(date) as DATE
        FROM (
                SELECT  vs.person_id, VIDEO_PRODUCTION_END_DATE AS date
                FROM VIDEO_farmers_shown vs, VIDEO vid
                WHERE vs.video_id = vid.id

                UNION

                SELECT  pa.person_id, DATE
                FROM PERSON_MEETING_ATTENDANCE pa, SCREENING sc
                WHERE pa.screening_id = sc.id ) TMP
                GROUP BY person_id
        )AS TAB""")
        sql_ds['join'].append(['PERSON P',"TAB.person_id = P.id"])
        main_tab_abb = 'P'
        date_field = "TAB.DATE"
    if(geog=="COUNTRY"):
        #Hacking attach_geog_date for attaching geography till state in country case.
        attach_geog_date(sql_ds,main_tab_abb,date_field,'STATE',0, from_date,to_date)
        sql_ds['where'].pop();
        if(partners):
            sql_ds['where'].append("D.id in (SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(partners)+"))")
        sql_ds['lojoin'].append(['STATE S','S.id = D.state_id']);
    else:
        filter_partner_geog_date(sql_ds,main_tab_abb,date_field,geog,id,from_date,to_date,partners)

    sql_ds['group by'].append(geog_child.lower()+"_id")
    sql_ds['order by'].append(geog_child.lower()+"_id")

    return join_sql_ds(sql_ds);

#Query for Line Chart in Overview module. It returns date and count of the metric on that date.
#Context Required:'type' can be (production/screening/adoption/practice/person)
def overview_line_chart(geog,id,from_date, to_date, partners,type):
    sql_ds = get_init_sql_ds();
    sql_inn_ds = get_init_sql_ds();

    if(type=='practice'):
        sql_ds['select'].extend(["date", "COUNT(*)"])

        sql_inn_ds = get_init_sql_ds();
        sql_inn_ds['select'].extend(["VRAP.practices_id" , "MIN(VIDEO_PRODUCTION_END_DATE) AS date"])
        sql_inn_ds['from'].append("VIDEO VID");
        sql_inn_ds['join'].append(["VIDEO_related_agricultural_practices VRAP","VRAP.video_id = VID.id"])
        filter_partner_geog_date(sql_inn_ds,'VID','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("practices_id");

        sql_ds['from'].append('('+join_sql_ds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
    elif(type=='person'):
        sql_ds['select'].extend(["date", "COUNT(*)"])

        sql_inn_ds = get_init_sql_ds();
        sql_inn_ds['select'].extend(["person_id", "MIN(date) as date"])
        sql_inn_ds['from'].append("""(
                SELECT  vs.person_id, VIDEO_PRODUCTION_END_DATE AS date
                FROM VIDEO_farmers_shown vs, VIDEO vid
                WHERE vs.video_id = vid.id

                UNION

                SELECT  pa.person_id, DATE
                FROM PERSON_MEETING_ATTENDANCE pa, SCREENING sc
                WHERE pa.screening_id = sc.id

        ) as tab""");
        if(geog!="COUNTRY" or partners):
            sql_inn_ds['join'].append(["PERSON P","P.id = tab.person_id"])
            filter_partner_geog_date(sql_inn_ds,'P','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("tab.person_id");

        sql_ds['from'].append('('+join_sql_ds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
    elif(type=='production'):
        sql_ds['select'].extend(["VIDEO_PRODUCTION_END_DATE as date", "count(*)"])
        sql_ds['from'].append("VIDEO VID");
        filter_partner_geog_date(sql_ds,'VID','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("VIDEO_PRODUCTION_END_DATE");
    elif(type=='screening'):
        sql_ds['select'].extend(["DATE AS date", "count(*)"])
        sql_ds['from'].append("SCREENING SC");
        filter_partner_geog_date(sql_ds,'SC','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("DATE");
    elif(type=='adoption'):
        sql_ds['select'].extend(["DATE_OF_ADOPTION AS date", "count(*)"])
        sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP");
        if(geog!="COUNTRY" or partners):
            sql_ds['join'].append(["PERSON P","P.id = PAP.person_id"])
            filter_partner_geog_date(sql_ds,'P','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("DATE_OF_ADOPTION");
    elif(type=='village'):
        if(geog not in ["COUNTRY", "STATE", "DISTRICT"]):
            return ""
        sql_ds['select'].extend(["DISTINCT DATE as date, village_id"])
        sql_ds['from'].append("SCREENING SC")
        filter_partner_geog_date(sql_ds,'SC','dummy',geog,id,None,None,partners)
        

    if(from_date is not None and to_date is not None):
        sql_ds['having'].append("date between '"+from_date+"' and '"+to_date+"'")

    return join_sql_ds(sql_ds)


#'type' can be prod_tar/screen_tar/adopt_tar
def target_lines(geog,id, from_date, to_date, partners, type):
    sql_ds = get_init_sql_ds();

    if(geog == 'STATE'):
        sql_ds['join'].append(["DISTRICT D", "D.id = D_T.district_id"])
        sql_ds['where'].append("D.state_id = "+str(id))
        if(partners):
            sql_ds['where'].append("D.partner_id IN ("+','.join(partners)+")")
    elif(geog == 'DISTRICT'):
        sql_ds['where'].append("D_T.district_id = "+str(id))
    elif(geog == "COUNTRY"):
        if(partners):
            sql_ds['join'].append(["DISTRICT D", "D.id = D_T.district_id"])
            sql_ds['where'].append("D.partner_id IN ("+','.join(partners)+")")
    else:
        return '';
    if(from_date and to_date):
        sql_ds['where'].append("month_year  BETWEEN '"+from_date+"' AND '"+to_date+"'")
    sql_ds['select'].append('month_year as date')
    sql_ds['from'].append("dashboard_target D_T")

    if(type=='screen_tar'):
        sql_ds['select'].append("disseminations")
        sql_ds['where'].append("disseminations IS NOT NULL")
    elif(type=='prod_tar'):
        sql_ds['select'].append("video_production")
        sql_ds['where'].append("video_production IS NOT NULL")
    elif(type=='adopt_tar'):
        sql_ds['select'].append('disseminations*adoption_per_dissemination')
        sql_ds['where'].append("disseminations*adoption_per_dissemination IS NOT NULL")
    else:
        return ""

    return join_sql_ds(sql_ds);


#Query for number of distinct persons who attended a screening in the past 60 days from 'to_date'
def tot_dist_attendees_60_days(geog, id, to_date, partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("COUNT(DISTINCT person_id) as tot_per")
    sql_ds['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    sql_ds['join'].append(["SCREENING SC","SC.id = PMA.screening_id"])
    sql_ds['where'].append("DATE BETWEEN SUBDATE('"+to_date+"',INTERVAL 60 DAY) AND '"+to_date+"'")
    filter_partner_geog_date(sql_ds,"SC","DUMMY",geog,id,None,None,partners)
    
    return join_sql_ds(sql_ds);

def tot_dist_adopt_60_days(geog, id, to_date, partners):
    inner_sql = get_init_sql_ds()
    inner_sql['select'].append("DISTINCT person_id")
    inner_sql['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    inner_sql['join'].append(["SCREENING SC","SC.id = PMA.screening_id"])
    inner_sql['where'].append("DATE BETWEEN SUBDATE('"+to_date+"',INTERVAL 60 DAY) AND '"+to_date+"'")
    filter_partner_geog_date(inner_sql,"SC","DUMMY",geog,id,None,None,partners)
    
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("COUNT(DISTINCT person_id) as tot_adop_per")
    sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP")
    sql_ds['where'].append("person_id IN ("+join_sql_ds(inner_sql)+")")
    
    return join_sql_ds(sql_ds)