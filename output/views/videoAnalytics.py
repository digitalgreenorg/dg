from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
from dg.output.database  import videoAnalyticsSQL, common
from dg.output import views
from dg.output.database.common import run_query, run_query_dict, run_query_dict_list, construct_query
import random

#Main view for the video module. Render's the main HTML page. 
#Views below this, serve the AJAX calls from the graphs.
def video_module(request,geog,id):
    
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

    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        tot_vid = run_query(videoAnalyticsSQL.video_tot_video(geog=geog,id=id,from_date=from_date,to_date=to_date))[0]['count']
        tot_scr = run_query(videoAnalyticsSQL.video_tot_scr(geog=geog,id=id,from_date=from_date,to_date=to_date))[0]['count']
        tot_avg = run_query(videoAnalyticsSQL.video_avg_time(geog=geog,id=id,from_date=from_date,to_date=to_date))[0]['avg']
    else:
        date_range = 0
        tot_vid = run_query(videoAnalyticsSQL.video_tot_video(geog = geog, id = id))[0]['count']
        tot_scr = run_query(videoAnalyticsSQL.video_tot_scr(geog = geog, id = id))[0]['count']
        tot_avg = run_query(videoAnalyticsSQL.video_avg_time(geog = geog, id = id))[0]['avg']
        min_date = run_query(videoAnalyticsSQL.video_min_date(geog = geog, id=id))
        start_date = min_date[0]['date']
        if not start_date:
            start_date = datetime.date.today()
           
    if date_range==1:
        return render_to_response('video_module.html',dict(geog=geog,id=id,tot_video=tot_vid,\
                                                    tot_screening=tot_scr, tot_average= tot_avg,from_date = from_date,to_date=to_date,sel_val= views.common.breadcrumbs_options(geog,id)))
    else:
        return render_to_response('video_module.html',dict(geog=geog,id=id,tot_video=tot_vid,\
                                                    start_date = start_date, tot_screening=tot_scr, tot_average= tot_avg,sel_val= views.common.breadcrumbs_options(geog,id)))

   
    ################
    ## PIE CHARTS ##
    ################


# Pie chart for male-female ratio in video module 
def video_pie_graph_mf_ratio(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']        
        male_female_ratio_sql = videoAnalyticsSQL.video_malefemale_ratio(dict(geog = geog, id = id,from_date = from_date, to_date = to_date))    
    else:
        male_female_ratio_sql = videoAnalyticsSQL.video_malefemale_ratio(dict(geog = geog, id = id))
    
    return_val = run_query(male_female_ratio_sql);
  
    str_list = []
    str_list.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    if return_val == []:
        str_list.append('')
    else:
        for i in range(len(return_val)):
            if return_val[i]['gender'] == 'F':
                str_list.append('Female;'+str(return_val [i]['count'])+\
                                ';true;99FF33;;Ratio of videos featuring Female actors')
            else:
                str_list.append('Male;'+str(return_val [i]['count'])+\
                                ';;339900;;Ratio of videos featuring male actors')
    
    return HttpResponse('\n'.join(str_list))


#Data generator for Actor Wise Pie chart
def video_actor_wise_pie(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query_dict(videoAnalyticsSQL.video_actor_wise_pie(geog=geog,id=id,from_date=from_date,to_date=to_date),\
                            'actors')
    
    else:
        rs = run_query_dict(videoAnalyticsSQL.video_actor_wise_pie(geog=geog,id=id),'actors')
    
    actors = ['Individual','Group','Family']
  
    str_list = []
    str_list.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    if not rs:
       return HttpResponse(';')
    else:
        for actor in actors:
            if(actor[0] in rs):
                str_list.append(actor+';'+str(rs[actor[0]][0])+';;;;Ratio of Videos featuring '+actor+\
                                ' actor')
            else:
                str_list.append(actor+';0;;;;Ratio of Videos featuring '+actor+\
                                ' actor')
                
    return HttpResponse('\n'.join(str_list))

#Data generator for Video-Type Wise Pie chart
def video_type_wise_pie(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query_dict(videoAnalyticsSQL.video_type_wise_pie(geog=geog,id=id,from_date=from_date,to_date=to_date),\
                            'VIDEO_TYPE')
    
    else:
        rs = run_query_dict(videoAnalyticsSQL.video_type_wise_pie(geog=geog,id=id),'VIDEO_TYPE')
    
    video_type = ['1Demonstration','2Success Story','3Activity Introduction','4Discussion', '5General Awareness']
  
    str_list = []
    str_list.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    if not rs:
       return HttpResponse(';')
    else:
        for type in video_type:
            if(int(type[0]) in rs):
                str_list.append(type[1:]+';'+str(rs[int(type[0])][0])+';;;;Ratio of Videos featuring '+type[1:]+\
                                ' type')
            else:
                str_list.append(type[1:]+';0;;;;Ratio of Videos featuring '+type[1:]+\
                                ' type')
                
    return HttpResponse('\n'.join(str_list))

#Data generator to generate Geography Wise Pie.
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
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        vid_prod = run_query(construct_query(common.overview,dict(type='production',geography=geog,geog_child=geog_child, \
                                                                  from_date=from_date,to_date=to_date,id=id)));
        url1 = ";;;/output/video/module/"+geog_child+"/"
        url2 = "/?from_date="+from_date+"&to_date="+to_date
        return_val = []
        return_val.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
        for item in vid_prod:
            return_val.append(item['name']+';'+str(item['tot_pro'])+url1+str(item['id'])+url2+";Ratio of Video Productions in "+item['name'])
        
    else:
        vid_prod = run_query(construct_query(common.overview,dict(type='production',geography=geog,geog_child=geog_child,id=id)));
        url = ";;;/output/video/module/"+geog_child+"/"
        return_val = []
        return_val.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
        for item in vid_prod:
            return_val.append(item['name']+';'+str(item['tot_pro'])+url+str(item['id'])+";Ratio of Video Productions in "+item['name'])
        
    
    return HttpResponse('\n'.join(return_val))

    ####################
    ## Scatter Charts ##
    ####################
    

def video_language_wise_scatter_data(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query(videoAnalyticsSQL.video_language_wise_scatter(geog=geog,id=id,from_date=from_date,to_date=to_date))
    
    else:
        rs = run_query(videoAnalyticsSQL.video_language_wise_scatter(geog=geog,id=id))
    
    if not rs:
        return HttpResponse(' ');
    
    count_lang_dict = {}
    for item in rs:
        if item['count'] in count_lang_dict:
            count_lang_dict[item['count']].append(item['lname'])
        else:
            count_lang_dict[item['count']] = [item['lname']]
    
    x_axis_len = max([len(x) for x in count_lang_dict.values()]) * 2
    if(x_axis_len<10): x_axis_len = 10;
    return_val = []
    return_val.append('[x];[y];[value];[bullet_color];[bullet_size];[url];[description]')
    
    random.seed();
    for tot,pracs in count_lang_dict.iteritems():
        flag = [ 0 for i in range(0,x_axis_len+1)]
        for prac in pracs:        
            x = random.randrange(1,x_axis_len)
            while(flag[x] != 0):
                x = random.randrange(1,x_axis_len)
            flag[x] = 1
            return_val.append(str(x)+';'+str(tot)+';'+str(tot)+';;;;'+prac)
    
    return HttpResponse('\n'.join(return_val))
   
    
def video_practice_wise_scatter(request,geog,id):
    id = int(id)
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query(videoAnalyticsSQL.video_practice_wise_scatter(geog=geog,id=id,from_date=from_date,to_date=to_date))
    
    else:
        rs = run_query(videoAnalyticsSQL.video_practice_wise_scatter(geog=geog,id=id))
    
    if not rs:
        return HttpResponse(' ');
    
    count_prac_dict = {}
    for item in rs:
        if item['count'] in count_prac_dict:
            count_prac_dict[item['count']].append(item['name'])
        else:
            count_prac_dict[item['count']] = [item['name']]
    
    x_axis_len = max([len(x) for x in count_prac_dict.values()]) * 2
    if(x_axis_len<10): x_axis_len = 10;
    return_val = []
    return_val.append('[x];[y];[value];[bullet_color];[bullet_size];[url];[description]')
    
    random.seed();
    for tot,pracs in count_prac_dict.iteritems():
        flag = [ 0 for i in range(0,x_axis_len+1)]
        for prac in pracs:        
            x = random.randrange(1,x_axis_len)
            while(flag[x] != 0):
                x = random.randrange(1,x_axis_len)
            flag[x] = 1
            return_val.append(str(x)+';'+str(tot)+';'+str(tot)+';;;;'+prac)
    
    return HttpResponse('\n'.join(return_val))





    ###############
    ## Bar Graph ##
    ###############


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

#Data generator for Month-wise Bar graph
def video_monthwise_bar_data(request,geog,id):
    id = int(id)
    date_range = 0
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        date_range = 1
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        rs = run_query(videoAnalyticsSQL.video_month_bar(dict(geog = geog, id = id,from_date = from_date, to_date = to_date)))    
    
    else:
        rs = run_query(videoAnalyticsSQL.video_month_bar(dict(geog = geog, id = id)));
    
    if rs:
        dic = make_dict(rs)
    else:
        return HttpResponse(' ');
        
    if date_range is not 1:
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


#Settings generator for Month-wise Bar graph
def video_monthwise_bar_settings(request,geog,id):
    id = int(id)
     
    if 'from_date' in request.GET and request.GET['from_date'] \
    and 'to_date' in request.GET and request.GET['to_date']:
        from_year = int(request.GET['from_date'].split('-')[0])
        to_year = int(request.GET['to_date'].split('-')[0]);
        year_list = range(from_year,to_year+1,1)
    else:
        rs = run_query(videoAnalyticsSQL.video_month_bar(dict(geog = geog, id = id)));
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
            settings.append(r'<graph><type/><title>'+str(year)+'</title><balloon_text>{series},{title}: Video Production = {value}</balloon_text></graph>')
            
            
        settings.append(r'</graphs></settings>')
        settings = ''.join(settings)
        
    else:
        settings = ''
           
    return HttpResponse(settings)