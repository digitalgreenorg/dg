from dg.output.database.utility import *

# query constructor for malefeamle ratio pie chaart
def mvideo_malefemale_ratio(request,geog,id):
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
    
def video_malefemale_ratio(**arg_dict):
    sql = []
    sql.append(r'SELECT p.GENDER as pie_key, COUNT(*) as count FROM   PERSON p, VIDEO_farmers_shown vs')
    if 'geog' in arg_dict:
        if arg_dict['geog'] == 'country':
            sql.append('where')
        if arg_dict['geog'] == 'state':
            sql.append(r""", VILLAGE vil, BLOCK b, DISTRICT d 
            WHERE p.village_id = vil.id AND vil.block_id = b.id 
            AND b.district_id = d.id AND d.state_id ="""+ str(arg_dict['id'])+' AND')                
        elif arg_dict['geog'] == 'district':
            sql.append(r""", VILLAGE vil, BLOCK b 
            WHERE  p.village_id = vil.id AND vil.block_id = b.id 
            AND b.district_id ="""+ str(arg_dict['id'])+' AND')
        elif arg_dict['geog'] == 'block':
            sql.append(r""", VILLAGE vil 
            WHERE  p.village_id = vil.id AND vil.block_id ="""+ str(arg_dict['id'])+' AND')
        
        elif arg_dict['geog'] == 'village':
            sql.append(r' WHERE  p.village_id ='+ str(arg_dict['id'])+' AND')

    if 'from_date' in arg_dict and 'to_date' in arg_dict:
        sql[1:1] = [",VIDEO vid"]
        sql[3:3] = ["vid.id = vs.video_id AND"]
        sql.append('vid.VIDEO_PRODUCTION_END_DATE BETWEEN \''+arg_dict['from_date']+'\' AND \''+arg_dict['to_date']+'\' AND')
    
    sql.append(r'vs.person_id = p.id GROUP BY p.GENDER')

    return ' '.join(sql)


# query constructor for month wise production of videos bar graph.
def mvideo_month_bar(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["COUNT( DISTINCT VID.ID ) AS count", "MONTH( VID.VIDEO_PRODUCTION_END_DATE ) AS MONTH","YEAR( VID.VIDEO_PRODUCTION_END_DATE ) AS YEAR"])
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].extend(["YEAR","MONTH"])
    sql_ds['order by'].extend(["YEAR","MONTH"])
    return joinSQLds(sql_ds)

def video_month_bar(**arg_dict):
    sql = []
    sql.append(r' SELECT COUNT( DISTINCT vid.ID ) AS count, MONTH( vid.VIDEO_PRODUCTION_END_DATE ) AS MONTH,YEAR( vid.VIDEO_PRODUCTION_END_DATE ) AS YEAR FROM VIDEO vid, VILLAGE vil')
    if 'geog' in arg_dict:
        if arg_dict['geog'] == 'state':
            sql.append(r',BLOCK b, DISTRICT d WHERE vid.village_id = vil.id AND vil.block_id = b.id AND b.district_id = d.id AND d.state_id = '+str(arg_dict['id']) )
        elif arg_dict['geog'] == 'district':
            sql.append(r""",BLOCK b WHERE vid.village_id = vil.id AND vil.block_id = b.id AND b.district_id = """+str(arg_dict['id']) )
        
        elif arg_dict['geog'] == 'block':
            sql.append(r""" WHERE vid.village_id = vil.id AND vil.block_id = """+str(arg_dict['id']) )
        
        elif arg_dict['geog'] == 'village':
            sql.append(r""" WHERE vid.village_id = """+str(arg_dict['id']) )
        
    if 'from_date' in arg_dict and 'to_date' in arg_dict:
        if arg_dict['geog'] == 'country':
            sql.append(" WHERE vid.VIDEO_PRODUCTION_END_DATE BETWEEN \'"+arg_dict['from_date']+ \
                        "\' AND \'"+arg_dict['to_date'] + "\'")
        else:
            sql.append(" AND vid.VIDEO_PRODUCTION_END_DATE BETWEEN \'"+arg_dict['from_date']+ \
                       "\' AND \'"+arg_dict['to_date']+"\'")
        
    
    sql.append(r""" GROUP BY YEAR,MONTH ORDER BY YEAR,MONTH """)
    
    return ''.join(sql)


def mvideo_actor_wise_pie(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["actors as pie_key", "count(*) as count"])
    sql_ds['from'].append("VIDEO VID")
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("actors")
    
    return joinSQLds(sql_ds)

def video_actor_wise_pie(**args):
    sql = []
    sql.append("""SELECT actors as pie_key, count(*) as count
    FROM VIDEO vid""")
    if 'geog' in args:
        if args['geog'] == 'village':
            sql.append("WHERE vid.village_id = "+str(args['id']))
        elif args['geog'] == 'block':
            sql.append(""", VILLAGE v
            WHERE vid.village_id = v.id
            AND v.block_id = """ +str(args['id']))
        elif args['geog'] == 'district':    
            sql.append(""", VILLAGE v, BLOCK b
            WHERE vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = """ +str(args['id']))
        elif args['geog'] == 'state':
            sql.append(""",VILLAGE v, BLOCK b, DISTRICT d
            WHERE vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = d.id
            AND d.state_id = """ +str(args['id']))

    if 'from_date' in args and 'to_date' in args:
        if args['geog'] == 'country':
            sql.append(" WHERE VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                        "\' AND \'"+args['to_date'] + "\'")
        else:
            sql.append(" AND VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                       "\' AND \'"+args['to_date']+"\'")

    sql.append("GROUP BY actors")
    return "\n".join(sql)

def mvideo_language_wise_scatter(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["L.language_name as name", "COUNT(VID.id) as count"])
    sql_ds['from'].append("LANGUAGE L");
    sql_ds['join'].append(["VIDEO VID", "VID.language_id = L.id"])
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append("language_name")
    
    return joinSQLds(sql_ds)


def video_language_wise_scatter(**args):
    sql = []
    sql.append("""SELECT l.language_name as name, COUNT(vid.id) as count
            FROM LANGUAGE l, VIDEO vid
            """)

    if 'geog' in args:
        if args['geog'] == 'village':
            sql.append("WHERE vid.language_id = l.id AND vid.village_id = "+str(args['id']))
        elif args['geog'] == 'block':
            sql.append(""", VILLAGE v
            WHERE vid.language_id = l.id
            AND vid.village_id = v.id
            AND v.block_id = """ +str(args['id']))
        elif args['geog'] == 'district':    
            sql.append(""", VILLAGE v, BLOCK b
            WHERE vid.language_id = l.id
            AND vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = """ +str(args['id']))
        elif args['geog'] == 'state':
            sql.append(""",VILLAGE v, BLOCK b, DISTRICT d
            WHERE vid.language_id = l.id
            AND vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = d.id
            AND d.state_id = """ +str(args['id']))
        elif args['geog'] == 'country':
            sql.append("WHERE vid.language_id = l.id")

    if 'from_date' in args and 'to_date' in args:
            sql.append(" AND VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                       "\' AND \'"+args['to_date']+"\'")

        
    sql.append("""GROUP BY language_name""")

    return '\n'.join(sql)


# This below section contains Query constructors for  
# total number of videos/screenings/avg time taken.
#arguments (geod, id) and (from_date, to_date) optional
def mvideo_tot_video(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("COUNT(DISTINCT VID.id ) AS count")
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    
    return joinSQLds(sql_ds)

def video_tot_video(**args):
    sql = []
    sql.append(r' SELECT COUNT(DISTINCT VID.id ) AS count FROM VIDEO VID, VILLAGE VIL')
    if 'geog' in args:
        if args['geog'] == 'state':
            sql.append(r',BLOCK B, DISTRICT D WHERE VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = D.id AND D.state_id = '+str(args['id']) )
        elif args['geog'] == 'district':
            sql.append(r""",BLOCK B WHERE VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = """+str(args['id']) )
        
        elif args['geog'] == 'block':
            sql.append(r""" WHERE VID.village_id = VIL.id AND VIL.block_id  = """+str(args['id']) )
        
        elif args['geog'] == 'village':
            sql.append(r""" WHERE VID.village_id = """+str(args['id']) )
        
    if 'from_date' in args and 'to_date' in args:
        if args['geog'] == 'country':
            sql.append(' WHERE VID.VIDEO_PRODUCTION_END_DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
        else:
            sql.append(' AND VID.VIDEO_PRODUCTION_END_DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
           
    return ''.join(sql)

# Query constructor for generating total screenings.
#arguments (geod, id) and (from_date, to_date) optional
def mvideo_tot_scr(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("COUNT(DISTINCT SCR.video_id) AS count")
    sql_ds['from'].append("SCREENING_videoes_screened SCR");
    if(geog.upper()!="COUNTRY" or (to_date and from_date)):
        sql_ds['join'].append(["SCREENING SC", "SC.id = SCR.screening_id"])
        filterPartnerGeogDate(sql_ds,'SC','SC.DATE',geog,id,from_date,to_date,partners)
    
    return joinSQLds(sql_ds)

def video_tot_scr(**args):
    sql = []
    sql.append(r' SELECT COUNT(DISTINCT SC.video_id) AS count FROM SCREENING_videoes_screened SC, SCREENING scr')
    if 'geog' in args:
        if args['geog'] == 'state':
            sql.append(r',VILLAGE VIL,BLOCK B, DISTRICT D WHERE SC.screening_id = scr.id AND scr.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = D.id AND D.state_id = '+str(args['id']) )
       
        elif args['geog'] == 'district':
            sql.append(r""",VILLAGE VIL,BLOCK B WHERE SC.screening_id = scr.id AND scr.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = """+str(args['id']) )
        
        elif args['geog'] == 'block':
            sql.append(r""" ,VILLAGE VIL WHERE SC.screening_id = scr.id AND scr.village_id  = VIL.id AND VIL.block_id  = """+str(args['id']) )
        
        elif args['geog'] == 'village':
            sql.append(r""" WHERE SC.screening_id = scr.id AND scr.village_id  = """+str(args['id']) )
        
    if 'from_date' in args and 'to_date' in args:
        if args['geog'] == 'country':
            sql.append(' WHERE SC.screening_id = scr.id AND scr.DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
        else:
            sql.append(' AND scr.DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
           
    return ''.join(sql)

# Query constructor for generating average time taken to produce video
#arguments (geod, id) and (from_date, to_date) optional
def mvideo_avg_time(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("AVG(DATEDIFF(VIDEO_PRODUCTION_END_DATE ,VIDEO_PRODUCTION_START_DATE)+1) as avg")
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    
    return joinSQLds(sql_ds)

def video_avg_time(**args):
    sql = []
    sql.append(r' SELECT AVG(DATEDIFF(VIDEO_PRODUCTION_END_DATE ,VIDEO_PRODUCTION_START_DATE)+1) as avg FROM VIDEO VID, VILLAGE VIL')
    if 'geog' in args:
        if args['geog'] == 'state':
            sql.append(r',BLOCK B, DISTRICT D WHERE VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = D.id AND D.state_id = '+str(args['id']) )
        elif args['geog'] == 'district':
            sql.append(r""",BLOCK B WHERE VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = """+str(args['id']) )
        
        elif args['geog'] == 'block':
            sql.append(r""" WHERE VID.village_id = VIL.id AND VIL.block_id  = """+str(args['id']) )
        
        elif args['geog'] == 'village':
            sql.append(r""" WHERE VID.village_id = """+str(args['id']) )
        
    if 'from_date' in args and 'to_date' in args:
        if args['geog'] == 'country':
            sql.append(' WHERE VID.VIDEO_PRODUCTION_END_DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
        else:
            sql.append(' AND VID.VIDEO_PRODUCTION_END_DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
           
    return ''.join(sql)


def mvideo_type_wise_pie(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].extend(["VIDEO_TYPE as pie_key", "count(*) as count"])
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    sql_ds['group by'].append('VIDEO_TYPE')
    
    return joinSQLds(sql_ds)

def video_type_wise_pie(**args):
    sql = []
    sql.append("""SELECT VIDEO_TYPE as pie_key, count(*) as count
    FROM VIDEO vid""")
    if 'geog' in args:
        if args['geog'] == 'village':
            sql.append("WHERE vid.village_id = "+str(args['id']))
        elif args['geog'] == 'block':
            sql.append(""", VILLAGE v
            WHERE vid.village_id = v.id
            AND v.block_id = """ +str(args['id']))
        elif args['geog'] == 'district':    
            sql.append(""", VILLAGE v, BLOCK b
            WHERE vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = """ +str(args['id']))
        elif args['geog'] == 'state':
            sql.append(""",VILLAGE v, BLOCK b, DISTRICT d
            WHERE vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = d.id
            AND d.state_id = """ +str(args['id']))

    if 'from_date' in args and 'to_date' in args:
        if args['geog'] == 'country':
            sql.append(" WHERE VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                        "\' AND \'"+args['to_date'] + "\'")
        else:
            sql.append(" AND VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                       "\' AND \'"+args['to_date']+"\'")

    sql.append("GROUP BY VIDEO_TYPE ORDER BY VIDEO_TYPE")
    return "\n".join(sql)

def mvideo_practice_wise_scatter(request, geog, id):
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

def video_practice_wise_scatter(**args):
    sql = []
    sql.append("""SELECT PRACTICE_NAME as name, COUNT(vid.id) as count
            FROM PRACTICES p,VIDEO_related_agricultural_practices vap, VIDEO vid""")
    if 'geog' in args:
        if args['geog'] == 'village':
            sql.append("WHERE p.id = vap.practices_id AND vap.video_id = vid.id AND vid.village_id = "+str(args['id']))
        elif args['geog'] == 'country':
            sql.append("WHERE p.id = vap.practices_id AND vap.video_id = vid.id")
        elif args['geog'] == 'block':
            sql.append(""", VILLAGE v
            WHERE p.id = vap.practices_id AND vap.video_id = vid.id AND vid.village_id = v.id
            AND v.block_id = """ +str(args['id']))
        elif args['geog'] == 'district':    
            sql.append(""", VILLAGE v, BLOCK b
            WHERE p.id = vap.practices_id AND vap.video_id = vid.id AND vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = """ +str(args['id']))
        elif args['geog'] == 'state':
            sql.append(""",VILLAGE v, BLOCK b, DISTRICT d
            WHERE p.id = vap.practices_id AND vap.video_id = vid.id AND vid.village_id = v.id
            AND v.block_id = b.id
            AND b.district_id = d.id
            AND d.state_id = """ +str(args['id']))

    if 'from_date' in args and 'to_date' in args:
        if args['geog'] == 'country':
            sql.append(" AND VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                        "\' AND \'"+args['to_date'] + "\'")
        else:
            sql.append(" AND VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                       "\' AND \'"+args['to_date']+"\'")

    sql.append("GROUP BY PRACTICE_NAME ORDER BY count")
    return "\n".join(sql)

def video_min_date(request, geog, id):
    from_date, to_date, partners = getDatesPartners(request)
    
    sql_ds = getInitSQLds();
    sql_ds['select'].append("MIN(VIDEO_PRODUCTION_END_DATE) as date")
    sql_ds['from'].append("VIDEO VID");
    filterPartnerGeogDate(sql_ds,'VID','VID.VIDEO_PRODUCTION_END_DATE',geog,id,from_date,to_date,partners)
    return joinSQLds(sql_ds)
