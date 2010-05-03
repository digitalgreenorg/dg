from dg.output.database.utility import *


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

def get_partners_sql(geog, id):
    geog = geog.upper()
    if geog not in ["COUNTRY", "STATE"]:
        return ''
    
    sql_ds = getInitSQLds()
    sql_ds['select'].extend(["DISTINCT P.id", "P.PARTNER_NAME"])
    sql_ds['from'].append("DISTRICT D")
    sql_ds['join'].append(["PARTNERS P", "P.id = D.partner_id"])
    if (geog=="STATE"):
        sql_ds['where'].append("D.state_id = "+str(id))
    
    return joinSQLds(sql_ds);

def child_geog_list(request, geog, id):
    from_date, to_date, partner_id = getDatesPartners(request)
    geog = geog.upper()
    if(geog == "COUNTRY"):
        sql = "SELECT DISTINCT S.id, STATE_NAME AS name from STATE S"
        if(partner_id):
            sql+=  """ JOIN DISTRICT D ON (D.state_id = S.id)
                  WHERE D.partner_id in ("""+','.join(partner_id)+")"
    elif(geog == "STATE"):
        sql = """SELECT DISTINCT D.id, DISTRICT_NAME AS name from DISTRICT D
                  WHERE state_id = """+str(id)
        if(partner_id):
            dist_part = run_query_raw("SELECT DISTINCT partner_id FROM DISTRICT WHERE state_id = "+str(id))
            filtered_partner_list = [str(x[0]) for x in dist_part if str(x[0]) in partner_id]
            if(filtered_partner_list):
                sql += " AND D.partner_id in ("+','.join(filtered_partner_list)+")"
    elif(geog == 'DISTRICT'):
        sql="SELECT id, BLOCK_NAME as name FROM BLOCK where district_id = "+str(id)
    elif(geog == "BLOCK"):
        sql="SELECT id, VILLAGE_NAME AS name FROM VILLAGE WHERE block_id = "+str(id)
    elif(geog == "VILLAGE"):
        sql="SELECT id, VILLAGE_NAME AS name FROM VILLAGE WHERE id = "+str(id);
    else:
        sql = ''
    
    return sql;

def method_overview(request, geog,id, type):
    geog = geog.upper();
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    from_date, to_date, partners = getDatesPartners(request)
    
    if(geog == 'VILLAGE'):
        geog_child = 'VILLAGE'
    else:
        geog_child = geog_list[geog_list.index(geog)+1]
    
    date_field = main_tab_abb = ''
    sql_ds = getInitSQLds();
    if(geog=="VILLAGE"):
        sql_ds['select'].append("village_id as id")
    else:
        sql_ds['select'].append(geog_child[0]+".id as id")
    if(type == 'production'):
        sql_ds['select'].append('COUNT(DISTINCT VID.id) as tot_pro')
        sql_ds['from'].append('VIDEO VID')
        main_tab_abb = "VID"
        date_field = "VID.VIDEO_PRODUCTION_END_DATE"
    elif(type=='screening'):
        sql_ds['select'].append('COUNT(DISTINCT SC.id) as tot_scr')
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
        sql_ds['select'].append('COUNT(DISTINCT P.id) as tot_per')
        sql_ds['from'].append('PERSON P')
        main_tab_abb = 'P'
        if(from_date is not None and to_date is not None):
            sql_ds['join'].append(["""(
            SELECT person_id, min(date) as DATE
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
                WHERE pa.screening_id = sc.id ) TMP
                GROUP BY person_id
            )AS TAB""", "TAB.person_id = P.id"])
            date_field = "TAB.DATE"
            
    
    if(geog=="COUNTRY"):
        #Hacking attachGeogDate for attaching geography till state in country case.
        attachGeogDate(sql_ds,main_tab_abb,date_field,'state',0, from_date,to_date)
        sql_ds['where'].pop();
        if(partners):
            sql_ds['where'].append("D.id in (SELECT id FROM DISTRICT WHERE partner_id in ("+','.join(partners)+"))")
        sql_ds['lojoin'].append(['STATE S','S.id = D.state_id']);
    else:
        filterPartnerGeogDate(sql_ds,main_tab_abb,date_field,geog,id,from_date,to_date,partners)
    
    if(geog!="VILLAGE"):
        sql_ds['group by'].append(geog_child+"_NAME")
        sql_ds['order by'].append(geog_child+"_NAME")
    
    return joinSQLds(sql_ds);
    
#Query for Total Video Production in Overview module
#Context Required:'type' can be (production/screening/adoption/practice/person)
#                :'geography' can be (state/district/block/village
#                : 'to_date' and 'from_date' (as required by MySQL format) are OPTIONAL
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
    
def method_overview_line_chart(request,geog,id,type):
    sql_ds = getInitSQLds();
    sql_inn_ds = getInitSQLds();
    from_date, to_date, partners = getDatesPartners(request)
    
    if(type=='practice'):
        sql_ds['select'].extend(["date", "COUNT(*)"])
        
        sql_inn_ds = getInitSQLds();
        sql_inn_ds['select'].extend(["VRAP.practices_id" , "MIN(VIDEO_PRODUCTION_END_DATE) AS date"])
        sql_inn_ds['from'].append("VIDEO VID");
        sql_inn_ds['join'].append(["VIDEO_related_agricultural_practices VRAP","VRAP.video_id = VID.id"])
        filterPartnerGeogDate(sql_inn_ds,'VID','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("practices_id");
        
        sql_ds['from'].append('('+joinSQLds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
    elif(type=='person'):
        sql_ds['select'].extend(["date", "COUNT(*)"])
        
        sql_inn_ds = getInitSQLds();
        sql_inn_ds['select'].extend(["person_id", "MIN(date) as date"])
        sql_inn_ds['from'].append("""(
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

        ) as tab""");
        if(geog.upper()!="COUNTRY" or partners):
            sql_inn_ds['join'].append(["PERSON P","P.id = tab.person_id"])
            filterPartnerGeogDate(sql_inn_ds,'P','dummy',geog,id,None,None,partners)
        sql_inn_ds['group by'].append("tab.person_id");
        
        sql_ds['from'].append('('+joinSQLds(sql_inn_ds)+') as tab1')
        sql_ds['group by'].append('date');
    elif(type=='production'):
        sql_ds['select'].extend(["VIDEO_PRODUCTION_END_DATE as date", "count(*)"])
        sql_ds['from'].append("VIDEO VID");
        filterPartnerGeogDate(sql_ds,'VID','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("VIDEO_PRODUCTION_END_DATE");
    elif(type=='screening'):
        sql_ds['select'].extend(["DATE AS date", "count(*)"])
        sql_ds['from'].append("SCREENING SC");
        filterPartnerGeogDate(sql_ds,'SC','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("DATE");
    elif(type=='adoption'):
        sql_ds['select'].extend(["DATE_OF_ADOPTION AS date", "count(*)"])
        sql_ds['from'].append("PERSON_ADOPT_PRACTICE PAP");
        if(geog.upper()!="COUNTRY" or partners):
            sql_ds['join'].append(["PERSON P","P.id = PAP.person_id"])
            filterPartnerGeogDate(sql_ds,'P','dummy',geog,id,None,None,partners)
        sql_ds['group by'].append("DATE_OF_ADOPTION");
        
    if(from_date is not None and to_date is not None):
        sql_ds['having'].append("date between '"+from_date+"' and '"+to_date+"'")
        
    return joinSQLds(sql_ds)

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

