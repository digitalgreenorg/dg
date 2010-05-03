from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
from dg.output.database  import utility
from dg.output.database.SQL import sharedSQL
from dg.output.database.utility import run_query, run_query_dict, run_query_dict_list, construct_query
import datetime
import django 
import re, random


def test_output(request,geog,id=None):
    
    #return render_to_response('amcolumn.html')
    return render_to_response('test.html',{'flash_geog':geog,'id':id})

  
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
        return_val.append(run_query_dict_list(sharedSQL.breadcrumbs_options_sql(geog_list[geog_list.index(geog)-1],id,1),'id'))
    #Starting from the passed geog, we'll calculate 'options' and append to return_val,
    #and end up at top most geog 'state'.    
    for i in range(geog_list.index(geog),len(geog_list)):
        geog = geog_list[i]
        query_return = run_query_dict_list(sharedSQL.breadcrumbs_options_sql(geog,id,0),'id')
        if(id!=-1):
            query_return[id].append('true')  
        if(geog!='state'):    
            id  = query_return[id][1]    
           
        return_val.append(query_return);
    
    return_val.reverse();
    return return_val 

#Returns a dictionary containing parameters for the search box on the right hand side of the page.
def get_search_box(request,geog,id, min_date_func):
    from_date, to_date, partner = utility.getDatesPartners(request);
    search_box_params = {}
    search_box_params['partners'] = get_partner_list(geog,id, partner);
    if(from_date and to_date):
        search_box_params['is_date_selected'] = 1
    else:
        search_box_params['is_date_selected'] = 0
        from_date =  (run_query(min_date_func(request, geog, id)))[0]['date']
        if(not from_date):
            from_date = datetime.date.today()
        to_date = datetime.date.today()
    
    search_box_params['from_date'] = from_date
    search_box_params['to_date'] = to_date
    search_box_params['geog_val'] = breadcrumbs_options(geog,id)
    search_box_params['cur_geog'] = geog
    search_box_params['cur_id'] = id
    search_box_params['base_url'] = '/'.join(request.path.split('/')[:-3] + [''])
    
    

    return search_box_params
    
    
#Returns a dictionary of list of PARTNER_NAME, id
#If partners were selected i.e. argument 'partners' is not empty,
#  those that are not present are marked with 'unmarked = 1'
def get_partner_list(geog,id, partners):
    sql = sharedSQL.get_partners_sql(geog,id)
    if(sql):
         part_list = run_query(sql)
         if(not partners or len(part_list) == 1):
             return part_list
         filtered_partners = [x['id'] for x in part_list if str(x['id']) in partners]
         for partner in part_list:
             if partner['id'] not in filtered_partners:
                 partner['unmarked'] = 1        
         return part_list
    else:
        return {}
    
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
    rs = run_query(construct_query(sharedSQL.search_drop_down_list,dict(geog=geog,geog_parent=geog_parent,id=id)));
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
        vid_prod_rs = run_query_dict(sharedSQL.method_overview_line_chart(type='production',geog=geog,id=id, request=request),'date');
    else:
        vid_prod_rs = []
        
    if('screen' in type):
        sc_rs = run_query_dict(sharedSQL.method_overview_line_chart(type='screening',geog=geog,id=id, request=request),'date');
    else:
        sc_rs = []
        
    if('adopt' in type):
        adopt_rs = run_query_dict(sharedSQL.method_overview_line_chart(type='adoption',geog=geog,id=id, request=request),'date');
    else:
        adopt_rs = []
        
    if('prac' in type):
        prac_rs = run_query_dict(sharedSQL.method_overview_line_chart(type='practice',geog=geog,id=id, request=request),'date');
    else:
        prac_rs = []
        
    if('person' in type):
        person_rs = run_query_dict(sharedSQL.method_overview_line_chart(type='person',geog=geog,id=id, request=request),'date');
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
    
    
#generic functin to render Pie Chart data 
#sqlFunc is the function to generate SQL query, should generate first select column as 'pie_key'
#pieNameDict is the dictionary in which key is the database entry (like "M") and value is the one that 
#        is show in Pie chart (Like "Male" for "M")
#desc is the description string for the pie, can use variables  - {{key}}, {{value}} within it 
def pie_chart_data(request,geog,id,sqlFunc,pieNameDict, desc):
    id = int(id)
    """
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query_dict(sqlFunc(geog=geog,id=id,from_date=from_date,to_date=to_date),'pie_key')
    
    else:
        rs = run_query_dict(sqlFunc(geog=geog,id=id),'pie_key')
    """
    rs = run_query_dict(sqlFunc(request,geog,id),'pie_key')
    str_list = []
    str_list.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    if not rs:
       return HttpResponse(';')
    else:
        for key, value in pieNameDict.iteritems():
            if(key in rs):
                str_list.append(value+';'+str(rs[key][0])+';;;;'+re.sub('{{key}}',str(key),re.sub('{{value}}',str(value),desc)))
            else:
                str_list.append(value+';0;;;;'+re.sub('{{key}}',str(key),re.sub('{{value}}',str(value),desc)))
                
    return HttpResponse('\n'.join(str_list))

#generic function to render data for Scatter Charts
#sqlFunc is the function which renders the SQL query.
#Pre-requisite: SQL function should generate name, count & in that order.(Other variable names would throw error)
def scatter_chart_data(request,geog,id,sqlFunc):
    id = int(id)
    
    """
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query(sqlFunc(geog=geog,id=id,from_date=from_date,to_date=to_date))
    
    else:
        rs = run_query(sqlFunc(geog=geog,id=id))
    """
    
    rs = run_query(sqlFunc(request,geog=geog,id=id))
    if not rs:
        return HttpResponse(' ');
    
    count_dict = {}
    for item in rs:
        if item['count'] in count_dict:
            count_dict[item['count']].append(item['name'])
        else:
            count_dict[item['count']] = [item['name']]
    
    x_axis_len = max([len(x) for x in count_dict.values()]) * 2
    if(x_axis_len<10): x_axis_len = 10;
    return_val = []
    return_val.append('[x];[y];[value];[bullet_color];[bullet_size];[url];[description]')
    
    random.seed();
    for tot,pracs in count_dict.iteritems():
        flag = [ 0 for i in range(0,x_axis_len+1)]
        for prac in pracs:        
            x = random.randrange(1,x_axis_len)
            while(flag[x] != 0):
                x = random.randrange(1,x_axis_len)
            flag[x] = 1
            return_val.append(str(x)+';'+str(tot)+';'+str(tot)+';;;;'+prac)
    
    return HttpResponse('\n'.join(return_val))


#MyDate class, a 'type' with attrib month, m and year, y.(Used in view of Monthwise bar graph)
#Methods addMonth: adds 'x' number of months to itself.
#                Doesn't allow negative month addition (for simplicity)
#        compare: compares itself with another MyDate object and returns -1 (if self is lesser), 0 , 1.
class MyDate:
    def __str__(self):
        return (str(self.m)+','+str(self.y))
    
    def __init__(self, month, year):
        if(month not in range(1,13)):
            raise Exception,"Invalid Params"
        self.m = month
        self.y = year
    
    def addMonth(self,delta):
        if delta < 1:
            raise Exception('Only positive delta allowed')
        
        self.m += delta;
        self.y += (self.m-1)/12
        self.m = self.m%12
        
        if(self.m==0): self.m = 12
        
        
    def compare(self,date1):
        if(self.y < date1.y):
            return -1
        elif(self.y > date1.y):
            return 1
        elif(self.m < date1.m):
            return -1
        elif(self.m > date1.m):
            return 1
        else:
            return 0
  

#Private function used in month-wise bar data.
def make_dict(dic):
    min = int(dic[0]['YEAR'])
    max = int(dic[-1]['YEAR'])+1
    
    return_val = {}
    for y in range(min,max):
        return_val[y] = {}
        for item in dic:
            if int(item['YEAR'])>y:
                break
            if int(item['YEAR'])==y:
                return_val[y][int(item['MONTH'])] = item['count']
    
    
    return return_val
#used to render data for month bar data in modules
#sqlFunc is the func for the SQL query generator
def month_bar_data(request,geog,id,sqlFunc):
    
    id = int(id)
    date_range = 0
    """
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query(sqlFunc(geog = geog, id = id,from_date = from_date, to_date = to_date))    
    
    else:
        rs = run_query(sqlFunc(geog = geog, id = id));
    """
    
    rs = run_query(sqlFunc(request, geog = geog, id = id));
    if rs:
        dic = make_dict(rs)
    else:
        return HttpResponse(' ');
    
    from_date, to_date, partner = utility.getDatesPartners(request);
    if(not(from_date and to_date)):
        from_date = str(rs[0]['YEAR'])+'-'+str(rs[0]['MONTH'])+'-01'
        to_date = str(datetime.date.today());
    
    from_date = MyDate(* [int(x) for x in reversed(from_date.split('-')[:2])])
    to_date = MyDate(* [int(x) for x in reversed(to_date.split('-')[:2])])
    
    data = [['Jan'],['Feb'],['Mar'],['Apr'],['May'],['Jun'],['Jul'],['Aug'],['Sep'],['Oct'],['Nov'],['Dec']]
    
    if(from_date.y != to_date.y):
        loop_from = MyDate(1,from_date.y)
        loop_to = MyDate(12, to_date.y)
    else:
        loop_from = from_date;
        loop_to = to_date;
    while(loop_from.compare(loop_to)!=1):
        if(loop_from.compare(from_date)==-1 or loop_from.compare(to_date)==1):
            data[loop_from.m - 1][-1] += ';'
            loop_from.addMonth(1)
            continue
        if(loop_from.y in dic and loop_from.m in dic[loop_from.y]):
            data[loop_from.m - 1].append(str(dic[loop_from.y][loop_from.m]))
        else:
            data[loop_from.m - 1].append(str(0))
        
        loop_from.addMonth(1)
    
    return HttpResponse('\n'.join([';'.join(x) for x in data if len(x) > 1]))

#used to render data for month bar settings in modules
#sqlFunc is the func for the SQL query generator
#ballon_string is the string shown in ballon text on graph hover.
def month_bar_settings(request,geog,id,sqlFunc,ballon_string):
    
    """
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        from_year = int(request.GET['from_date'].split('-')[0])
        to_year = int(request.GET['to_date'].split('-')[0]);
        year_list = range(from_year,to_year+1,1)
    else:
        """
        
    rs = run_query(sqlFunc(request,geog = geog, id = id));
    year_list = []
    for i in range(len(rs)):
        if rs [i]['YEAR'] not in year_list:
            year_list.append(rs[i]['YEAR'])
                
    if year_list:
        from_year = int(min(year_list))
        to_year = int(max(year_list))
        year_list = range(from_year,to_year+1)

        #Making Settings file
        settings = []
        settings.append(r'<settings><graphs>')
        
        for year in year_list:
            settings.append(r'<graph><type/><title>'+str(year)+'</title><balloon_text>{series},{title}: '+ballon_string+' = {value}</balloon_text></graph>')
            
            
        settings.append(r'</graphs></settings>')
        settings = ''.join(settings)
        
    else:
        settings = ''
           
    return HttpResponse(settings)