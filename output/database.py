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
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village v on (v.block_id = b.id)
    {% ifequal type 'production' %}
        LEFT OUTER JOIN video pro on (pro.village_id = v.id
    {% else %}{% ifequal type 'screening' %}
        LEFT OUTER JOIN screening scr on (scr.village_id = v.id
    {% else %}{% ifequal type 'adoption' %}
        LEFT OUTER JOIN person p on (p.village_id = v.id)
        LEFT OUTER JOIN person_adopt_practice ado  on (ado.person_id = p.id
    {% else %}{% ifequal type 'practice' %}
        LEFT OUTER JOIN video vid on (vid.village_id = v.id)
        LEFT OUTER JOIN video_related_agricultural_practices vid_pr
                ON (vid_pr.video_id = vid.id
    {% else %}{% ifequal type 'person' %}
        LEFT OUTER JOIN person per on (per.village_id = v.id
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
                                    FROM video_farmers_shown vs, video v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE between '{{from_date}}' and '{{to_date}}'
            
                                    UNION
            
                                    SELECT person_id
                                    FROM person_adopt_practice
                                    WHERE DATE_OF_ADOPTION between '{{from_date}}' and '{{to_date}}'
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM person_meeting_attendance pa, screening sc
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
FROM {{geog}}
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
         FROM video vid, video_related_agricultural_practices vid_pr
        {%ifequal geography 'village' %}
            WHERE vid.id = vid_pr.video_id AND vid.village_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'block' %}
            , village vil
            WHERE vid.id = vid_pr.video_id 
            AND vid.village_id = vil.id
            AND vil.block_id = {{id}}        
        {% endifequal %}
        {%ifequal geography 'district' %}
            , village vil , block b
            WHERE vid.id = vid_pr.video_id 
            AND vid.village_id = vil.id 
            AND vil.block_id = b.id 
            AND b.district_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'state' %}
            , village vil , block b, district d
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
            FROM video_farmers_shown vs, video vid
            WHERE vs.video_id = vid.id

            UNION

            SELECT  person_id , DATE_OF_ADOPTION AS date
            FROM person_adopt_practice pa

            UNION

            SELECT  pa.person_id, DATE
            FROM person_meeting_attendance pa, screening sc
            WHERE pa.screening_id = sc.id

        ) as tab
        {%ifequal geography 'village' %}
            , person p
            WHERE tab.person_id = p.id 
            AND p.village_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'block' %}
            , person p, village vil
            WHERE tab.person_id = p.id 
            AND p.village_id = vil.id 
            AND vil.block_id = {{id}}        
        {% endifequal %}
        {%ifequal geography 'district' %}
            , person p, village vil , block b
            WHERE tab.person_id = p.id 
            AND p.village_id = vil.id 
            AND vil.block_id = b.id
            AND b.district_id = {{id}}
        {% endifequal %}
        {%ifequal geography 'state' %}
            , person p, village vil , block b, district d
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
    FROM video vid
    {%ifequal geography 'village' %}
        WHERE vid.village_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'block' %}
        , village vil
        WHERE vid.village_id = vil.id 
        AND vil.block_id = {{id}}        
    {% endifequal %}
    {%ifequal geography 'district' %}
        , village vil , block b
        WHERE vid.village_id = vil.id 
        AND vil.block_id = b.id 
        AND b.district_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'state' %}
        , village vil , block b, district d
        WHERE vid.village_id = vil.id 
        AND vil.block_id = b.id 
        AND b.district_id = d.id 
        AND d.state_id = {{id}}
    {% endifequal %}
    GROUP BY VIDEO_PRODUCTION_END_DATE
{%else%}{% ifequal type 'screening' %}
    SELECT DATE AS date, count(*)
    FROM screening sc
    {%ifequal geography 'village' %}
        WHERE sc.village_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'block' %}
        , village vil
        WHERE sc.village_id = vil.id 
        AND vil.block_id = {{id}}        
    {% endifequal %}
    {%ifequal geography 'district' %}
        , village vil , block b
        WHERE sc.village_id = vil.id 
        AND vil.block_id = b.id 
        AND b.district_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'state' %}
        , village vil , block b, district d
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
        , person p
        WHERE pa.person_id = p.id AND p.village_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'block' %}
        , person p, village vil
        WHERE pa.person_id = p.id 
        AND p.village_id = vil.id
        AND vil.block_id = {{id}}        
    {% endifequal %}
    {%ifequal geography 'district' %}
        , person p, village vil , block b
        WHERE pa.person_id = p.id 
        AND p.village_id = vil.id
        AND vil.block_id = b.id 
        AND b.district_id = {{id}}
    {% endifequal %}
    {%ifequal geography 'state' %}
        , person p, village vil , block b, district d
        WHERE pa.person_id = p.id 
        AND p.village_id = vil.id
        AND vil.block_id = b.id 
        AND b.district_id = d.id 
        AND d.state_id = {{id}}
    {% endifequal %}
    GROUP BY DATE_OF_ADOPTION
{% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}{% endifequal %}
"""

def video_malefemale_ratio(arg_dict):
    sql = []
    sql.append(r'SELECT COUNT(DISTINCT p.id) as count, p.GENDER as gender FROM   person p, video_farmers_shown vs')
    if 'geog' in arg_dict:
        if arg_dict['geog'] == 'state':
            sql.append(r""", village vil, block b, district d 
            WHERE p.village_id = vil.id AND vil.block_id = b.id 
            AND b.district_id = d.id AND d.state_id ="""+ str(arg_dict['id'])+' AND')                
        elif arg_dict['geog'] == 'district':
            sql.append(r""", village vil, block b 
            WHERE  p.village_id = vil.id AND vil.block_id = b.id 
            AND b.district_id ="""+ str(arg_dict['id'])+' AND')
        elif arg_dict['geog'] == 'block':
            sql.append(r""", village vil 
            WHERE  p.village_id = vil.id AND vil.block_id ="""+ str(arg_dict['id'])+' AND')
        
        elif arg_dict['geog'] == 'village':
            sql.append(r' WHERE  p.village_id ='+ str(arg_dict['id'])+' AND')

    if 'from_date' in arg_dict and 'to_date' in arg_dict:
        sql[1:1] = [",video vid"]
        sql[3:3] = ["vid.id = vs.video_id AND"]
        sql.append('vid.VIDEO_PRODUCTION_END_DATE BETWEEN \''+arg_dict['from_date']+'\' AND \''+arg_dict['to_date']+'\' AND')
    
    sql.append(r'vs.person_id = p.id GROUP BY p.GENDER')

    return ' '.join(sql)        
        
        
        