from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
from calendar import week
import datetime
import string
from dg.output  import database
from dg.output.database import run_query, run_query_dict, construct_query, video_malefemale_ratio
import django 

def overview(request,geog,id):
    
    if('village' in request.GET and request.GET['village'] and request.GET['village']!='-1'):
        geog = 'village'
        id = int(request.GET['village'])
    elif('block' in request.GET and request.GET['block'] and request.GET['block']!='-1'):
        geog = 'block'
        id = int(request.GET['block'])
    elif('district' in request.GET and request.GET['district'] and request.GET['district']!='-1'):
        geog = 'district'
        id = int(request.GET['district'])        
    elif('state' in request.GET and request.GET['state']): 
        if(request.GET['state']=='-1'):
            geog='country'
            id = 1
        else:
            geog = 'state'
            id = int(request.GET['state'])    
         
    geog_list = ['country','state','district','block','village']
    if(geog not in geog_list):
        raise Http404()
            
    
    if(geog == 'village'):
        geog_child = 'village'
    
    else:
        geog_child = geog_list[geog_list.index(geog)+1]
    
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1

        from_date = request.GET['from_date']
        temp = string.split(from_date,'-')
        temp.reverse()
        mysql_from_date='-'.join(temp)

        to_date = request.GET['to_date']
        temp = string.split(to_date,'-')
        temp.reverse()
        mysql_to_date='-'.join(temp)
        
        par_geog = run_query(database.overview_sum_geog(dict(geog=geog,from_date=mysql_from_date,to_date=mysql_to_date,id=id)))
        vid_prod = run_query(construct_query(database.overview,dict(type='production',geography=geog,geog_child=geog_child,from_date=mysql_from_date,to_date=mysql_to_date,id=id)));
        vid_screening = run_query(construct_query(database.overview,dict(type='screening',geography=geog,geog_child=geog_child,from_date=mysql_from_date,to_date=mysql_to_date,id=id)));
        adoption = run_query(construct_query(database.overview,dict(type='adoption',geography=geog,geog_child=geog_child,from_date=mysql_from_date,to_date=mysql_to_date,id=id)));
        tot_prac = run_query(construct_query(database.overview,dict(type='practice',geography=geog,geog_child=geog_child,from_date=mysql_from_date,to_date=mysql_to_date,id=id)));
        tot_per = run_query(construct_query(database.overview,dict(type='person',geography=geog,geog_child=geog_child,from_date=mysql_from_date,to_date=mysql_to_date,id=id)));

    else:
        date_range = 0
        par_geog = run_query(database.overview_sum_geog(dict(geog=geog,id=id)))
        vid_prod = run_query(construct_query(database.overview,dict(type='production',geography=geog,geog_child=geog_child,id=id)));
        vid_screening = run_query(construct_query(database.overview,dict(type='screening',geography=geog,geog_child=geog_child,id=id)));
        adoption = run_query(construct_query(database.overview,dict(type='adoption',geography=geog,geog_child=geog_child,id=id)));
        tot_prac = run_query(construct_query(database.overview,dict(type='practice',geography=geog,geog_child=geog_child,id=id)));
        tot_per = run_query(construct_query(database.overview,dict(type='person',geography=geog,geog_child=geog_child,id=id)));
    
    return_val = vid_prod
    if (len(vid_screening) != len(return_val)) or (len(return_val)!=len(adoption))or \
    (len(return_val)!=len(tot_per)) or (len(return_val)!=len(tot_prac)):
        raise Exception,"Query return list not of same size"
    for i in range(len(vid_screening)):
        if (vid_screening[i]['name'] != return_val[i]['name']) or \
        (adoption[i]['name'] != return_val[i]['name']) or (tot_per[i]['name'] != return_val[i]['name']) or \
        (tot_prac[i]['name'] != return_val[i]['name']):
            raise Exception,"Query return list do not match"
        
        return_val[i]['tot_ado'] = adoption[i]['tot_ado']
        return_val[i]['tot_scr'] = vid_screening[i]['tot_scr']
        return_val[i]['tot_pra'] = tot_prac[i]['tot_pra']
        return_val[i]['tot_per'] = tot_per[i]['tot_per'] 
    if date_range==1:
        return render_to_response('overview.html',{'item_list':return_val,'geography':geog_child,'flash_geog':geog,'id':id,\
                                                 'from_date':from_date,'to_date':to_date,'flash_from_date':mysql_from_date,'flash_to_date':mysql_to_date,'par_geog':par_geog[0]})
    else:
        return render_to_response('overview.html',{'item_list':return_val,'geography':geog_child,'flash_geog':geog,'id':id,'par_geog':par_geog[0]})
    
def overview_drop_down(request):
    if 'geog' in request.GET and request.GET['geog'] \
     and 'id' in request.GET and request.GET['id']:
         geog = request.GET['geog']
         id = request.GET['id']
         id = int(id)
    else:
        raise Http404()
    geog_list = ['state','district','block','village']
    if geog=='state':
        geog_parent = 'state'
    else:
        geog_parent = geog_list[geog_list.index(geog)-1]
    
    
    temp = """
    <option value='-1'>Select {{geog|title}}</option>
    {% for row in rs %}
    <option value="{{row.id}}">{{row.name}}</option>
    {%endfor%}
    """
    t = django.template.Template(temp);
    rs = run_query(construct_query(database.search_drop_down_list,dict(geog=geog,geog_parent=geog_parent,id=id)));
    html = t.render(django.template.Context(dict(geog=geog,rs=rs)))
    
    return HttpResponse(html)
    
         
def overview_line_graph(request,geog,id):
    id = int(id)
    vid_prod_rs = run_query_dict(construct_query(database.overview_line_chart,dict(type='production',geography=geog,id=id)),'date');
    sc_rs = run_query_dict(construct_query(database.overview_line_chart,dict(type='screening',geography=geog,id=id)),'date');
    adopt_rs = run_query_dict(construct_query(database.overview_line_chart,dict(type='adoption',geography=geog,id=id)),'date');
    prac_rs = run_query_dict(construct_query(database.overview_line_chart,dict(type='practice',geography=geog,id=id)),'date');
    person_rs = run_query_dict(construct_query(database.overview_line_chart,dict(type='person',geography=geog,id=id)),'date');
        
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
    

# Pie chart for male-female ratio in video module  
def video_pie_graph_mf_ratio(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        male_female_ratio_sql = video_malefemale_ratio(dict(geog = geog, id = id,from_date = from_date, to_date = to_date))    
    
    else:
        male_female_ratio_sql = video_malefemale_ratio(dict(geog = geog, id = id))
    
    return_val = run_query(male_female_ratio_sql);
  
    str_list = []
    str_list.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    if return_val == []:
        str_list.append('There are No Video Productions in this region')
    else:
        for i in range(len(return_val)):
            if return_val[i]['gender'] == 'F':
                str_list.append('Female;'+return_val [i]['count'].__str__()+\
                                ';;;;Ratio of videos featuring Female actors')
            else:
                str_list.append('Male;'+return_val [i]['count'].__str__()+\
                                ';;#3299CC;;Ratio of videos featuring male actors')
       
    
    return HttpResponse('\n'.join(str_list))    
    
    