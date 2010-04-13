from dg.dashboard.models import *
from django.db import connection
from django.template import Template, Context


#Query for extra data for country in Overview page
def overview_nation_pg_vil_total():
    return """SELECT * FROM
          (SELECT COUNT(*) AS tot_vil FROM VILLAGE) t1,
          (SELECT COUNT(*) AS tot_pg FROM PERSON_GROUPS) t2"""
          
          

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


def overview_min_date(**args):
    sql = []
    if 'geog' in args:
        if(args['geog'] == 'village'):
            temp = " WHERE x.village_id = "+str(args['id'])
            from_clause = ''
        elif(args['geog'] == 'block'):
            temp = " WHERE x.village_id = VIL.id AND VIL.block_id = "+str(args['id'])
            from_clause = ",VILLAGE VIL "
        elif(args['geog'] == 'district'):
            temp = " WHERE x.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = " +str(args['id'])
            from_clause = ",VILLAGE VIL ,BLOCK B "
        elif(args['geog'] == 'state'):
            temp = " WHERE x.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = D.id AND D.state_id = " +str(args['id'])
            from_clause = ",VILLAGE VIL,BLOCK B, DISTRICT D "
        elif(args['geog'] == 'country'):
            temp = ''
            from_clause = ''
   
    sql.append("""
    SELECT MIN(DATE) as date
    FROM (
       SELECT MIN(VIDEO_PRODUCTION_END_DATE) AS DATE
       FROM VIDEO x""" + from_clause + temp + """
    
       UNION
       SELECT MIN(DATE) AS DATE
       FROM SCREENING x"""+ from_clause + temp + """
    
       UNION
       SELECT MIN(DATE_OF_ADOPTION) AS DATE
        FROM PERSON_ADOPT_PRACTICE PA""")
    if temp:
        sql.append("""
        , PERSON x """ + from_clause + temp + """ AND PA.person_id = x.id""")
   
    sql.append(") AS T1")
    return '\n'.join(sql)


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