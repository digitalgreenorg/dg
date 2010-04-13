from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
from dg.output.database  import common
from dg.output.database.common import run_query, run_query_dict, run_query_dict_list, construct_query
import datetime
import django 
import re


def test_output(request,geog,id):
    
    #return render_to_response('amcolumn.html')
    return render_to_response('amcolumn.html',{'flash_geog':geog,'id':id})

  
#function for breadcrumbs
#returns a list of geog upto state
#Datastructure returned is [{state_id:((state_name),true if this should be marked as selected else it's not nested tuple),..},
#                           {district_id: ---do---  ,district_id:.........}]              
def breadcrumbs_options(geog,id):
    id = int(id)
    if(geog=='country'):
        return breadcrumbs_options('state',-1);
    geog_list = ['village','block','district','state'];
    return_val = []
    
    if(geog!='village'):
        return_val.append(run_query_dict_list(common.breadcrumbs_options_sql(geog_list[geog_list.index(geog)-1],id,1),'id'))
    #Starting from the passed geog, we'll calculate 'options' and append to return_val,
    #and end up at top most geog 'state'.    
    for i in range(geog_list.index(geog),len(geog_list)):
        geog = geog_list[i]
        query_return = run_query_dict_list(common.breadcrumbs_options_sql(geog,id,0),'id')
        if(id!=-1):
            query_return[id].append('true')  
        if(geog!='state'):    
            id  = query_return[id][1]    
           
        return_val.append(query_return);
    
    return_val.reverse();
    return return_val 
    
#Responds to AJAX calls on geography selection for dropdown.
#Returns Options list for the child geography.
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
    rs = run_query(construct_query(common.search_drop_down_list,dict(geog=geog,geog_parent=geog_parent,id=id)));
    html = t.render(django.template.Context(dict(geog=geog,rs=rs)))
    
    return HttpResponse(html)
    

#This is the method to generate Data for line graph for # vs time. (eg Overview module)
#Takes 'type' GET param which can be 'prod','screen','prac','person','adopt'
#    Based on the 'type', it generates the data for that set only
#    If 'type' is not specified, it generates for all.         
def overview_line_graph(request,geog,id):
    id = int(id)
    if('type' in request.GET):
        type = request.GET.getlist('type')
    else:
        type = ['prod','screen','prac','person','adopt']
    
    if('prod' in type):
        vid_prod_rs = run_query_dict(construct_query(common.overview_line_chart,dict(type='production',geography=geog,id=id)),'date');
    else:
        vid_prod_rs = []
        
    if('screen' in type):
        sc_rs = run_query_dict(construct_query(common.overview_line_chart,dict(type='screening',geography=geog,id=id)),'date');
    else:
        sc_rs = []
        
    if('adopt' in type):
        adopt_rs = run_query_dict(construct_query(common.overview_line_chart,dict(type='adoption',geography=geog,id=id)),'date');
    else:
        adopt_rs = []
        
    if('prac' in type):
        prac_rs = run_query_dict(construct_query(common.overview_line_chart,dict(type='practice',geography=geog,id=id)),'date');
    else:
        prac_rs = []
        
    if('person' in type):
        person_rs = run_query_dict(construct_query(common.overview_line_chart,dict(type='person',geography=geog,id=id)),'date');
    else:
        person_rs = []
        
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
            
        append_str = iter_date.__str__() +';'
        if('prod' in type): append_str += str(sum_vid)+';'
        if('screen' in type): append_str += str(sum_sc)+';'       
        if('adopt' in type): append_str += str(sum_adopt)+';'    
        if('prac' in type): append_str +=  str(sum_prac)+';'   
        if('person' in type): append_str += str(sum_person)+';'
        
        
        str_list.append(append_str[:-1])
        
    if(len(str_list)==1):
        m = re.search("^\d\d\d\d-\d\d-\d\d((;0)*)$",str_list[0]);
        if(m!=None): return HttpResponse(re.sub(r'0','',m.group(1)));
    else:
        return HttpResponse('\n'.join(str_list))

    
