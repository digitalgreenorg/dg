from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
from dg.output.database.SQL  import video_analytics_sql, shared_sql
from dg.output.database import utility
from dg.output import views
from dg.output.views.common import get_geog_id
from dg.output.database.utility import run_query, run_query_dict, run_query_dict_list, construct_query


#Main view for the video module. Render's the main HTML page.
#Views below this, serve the AJAX calls from the graphs.
def video_module(request):
    geog, id = get_geog_id(request)

    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog not in geog_list):
        raise Http404()

    tot_vid = run_query(video_analytics_sql.video_tot_video(request,geog=geog,id=id))[0]['count']
    tot_scr = run_query(video_analytics_sql.video_tot_scr(request,geog=geog,id=id))[0]['count']
    tot_avg = run_query(video_analytics_sql.video_avg_time(request,geog=geog,id=id))[0]['avg']
    search_box_params = views.common.get_search_box(request, video_analytics_sql.video_min_date)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url

    return render_to_response('video_module.html',dict(search_box_params = search_box_params,\
                                                          tot_video=tot_vid,\
                                                          tot_screening=tot_scr, \
                                                          tot_average= tot_avg, \
                                                          get_req_url = get_req_url
                                                          ))



    ################
    ## PIE CHARTS ##
    ################


# Pie chart for male-female ratio in video module
def video_pie_graph_mf_ratio(request):
    return views.common.pie_chart_data(request,video_analytics_sql.video_malefemale_ratio, \
                                      {"M":"Male","F":"Female"}, 'Ratio of videos featuring {{value}} actors')

#Data generator for Actor Wise Pie chart
def video_actor_wise_pie(request):
    return views.common.pie_chart_data(request,video_analytics_sql.video_actor_wise_pie, \
                                      {"I":"Individual","F":"Family","G":"Group"}, 'Ratio of videos featuring {{value}} actor')


#Data generator for Video-Type Wise Pie chart
def video_type_wise_pie(request):
    return views.common.pie_chart_data(request,video_analytics_sql.video_type_wise_pie, \
                                      {1:"Demonstration",2:"Success Story",3:"Activity Introduction",4:"Discussion",5:"General Awareness"}, \
                                      'Ratio of videos featuring {{value}} type')

#Data generator to generate Geography Wise Pie.
def video_geog_pie_data(request):
    geog, id = get_geog_id(request)
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
    if(geog not in geog_list[:-1]):
        raise Http404()
    
    get_req_url = request.META['QUERY_STRING']
    get_req_url = [i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id']
    get_req_url.append("geog="+geog_list[geog_list.index(geog)+1].lower())

    url = ";;;/analytics/video_module?"


    vid_prod = run_query(shared_sql.overview(request,geog,id,'production'))
    geog_name = run_query_dict(shared_sql.child_geog_list(request, geog, id),'id')

    return_val = []
    return_val.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    for item in vid_prod:
        append_str = geog_name[item['id']][0]+';'+str(item['tot_pro'])
        if(geog.upper()!= "VILLAGE"):
            temp_get_req_url = get_req_url[:]
            temp_get_req_url.append("id="+str(item['id']))
            append_str += url+'&'.join(temp_get_req_url)
        append_str += ";Ratio of Video Productions in "+geog_name[item['id']][0]
        return_val.append(append_str)

    return HttpResponse('\n'.join(return_val))

    ####################
    ## Scatter Charts ##
    ####################


def video_language_wise_scatter_data(request):
    return views.common.scatter_chart_data(request,video_analytics_sql.video_language_wise_scatter)


def video_practice_wise_scatter(request):
    return views.common.scatter_chart_data(request,video_analytics_sql.video_practice_wise_scatter)


    ###############
    ## Bar Graph ##
    ###############

#Data generator for Month-wise Bar graph
def video_monthwise_bar_data(request):
    return views.common.month_bar_data(request,video_analytics_sql.video_month_bar);

#Settings generator for Month-wise Bar graph
def video_monthwise_bar_settings(request):
    return views.common.month_bar_settings(request,video_analytics_sql.video_month_bar, "Video Production")


###########################
##     VIDEO PAGE        ##
###########################

def video(request):
    id = int(request.GET['id'])
    vid = Video.objects.all().filter(pk=id)[0]
    
    #Many questions are irrelevant to the video. Ranking the questions by using the number of matches
    #in title and question
    title = vid.title
    x = title.split(' ')
    title_arr = []
    for elem in x:
         title_arr.extend(elem.split('_'))
    #title_arr is the final array of tokens from Title after splitting by ' ' and '_'
    
    ques = run_query_raw(question_list_for_video(id))
    if(ques):
        ques_arr = []
        for x in ques:
            ques_arr.append([x[0].split(' '), x[0]])
            
        scores = []
        for ques in ques_arr:
            count = 0
            for tok in title_arr:
                if tok in ques[0]:
                    count = count+1
            scores.append([count, ques[1]])
                    
        scores.sort(key = (lambda x: x[0]), reverse = True)
        ques = scores
    #ques is the final array of Question. It is SORTED list of lists, each list of the form [scores, questions]
    
    raise Http404
    
    
    
    
