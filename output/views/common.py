from django.shortcuts import *
from django.http import Http404, HttpResponse
from dashboard.models import *
from output.database  import utility
from output.database.SQL import shared_sql, overview_analytics_sql
from output.database.utility import run_query, run_query_raw, run_query_dict, run_query_dict_list, construct_query, get_dates_partners
import datetime
import django
import re, random, cjson


def home_with_analytics():
    tot_scr = Screening.objects.count()
    tot_vid = Video.objects.filter(video_suitable_for = 1).count()
    tot_per = Person.objects.exclude(date_of_joining = None).count()
    analytics_data = dict(tot_scr = tot_scr, tot_vid = tot_vid, tot_per = tot_per)
    #Randomly retreiving person ids for home page thumbnails
    person_data = Person.farmerbook_objects.all().order_by('?')[:18].values_list('id', 'village__village_name', 
                                    'village__block__block_name', 'village__block__district__district_name')
    print len(person_data)
    return render_to_response('base_home.html', dict(analytics_data = analytics_data, person_data = person_data))

def test_output(request,geog,id=None):

    #return render_to_response('amcolumn.html')
    return render_to_response('test.html',{'flash_geog':geog,'id':id})


#function for breadcrumbs
#returns a list of geog upto state
#Datastructure returned is [{state_id:((state_name),true if this should be marked as selected else it's not nested tuple),..},
#                                                  {district_id: ---do---  ,district_id:.........}]
def breadcrumbs_options(geog,id):
    id = int(id)
    if(geog=='COUNTRY'):
        return breadcrumbs_options('STATE',-1);
    geog_list = ['VILLAGE','BLOCK','DISTRICT','STATE'];
    return_val = []

    if(geog!='VILLAGE'):
        return_val.append(run_query_dict_list(shared_sql.breadcrumbs_options_sql(geog_list[geog_list.index(geog)-1],id,1),'id'))
    #Starting from the passed geog, we'll calculate 'options' and append to return_val,
    #and end up at top most geog 'state'.
    for i in range(geog_list.index(geog),len(geog_list)):
        geog = geog_list[i]
        query_return = run_query_dict_list(shared_sql.breadcrumbs_options_sql(geog,id,0),'id')
        if(id!=-1):
            query_return[id].append('true')
        if(geog!='STATE'):
            id  = query_return[id][1]

        return_val.append(query_return);

    return_val.reverse();
    return return_val

#Returns a dictionary containing parameters for the search box on the right hand side of the page.
def get_search_box(request, min_date_func=None):
    geog, id = get_geog_id(request);
    from_date, to_date, partner = utility.get_dates_partners(request);
    search_box_params = {}
    search_box_params['partners'] = get_partner_list(geog,id, partner);
    
    if(from_date and to_date):
        search_box_params['is_date_selected'] = 1
    else:
        search_box_params['is_date_selected'] = 0
        if(min_date_func):
            from_date =  (run_query(min_date_func(geog, id, from_date, to_date, partner)))[0]['date']
        else:
            from_date = None
        if(not from_date):
            from_date = datetime.date.today()
        to_date = datetime.date.today()

    search_box_params['from_date'] = str(from_date)
    search_box_params['to_date'] = str(to_date)
    search_box_params['geog_val'] = breadcrumbs_options(geog,id)
    search_box_params['cur_geog'] = geog.lower()
    search_box_params['cur_id'] = id
    search_box_params['base_url'] = request.path

    return search_box_params

#Helper function to return geog, id from request object.
def get_geog_id(request):
    return request.GET['geog'].upper(),int(request.GET['id'])


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
    rs = run_query(shared_sql.search_drop_down_list(geog=geog,geog_parent=geog_parent,id=id));
    html = t.render(django.template.Context(dict(geog=geog,rs=rs)))

    return HttpResponse(html)


#This is the method to generate Data for line graph for # vs time. (eg Overview module)
#type can be ['prod','screen','prac','person','adopt', 'prod_tar', 'screen_tar', 'adopt_tar']
#       Based on the 'type', it generates the data for that set only
#       If 'type' is not specified, it generates for all.
def overview_line_graph(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)

    if('type' in request.GET):
        type = request.GET.getlist('type')
    else:
        type = ['prod', 'screen', 'prac', 'person', 'adopt', 'prod_tar', 'screen_tar', 'adopt_tar']

    if('prod' in type):
        vid_prod_rs = run_query_dict(shared_sql.overview_line_chart(type='production',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        vid_prod_rs = []

    if('screen' in type):
        sc_rs = run_query_dict(shared_sql.overview_line_chart(type='screening',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        sc_rs = []

    if('adopt' in type):
        adopt_rs = run_query_dict(shared_sql.overview_line_chart(type='adoption',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        adopt_rs = []

    if('prac' in type):
        prac_rs = run_query_dict(shared_sql.overview_line_chart(type='practice',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        prac_rs = []

    if('person' in type):
        person_rs = run_query_dict(shared_sql.overview_line_chart(type='person',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date');
    else:
        person_rs = []
    
    if('village' in type):
        village_rs = run_query_raw(shared_sql.overview_line_chart(type='village',geog=geog,id=id,from_date=from_date, to_date=to_date, partners=partners));
    else:
        village_rs = []

    if('prod_tar' in type):
        prod_tar_rs = run_query_dict(shared_sql.target_lines(type='prod_tar',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date')
    else:
        prod_tar_rs = []

    if('adopt_tar' in type):
        adopt_tar_rs = run_query_dict(shared_sql.target_lines(type='adopt_tar',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date')
    else:
        adopt_tar_rs = []

    if('screen_tar' in type):
        screen_tar_rs = run_query_dict(shared_sql.target_lines(type='screen_tar',geog=geog,id=id, from_date=from_date, to_date=to_date, partners=partners),'date')
    else:
        screen_tar_rs = []


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
    if screen_tar_rs:
        start_date = min(start_date,*(screen_tar_rs.keys()))
    if adopt_tar_rs:
        start_date = min(start_date,*(adopt_tar_rs.keys()))
    if prod_tar_rs:
        start_date = min(start_date,*(prod_tar_rs.keys()))
        
    
   ###Calculating village operational on each day.
    
    #village_rs -> temp. temp is a dictionary of date vs list of village IDS
    temp = {}
    for i in village_rs:
        if i[0] in temp:
            temp[i[0]].append(i[1])
        else:
            temp[i[0]] = [i[1]]
          
   #vil_vals is cumulatively added list of villages for every date.
   #i.e. vil_vals is a dictionary of date to list of villages that had screening on any date before that.  
    vil_vals = {}
    min_date = start_date;
    max_date = today
    if(min_date in temp):
    	vil_vals[min_date] = temp[min_date]
    else:
    	vil_vals[min_date] = []
    min_date = min_date + datetime.timedelta(days=1)
    while min_date <= max_date:
    	vil_vals[min_date] = vil_vals[min_date - datetime.timedelta(days=1)][:]
    	if min_date in temp:
    		vil_vals[min_date].extend(temp[min_date])
    	min_date = min_date + datetime.timedelta(days=1)
    	
    min_date =  start_date + datetime.timedelta(days=61)
    
    while min_date <= max_date:
    	vil_vals[max_date] = len(set(vil_vals[max_date][len(vil_vals[(max_date - datetime.timedelta(days=61))]):]))
    	max_date = max_date - datetime.timedelta(days=1)	
    while start_date <= max_date:
    	vil_vals[max_date]  = len(set(vil_vals[max_date]))
    	max_date = max_date - datetime.timedelta(days=1)
		
    #End of Village Operational calculation

    diff = (today - start_date).days

    str_list = []
    sum_vid = sum_sc = sum_adopt =sum_prac = sum_person = sum_vid_tar = sum_sc_tar = sum_adopt_tar = 0
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
        if iter_date in prod_tar_rs:
            sum_vid_tar += prod_tar_rs[iter_date][0]
        if iter_date in screen_tar_rs:
            sum_sc_tar += screen_tar_rs[iter_date][0]
        if iter_date in adopt_tar_rs:
            sum_adopt_tar += adopt_tar_rs[iter_date][0]

        append_str = str(iter_date) +';'
        if('prod' in type): append_str += str(sum_vid)+';'
        if('screen' in type): append_str += str(sum_sc)+';'
        if('adopt' in type): append_str += str(sum_adopt)+';'
        if('prac' in type): append_str +=  str(sum_prac)+';'
        if('person' in type): append_str += str(sum_person)+';'
        if(geog in ["COUNTRY","STATE","DISTRICT"]):
        	if('village' in type): append_str += str(vil_vals[iter_date])+';'
        	if('prod_tar' in type): append_str += str(sum_vid_tar)+';'
        	if('screen_tar' in type): append_str += str(sum_sc_tar)+';'
        	if('adopt_tar' in type): append_str += str(sum_adopt_tar)+';'


        str_list.append(append_str[:-1])

	#If no data, changing the values so that Flash Charts show proper Errro Msg
    if(len(str_list)==1):
        m = re.search("^\d\d\d\d-\d\d-\d\d((;0)*)$",str_list[0]);
        if(m!=None): data = re.sub(r'0','',m.group(1));
    else:
        data = '\n'.join(str_list)

    #For settings
    i=1;
    settings = ["<settings><graphs>"]
    if('prod' in type):
        settings.append("<graph gid='"+str(i)+"'><title>Total Videos Produced</title><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
        i= i+1
    if('screen' in type):
        settings.append("<graph gid='"+str(i)+"'><title>Total Disseminations</title><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
        i= i+1
    if('adopt' in type):
        settings.append("<graph gid='"+str(i)+"'><title>Total Adoptions</title><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
        i= i+1
    if('prac' in type):
        settings.append("<graph gid='"+str(i)+"'><title>Total Practices</title><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
        i= i+1
    if('person' in type):
        settings.append("<graph gid='"+str(i)+"'><title>Total Farmers</title><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
        i= i+1
    if(geog in ["COUNTRY","STATE","DISTRICT"]):
    	if('village' in type):
			settings.append("<graph gid='"+str(i)+"'><title>Operational Villages</title><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
			i= i+1
        if('prod_tar' in type):
            settings.append("<graph gid='"+str(i)+"'><title>Video Production Target</title><hidden>true</hidden><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
            i= i+1
        if('screen_tar' in type):
            settings.append("<graph gid='"+str(i)+"'><title>Disseminations Target</title><hidden>true</hidden><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
            i= i+1
        if('adopt_tar' in type):
            settings.append("<graph gid='"+str(i)+"'><title>Adoptions Target</title><hidden>true</hidden><balloon_text><![CDATA[{value}]]></balloon_text></graph>")
            i= i+1
    settings.append("</graphs></settings>")

    return HttpResponse(cjson.encode(dict(settings='\n'.join(settings),data=data)))

#generic functin to render Pie Chart data
#sqlFunc is the function to generate SQL query, should generate first select column as 'pie_key'
#pieNameDict is the dictionary in which key is the database entry (like "M") and value is the one that
#               is show in Pie chart (Like "Male" for "M")
#desc is the description string for the pie, can use variables  - {{key}}, {{value}} within it
def pie_chart_data(sqlFunc,pieNameDict, desc, **args):
    rs = run_query_dict(sqlFunc(**args),'pie_key')
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
def scatter_chart_data(sqlFunc, **args):
    rs = run_query(sqlFunc(**args))
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
def month_bar_data(sqlFunc, setting_from_date, setting_to_date, **args):
    rs = run_query(sqlFunc(**args));
    if rs:
        dic = make_dict(rs)
    else:
        return HttpResponse(' ');

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
        loop_from = setting_from_date;
        loop_to = setting_to_date;
    while(loop_from.compare(loop_to)!=1):
        if(loop_from.compare(setting_from_date)==-1 or loop_from.compare(setting_to_date)==1):
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
def month_bar_settings(sqlFunc,ballon_string, **args):
    rs = run_query(sqlFunc(**args));
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
        settings.append(r'<graphs>')

        for year in year_list:
            settings.append(r'<graph><type/><title>'+str(year)+'</title><balloon_text>{series},{title}: '+ballon_string+' = {value}</balloon_text></graph>')


        settings.append(r'</graphs>')
        return HttpResponse(''.join(settings))

    else:
        return HttpResponse('')
