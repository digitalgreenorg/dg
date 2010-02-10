from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
from calendar import week
import datetime
from dg.output.run_query import *

def test_output(request, url):
    date = datetime.date.today()
    weekdelta = datetime.timedelta(weeks = -1)
    
    test_val = Village.objects.filter(start_date__range=(date+weekdelta, date)).count()
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
    
    if date_range == 1: 
        vid_prod_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        vid_screening_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        adoption_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
    
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
    
    
    vid_prod = run_query(vid_prod_sql);
    vid_screening = run_query(vid_screening_sql);
    adoption = run_query(adoption_sql);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen'] 
    
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
    
    if date_range == 1: 
        tot_vid_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_screen_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_adopt_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
    
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
    
    vid_prod = run_query(tot_vid_sql,id);
    vid_screening = run_query(tot_screen_sql,id);
    adoption = run_query(tot_adopt_sql,id);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen'] 
    
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
    
    if date_range == 1: 
        tot_vid_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_screen_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_adopt_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
    
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
    
    vid_prod = run_query(tot_vid_sql,id);
    vid_screening = run_query(tot_screen_sql,id);
    adoption = run_query(tot_adopt_sql,id);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen'] 
    
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
    
    if date_range == 1: 
        tot_vid_sql += " AND VIDEO_PRODUCTION_END_DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_screen_sql += " AND sc.DATE between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
        tot_adopt_sql += " AND p_ad.DATE_OF_ADOPTION between str_to_date( '%s','%%%%d/%%%%m/%%%%Y') \
        and str_to_date( '%s','%%%%d/%%%%m/%%%%Y') " % (request.GET['from_date'], request.GET['to_date']) 
    
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

    
    vid_prod = run_query(tot_vid_sql,id);
    vid_screening = run_query(tot_screen_sql,id);
    adoption = run_query(tot_adopt_sql,id);
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_adopt'] = adoption[i]['tot_adopt']
        return_val[i]['tot_screen'] = vid_screening[i]['tot_screen'] 
    
    return render_to_response('viewtable.html',{'item_list':return_val,'geography':'village'})
    

def overview_flash_output(request):
    vid_prod_sql = """
    SELECT VIDEO_PRODUCTION_END_DATE as date, count(*)
    FROM video
    GROUP BY VIDEO_PRODUCTION_END_DATE
    """
    
    vid_prod_rs = run_query_dict(vid_prod_sql,'date')
    
    start_date = min(vid_prod_rs.keys())
    today = datetime.date.today()
    
    diff = (today - start_date).days
    
    str_list = []
    sum = 0
    for i in range(1,diff+1):
        iter_date = start_date + datetime.timedelta(days=i)
                
        if iter_date in vid_prod_rs:
            sum += vid_prod_rs[iter_date][0]
        
        str_list.append(iter_date.__str__() +';'+ sum.__str__())
        
    return HttpResponse('\n'.join(str_list))
            
        
        

    

    
    
    
    