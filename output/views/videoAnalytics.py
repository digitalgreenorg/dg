from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
from dg.output.database.SQL  import videoAnalyticsSQL, sharedSQL
from dg.output.database import utility
from dg.output import views
from dg.output.database.utility import run_query, run_query_dict, run_query_dict_list, construct_query


#Main view for the video module. Render's the main HTML page. 
#Views below this, serve the AJAX calls from the graphs.
def video_module(request,geog,id): 
    geog_list = ['country','state','district','block','village']
    if(geog not in geog_list):
        raise Http404()

    tot_vid = run_query(videoAnalyticsSQL.mvideo_tot_video(request,geog=geog,id=id))[0]['count']
    tot_scr = run_query(videoAnalyticsSQL.mvideo_tot_scr(request,geog=geog,id=id))[0]['count']
    tot_avg = run_query(videoAnalyticsSQL.mvideo_avg_time(request,geog=geog,id=id))[0]['avg']
    search_box_params = views.common.get_search_box(request,geog,id, videoAnalyticsSQL.video_min_date)
    
    get_req_url = request.META['QUERY_STRING']
    if(get_req_url): get_req_url = '?'+get_req_url
    
    return render_to_response('base_production.html',dict(search_box_params = search_box_params,\
                                                          tot_video=tot_vid,\
                                                          tot_screening=tot_scr, \
                                                          tot_average= tot_avg, \
                                                          get_req_url = get_req_url
                                                          ))


   
    ################
    ## PIE CHARTS ##
    ################


# Pie chart for male-female ratio in video module 
def video_pie_graph_mf_ratio(request,geog,id):
    return views.common.pie_chart_data(request,geog,id,videoAnalyticsSQL.mvideo_malefemale_ratio, \
                                      {"M":"Male","F":"Female"}, 'Ratio of videos featuring {{value}} actors')
    
#Data generator for Actor Wise Pie chart
def video_actor_wise_pie(request,geog,id):
    return views.common.pie_chart_data(request,geog,id,videoAnalyticsSQL.mvideo_actor_wise_pie, \
                                      {"I":"Individual","F":"Family","G":"Group"}, 'Ratio of videos featuring {{value}} actor')
    

#Data generator for Video-Type Wise Pie chart
def video_type_wise_pie(request,geog,id):
    return views.common.pie_chart_data(request,geog,id,videoAnalyticsSQL.mvideo_type_wise_pie, \
                                      {1:"Demonstration",2:"Success Story",3:"Activity Introduction",4:"Discussion",5:"General Awareness"}, \
                                      'Ratio of videos featuring {{value}} type')
    
#Data generator to generate Geography Wise Pie.
def video_geog_pie_data(request,geog,id):
    geog_list = ['country','state','district','block','village', 'dummy']
    if(geog not in geog_list):
        raise Http404()

    url1 = ";;;/output/video/module/"+geog_list[geog_list.index(geog)+1]+"/"
    url2 = request.META['QUERY_STRING']
    if(url2): url2 = '/?'+url2
        
    vid_prod = run_query(sharedSQL.method_overview(request,geog,id,'production'))
    geog_name = run_query_dict(sharedSQL.child_geog_list(request, geog, id),'id')
    
    return_val = []
    return_val.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    for item in vid_prod:
        append_str = geog_name[item['id']][0]+';'+str(item['tot_pro'])
        if(geog.upper()!= "VILLAGE"):
            append_str += url1+str(item['id'])+url2
        append_str += ";Ratio of Video Productions in "+geog_name[item['id']][0]
        return_val.append(append_str)
    
    return HttpResponse('\n'.join(return_val))

    ####################
    ## Scatter Charts ##
    ####################
    

def video_language_wise_scatter_data(request,geog,id):
    return views.common.scatter_chart_data(request,geog,id,videoAnalyticsSQL.mvideo_language_wise_scatter)
    
    
def video_practice_wise_scatter(request,geog,id):
    return views.common.scatter_chart_data(request,geog,id,videoAnalyticsSQL.mvideo_practice_wise_scatter)
    

    ###############
    ## Bar Graph ##
    ###############

#Data generator for Month-wise Bar graph
def video_monthwise_bar_data(request,geog,id):
    return views.common.month_bar_data(request,geog,id,videoAnalyticsSQL.mvideo_month_bar);

#Settings generator for Month-wise Bar graph
def video_monthwise_bar_settings(request,geog,id):
    return views.common.month_bar_settings(request,geog,id,videoAnalyticsSQL.mvideo_month_bar, "Video Production")
   