from dashboard.models import *
from django.http import Http404, HttpResponse
from django.shortcuts import *
from django.template import Template, Context
from output.database import utility
from output.database.SQL import shared_sql, overview_analytics_sql, \
    screening_analytics_sql
from output.database.SQL.shared_sql import practice_options_sql
from output.database.utility import run_query, run_query_raw, run_query_dict, \
    run_query_dict_list, construct_query, get_dates_partners
from copy import deepcopy
import datetime
import json
import random
import re

##DELETE
from output.database.SQL  import video_analytics_sql, shared_sql

def test(request):
    return render_to_response('test.html')

def test_data(request):
    geog="country"
    id = 1
    from_date, to_date, partners = None,None,[]
    return scatter_chart_data(video_analytics_sql.video_practice_wise_scatter, \
                                           geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)

def home_with_analytics():
    tot_scr = Screening.objects.count()
    tot_vid = Video.objects.filter(video_suitable_for = 1).count()
    tot_per = Person.objects.exclude(date_of_joining = None).count()
    analytics_data = dict(tot_scr = tot_scr, tot_vid = tot_vid, tot_per = tot_per)
    #Randomly retreiving person ids for home page thumbnails
    person_data = Person.farmerbook_objects.all().order_by('?')[:18].values_list('id', 'village__village_name', 
                                    'village__block__block_name', 'village__block__district__district_name')
    #print len(person_data)
    return render_to_response('base_home.html', dict(analytics_data = analytics_data, person_data = person_data))


#function for breadcrumbs
#returns a list of geog upto country
#Datastructure returned is [{state_id:((state_name),true if this should be marked as selected else it's not nested tuple),..},
#                                                  {district_id: ---do---  ,district_id:.........}]
def breadcrumbs_options(geog,id):
    if(geog is None):
        return breadcrumbs_options('COUNTRY',-1);
    geog_list = ['VILLAGE','BLOCK','DISTRICT','STATE','COUNTRY'];
    id = int(id)
    return_val = []

    if(geog!='VILLAGE'):
        return_val.append(run_query_dict_list(shared_sql.breadcrumbs_options_sql(geog_list[geog_list.index(geog)-1],id,1),'id'))
    #Starting from the passed geog, we'll calculate 'options' and append to return_val,
    #and end up at top most geog 'country'.
    for i in range(geog_list.index(geog),len(geog_list)):
        geog = geog_list[i]
        query_return = run_query_dict_list(shared_sql.breadcrumbs_options_sql(geog,id,0),'id')
        if(id!=-1):
            query_return[id].append('true')
        if(geog!='COUNTRY'):
            id  = query_return[id][1]

        return_val.append(query_return);

    return_val.reverse();
    return return_val

#Returns a dictionary containing parameters for the search box on the right hand side of the page.
def get_search_box(request):
    geog, id = get_geog_id(request);
    from_date, to_date, partner = utility.get_dates_partners(request);
    search_box_params = {}
    search_box_params['partners'] = get_partner_list(geog,id, partner);
    
    if(from_date == str(datetime.date.today() - datetime.timedelta(365)) and to_date == str(datetime.date.today())):
        search_box_params['is_date_selected'] = 0
    else:
        search_box_params['is_date_selected'] = 1
        
    search_box_params['from_date'] = str(from_date)
    search_box_params['to_date'] = str(to_date)
    search_box_params['geog_val'] = breadcrumbs_options(geog,id)
    search_box_params['cur_geog'] = geog.lower() if geog != None else None
    search_box_params['cur_id'] = id
    search_box_params['base_url'] = request.path

    return search_box_params

def practice_change(request):
    
    sec=request.GET.get('sec')
    subsec=request.GET.get('subsec')
    top=request.GET.get('top')
    subtop=request.GET.get('subtop')
    sub=request.GET.get('sub')
    if(sec=="-1"):
        sec=None
    if(subsec=="-1"):
        subsec=None
    if(top=="-1"):
        top=None
    if(subtop=="-1"):
        subtop=None
    if(sub=="-1"):
        sub=None        
    
    sql_result = practice_options(sec,subsec,top,subtop,sub)
    
    html_sec = """
    <option value='-1'>Any Sector</option>
    {% for key,item in sql_result.0 %}
        <option value='{{key}}' {% if item.1 %}selected="selected"{% endif %}>{{item.0}}</option>
    {%endfor%}
    """
    html_subsec = """
    <option value='-1'>Any Subsector</option>
    {% for key,item in sql_result.1 %}
        <option value='{{key}}' {% if item.1 %}selected="selected"{% endif %}>{{item.0}}</option>
    {%endfor%}
    """
    html_top = """
    <option value='-1'>Any Topic</option>
    {% for key,item in sql_result.2 %}
        <option value='{{key}}' {% if item.1 %}selected="selected"{% endif %}>{{item.0}}</option>
    {%endfor%}
    """
    html_subtop = """
    <option value='-1'>Any Subtopic</option>
    {% for key,item in sql_result.3 %}
        <option value='{{key}}' {% if item.1 %}selected="selected"{% endif %}>{{item.0}}</option>
    {%endfor%}
    """
    html_sub = """
    <option value='-1'>Any Subject</option>
    {% for key,item in sql_result.4 %}
        <option value='{{key}}' {% if item.1 %}selected="selected"{% endif %}>{{item.0}}</option>
    {%endfor%}
    """
    
    def render_option(option_string, context_dict):
        html = Template(option_string)
        return html.render(Context(context_dict))  
    
    return HttpResponse(json.dumps(map(render_option, [html_sec, html_subsec, html_top, html_subtop, html_sub], [dict(sql_result=sql_result)] * 5)))
                                             
def practice_options(sec, subsec, top, subtop, sub):
    tuple_val=run_query_raw(practice_options_sql(sec, subsec, top, subtop, sub))
    list_dict=[{}, {}, {}, {}, {}]
    for i in range(len(tuple_val)):
        val=tuple_val[i]
        for j in range(len(val)/2):
            if(val[j*2]!=None):
                list_dict[j][val[j*2]]=[val[(j*2)+1]]
                
    args = [sec, subsec, top, subtop, sub]                
    for i in range(len(args)):
        if args[i] is not None:
            list_dict[i][int(args[i])].append('true')
    
    list_dict = [sorted(i.iteritems(), key=lambda x: x[1][0]) for i in list_dict]

    return list_dict

#Helper function to return geog, id from request object.
def get_geog_id(request):
    if "id" in request.GET and 'geog' in request.GET:
        return request.GET['geog'].upper(),int(request.GET['id'])
    else:
        return None, None


#Returns a dictionary of list of PARTNER_NAME, id
#If partners were selected i.e. argument 'partners' is not empty,
#  those that are not present are marked with 'unmarked = 1'
def get_partner_list(geog,id, partners):
    sql = shared_sql.get_partners_sql(geog,id)
    if(sql):
        part_list = run_query(sql)
        if(not partners or len(part_list) == 1):
            return part_list
        filtered_partners = [x['id'] for x in part_list if str(x['id']) in partners]
        if not filtered_partners:
            return part_list
        for partner in part_list:
            if partner['id'] not in filtered_partners:
                partner['unmarked'] = 1
        return part_list
    else:
        return {}

#Responds to AJAX calls on geography selection for dropdown.
#Returns Options list for the child geography.
def drop_down_val(request):
    if 'geog' in request.GET and request.GET['geog'] \
     and 'id' in request.GET and request.GET['id']:
        geog = request.GET['geog'].lower()
        id = request.GET['id']
        id = int(id)
    else:
        raise Http404()
    geog_list = ['country','state','district','block','village']
    if geog=='country':
        geog_parent = 'country'
    else:
        geog_parent = geog_list[geog_list.index(geog)-1]


    html_option = """
    <option value='-1'>Select {{geog|title}}</option>
    {% for row in rs %}
    <option value="{{row.id}}">{{row.name}}</option>
    {%endfor%}
    """
    t = Template(html_option);
    rs = run_query(shared_sql.search_drop_down_list(geog=geog,geog_parent=geog_parent,id=id));
    html = t.render(Context(dict(geog=geog,rs=rs)))

    return HttpResponse(html)



#This is the method to generate Data for line graph for # vs time. (eg Overview module)
#type can be ['prod','screen','prac','person','adopt']
#       Based on the 'type', it generates the data for that set only
#       If 'type' is not specified, it generates for all.
def overview_line_graph(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)

    if('type' in request.GET):
        graph_type = request.GET.getlist('type')
    else:
        graph_type = ['prod', 'screen', 'prac', 'person', 'adopt']

    if('prod' in graph_type):
        vid_prod_rs = run_query_dict(shared_sql.overview_line_chart(type='production',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        vid_prod_rs = []

    if('screen' in graph_type):
        sc_rs = run_query_dict(shared_sql.overview_line_chart(type='screening',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        sc_rs = []

    if('adopt' in graph_type):
        adopt_rs = run_query_dict(shared_sql.overview_line_chart(type='adoption',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        adopt_rs = []

    if('prac' in graph_type):
        prac_rs = run_query_dict(shared_sql.overview_line_chart(type='practice',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        prac_rs = []

    if('person' in graph_type):
        person_rs = run_query_dict(shared_sql.overview_line_chart(type='person',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
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

        append_str = [str(iter_date)]
        if('prod' in graph_type): append_str.append(float(sum_vid))
        if('screen' in graph_type): append_str.append(float(sum_sc))
        if('adopt' in graph_type): append_str.append(float(sum_adopt))
        if('prac' in graph_type): append_str.append(float(sum_prac))
        if('person' in graph_type): append_str.append(float(sum_person))

        str_list.append(append_str)

    #For settings
    header=['date']
    if('prod' in graph_type):
        header.append('Total videos produced')
    if('screen' in graph_type):
        header.append('Total disseminations')
    if('adopt' in graph_type):
        header.append('Total adoptions')
    if('prac' in graph_type):

        header.append('Total practices')
    if('person' in graph_type):
        header.append('Total viewers')

    str_list.insert(0,header)
    return HttpResponse(json.dumps(str_list))

#generic functin to render Pie Chart data
#sqlFunc is the function to generate SQL query, should generate first select column as 'pie_key'
#pieNameDict is the dictionary in which key is the database entry (like "M") and value is the one that
#               is show in Pie chart (Like "Male" for "M")
#desc is the description string for the pie, can use variables  - {{key}}, {{value}} within it
def pie_chart_data(sqlFunc,pieNameDict, desc, **args):
    rs = run_query_dict(sqlFunc(**args),'pie_key')
    str_list = [['Gender','value']]
    if not rs:
        return HttpResponse(json.dumps(str_list))
    
    for key, value in pieNameDict.iteritems():
        if(key in rs):
            str_list.append([value,rs[key][0]])
        else:
            str_list.append([value,0])
            
    return HttpResponse(json.dumps(str_list))

#generic function to render data for Scatter Charts
#sqlFunc is the function which renders the SQL query.
#Pre-requisite: SQL function should generate name, count & in that order.(Other variable names would throw error)
def practice_scatter_chart_data(sqlFunc, **args):
    rs = run_query(sqlFunc(**args))
    if not rs:
        return HttpResponse(json.dumps([[]]));

    count_dict = {}
    for item in rs:
        if item['count'] in count_dict:
            count_dict[item['count']].append([item['name'],item['sec'],item['subsec'],item['top'],item['subtop'],item['sub']])
        else:
            count_dict[item['count']] = [[item['name'],item['sec'],item['subsec'],item['top'],item['subtop'],item['sub']]]
    x_axis_len = max([len(x) for x in count_dict.values()]) * 2
    if(x_axis_len<10): x_axis_len = 10;
    return_val = [['practice_name','Sector','Sub Sector','Topic','Sub Topic','Subject','','','','Number']]
    random.seed();
    for tot, pracs_arr in count_dict.iteritems():
        for pracs in pracs_arr:
            flag = [0] * x_axis_len
            x = random.randrange(1,x_axis_len)
            while(flag[x] != 0):
                x = random.randrange(1,x_axis_len)
            flag[x] = 1
            return_val.append([pracs[0],pracs[1],pracs[2],pracs[3],pracs[4],pracs[5],x,tot,"",tot])

    return HttpResponse(json.dumps(return_val))


def scatter_chart_data(sqlFunc, **args):
    rs = run_query(sqlFunc(**args))
    return_val = [['','','','','Number']]
    if not rs:
        return HttpResponse(json.dumps([[]]));

    count_dict = {}
    for item in rs:
        if item['count'] in count_dict:
            count_dict[item['count']].append(item['name'])
        else:
            count_dict[item['count']] = [item['name']]

    x_axis_len = max([len(x) for x in count_dict.values()]) * 2
    if(x_axis_len<10): x_axis_len = 10;

    random.seed();
    for tot,pracs in count_dict.iteritems():
        flag = [0] * x_axis_len
        for prac in pracs:
            x = random.randrange(1,x_axis_len)
            while(flag[x] != 0):
                x = random.randrange(1,x_axis_len)
            flag[x] = 1
            return_val.append([prac,x,tot,"",tot])

    return HttpResponse(json.dumps(return_val))


#MyDate class, a 'type' with attrib month, m and year, y.(Used in view of Monthwise bar graph)
#Methods addMonth: adds 'x' number of months to itself.
#                               Doesn't allow negative month addition (for simplicity)
#               compare: compares itself with another MyDate object and returns -1 (if self is lesser), 0 , 1.
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


    def __cmp__(self,date1):
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

#used to render data for month bar data in modules
#sqlFunc is the func for the SQL query generator
def month_bar_data(sqlFunc, setting_from_date, setting_to_date, **args):
    rs = run_query(sqlFunc(**args));
    if rs:
        min = int(rs[0]['YEAR'])
        max = int(rs[-1]['YEAR'])+1
    
        dic = {}
        for y in range(min,max):
            dic[y] = {}
            for item in rs:
                if int(item['YEAR'])>y:
                    break
                if int(item['YEAR'])==y:
                    dic[y][int(item['MONTH'])] = item['count']
    else:
        return HttpResponse(json.dumps([['Name','Value']]));

    if(not(setting_from_date and setting_to_date)):
        setting_from_date = str(rs[0]['YEAR'])+'-'+str(rs[0]['MONTH'])+'-01'
        setting_to_date = str(datetime.date.today());
    setting_from_date = MyDate(* [int(x) for x in reversed(setting_from_date.split('-')[:2])])
    setting_to_date = MyDate(* [int(x) for x in reversed(setting_to_date.split('-')[:2])])
    data = [['Jan'],['Feb'],['Mar'],['Apr'],['May'],['Jun'],['Jul'],['Aug'],['Sep'],['Oct'],['Nov'],['Dec']]

    if(setting_from_date.y != setting_to_date.y):
        loop_from = MyDate(1,setting_from_date.y)
        loop_to = MyDate(12, setting_to_date.y)
    else:
        loop_from = MyDate(setting_from_date.m, setting_from_date.y);
        loop_to = MyDate(setting_to_date.m, setting_to_date.y);
    
    while(loop_from <= loop_to):
        value = dic[loop_from.y][loop_from.m] if loop_from.y in dic and loop_from.m in dic[loop_from.y] else 0
        data[loop_from.m - 1].append(float(value))
        loop_from.addMonth(1)
    header = ["Month"] + map(str,range(setting_from_date.y, setting_to_date.y + 1))
    return HttpResponse(json.dumps([header] + filter(lambda x: len(x) > 1, data)))
    
