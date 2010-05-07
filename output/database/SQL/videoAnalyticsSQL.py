from dg.output.database.utility import *

# query constructor for malefeamle ratio pie chaart
def video_malefemale_ratio(request,geog,id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["P.GENDER as pie_key", "COUNT(*) as count"])
    sql_ds['from'].append('PERSON P')
    sql_ds['join'].append(["VIDEO_farmers_shown VFS", "P.id = VFS.person_id"])
    if(from_date and to_date):
        sql_ds['join'].append(["VIDEO VID","VID.id = VFS.video_id"])
        filterPartnerGeogDate(sql_ds,'P','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    else:
        filterPartnerGeogDate(sql_ds,'P',"dummy",geog,id,from_date,to_date,partners)
    
    sql_ds['group by'].append("P.GENDER")
    
    return joinSQLds(sql_ds);



# query constructor for month wise production of videos bar graph.
def video_month_bar(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["COUNT( DISTINCT VID.ID ) AS count", "MONTH( VID.VIDEO_PRODUCTION_END_DATE ) AS MONTH","YEAR( VID.VIDEO_PRODUCTION_END_DATE ) AS YEAR"])
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].extend(["YEAR","MONTH"])
    sql_ds['order by'].extend(["YEAR","MONTH"])
    return joinSQLds(sql_ds)

def video_actor_wise_pie(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["actors as pie_key", "count(*) as count"])
    sql_ds['from'].append("VIDEO VID")
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("actors")
    
    return joinSQLds(sql_ds)

def video_language_wise_scatter(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["L.language_name as name", "COUNT(VID.id) as count"])
    sql_ds['from'].append("LANGUAGE L");
    sql_ds['join'].append(["VIDEO VID", "VID.language_id = L.id"])
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("language_name")
    
    return joinSQLds(sql_ds)

# This below section contains Query constructors for  
# total number of videos/screenings/avg time taken.
#arguments (geod, id) and (from_date, to_date) optional
def video_tot_video(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("COUNT(DISTINCT VID.id ) AS count")
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    
    return joinSQLds(sql_ds)

# Query constructor for generating total screenings.
#arguments (geod, id) and (from_date, to_date) optional
def video_tot_scr(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("COUNT(DISTINCT SCR.video_id) AS count")
    sql_ds['from'].append("SCREENING_videoes_screened SCR");
    if(geog.upper()!="COUNTRY" or (to_date and from_date)):
        sql_ds['join'].append(["SCREENING SC", "SC.id = SCR.screening_id"])
        filterPartnerGeogDate(sql_ds,'SC','SC.DATE',geog,id,from_date,to_date,partners)
    
    return joinSQLds(sql_ds)

# Query constructor for generating average time taken to produce video
#arguments (geod, id) and (from_date, to_date) optional
def video_avg_time(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("AVG(DATEDIFF(VIDEO_PRODUCTION_END_DATE ,VIDEO_PRODUCTION_START_DATE)+1) as avg")
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    
    return joinSQLds(sql_ds)

def video_type_wise_pie(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["VIDEO_TYPE as pie_key", "count(*) as count"])
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append('VIDEO_TYPE')
    
    return joinSQLds(sql_ds)

def video_practice_wise_scatter(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["PRACTICE_NAME as name", "COUNT(VID.id) as count"])
    sql_ds['from'].append("VIDEO VID");
    sql_ds['join'].append(["VIDEO_related_agricultural_practices VRAP","VRAP.video_id = VID.id"])
    sql_ds['join'].append(["PRACTICES P","VRAP.practices_id = P.id"])
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("PRACTICE_NAME")
    sql_ds['order by'].append("count")
    return joinSQLds(sql_ds)

def video_min_date(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("MIN(VIDEO_PRODUCTION_END_DATE) as date")
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    return joinSQLds(sql_ds)
