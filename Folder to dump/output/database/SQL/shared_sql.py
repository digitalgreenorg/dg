from output.database.utility import *


#Query for the drop down menu in search box
def search_drop_down_list(geog, geog_parent, id):
    sql_ds = get_init_sql_ds();
    sql_ds['select'].extend(['id', geog.upper()+'_NAME as name'])
    sql_ds['from'].append('geographies_%s' % geog.upper())
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
        return 'SELECT id, COUNTRY_NAME as name FROM geographies_COUNTRY'

    par_geog = geog_list[geog_list.index(geog)+1];

    sql_ds = get_init_sql_ds()
    if(is_child == 1):
        sql_ds['select'].extend(['id', geog+'_NAME'])
        sql_ds['from'].append('geographies_%s' % geog)
        sql_ds['where'].append(par_geog.lower()+'_id = '+str(id))
    else:
        #SQL for filtering all geography below the parent geog. For e.g. - Will filter all India states, if Bihar is passed in geog, id
        sql_ds['select'].extend([geog[0] + '1.id' ,"%s1.%s_NAME" %(geog[0], geog.upper()), "%s1.%s_id" % (geog[0], par_geog)])
        sql_ds['from'].append("geographies_%s %s1" % (geog, geog[0]))
        sql_ds['join'].append(["geographies_%s %s2" % (geog, geog[0]),'%s1.%s_id = %s2.%s_id' %(geog[0], par_geog, geog[0], par_geog)])
        sql_ds['where'].append("%s2.id = %s" % (geog[0], str(id)))

    return join_sql_ds(sql_ds)


#Generates SQL for getting Partner_ID, Partner_name given Geog, id.
#Returns '' if geography!= country or geography!=state

def practice_options_sql(sec, subsec, top, subtop, sub):
    sql_ds =  get_init_sql_ds()
    sql_ds['select'].extend(["S.ID","S.name","SS.ID","SS.name","T.ID","T.name","ST.ID","ST.name","SUB.ID","SUB.name"])
    sql_ds['from'].append("videos_practice P")
    sql_ds['lojoin'].append(["videos_practicesector S", "S.id = P.practice_sector_id"])
    sql_ds['lojoin'].append(["videos_practicesubsector SS", "SS.id = P.practice_subsector_id"])
    sql_ds['lojoin'].append(["videos_practicesubtopic ST", "ST.id = P.practice_subtopic_id"])
    sql_ds['lojoin'].append(["videos_practicetopic T", "T.id = P.practice_topic_id"])
    sql_ds['lojoin'].append(["videos_practicesubject SUB", "SUB.id = P.practice_subject_id"])
    sql_ds['join'].append(["videos_video vid", "vid.related_practice_id = P.id"])
    if(sec):
        sql_ds['where'].append('practice_sector_id = %s' % sec)
    if(subsec):
        sql_ds['where'].append('practice_subsector_id = %s' % subsec)
    if(top):
        sql_ds['where'].append('practice_topic_id = %s' % top)
    if(subtop):
        sql_ds['where'].append('practice_subtopic_id = %s' % subtop)
    if(sub):
        sql_ds['where'].append('practice_subject_id = %s' % sub)
        
    return join_sql_ds(sql_ds)
        
        

def get_partners_sql(geog, id):
    if geog not in [None, "COUNTRY", "STATE", "DISTRICT", "BLOCK", "VILLAGE"]:
        return ''
    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(["DISTINCT vcp.partner_id", "P.PARTNER_NAME"])
    sql_ds['from'].append("village_precalculation_copy vcp")
    sql_ds['join'].append(["programs_PARTNER P", "P.id = vcp.partner_id"])
    if (geog):
        sql_ds['where'].append("vcp.%s_id = %s" %(geog.lower(), str(id)))
    sql_ds['order by'].append("P.PARTNER_NAME")
    return join_sql_ds(sql_ds);

def child_geog_list(geog, id, from_date, to_date):
    sql_ds = get_init_sql_ds()
    if(geog == None):
        sql_ds['select'].extend(['DISTINCT C.id', 'COUNTRY_NAME AS name'])
        sql_ds['from'].append("geographies_COUNTRY C")
    elif(geog == "COUNTRY"):
        sql_ds['select'].extend(['DISTINCT S.id', 'STATE_NAME AS name'])
        sql_ds['from'].append("geographies_STATE S")
        sql_ds['where'].append("S.country_id = " + str(id))
    elif(geog == "STATE"):
        sql_ds['select'].extend(['DISTINCT D.id', 'DISTRICT_NAME AS name'])
        sql_ds['from'].append("geographies_DISTRICT D")
        sql_ds['where'].append("state_id = " + str(id))
    elif(geog == 'DISTRICT'):
        sql_ds['select'].extend(['id', 'BLOCK_NAME as name'])
        sql_ds['from'].append('geographies_BLOCK B')
        sql_ds['where'].append("district_id = " + str(id))
    elif(geog == "BLOCK"):
        sql_ds['select'].extend(['id', 'VILLAGE_NAME AS name'])
        sql_ds['from'].append("geographies_VILLAGE V")
        sql_ds['where'].append("block_id = " + str(id))
    elif(geog == "VILLAGE"):
        sql_ds['select'].extend(['id', 'VILLAGE_NAME AS name'])
        sql_ds['from'].append("geographies_VILLAGE V")
        sql_ds['where'].append("id = " + str(id))
        sql="SELECT id, VILLAGE_NAME AS name FROM geographies_VILLAGE WHERE id = "+str(id);

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
        sql_ds['select'].append('SUM(total_videos_produced) as tot_pro')
        sql_ds['from'].append('village_precalculation_copy VPC')
        sql_ds['force index'].append('(village_precalculation_copy_village_id)')
        main_tab_abb = "VPC"
        date_field = "VPC.date"
    elif(type=='screening'):
        sql_ds['select'].append('SUM(total_screening) as tot_scr')
        sql_ds['from'].append('village_precalculation_copy VPC')
        sql_ds['force index'].append('(village_precalculation_copy_village_id)')
        main_tab_abb = "VPC"
        date_field = "VPC.date"
    elif(type=='village'):
        sql_ds['select'].append('COUNT(DISTINCT SCM.village_id) as tot_vil')
        sql_ds['from'].append('screening_myisam SCM')
        sql_ds['force index'].append('(screening_myisam_village_id)')
        main_tab_abb = "SCM"
        date_field = "SCM.date"
    elif(type=='adoption'):
        sql_ds['select'].append('SUM(total_adoption) as tot_ado')
        sql_ds['from'].append('village_precalculation_copy VPC')
        sql_ds['force index'].append('(village_precalculation_copy_village_id)')
        main_tab_abb = "VPC"
        date_field = "VPC.date"
    elif(type=='practice'):
        sql_ds['select'].append('COUNT(DISTINCT VIDM.practice_id) as tot_pra')
        sql_ds['from'].append('video_myisam VIDM')
        main_tab_abb = 'VIDM'
        date_field = "VIDM.video_production_date"
    elif(type=='person'):
        sql_ds['select'].append('COUNT(DISTINCT PMAM.person_id) as tot_per')
        sql_ds['from'].append('person_meeting_attendance_myisam PMAM')
        sql_ds['force index'].append('(person_meeting_attendance_myisam_village_id)')
        main_tab_abb = "PMAM"
        date_field = "PMAM.date"
 
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
        sql_inn_ds['select'].extend(["VIDM.practice_id" , "MIN(video_production_date) AS date"])
        sql_inn_ds['from'].append("video_myisam VIDM");
        filter_partner_geog_date(sql_inn_ds,'VIDM','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("practice_id");
        sql_ds['from'].append('('+join_sql_ds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
    elif(type=='person'):
        sql_ds['select'].extend(["date", "COUNT(*)"])
        
        sql_inn_ds = get_init_sql_ds();
        sql_inn_ds['select'].extend(["PMAM.person_id" , "MIN(date) AS date"])
        sql_inn_ds['from'].append("person_meeting_attendance_myisam PMAM");
        sql_inn_ds['force index'].append("(person_meeting_attendance_myisam_village_id)");
        filter_partner_geog_date(sql_inn_ds,'PMAM','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("person_id");

        sql_ds['from'].append('('+join_sql_ds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
#        sql_ds['select'].extend(["date_of_joining as date", "COUNT(*)"])
#        sql_ds['from'].append("PERSON P")
#        sql_ds['where'].append("P.date_of_joining is not NULL")
#        filter_partner_geog_date(sql_ds,"P",'dummy',geog,id,None,None,partners)
#        sql_ds['group by'].append('date');
    elif(type=='production'):
        sql_ds['select'].extend(["date", "SUM(total_videos_produced)"])
        sql_ds['from'].append("village_precalculation_copy VPC");
        sql_ds['force index'].append("(village_precalculation_copy_village_id)");
        filter_partner_geog_date(sql_ds,'VPC','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("date");
    elif(type=='screening'):
        sql_ds['select'].extend(["date", "SUM(total_screening)"])
        sql_ds['from'].append("village_precalculation_copy VPC");
        sql_ds['force index'].append("(village_precalculation_copy_village_id)");
        filter_partner_geog_date(sql_ds,'VPC','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("date");
    elif(type=='adoption'):
        sql_ds['select'].extend(["date", "SUM(total_adoption)"])
        sql_ds['from'].append("village_precalculation_copy VPC");
        sql_ds['force index'].append("(village_precalculation_copy_village_id)");
        filter_partner_geog_date(sql_ds,'VPC','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("date");

    if(from_date is not None and to_date is not None):
        sql_ds['having'].append("date between '"+from_date+"' and '"+to_date+"'")

    return join_sql_ds(sql_ds)



def get_totals(geog, id, from_date, to_date, partners, values_to_fetch=None):
    sql_ds = get_init_sql_ds();
    if(values_to_fetch==None or 'tot_scr' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_screening) as tot_scr");
    if(values_to_fetch==None or 'tot_vid' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_videos_produced) as tot_vid");
    if(values_to_fetch==None or 'tot_ado' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_adoption) as tot_ado");
    if(values_to_fetch==None or 'tot_male_ado' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_male_adoptions) as tot_male_ado");
    if(values_to_fetch==None or 'tot_fem_ado' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_female_adoptions) as tot_fem_ado");
    if(values_to_fetch==None or 'tot_att' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_attendance) as tot_att");
    if(values_to_fetch==None or 'tot_male_att' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_male_attendance) as tot_male_att");
    if(values_to_fetch==None or 'tot_fem_att' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_female_attendance) as tot_fem_att");
    if(values_to_fetch==None or 'tot_que' in values_to_fetch):
        sql_ds['select'].append("SUM(VPC.total_questions_asked) as tot_que");
        
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append('(village_precalculation_copy_village_id)')
    filter_partner_geog_date(sql_ds,"VPC","VPC.date",geog,id,from_date,to_date,partners)
        
    return join_sql_ds(sql_ds)


def adoption_rate_totals(geog, id, to_date,partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(['SUM(total_adopted_attendees) AS tot_adopt_per ', 
                             'SUM(total_active_attendees) AS tot_per', 
                             'SUM(total_adoption_by_active) AS tot_active_adop'])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append('(village_precalculation_copy_village_id)')
    sql_ds['where'].append("date = '%s'" % str(to_date))
    filter_partner_geog_date(sql_ds, "VPC", "DUMMY", geog, id, None, None, partners)
    
    return join_sql_ds(sql_ds);

def get_start_date(geog, id):
    geog = geog.upper() if geog is not None else None
    sql_ds = get_init_sql_ds()
    if geog is None:
        sql_ds['select'].append("MIN(START_DATE) AS date")
        sql_ds['from'].append("geographies_COUNTRY C")
    elif geog in ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']:
        sql_ds['select'].append("START_DATE AS date")
        sql_ds['from'].append("geographies_" + geog + " " + geog[0])
        sql_ds['where'].append("id = " + str(id))
    else:
        raise Exception("Invalid Geography " + geog)
        
    return join_sql_ds(sql_ds)
    
def calculate_start_date(geog, id):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append("MIN(date) AS date")
    sql_ds['from'].append("village_precalculation_copy VPC")
    if geog is not None:
        sql_ds['where'].append("%s_id = %s" % (geog.lower(), str(id)))

    return join_sql_ds(sql_ds)
