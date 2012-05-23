from output.database.utility import *


#Query for the drop down menu in search box
def search_drop_down_list(geog, geog_parent, id):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(['id', geog.upper()+'_NAME as name'])
    sql_ds['from'].append(geog.upper())
    if(geog.upper() != "COUNTRY"):
        sql_ds['where'].append(geog_parent.lower()+'_id = '+str(id))
    sql_ds['order by'].append('name')
    
    return join_sql_ds(sql_ds)

#Query for breadcrumbs
#Params: geog - options to be calculated for this geog
#               id - id of 'geog' if is_child = false else it's parent geog's id
#               is_child: flag(0/1) if the options are one level below then selected
#                               e.g for district 'x', option for x's blocks must be presented with nothing pre-selected.
def breadcrumbs_options_sql(geog, id, is_child):
    geog_list = ['VILLAGE','BLOCK','DISTRICT','STATE','COUNTRY'];

    if(geog=='COUNTRY'):
        return 'SELECT id, COUNTRY_NAME as name FROM COUNTRY'

    par_geog = geog_list[geog_list.index(geog)+1];

    sql_ds = get_init_sql_ds()
    if(is_child == 1):
        sql_ds['select'].extend(['id', geog+'_NAME'])
        sql_ds['from'].append(geog)
        sql_ds['where'].append(par_geog.lower()+'_id = '+str(id))
    else:
        #SQL for filtering all geography below the parent geog. For e.g. - Will filter all India states, if Bihar is passed in geog, id
        sql_ds['select'].extend([geog[0] + '1.id' ,"%s1.%s_NAME" %(geog[0], geog.upper()), "%s1.%s_id" % (geog[0], par_geog)])
        sql_ds['from'].append("%s %s1" % (geog, geog[0]))
        sql_ds['join'].append(["%s %s2" % (geog, geog[0]),'%s1.%s_id = %s2.%s_id' %(geog[0], par_geog, geog[0], par_geog)])
        sql_ds['where'].append("%s2.id = %s" % (geog[0], str(id)))

    return join_sql_ds(sql_ds)


#Generates SQL for getting Partner_ID, Partner_name given Geog, id.
#Returns '' if geography!= country or geography!=state
def get_partners_sql(geog, id):
    if geog not in [None, "COUNTRY", "STATE"]:
        return ''

    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(["DISTINCT P.id", "P.PARTNER_NAME"])
    sql_ds['from'].append("DISTRICT D")
    sql_ds['join'].append(["PARTNERS P", "P.id = D.partner_id"])
    if (geog=="STATE"):
        sql_ds['where'].append("D.state_id = "+str(id))
    elif(geog=="COUNTRY"):
        sql_ds['join'].append(["STATE S", "S.id = D.state_id"])
        sql_ds['where'].append("S.country_id = " + str(id))

    return join_sql_ds(sql_ds);

def child_geog_list(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds()
    if(geog == None):
        sql_ds['select'].extend(['DISTINCT C.id', 'COUNTRY_NAME AS name'])
        sql_ds['from'].append("COUNTRY C")
        if(partners):
            sql_ds['join'].append(['STATE S', 'S.country_id = C.id'])
            sql_ds['join'].append(['DISTRICT D', 'D.state_id = S.id'])
            sql_ds['where'].append("D.partner_id in ("+','.join(partners)+")")
    elif(geog == "COUNTRY"):
        sql_ds['select'].extend(['DISTINCT S.id', 'STATE_NAME AS name'])
        sql_ds['from'].append("STATE S")
        sql_ds['where'].append("S.country_id = " + str(id))
        if(partners):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT D JOIN STATE S ON S.id = D.state_id WHERE country_id = "+str(id))
            filtered_partner_list = [str(x[0]) for x in dist_part if str(x[0]) in partners]
            if(filtered_partner_list):
                sql_ds['join'].append(["DISTRICT D", "S.id = D.state_id"])
                sql_ds['where'].append("D.partner_id in ("+','.join(filtered_partner_list)+")")
    elif(geog == "STATE"):
        sql_ds['select'].extend(['DISTINCT D.id', 'DISTRICT_NAME AS name'])
        sql_ds['from'].append("DISTRICT D")
        sql_ds['where'].append("state_id = " + str(id))
        if(partners):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            filtered_partner_list = [str(x[0]) for x in dist_part if str(x[0]) in partners]
            if(filtered_partner_list):
                sql_ds['where'].append("D.partner_id in ("+','.join(filtered_partner_list)+")")
    elif(geog == 'DISTRICT'):
        sql_ds['select'].extend(['id', 'BLOCK_NAME as name'])
        sql_ds['from'].append('BLOCK B')
        sql_ds['where'].append("district_id = " + str(id))
    elif(geog == "BLOCK"):
        sql_ds['select'].extend(['id', 'VILLAGE_NAME AS name'])
        sql_ds['from'].append("VILLAGE V")
        sql_ds['where'].append("block_id = " + str(id))
    elif(geog == "VILLAGE"):
        sql_ds['select'].extend(['id', 'VILLAGE_NAME AS name'])
        sql_ds['from'].append("VILLAGE V")
        sql_ds['where'].append("id = " + str(id))
        sql="SELECT id, VILLAGE_NAME AS name FROM VILLAGE WHERE id = "+str(id);

    return join_sql_ds(sql_ds);

#Query for the table in overview module and pie graphs.
#Parameter Required:'type' can be (production/screening/adoption/practice/person/village)
def overview(geog, id, from_date, to_date, partners, type):
    geog_list = [None, 'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']

    if(geog == 'VILLAGE'):
        geog_child = 'VILLAGE'
    else:
        geog_child = geog_list[geog_list.index(geog)+1]

    date_field = main_tab_abb = ''
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append(geog_child.lower()+"_id as id")
    if(type == 'production'):
        sql_ds['select'].append('COUNT(DISTINCT VID.id) as tot_pro')
        sql_ds['from'].append('VIDEO VID')
        sql_ds['where'].append('VID.VIDEO_SUITABLE_FOR = 1')
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
        if(from_date and to_date):
            sql_ds['select'].append('COUNT(DISTINCT PMA.person_id) as tot_per')
            sql_ds['from'].append('PERSON_MEETING_ATTENDANCE PMA')
            sql_ds['join'].append(['SCREENING SC', 'SC.id = PMA.screening_id'])
            main_tab_abb = "SC"
            date_field = "SC.DATE"
        else:
            sql_ds['select'].append('COUNT(P.id) as tot_per')
            sql_ds['from'].append("PERSON P")
            sql_ds['where'].append("P.date_of_joining is not NULL")
            main_tab_abb = 'P'
            date_field = "P.date_of_joining"
    if(geog==None):
         #Hacking attach_geog_date for attaching geography till state in country case.
         attach_geog_date(sql_ds,main_tab_abb,date_field,'COUNTRY',0, from_date,to_date)
         sql_ds['where'].pop();
         if(partners):
             sql_ds['where'].append("district_id in (SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(partners)+"))")
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
        sql_ds['select'].extend(["date_of_joining as date", "COUNT(*)"])
        sql_ds['from'].append("PERSON P")
        sql_ds['where'].append("P.date_of_joining is not NULL")
        filter_partner_geog_date(sql_ds,"P",'dummy',geog,id,None,None,partners)
        sql_ds['group by'].append('date');
    elif(type=='production'):
        sql_ds['select'].extend(["VIDEO_PRODUCTION_END_DATE as date", "count(*)"])
        sql_ds['from'].append("VIDEO VID");
        sql_ds['where'].append('VID.VIDEO_SUITABLE_FOR = 1')
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
        if(geog!=None or partners):
            sql_ds['join'].append(["PERSON P","P.id = PAP.person_id"])
            filter_partner_geog_date(sql_ds,'P','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("DATE_OF_ADOPTION");
    elif(type=='village'):
        if(geog not in [None, "COUNTRY", "STATE", "DISTRICT"]):
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
        sql_ds['join'].append(["DISTRICT D", "D.id = D_T.district_id"])
        sql_ds['join'].append(["STATE S", "S.id = D.state_id"])
        sql_ds['where'].append("S.country_id = "+str(id))
        if(partners):
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
def tot_dist_attendees_adopt_60_days(geog, id, to_date,partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(["COUNT(DISTINCT PMA.person_id) as tot_per", "COUNT(DISTINCT PAP.person_id) as tot_adop_per", "COUNT(DISTINCT PAP.id) as tot_active_adop"])
    sql_ds['from'].append("SCREENING SC")
    sql_ds['lojoin'].append(["PERSON_MEETING_ATTENDANCE PMA", "PMA.screening_id = SC.id"])
    sql_ds['lojoin'].append(["PERSON_ADOPT_PRACTICE PAP", "PAP.person_id = PMA.person_id"])
    sql_ds['where'].append("DATE BETWEEN SUBDATE('"+to_date+"',INTERVAL 60 DAY) AND '"+to_date+"'")
    filter_partner_geog_date(sql_ds,"SC","DUMMY",geog,id,None,None,partners)
    
    return join_sql_ds(sql_ds);

def tot_attendance(geog, id, from_date, to_date, partners):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append("COUNT(PMA.id) as count")
    sql_ds['from'].append("PERSON_MEETING_ATTENDANCE PMA")
    if geog is not None or partners or (from_date and to_date):
        sql_ds['lojoin'].append(["SCREENING SC", "SC.id = PMA.screening_id"])
        filter_partner_geog_date(sql_ds,"SC","SC.DATE",geog,id,from_date,to_date,partners)
        
    return join_sql_ds(sql_ds)

def adoption_rate(geog, id, to_date,partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(['SUM(total_adopted_attendees) AS tot_adopt_per ', 'SUM(total_active_attendees) AS tot_per', 'SUM(total_adoption_by_active) AS tot_active_adop'])
    sql_ds['from'].append("village_precalculation VP")
    sql_ds['where'].append("date = '%s'" % str(to_date))
    filter_partner_geog_date(sql_ds, "VP", "DUMMY", geog, id, None, None, partners)
    
    return join_sql_ds(sql_ds);

def get_start_date(geog, id):
    geog = geog.upper() if geog is not None else None
    sql_ds = get_init_sql_ds()
    if geog is None:
        sql_ds['select'].append("MIN(START_DATE) AS date")
        sql_ds['from'].append("COUNTRY C")
    elif geog in ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']:
        sql_ds['select'].append("START_DATE AS date")
        sql_ds['from'].append(geog + " " + geog[0])
        sql_ds['where'].append("id = " + str(id))
    else:
        raise Exception("Invalid Geography " + geog)
        
    return join_sql_ds(sql_ds)
    