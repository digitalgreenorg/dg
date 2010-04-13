from dg.dashboard.models import *
from django.db import connection
from django.template import Template, Context

# query constructor for malefeamle ratio pie chaart
def video_malefemale_ratio(arg_dict):
    sql = []
    sql.append(r'SELECT COUNT(*) as count, p.GENDER as gender FROM   PERSON p, VIDEO_farmers_shown vs')
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
def video_month_bar(arg_dict):
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


def video_actor_wise_pie(**args):
    sql = []
    sql.append("""SELECT actors, count(*) as count
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

def video_language_wise_scatter(**args):
    sql = []
    sql.append("""SELECT l.language_name as lname, COUNT(vid.id) as count
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


def video_month_bar_year(arg_dict):
    return """
    SELECT min(YEAR( vid.VIDEO_PRODUCTION_END_DATE )) as min_year, 
           max(YEAR( vid.VIDEO_PRODUCTION_END_DATE )) as max_year
    FROM VIDEO vid"""

# This below section contains Query constructors for  
# total number of videos/screenings/avg time taken.
#arguments (geod, id) and (from_date, to_date) optional
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


def video_type_wise_pie(**args):
    sql = []
    sql.append("""SELECT VIDEO_TYPE, count(*) as count
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


def video_min_date(**args):
    sql = []
    sql.append("SELECT MIN(VIDEO_PRODUCTION_END_DATE) as date from VIDEO VID ")
    if 'geog' in args:
        if(args['geog'] == 'village'):
            sql.append(" WHERE VID.village_id = "+str(args['id']))
            from_clause = ''
        elif(args['geog'] == 'block'):
            sql.append(" , VILLAGE VIL WHERE VID.village_id = VIL.id AND VIL.block_id = "+str(args['id']))
        elif(args['geog'] == 'district'):
            sql.append(" ,VILLAGE VIL ,BLOCK B WHERE VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = " +str(args['id']))
        elif(args['geog'] == 'state'):
            sql.append(",VILLAGE VIL,BLOCK B, DISTRICT D  WHERE VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = D.id AND D.state_id = " +str(args['id']))
     
    return '\n'.join(sql)