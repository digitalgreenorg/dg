from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
from calendar import week
import datetime
import string
from dg.output  import database
from dg.output.database import run_query, run_query_dict, construct_query, video_malefemale_ratio, video_month_bar
import django 

def test_output(request,geog,id):
    
    #return render_to_response('amcolumn.html')
    return render_to_response('amcolumn.html',{'flash_geog':geog,'id':id})


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
                                ';true;99FF33;;Ratio of videos featuring Female actors')
            else:
                str_list.append('Male;'+return_val [i]['count'].__str__()+\
                                ';;339900;;Ratio of videos featuring male actors')
    
    return HttpResponse('\n'.join(str_list))    

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

def video_monthwise_bar_data(request,geog,id):
    id = int(id)
    date_range = 0
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query(database.video_month_bar(dict(geog = geog, id = id,from_date = from_date, to_date = to_date)))    
    
    else:
        rs = run_query(database.video_month_bar(dict(geog = geog, id = id)));
    
    if rs:
        dic = make_dict(rs)
    else:
        return HttpResponse(';');
        
    if date_range is not 1:
        from_date = str(rs[0]['YEAR'])+'-'+str(rs[0]['MONTH'])+'-01'
        to_date = str(rs[len(rs)-1]['YEAR'])+'-'+str(rs[len(rs)-1]['MONTH'])+'-01'
    
    from_date = MyDate(* [int(x) for x in reversed(from_date.split('-')[:2])])
    to_date = MyDate(* [int(x) for x in reversed(to_date.split('-')[:2])])
    
    data = [['Jan'],['Feb'],['Mar'],['Apr'],['May'],['Jun'],['Jul'],['Aug'],['Sep'],['Oct'],['Nov'],['Dec']]
    #dic = make_dict(rs)
    
    
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

def video_monthwise_bar_settings(request,geog,id):
    id = int(id)
     
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        from_year = int(from_date.split('-')[0])
        to_year = int(to_date.split('-')[0]);
        
    else:
        rs = run_query(database.video_month_bar(dict(geog = geog, id = id)));
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
                settings.append(r'<graph><type/><title>'+str(year)+'</title></graph>')
                
                
            settings.append(r'</graphs></settings>')
            settings = ''.join(settings)
            
        else:
            settings = []
            settings.append(r'<settings><graphs></settings></graphs>')
           
    return HttpResponse(settings)

def video_actor_wise_pie(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query_dict(database.video_actor_wise_pie(geog=geog,id=id,from_date=from_date,to_date=to_date),\
                            'actors')
    
    else:
        rs = run_query_dict(database.video_actor_wise_pie(geog=geog,id=id),'actors')
    
    actors = ['Individual','Group','Family']
  
    str_list = []
    str_list.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    if not rs:
       return HttpResponse('')
    else:
        for actor in actors:
            if(actor[0] in rs):
                str_list.append(actor+';'+str(rs[actor[0]][0])+';;;;Ratio of Videos featuring '+actor+\
                                ' actor')
            else:
                str_list.append(actor+';0;;;;Ratio of Videos featuring '+actor+\
                                ' actor')
                
    return HttpResponse('\n'.join(str_list)) 
    
def video_language_wise_bar_data(request,geog,id):
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query(database.video_language_wise_bar(geog=geog,id=id,from_date=from_date,to_date=to_date))
    
    else:
        rs = run_query(database.video_language_wise_bar(geog=geog,id=id))
    
    return_val = []
    for row in rs:
        return_val.append(row['lname']+';'+str(row['count']))
        
    return HttpResponse('\n'.join(return_val))
    

def video_geog_pie_data(request,geog,id):
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
        vid_prod = run_query(construct_query(database.overview,dict(type='production',geography=geog,geog_child=geog_child, \
                                                                    from_date=mysql_from_date,to_date=mysql_to_date,id=id)));
    else:
        vid_prod = run_query(construct_query(database.overview,dict(type='production',geography=geog,geog_child=geog_child,id=id)));
    
    
    return_val = []
    return_val.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    for item in vid_prod:
        return_val.append(item['name']+';'+str(item['tot_pro'])+";;;;Ratio of Video Productions in "+item['name'])
        
    
    return HttpResponse('\n'.join(return_val))
        
    
def video_module(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        tot_vid = run_query(database.video_tot_video(geog=geog,id=id,from_date=from_date,to_date=to_date))
        tot_scr = run_query(database.video_tot_scr(geog=geog,id=id,from_date=from_date,to_date=to_date))
        tot_avg = run_query(database.video_avg_time(geog=geog,id=id,from_date=from_date,to_date=to_date))
    else:
        date_range = 0    
        tot_vid = run_query(database.video_tot_video(geog = geog, id = id))
        tot_scr = run_query(database.video_tot_scr(geog = geog, id = id))
        tot_avg = run_query(database.video_avg_time(geog = geog, id = id))
        
    # calculating average
    tot = 0
    for i in range(len(tot_avg)):
        if tot_avg[i]['dif'] == 0:
            tot_avg[i]['dif'] = 1
    
    for i in range(len(tot_avg)):
        tot = tot + tot_avg[i]['dif']
    
    tot_video = tot_vid[0]['count']
    tot_screening = tot_scr[0]['count']
    if len(tot_avg) == 0:
        tot_average = 0
    else:
        tot_average = tot/len(tot_avg)
        
    
    return render_to_response('video_module.html',dict(geog=geog,id=id,tot_video=tot_video,tot_screening=tot_screening, \
                                                       tot_average= tot_average))
    #{'tot_video':tot_video,'tot_screening':tot_screening,'tot_average':tot_average}


