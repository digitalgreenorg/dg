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

#this returns 
#{ dict_key : (tuple of remaing columns), ...}

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

#this returns 
#{ dict_key : [list of remaing columns], ...}

def run_query_dict_list(query_string, dict_key, *query_args):
    return_list = {}
    cursor = connection.cursor()
    cursor.execute(query_string,query_args)
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    if(dict_key != col_names[0]):
        raise Exception, dict_key+" is not the first column in returned query's column list"
    for row in rows:
        return_list[row[0]] = list(row[1:])
        
    return return_list


    
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

#Query for breadcrumbs
#Params: geog - options to be calculated for this geog
#        id - id of 'geog' if is_child = false else it's parent geog's id
#        is_child: flag(0/1) if the options are one level below then selected
#                e.g for district 'x', option for x's blocks must be presented with nothing pre-selected.
def breadcrumbs_options_sql(geog,id, is_child):
    geog_list = ['village','block','district','state'];
    
    if(geog=='state'):
        return 'SELECT id, STATE_NAME as name FROM STATE'
    
    par_geog = geog_list[geog_list.index(geog)+1]; 
    
    if(is_child == 1):
        return construct_query(""" SELECT id, {{geog|upper}}_NAME 
            FROM {{geog|upper}}
            WHERE {{par_geog}}_id = {{id}}
        """,dict(geog=geog,id=id,par_geog=par_geog))
    
    return construct_query("""SELECT {{geog|first}}1.id ,{{geog|first}}1.{{geog|upper}}_NAME, {{geog|first}}1.{{par_geog}}_id
    FROM {{geog|upper}} {{geog|first}}1, {{geog|upper}} {{geog|first}}2
    WHERE {{geog|first}}1.{{par_geog}}_id = {{geog|first}}2.{{par_geog}}_id
        and {{geog|first}}2.id = {{id}}""",dict(geog=geog,par_geog=par_geog,id=id))




#Query for Total Video Production in Overview module
#Context Required:'type' can be (production/screening/adoption/practice/person)
#                :'geography' can be (state/district/block/village
#                : 'to_date' and 'from_date' (as required by MySQL) are OPTIONAL
#                : id of parent geography (e.g. for 'district' parent is 'state'). For state, this can be omitted
overview = r"""    
    SELECT {{geog_child|first }}.id as id, {{geog_child|upper }}_NAME as name, COUNT({% ifequal type 'practice' %} distinct vid_pr.practices_id {%else%}{{type|slice:":3"}}.id {%endifequal%}) as tot_{{type|slice:":3"}}
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
        {%ifequal geography 'country' %}
            WHERE vid.id = vid_pr.video_id
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

