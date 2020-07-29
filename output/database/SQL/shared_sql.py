from output.database.utility import *
from activities.models import AP_Screening
from django.db.models import *
from django.conf import settings
import datetime

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
        sql_ds['where'].append("S.country_id = " + str(id) + " And S.active = 1")
    elif(geog == "STATE"):
        sql_ds['select'].extend(['DISTINCT D.id', 'DISTRICT_NAME AS name'])
        sql_ds['from'].append("geographies_DISTRICT D")
        sql_ds['where'].append("state_id = " + str(id) + " And D.active = 1")
    elif(geog == 'DISTRICT'):
        sql_ds['select'].extend(['id', 'BLOCK_NAME as name'])
        sql_ds['from'].append('geographies_BLOCK B')
        sql_ds['where'].append("district_id = " + str(id) + " And B.active = 1")
    elif(geog == "BLOCK"):
        sql_ds['select'].extend(['id', 'VILLAGE_NAME AS name'])
        sql_ds['from'].append("geographies_VILLAGE V")
        sql_ds['where'].append("block_id = " + str(id)+  " And V.active = 1" )
    elif(geog == "VILLAGE"):
        sql_ds['select'].extend(['id', 'VILLAGE_NAME AS name'])
        sql_ds['from'].append("geographies_VILLAGE V")
        sql_ds['where'].append("id = " + str(id) + " And V.active = 1")
        sql="SELECT id, VILLAGE_NAME AS name FROM geographies_VILLAGE WHERE id = "+str(id);

    return join_sql_ds(sql_ds);

#Query for the table in overview module and pie graphs.
#Parameter Required:'type' can be (production/screening/adoption/practice/person/village)
def overview(geog, id, from_date, to_date, partners, type):
    geog_list = [None, 'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    geog_table_abb_list = [None, 'gc', 'gs', 'gd', 'gb', 'gv']

    if(geog == 'VILLAGE'):
        geog_child = 'VILLAGE'
        geog_table_abb = 'gv'
    else:
        geog_child = geog_list[geog_list.index(geog)+1]
        geog_table_abb = geog_table_abb_list[geog_list.index(geog)+1]

    date_field = par_table = ''
    sql_ds = get_init_sql_ds();
    sql_ds['select'].append(geog_table_abb+"."+"id as id")
    if(type == 'production'):
        sql_ds['select'].append('COUNT(DISTINCT vv.id) as tot_pro')
        sql_ds['from'].append('videos_video vv')
        sql_ds['join'].append(["geographies_village gv", "gv.id=vv.village_id "])
        
        par_table = "vv"
        date_field = "vv.production_date"

    elif(type=='screening'):
        sql_ds['select'].append('COUNT(DISTINCT scr.id) as tot_scr')
        sql_ds['from'].append('activities_screening scr')
        sql_ds['join'].append(["geographies_village gv", "gv.id=scr.village_id "])

        par_table = "scr"
        date_field = "scr.date"

    elif(type=='village'):
        sql_ds['select'].append('COUNT(DISTINCT gv.id) as tot_vil')
        sql_ds['from'].append('activities_screening scr')
        sql_ds['join'].append(["geographies_village gv", "gv.id=scr.village_id"])
        
        par_table = "scr"
        date_field = "scr.date"

    elif(type=='adoption'):
        sql_ds['select'].append('COUNT(DISTINCT pp.id) as tot_ado')
        sql_ds['from'].append('activities_personadoptpractice pap')
        sql_ds['join'].append(["people_person pp", "pp.id = pap.person_id "])
        sql_ds['join'].append(["geographies_village gv", "gv.id=pp.village_id "])
        
        par_table = "pap"
        date_field = "pap.date_of_adoption"

    elif(type=='practice'):
        sql_ds['select'].append('COUNT(DISTINCT vv.related_practice_id) as tot_pra')
        sql_ds['from'].append('videos_video vv')
        sql_ds['join'].append(["geographies_village gv", "gv.id = vv.village_id "])
        sql_ds["where"].append("vv.video_type = 1")
        
        par_table = "vv"
        date_field = "vv.production_date"

    elif(type=="person"):
        sql_ds["select"].append("COUNT(DISTINCT pma.person_id) as tot_per")
        sql_ds["from"].append("activities_personmeetingattendance pma")
        sql_ds["join"].append(["activities_screening scr", "scr.id=pma.screening_id "])
        sql_ds["join"].append(["people_person pp", "pp.id = pma.person_id "])
        sql_ds["join"].append(["geographies_village gv", "gv.id=pp.village_id "])

        par_table = "scr"
        date_field = "scr.date"

    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "])
 
    filter_partner_geog_date(sql_ds, par_table, date_field,geog,id,from_date,to_date,partners)

    sql_ds["group by"].append(geog_table_abb+"."+"id")
    sql_ds["order by"].append(geog_table_abb+"."+"id")

    return join_sql_ds(sql_ds);



# AP-Bluefrog specific data
def ap_overview(geog, id, from_date, to_date, partners, type):
    geog_list = [None, 'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']

    if(geog == 'VILLAGE'):
        geog_child = 'VILLAGE'
    else:
        geog_child = geog_list[geog_list.index(geog)+1]

    key = None
    if geog is None:
        key = 'screening__village__block__district__state__country_id'
        ap_total_per = \
             AP_Screening.objects.filter(screening__village__block__district__state__country_id=1, screening__date__range=[from_date, to_date]).values('screening__village__block__district__state__country_id').annotate(ap_tot_per=Sum('total_members'))
    elif  geog == "COUNTRY":
        key = 'screening__village__block__district__state_id'
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block__district__state__country_id=id) \
                   .values('screening__village__block__district__state_id').annotate(ap_tot_per=Sum('total_members'))
    elif geog == "STATE":
        key = 'screening__village__block__district_id'
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block__district__state_id=id) \
                .values('screening__village__block__district_id').annotate(ap_tot_per=Sum('total_members'))
    elif geog == "DISTRICT":
        key = 'screening__village__block_id'
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block__district_id=id) \
                .values('screening__village__block_id').annotate(ap_tot_per=Sum('total_members'))
    elif geog == "BLOCK":
        key = 'screening__village_id'
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block_id=id) \
                .values('screening__village_id').annotate(ap_tot_per=Sum('total_members'))
    else:
        key = 'screening__village_id'
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village_id=id) \
                .values('screening__village_id').annotate(ap_tot_per=Sum('total_members'))

    return (key, ap_total_per)


# AP-Bluefrog specific data
def ap_screening_overview(geog, id, from_date, to_date, partners):
    if geog is None:
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date]).aggregate(ap_tot_per=Sum('total_members'))
    elif  geog == "COUNTRY":
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block__district__state__country_id=id).aggregate(ap_tot_per=Sum('total_members'))
    elif geog == "STATE":
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block__district__state_id=id) \
                .aggregate(ap_tot_per=Sum('total_members'))
    elif geog == "DISTRICT":
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block__district_id=id) \
                .aggregate(ap_tot_per=Sum('total_members'))
    elif geog == "BLOCK":
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village__block_id=id) \
                .aggregate(ap_tot_per=Sum('total_members'))
    else:
        ap_total_per = \
             AP_Screening.objects.filter(screening__date__range=[from_date, to_date], screening__village_id=id) \
                .aggregate(ap_tot_per=Sum('total_members'))

    return ap_total_per


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
       # sql_ds['select'].extend(["date_of_joining as date", "COUNT(*)"])
       # sql_ds['from'].append("PERSON P")
       # sql_ds['where'].append("P.date_of_joining is not NULL")
       # filter_partner_geog_date(sql_ds,"P",'dummy',geog,id,None,None,partners)
       # sql_ds['group by'].append('date');
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
        sql_ds['select'].append('COUNT(DISTINCT scr.id) as tot_scr')
        sql_ds['from'].append('activities_screening scr')
        sql_ds['join'].append(["geographies_village gv", "gv.id=scr.village_id "])

        par_table = "scr"
        date_field = "scr.date"

    elif(values_to_fetch==None or 'tot_vid' in values_to_fetch):
        sql_ds['select'].append('COUNT(DISTINCT vv.id) as tot_pro')
        sql_ds['from'].append('videos_video vv')
        sql_ds['join'].append(["geographies_village gv", "gv.id=vv.village_id "])
        
        par_table = "vv"
        date_field = "vv.production_date"       

    elif(values_to_fetch==None or 'tot_ado' in values_to_fetch or 'tot_fem_ado' in values_to_fetch or 'tot_male_ado' in values_to_fetch):
        sql_ds['select'].append('COUNT(DISTINCT pp.id) as tot_ado')
        sql_ds["select"].append("COUNT(DISTINCT CASE WHEN pp.gender = 'F' THEN pp.id END) tot_fem_ado")
        sql_ds["select"].append("COUNT(DISTINCT CASE WHEN pp.gender = 'M' THEN pp.id END) tot_male_ado")
        sql_ds['from'].append('activities_personadoptpractice pap')
        sql_ds['join'].append(["people_person pp", "pp.id = pap.person_id "])
        sql_ds['join'].append(["geographies_village gv", "gv.id=pp.village_id "])
        
        par_table = "pap"
        date_field = "pap.date_of_adoption"

    elif(values_to_fetch==None or 'tot_nonunique_ado' in values_to_fetch or 'tot_nonunique_fem_ado' in values_to_fetch or 'tot_nonunique_male_ado' in values_to_fetch):
        sql_ds['select'].append('COUNT(pp.id) as tot_nonunique_ado')
        sql_ds["select"].append("COUNT(CASE WHEN pp.gender = 'F' THEN pp.id END) tot_nonunique_fem_ado")
        sql_ds["select"].append("COUNT(CASE WHEN pp.gender = 'M' THEN pp.id END) tot_nonunique_male_ado")
        sql_ds['from'].append('activities_personadoptpractice pap')
        sql_ds['join'].append(["people_person pp", "pp.id = pap.person_id "])
        sql_ds['join'].append(["geographies_village gv", "gv.id=pp.village_id "])
        
        par_table = "pap"
        date_field = "pap.date_of_adoption"
 
    elif(values_to_fetch==None or 'tot_att' in values_to_fetch or 'tot_fem_att' in values_to_fetch or 'tot_male_att' in values_to_fetch):
        sql_ds["select"].append("COUNT(DISTINCT pma.person_id) as tot_att")
        sql_ds["select"].append("COUNT(DISTINCT CASE WHEN pp.gender = 'F' THEN pma.person_id END) tot_fem_att")
        sql_ds["select"].append("COUNT(DISTINCT CASE WHEN pp.gender = 'M' THEN pma.person_id END) tot_male_att")
        sql_ds["from"].append("activities_personmeetingattendance pma")
        sql_ds["join"].append(["activities_screening scr", "scr.id=pma.screening_id "])
        sql_ds["join"].append(["people_person pp", "pp.id = pma.person_id "])
        sql_ds["join"].append(["geographies_village gv", "gv.id=pp.village_id "])

        par_table = "scr"
        date_field = "scr.date"

    elif(values_to_fetch==None or 'tot_que' in values_to_fetch):
        sql_ds['select'].append('SUM(scr.questions_asked) as tot_que')
        sql_ds['from'].append('activities_screening scr')
        sql_ds['join'].append(["geographies_village gv", "gv.id=scr.village_id "])

        par_table = "scr"
        date_field = "scr.date"

    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "]) 

    filter_partner_geog_date(sql_ds, par_table, date_field, geog,id,from_date,to_date,partners)

    return join_sql_ds(sql_ds)

def get_total_adopted_attendees(geog, id, from_date,to_date,partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('COUNT(DISTINCT pp.id) as tot_adopt_per')
    sql_ds['from'].append('activities_personadoptpractice pap ')
    sql_ds['join'].append(["people_person pp", "pp.id = pap.person_id "])
    sql_ds['join'].append(["geographies_village gv", "gv.id=pp.village_id "])
    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "]) 

    par_table = "pap"
    date_field = "pap.date_of_adoption"
    filter_partner_geog_date(sql_ds, par_table, date_field, geog, id, from_date, to_date, partners)
    
    return join_sql_ds(sql_ds);

def get_total_active_attendees(geog, id, from_date,to_date,partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].append('COUNT(DISTINCT pma.person_id) as tot_per')
    sql_ds['from'].append('activities_personmeetingattendance pma ')
    sql_ds['join'].append(["activities_screening scr", "scr.id=pma.screening_id "])
    sql_ds['join'].append(["geographies_village gv", "gv.id=scr.village_id "])
    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "]) 
    sql_ds['where'].append("scr.date BETWEEN '"+str(from_date)+"' AND '"+str(to_date)+"'")

    par_table = "pap"
    date_field = "DUMMY"
    filter_partner_geog_date(sql_ds, par_table, date_field, geog, id, None, None, partners)

    return join_sql_ds(sql_ds);

def get_total_adoption_by_active_attendees(geog, id, from_date,to_date,partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(['COUNT(DISTINCT pp.id) AS tot_active_adop',
                             'COUNT(pp.id) AS tot_active_adop_nonunique ', ])
    sql_ds['from'].append('activities_personadoptpractice pap ')
    sql_ds['join'].append(["people_person pp", "pp.id = pap.person_id "])
    sql_ds['join'].append(["activities_personmeetingattendance pma", "pma.person_id = pp.id "])
    sql_ds['join'].append(["activities_screening scr", "scr.id=pma.screening_id AND scr.date BETWEEN date_sub(pap.date_of_adoption, INTERVAL 60 DAY) AND pap.date_of_adoption "])
    sql_ds['join'].append(["geographies_village gv", "gv.id=pp.village_id "])
    sql_ds["join"].append(["geographies_block gb", "gb.id=gv.block_id "])
    sql_ds["join"].append(["geographies_district gd", "gd.id=gb.district_id "])
    sql_ds["join"].append(["geographies_state gs", "gs.id=gd.state_id "])
    sql_ds["join"].append(["geographies_country gc", "gc.id=gs.country_id "]) 

    par_table = "pap"
    date_field = "pap.date_of_adoption"
    filter_partner_geog_date(sql_ds, par_table, date_field, geog, id, from_date, to_date, partners)

    return join_sql_ds(sql_ds);


def adoption_rate_totals(geog, id, from_date,to_date,partners):
    sql_ds = get_init_sql_ds()
    sql_ds['select'].extend(['SUM(total_adopted_attendees) AS tot_adopt_per ', 
                             'SUM(total_active_attendees) AS tot_per', 
                             'SUM(total_adoption_by_active) AS tot_active_adop'])
    sql_ds['from'].append("village_precalculation_copy VPC")
    sql_ds['force index'].append('(village_precalculation_copy_village_id)')
    if(from_date is not None and to_date is not None):
        sql_ds['where'].append("date between '"+str(from_date)+"' and '"+str(to_date)+"'")
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
