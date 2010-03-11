from dg.dashboard.models import *
from django.db import connection
from django.template import Template, Context

def construct_query(var, context_dict):
    return Template(var).render(Context(context_dict))

def run_query(query_string, *query_args):
    return_list = []
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        return_list.append(dict(zip(col_names,row)))
    return return_list

def run_query_dict(query_string, dict_key, *query_args):
    return_list = {}
    cursor = connection.cursor()
    cursor.execute(query_string,query_args)
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    if(dict_key != col_names[0]):
        raise Exception, dict_key+" is not the first column in returned query's column list"
    for row in rows:
        return_list[row[0]] = row[1:]
        
    return return_list


#Query for Total Video Production in Overview module
#Context Required:'type' can be (production/screening/adoption/practice/person)
#                :'geography' can be (state/district/block/village
#                : 'to_date' and 'from_date' (as required by MySQL) are OPTIONAL
#                : id of parent geography (e.g. for 'district' parent is 'state'). For state, this can be omitted
overview = r"""    
    SELECT {{geog_child|first }}.id, {{geog_child|upper }}_NAME as name, COUNT({% ifequal type 'practice' %} distinct vid_pr.practices_id {%else%}{{type|slice:":3"}}.id {%endifequal%}) as tot_{{type|slice:":3"}}
    FROM STATE s
        LEFT OUTER JOIN DISTRICT d on (s.id = d.state_id)
        LEFT OUTER JOIN BLOCK b on (b.district_id = d.id)
        LEFT OUTER JOIN VILLAGE v on (v.block_id = b.id)
    {% ifequal type 'production' %}
        LEFT OUTER JOIN VIDEO pro on (pro.village_id = v.id
    {% else %}{% ifequal type 'screening' %}
        LEFT OUTER JOIN SCREENING scr on (scr.village_id = v.id
    {% else %}{% ifequal type 'adoption' %}
        LEFT OUTER JOIN PERSON p on (p.village_id = v.id)
        LEFT OUTER JOIN PERSON_ADOPT_PRACTICE ado  on (ado.person_id = p.id
    {% else %}{% ifequal type 'practice' %}
        LEFT OUTER JOIN VIDEO vid on (vid.village_id = v.id)
        LEFT OUTER JOIN VIDEO_related_agricultural_practices vid_pr
                ON (vid_pr.video_id = vid.id
    {% else %}{% ifequal type 'person' %}
        LEFT OUTER JOIN PERSON per on (per.village_id = v.id
    {% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}
    
    {% if to_date and from_date  %}
        {% ifequal type 'production' %}
            AND VIDEO_PRODUCTION_END_DATE between '{{from_date}}' 
            and '{{to_date}}'
        {% else %}{% ifequal type 'screening' %}
            AND scr.DATE between '{{from_date}}' and '{{to_date}}'
        {% else %}{% ifequal type 'adoption' %}
            AND ado.DATE_OF_ADOPTION between '{{from_date}}' and '{{to_date}}'
        {% else %}{% ifequal type 'practice' %}
            AND VIDEO_PRODUCTION_END_DATE  between '{{from_date}}' and '{{to_date}}'
        {% else %}{% ifequal type 'person' %}
            AND  per.id in 
                                (
                                    SELECT vs.person_id
                                    FROM VIDEO_farmers_shown vs, VIDEO v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE between '{{from_date}}' and '{{to_date}}'
            
                                    UNION
            
                                    SELECT person_id
                                    FROM PERSON_ADOPT_PRACTICE
                                    WHERE DATE_OF_ADOPTION between '{{from_date}}' and '{{to_date}}'
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM PERSON_MEETING_ATTENDANCE pa, SCREENING sc
                                    WHERE pa.screening_id = sc.id
                                    AND sc.DATE between '{{from_date}}' and '{{to_date}}'
                                )
        {% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}    
    {% endif %}
       )
       
    {% ifnotequal geography 'country' %}
       WHERE {{geography|first}}.id = {{id}}
    {% endifnotequal %}
    
    GROUP BY {{geog_child|upper }}_NAME
    ORDER BY {{geog_child|upper }}_NAME
    """
    
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

#Query for Line Chart in Overview module. It returns date and count of the metric on that date.
#Context Required:'type' can be (production/screening/adoption/practice/person)
#                :'geography' can be (state/district/block/village)

overview_line_chart = """
{%ifequal type 'practice' %}
SELECT date, COUNT(*)
    FROM(
         SELECT vid_pr.practices_id , MIN(VIDEO_PRODUCTION_END_DATE) AS date    
         FROM VIDEO vid, VIDEO_related_agricultural_practices vid_pr
        {%ifequal geography 'village' %}
            WHERE vid.id = vid_pr.video_id AND vid.village_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'block' %}
            , VILLAGE vil
            WHERE vid.id = vid_pr.video_id 
            AND vid.village_id = vil.id
            AND vil.block_id = {{id}}        
        {% endifequal %}
        {%ifequal geography 'district' %}
            , VILLAGE vil , BLOCK b
            WHERE vid.id = vid_pr.video_id 
            AND vid.village_id = vil.id 
            AND vil.block_id = b.id 
            AND b.district_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'state' %}
            , VILLAGE vil , BLOCK b, DISTRICT d
            WHERE vid.id = vid_pr.video_id 
            AND vid.village_id = vil.id 
            AND vil.block_id = b.id 
            AND b.district_id = d.id 
            AND d.state_id = {{id}}
        {% endifequal %}
        GROUP BY practices_id
         ) AS tab1
     GROUP BY date
{%else%}{% ifequal type 'person' %}
SELECT date, count(*)
    FROM (
        SELECT person_id, min(date) as date
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
            WHERE pa.screening_id = sc.id

        ) as tab
        {%ifequal geography 'village' %}
            , PERSON p
            WHERE tab.person_id = p.id 
            AND p.village_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'block' %}
            , PERSON p, VILLAGE vil
            WHERE tab.person_id = p.id 
            AND p.village_id = vil.id 
            AND vil.block_id = {{id}}        
        {% endifequal %}
        {%ifequal geography 'district' %}
            , PERSON p, VILLAGE vil , BLOCK b
            WHERE tab.person_id = p.id 
            AND p.village_id = vil.id 
            AND vil.block_id = b.id
            AND b.district_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'state' %}
            , PERSON p, VILLAGE vil , BLOCK b, DISTRICT d
            WHERE tab.person_id = p.id 
            AND p.village_id = vil.id 
            AND vil.block_id = b.id 
            AND b.district_id = d.id 
            AND d.state_id = {{id}}
        {% endifequal %}
      GROUP BY tab.person_id
    ) as tab1
    GROUP BY date
{%else%}{% ifequal type 'production' %}
    SELECT VIDEO_PRODUCTION_END_DATE as date, count(*)
    FROM VIDEO vid
    {%ifequal geography 'village' %}
        WHERE vid.village_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'block' %}
        , VILLAGE vil
        WHERE vid.village_id = vil.id 
        AND vil.block_id = {{id}}        
    {% endifequal %}
    {%ifequal geography 'district' %}
        , VILLAGE vil , BLOCK b
        WHERE vid.village_id = vil.id 
        AND vil.block_id = b.id 
        AND b.district_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'state' %}
        , VILLAGE vil , BLOCK b, DISTRICT d
        WHERE vid.village_id = vil.id 
        AND vil.block_id = b.id 
        AND b.district_id = d.id 
        AND d.state_id = {{id}}
    {% endifequal %}
    GROUP BY VIDEO_PRODUCTION_END_DATE
{%else%}{% ifequal type 'screening' %}
    SELECT DATE AS date, count(*)
    FROM SCREENING sc
    {%ifequal geography 'village' %}
        WHERE sc.village_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'block' %}
        , VILLAGE vil
        WHERE sc.village_id = vil.id 
        AND vil.block_id = {{id}}        
    {% endifequal %}
    {%ifequal geography 'district' %}
        , VILLAGE vil , BLOCK b
        WHERE sc.village_id = vil.id 
        AND vil.block_id = b.id 
        AND b.district_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'state' %}
        , VILLAGE vil , BLOCK b, DISTRICT d
        WHERE sc.village_id = vil.id 
        AND vil.block_id = b.id 
        AND b.district_id = d.id 
        AND d.state_id = {{id}}
    {% endifequal %}
    GROUP BY DATE
{%else%}{% ifequal type 'adoption' %}
    SELECT DATE_OF_ADOPTION as date, count(*)
    FROM PERSON_ADOPT_PRACTICE pa
    {%ifequal geography 'village' %}
        , PERSON p
        WHERE pa.person_id = p.id AND p.village_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'block' %}
        , PERSON p, VILLAGE vil
        WHERE pa.person_id = p.id 
        AND p.village_id = vil.id
        AND vil.block_id = {{id}}        
    {% endifequal %}
    {%ifequal geography 'district' %}
        , PERSON p, VILLAGE vil , BLOCK b
        WHERE pa.person_id = p.id 
        AND p.village_id = vil.id
        AND vil.block_id = b.id 
        AND b.district_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'state' %}
        , PERSON p, VILLAGE vil , BLOCK b, DISTRICT d
        WHERE pa.person_id = p.id 
        AND p.village_id = vil.id
        AND vil.block_id = b.id 
        AND b.district_id = d.id 
        AND d.state_id = {{id}}
    {% endifequal %}
    GROUP BY DATE_OF_ADOPTION
{% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}
"""

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

def video_language_wise_bar(**args):
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
    sql.append(r' SELECT COUNT(DISTINCT SC.video_id) AS count FROM SCREENING_videoes_screened SC, VIDEO VID')
    if 'geog' in args:
        if args['geog'] == 'state':
            sql.append(r',VILLAGE VIL,BLOCK B, DISTRICT D WHERE SC.video_id =VID.id AND VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = D.id AND D.state_id = '+str(args['id']) )
       
        elif args['geog'] == 'district':
            sql.append(r""",VILLAGE VIL,BLOCK B WHERE SC.video_id =VID.id AND VID.village_id = VIL.id AND VIL.block_id = B.id AND B.district_id = """+str(args['id']) )
        
        elif args['geog'] == 'block':
            sql.append(r""" ,VILLAGE VIL WHERE SC.video_id =VID.id AND VID.village_id  = VIL.id AND VIL.block_id  = """+str(args['id']) )
        
        elif args['geog'] == 'village':
            sql.append(r""" WHERE SC.video_id =VID.id AND VID.village_id  = """+str(args['id']) )
        
    if 'from_date' in args and 'to_date' in args:
        if args['geog'] == 'country':
            sql.append(' WHERE SC.video_id = VID.id AND VID.VIDEO_PRODUCTION_END_DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
        else:
            sql.append(' AND VID.VIDEO_PRODUCTION_END_DATE BETWEEN \''+args['from_date']+'\' AND \''+args['to_date']+ ' \'  ')
           
    return ''.join(sql)

# Query constructor for generating average time taken to produce video
#arguments (geod, id) and (from_date, to_date) optional

def video_avg_time(**args):
    sql = []
    sql.append(r' SELECT DISTINCT VID.id, DATEDIFF(VIDEO_PRODUCTION_END_DATE,VIDEO_PRODUCTION_START_DATE) as dif FROM VIDEO VID, VILLAGE VIL')
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
            sql.append(" WHERE VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                        "\' AND \'"+args['to_date'] + "\'")
        else:
            sql.append(" AND VIDEO_PRODUCTION_END_DATE BETWEEN \'"+args['from_date']+ \
                       "\' AND \'"+args['to_date']+"\'")

    sql.append("GROUP BY PRACTICE_NAME ORDER BY count")
    return "\n".join(sql)

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