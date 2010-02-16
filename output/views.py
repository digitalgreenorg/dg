from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
from calendar import week
import datetime
from dg.output.run_query import *

def test_output(request):
    
    return render_to_response('amline.html')

def state_overview(request):
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
    else:   
        date_range = 0
        
    vid_prod_sql = """
    SELECT s.id, STATE_NAME as name, COUNT(vid.id) as tot_vid
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id 
    """
    
    vid_screening_sql = """
    SELECT s.id, STATE_NAME as name, COUNT(sc.id) as tot_screen
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN screening sc on (sc.village_id = vil.id
    """
    
    adoption_sql = """
    SELECT s.id, STATE_NAME as name, COUNT(p_ad.id) as tot_adopt
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id)
        LEFT OUTER JOIN person_adopt_practice p_ad  on (p_ad.person_id = p.id
    """
    
    tot_prac_sql = """
    SELECT count(distinct vid_pr.practices_id) as tot_prac, STATE_NAME as name
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id)
        LEFT OUTER JOIN video_related_agricultural_practices vid_pr
                ON (vid_pr.video_id = vid.id
     """
    
    tot_person_sql = """ 
    SELECT COUNT(p.id) as tot_per, STATE_NAME as name
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id 
    
    """
    
    if date_range == 1: 
        vid_prod_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        
        vid_screening_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        
        adoption_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        
        tot_prac_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date'])
        
        tot_person_sql += """ AND  p.id in 
                                (
                                    SELECT vs.person_id
                                    FROM video_farmers_shown vs, video v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT person_id
                                    FROM person_adopt_practice
                                    WHERE DATE_OF_ADOPTION BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM person_meeting_attendance pa, screening sc
                                    WHERE pa.screening_id = sc.id
                                    AND sc.DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                )
                            """ % (request.GET['from_date'], request.GET['to_date'],request.GET['from_date'],\
                                   request.GET['to_date'],request.GET['from_date'], request.GET['to_date']) 
    
    vid_prod_sql += """)
    GROUP BY STATE_NAME
    ORDER BY STATE_NAME
    """
    vid_screening_sql += """)
    GROUP BY STATE_NAME
    ORDER BY STATE_NAME
    """
    adoption_sql += """)
    GROUP BY STATE_NAME
    ORDER BY STATE_NAME
    """
    tot_prac_sql += """)
    GROUP BY STATE_NAME
    ORDER BY STATE_NAME
    """
    tot_person_sql += """)
    GROUP BY STATE_NAME
    ORDER BY STATE_NAME
    """
    
    vid_prod = run_query(vid_prod_sql);
    vid_screening = run_query(vid_screening_sql);
    adoption = run_query(adoption_sql);
    tot_prac = run_query(tot_prac_sql);
    tot_per = run_query(tot_person_sql);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption))or \
    (len(return_val)!=len(tot_per)) or (len(return_val)!=len(tot_prac)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']) or (tot_per[i]['name'] != return_val[i]['name']) or \
        (tot_prac[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen']
        return_val[i]['tot_prac'] = tot_prac[i]['tot_prac']
        return_val[i]['tot_per'] = tot_per[i]['tot_per'] 
        
    return render_to_response('viewtable.html',{'item_list':return_val,'geography':'state'})
        
        
def district_overview(request,id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
    else:
        date_range = 0
    
    

    tot_vid_sql = """
    SELECT d.id, DISTRICT_NAME as name, COUNT(vid.id) as tot_vid
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id
        """
    
    tot_adopt_sql = """
    SELECT d.id, DISTRICT_NAME as name, COUNT(p_ad.id) as tot_adopt
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id)
        LEFT OUTER JOIN person_adopt_practice p_ad  on (p_ad.person_id = p.id
        """
    
    tot_screen_sql = """
    SELECT d.id, DISTRICT_NAME as name, COUNT(sc.id) as tot_screen
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN screening sc on (sc.village_id = vil.id        
        """
    tot_prac_sql = """
    SELECT count(distinct vid_pr.practices_id) as tot_prac, DISTRICT_NAME as name
    FROM district d
        LEFT OUTER JOIN state s on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id)
        LEFT OUTER JOIN video_related_agricultural_practices vid_pr
           on (vid_pr.video_id = vid.id
     """
    
    tot_person_sql = """
    SELECT count(p.id) as tot_per, DISTRICT_NAME as name
    FROM district d
        LEFT OUTER JOIN state s on (s.id = d.state_id )
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id
    """
    
    if date_range == 1: 
        tot_vid_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_screen_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_adopt_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_prac_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date'])
        
        tot_person_sql += """ AND  p.id in 
                                (
                                    SELECT vs.person_id
                                    FROM video_farmers_shown vs, video v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT person_id
                                    FROM person_adopt_practice
                                    WHERE DATE_OF_ADOPTION BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM person_meeting_attendance pa, screening sc
                                    WHERE pa.screening_id = sc.id
                                    AND sc.DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                )
                            """ % (request.GET['from_date'], request.GET['to_date'],request.GET['from_date'],\
                                   request.GET['to_date'],request.GET['from_date'], request.GET['to_date'])
        
    
    tot_vid_sql += """)
    WHERE s.id = %s
    GROUP BY DISTRICT_NAME
    ORDER BY DISTRICT_NAME
    """
    tot_screen_sql += """)
    WHERE s.id = %s
    GROUP BY DISTRICT_NAME
    ORDER BY DISTRICT_NAME
    """
    tot_adopt_sql += """)
    WHERE s.id = %s
    GROUP BY DISTRICT_NAME
    ORDER BY DISTRICT_NAME
    """
    tot_prac_sql += """)
    WHERE s.id = %s
    GROUP BY DISTRICT_NAME
    ORDER BY DISTRICT_NAME
    """
    tot_person_sql += """)
    WHERE s.id = %s
    GROUP BY DISTRICT_NAME
    ORDER BY DISTRICT_NAME
    """
    vid_prod = run_query(tot_vid_sql,id);
    vid_screening = run_query(tot_screen_sql,id);
    adoption = run_query(tot_adopt_sql,id);
    tot_prac = run_query(tot_prac_sql,id);
    tot_per = run_query(tot_person_sql,id);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption))or \
    (len(return_val)!=len(tot_per)) or (len(return_val)!=len(tot_prac)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']) or (tot_per[i]['name'] != return_val[i]['name']) or \
        (tot_prac[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen']
        return_val[i]['tot_prac'] = tot_prac[i]['tot_prac']
        return_val[i]['tot_per'] = tot_per[i]['tot_per']
    
    return render_to_response('viewtable.html',{'item_list':return_val,'geography':'district'})
    
def block_overview(request,id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
    else:
        date_range = 0

    tot_vid_sql = """
    SELECT b.id, BLOCK_NAME as name, COUNT(vid.id) as tot_vid
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id
       
    """
    
    tot_adopt_sql = """
    SELECT b.id, BLOCK_NAME as name, COUNT(p_ad.id) as tot_adopt
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id)
        LEFT OUTER JOIN person_adopt_practice p_ad  on (p_ad.person_id = p.id
       
    """
    
    tot_screen_sql = """
    SELECT b.id, BLOCK_NAME as name, COUNT(sc.id) as tot_screen
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN screening sc on (sc.village_id = vil.id
       
    """
    tot_prac_sql = """
    SELECT count(distinct vid_pr.practices_id) as tot_prac, BLOCK_NAME as name
    FROM block b
        LEFT OUTER JOIN district d on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id)
        LEFT OUTER JOIN video_related_agricultural_practices vid_pr
               on (vid_pr.video_id = vid.id
    """
    
    tot_person_sql = """
    SELECT count(p.id) as tot_per, BLOCK_NAME as name
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id        
    """
    if date_range == 1: 
        tot_vid_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_screen_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_adopt_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_prac_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date'])
        
        tot_person_sql += """ AND  p.id in 
                                (
                                    SELECT vs.person_id
                                    FROM video_farmers_shown vs, video v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT person_id
                                    FROM person_adopt_practice
                                    WHERE DATE_OF_ADOPTION BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM person_meeting_attendance pa, screening sc
                                    WHERE pa.screening_id = sc.id
                                    AND sc.DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                )
                            """ % (request.GET['from_date'], request.GET['to_date'],request.GET['from_date'],\
                                   request.GET['to_date'],request.GET['from_date'], request.GET['to_date'])
        
        
    tot_vid_sql += """)
    WHERE d.id = %s
    GROUP BY BLOCK_NAME
    ORDER BY BLOCK_NAME
    """
    tot_screen_sql += """)
    WHERE d.id = %s
    GROUP BY BLOCK_NAME
    ORDER BY BLOCK_NAME
    """
    tot_adopt_sql += """)
    WHERE d.id = %s
    GROUP BY BLOCK_NAME
    ORDER BY BLOCK_NAME
    """
    tot_prac_sql += """)
    WHERE d.id = %s
    GROUP BY BLOCK_NAME
    ORDER BY BLOCK_NAME
    """
    tot_person_sql += """)
    WHERE d.id = %s
    GROUP BY BLOCK_NAME
    ORDER BY BLOCK_NAME
    """

    vid_prod = run_query(tot_vid_sql,id);
    vid_screening = run_query(tot_screen_sql,id);
    adoption = run_query(tot_adopt_sql,id);
    tot_prac = run_query(tot_prac_sql,id);
    tot_per = run_query(tot_person_sql,id);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption))or \
    (len(return_val)!=len(tot_per)) or (len(return_val)!=len(tot_prac)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']) or (tot_per[i]['name'] != return_val[i]['name']) or \
        (tot_prac[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen']
        return_val[i]['tot_prac'] = tot_prac[i]['tot_prac']
        return_val[i]['tot_per'] = tot_per[i]['tot_per']
    
    return render_to_response('viewtable.html',{'item_list':return_val,'geography':'block'})


def village_overview(request,id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
    else:
        date_range = 0

    tot_vid_sql = """
    SELECT vil.id, VILLAGE_NAME as name, COUNT(vid.id) as tot_vid
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id
        """
    
    tot_adopt_sql = """
    SELECT vil.id, VILLAGE_NAME as name, COUNT(p_ad.id) as tot_adopt
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id)
        LEFT OUTER JOIN person_adopt_practice p_ad  on (p_ad.person_id = p.id
        """
    
    tot_screen_sql = """
    SELECT vil.id, VILLAGE_NAME as name, COUNT(sc.id) as tot_screen
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN screening sc on (sc.village_id = vil.id
        """


    tot_person_sql = """
    SELECT vil.id, VILLAGE_NAME as name, COUNT(p.id) as tot_per
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN person p on (p.village_id = vil.id
    """

    tot_prac_sql = """
    SELECT vil.id, count(distinct vid_pr.practices_id) as tot_prac, VILLAGE_NAME as name
    FROM state s
        LEFT OUTER JOIN district d on (s.id = d.state_id)
        LEFT OUTER JOIN block b on (b.district_id = d.id)
        LEFT OUTER JOIN village vil on (vil.block_id = b.id)
        LEFT OUTER JOIN video vid on (vid.village_id = vil.id)
        LEFT OUTER JOIN video_related_agricultural_practices vid_pr
           on (vid_pr.video_id = vid.id
        """

    
    if date_range == 1: 
        tot_vid_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_screen_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_adopt_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_prac_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date'])    
        
        tot_person_sql += """ AND  p.id in 
                                (
                                    SELECT vs.person_id
                                    FROM video_farmers_shown vs, video v
                                    WHERE vs.video_id = v.id
                                    AND v.VIDEO_PRODUCTION_END_DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT person_id
                                    FROM person_adopt_practice
                                    WHERE DATE_OF_ADOPTION BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
            
                                    UNION
            
                                    SELECT pa.person_id
                                    FROM person_meeting_attendance pa, screening sc
                                    WHERE pa.screening_id = sc.id
                                    AND sc.DATE BETWEEN str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                                AND str_to_date( '%s','%%%%d/%%%%m/%%%%Y')
                                )
                            """ % (request.GET['from_date'], request.GET['to_date'],request.GET['from_date'],\
                                   request.GET['to_date'],request.GET['from_date'], request.GET['to_date'])

        
        
    tot_vid_sql += """)
    WHERE b.id = %s
    GROUP BY VILLAGE_NAME
    ORDER BY VILLAGE_NAME
    """
    tot_screen_sql += """)
    WHERE b.id = %s
    GROUP BY VILLAGE_NAME
    ORDER BY VILLAGE_NAME
    """
    tot_adopt_sql += """)
    WHERE b.id = %s
    GROUP BY VILLAGE_NAME
    ORDER BY VILLAGE_NAME
    """
    tot_prac_sql += """)
    WHERE b.id = %s
    GROUP BY VILLAGE_NAME
    ORDER BY VILLAGE_NAME
    """
    tot_person_sql += """)
    WHERE b.id = %s
    GROUP BY VILLAGE_NAME
    ORDER BY VILLAGE_NAME
    """
    
    vid_prod = run_query(tot_vid_sql,id);
    vid_screening = run_query(tot_screen_sql,id);
    adoption = run_query(tot_adopt_sql,id);
    tot_prac = run_query(tot_prac_sql,id);
    tot_per = run_query(tot_person_sql,id);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption))or \
    (len(return_val)!=len(tot_per)) or (len(return_val)!=len(tot_prac)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']) or (tot_per[i]['name'] != return_val[i]['name']) or \
        (tot_prac[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen']
        return_val[i]['tot_prac'] = tot_prac[i]['tot_prac']
        return_val[i]['tot_per'] = tot_per[i]['tot_per']
    
    return render_to_response('viewtable.html',{'item_list':return_val,'geography':'village'})
    

#TODO: Add Error checking for empty result sets.
def overview_flash_state(request):
    vid_prod_sql = """
    SELECT VIDEO_PRODUCTION_END_DATE as date, count(*)
    FROM video
    GROUP BY VIDEO_PRODUCTION_END_DATE
    """
    
    sc_sql = """
    SELECT DATE AS date, COUNT(*) FROM SCREENING
    GROUP BY DATE
    """
    
    adopt_sql = """
    SELECT DATE_OF_ADOPTION as date, count(*)
    FROM PERSON_ADOPT_PRACTICE
    GROUP BY DATE_OF_ADOPTION
    """
    
    prac_sql = """
    SELECT VIDEO_PRODUCTION_END_DATE as date, count(DISTINCT vid_pr.practices_id)
      FROM video vid, video_related_agricultural_practices vid_pr
        WHERE vid.id = vid_pr.video_id
    GROUP BY VIDEO_PRODUCTION_END_DATE
    """
    
    person_sql = """
    SELECT date, count(*) 
    FROM (
        SELECT person_id, min(date) as date
        FROM (
            SELECT  vs.person_id, VIDEO_PRODUCTION_END_DATE AS date
            FROM video_farmers_shown vs, video v
            WHERE vs.video_id = v.id
    
            UNION
    
            SELECT  person_id , DATE_OF_ADOPTION AS date
            FROM person_adopt_practice
    
            UNION
    
            SELECT  pa.person_id, DATE
            FROM person_meeting_attendance pa, screening sc
            WHERE pa.screening_id = sc.id
        ) as tab
        GROUP BY person_id
    ) as tab1
    GROUP BY date   
    """
    
    
    vid_prod_rs = run_query_dict(vid_prod_sql,'date')
    sc_rs = run_query_dict(sc_sql,'date');
    adopt_rs = run_query_dict(adopt_sql, 'date');
    prac_rs = run_query_dict(prac_sql, 'date');
    person_rs = run_query_dict(person_sql, 'date');
    
    
    start_date = today = datetime.date.today()
    if vid_prod_rs:
        start_date = min(start_date, *(vid_prod_rs.keys()))
    if sc_rs:
        start_date = min(start_date,*(sc_rs.keys()))
    if adopt_rs:
        start_date = min(start_date,*(adopt_rs.keys()))
    if prac_rs:
        start_date = min(start_date,*(prac_rs.keys()))
    if person_rs:
        start_date = min(start_date,*(person_rs.keys()))
            
    diff = (today - start_date).days
    
    str_list = []
    sum_vid = sum_sc = sum_adopt =sum_prac = sum_person = 0
    for i in range(0,diff+1):
        iter_date = start_date + datetime.timedelta(days=i)
                
        if iter_date in vid_prod_rs:
            sum_vid += vid_prod_rs[iter_date][0]
        if iter_date in sc_rs:
            sum_sc += sc_rs[iter_date][0]
        if iter_date in adopt_rs:
            sum_adopt += adopt_rs[iter_date][0]
        if iter_date in prac_rs:
            sum_prac += prac_rs[iter_date][0]
        if iter_date in person_rs:
            sum_person += person_rs[iter_date][0]
        str_list.append(iter_date.__str__() +';'+ sum_vid.__str__()+';'+ sum_sc.__str__()+';'+ sum_adopt.__str__() \
                        +';'+ sum_prac.__str__()+';'+ sum_person.__str__())
        
    return HttpResponse('\n'.join(str_list))
     

def overview_flash_test(request,id):
    id = int(id)
    vid_prod_sql = """
    SELECT VIDEO_PRODUCTION_END_DATE as date, count(*)
    FROM video vid, village vil, block b, district d
    WHERE vid.village_id = vil.id AND vil.block_id = b.id AND b.district_id = d.id AND d.state_id =%s
    GROUP BY VIDEO_PRODUCTION_END_DATE
    """
    
    sc_sql = """
    SELECT DATE AS date, COUNT(*)
    FROM screening sc, village vil, block b, district d
    WHERE sc.village_id = vil.id AND vil.block_id = b.id AND b.district_id = d.id AND d.state_id = %s
    GROUP BY DATE;
    """
    
    adopt_sql = """
    SELECT DATE_OF_ADOPTION as date, count(*)
    FROM PERSON_ADOPT_PRACTICE pa, person p, village vil, block b, district d
    WHERE pa.person_id = p.id AND p.village_id = vil.id AND vil.block_id = b.id AND b.district_id = d.id 
            AND d.state_id = %s
    GROUP BY DATE_OF_ADOPTION
    """
    
    prac_sql = """
    SELECT date, COUNT(*)
    FROM(
         SELECT vid_pr.practices_id , MIN(VIDEO_PRODUCTION_END_DATE) AS date    
         FROM video vid, video_related_agricultural_practices vid_pr, village vil, block b, district d
         WHERE vid.id = vid_pr.video_id AND vid.village_id = vil.id AND vil.block_id = b.id 
             AND b.district_id = d.id AND d.state_id =%s
         GROUP BY practices_id
         ) AS tab1
     GROUP BY date
    """
    
    person_sql = """
    SELECT date, count(*)
    FROM (
        SELECT person_id, min(date) as date
        FROM (
            SELECT  vs.person_id, VIDEO_PRODUCTION_END_DATE AS date
            FROM video_farmers_shown vs, video vid, village vil, block b, district d
            WHERE vs.video_id = vid.id AND vid.village_id = vil.id AND vil.block_id = b.id
                 AND b.district_id = d.id AND d.state_id =%s

            UNION

            SELECT  person_id , DATE_OF_ADOPTION AS date
            FROM person_adopt_practice pa, person p, village vil, block b, district d
            WHERE pa.person_id = p.id AND p.village_id = vil.id AND vil.block_id = b.id 
                AND b.district_id = d.id AND d.state_id =%s

            UNION

            SELECT  pa.person_id, DATE
            FROM person_meeting_attendance pa, screening sc,village vil, block b, district d
            WHERE pa.screening_id = sc.id AND sc.village_id = vil.id
              AND vil.block_id = b.id AND b.district_id = d.id AND d.state_id =%s

        ) as tab
        GROUP BY person_id
    ) as tab1
    GROUP BY date
    """
    
    
    vid_prod_rs = run_query_dict(vid_prod_sql,'date',id)
    sc_rs = run_query_dict(sc_sql,'date',id);
    adopt_rs = run_query_dict(adopt_sql, 'date',id);
    prac_rs = run_query_dict(prac_sql, 'date',id);
    person_rs = run_query_dict(person_sql, 'date',id,id,id);
    
    
    start_date = today = datetime.date.today()
    if vid_prod_rs:
        start_date = min(vid_prod_rs.keys())
    if sc_rs:
        start_date = min(sc_rs.keys())
    if adopt_rs:
        start_date = min(adopt_rs.keys())
    if prac_rs:
        start_date = min(prac_rs.keys())
    if person_rs:
        start_date = min(person_rs.keys())
            
    diff = (today - start_date).days
    
    str_list = []
    sum_vid = sum_sc = sum_adopt =sum_prac = sum_person = 0
    for i in range(0,diff+1):
        iter_date = start_date + datetime.timedelta(days=i)
                
        if iter_date in vid_prod_rs:
            sum_vid += vid_prod_rs[iter_date][0]
        if iter_date in sc_rs:
            sum_sc += sc_rs[iter_date][0]
        if iter_date in adopt_rs:
            sum_adopt += adopt_rs[iter_date][0]
        if iter_date in prac_rs:
            sum_prac += prac_rs[iter_date][0]
        if iter_date in person_rs:
            sum_person += person_rs[iter_date][0]
        str_list.append(iter_date.__str__() +';'+ sum_vid.__str__()+';'+ sum_sc.__str__()+';'+ sum_adopt.__str__() \
                        +';'+ sum_prac.__str__()+';'+ sum_person.__str__())
        
    return HttpResponse('\n'.join(str_list))

    
    
    
    