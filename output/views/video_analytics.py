from django.shortcuts import *
from django.http import Http404, HttpResponse
from django.db.models import Count
from dg.dashboard.models import *
import datetime
from dg.output.database.SQL  import video_analytics_sql, shared_sql
from dg.output.database import utility
from dg.output import views
from dg.output.views.common import get_geog_id
from dg.output.database.utility import run_query, run_query_dict, run_query_dict_list, run_query_raw, construct_query, get_dates_partners


#Main view for the video module. Render's the main HTML page.
#Views below this, serve the AJAX calls from the graphs.
def video_module(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog not in geog_list):
        raise Http404()

    tot_vid = run_query(video_analytics_sql.video_tot_video(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners))[0]['count']
    tot_scr = run_query(video_analytics_sql.video_tot_scr(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners))[0]['count']
    tot_avg = run_query(video_analytics_sql.video_avg_time(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners))[0]['avg']
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
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.pie_chart_data(video_analytics_sql.video_malefemale_ratio, \
                                      {"M":"Male","F":"Female"}, 'Ratio of videos featuring {{value}} actors', \
                                      geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)

#Data generator for Actor Wise Pie chart
def video_actor_wise_pie(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.pie_chart_data(video_analytics_sql.video_actor_wise_pie, \
                                      {"I":"Individual","F":"Family","G":"Group"}, 'Ratio of videos featuring {{value}} actor',\
                                       geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)


#Data generator for Video-Type Wise Pie chart
def video_type_wise_pie(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.pie_chart_data(video_analytics_sql.video_type_wise_pie, \
                                      {1:"Demonstration",2:"Success Story",3:"Activity Introduction",4:"Discussion",5:"General Awareness"}, \
                                      'Ratio of videos featuring {{value}} type',\
                                      geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)

#Data generator to generate Geography Wise Pie.
def video_geog_pie_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
    if(geog not in geog_list[:-1]):
        raise Http404()
    
    get_req_url = request.META['QUERY_STRING']
    get_req_url = [i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id']
    get_req_url.append("geog="+geog_list[geog_list.index(geog)+1].lower())

    url = ";;;/analytics/video_module?"


    vid_prod = run_query(shared_sql.overview(geog,id, from_date, to_date, partners, 'production'))
    geog_name = run_query_dict(shared_sql.child_geog_list(geog, id, from_date, to_date, partners),'id')

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
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.scatter_chart_data(video_analytics_sql.video_language_wise_scatter, \
                                           geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)


def video_practice_wise_scatter(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.scatter_chart_data(video_analytics_sql.video_practice_wise_scatter, \
                                           geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)


    ###############
    ## Bar Graph ##
    ###############

#Data generator for Month-wise Bar graph
def video_monthwise_bar_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.month_bar_data(video_analytics_sql.video_month_bar, setting_from_date = from_date, setting_to_date = to_date, \
                                       geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners);

#Settings generator for Month-wise Bar graph
def video_monthwise_bar_settings(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.month_bar_settings(video_analytics_sql.video_month_bar, "Video Production", \
                                           geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)


###########################
##     VIDEO PAGE        ##
###########################

def video(request):
    id = int(request.GET['id'])
    vid = Video.objects.get(pk=id)
    scr = Screening.objects.all().filter(videoes_screened = vid)
    pma = PersonMeetingAttendance.objects.all().filter(screening__in = scr)
    prac_shown = vid.related_agricultural_practices.all()
    
    tot_vid_scr = len(scr)
    dist_shown = list(set([s.village.block.district.district_name for s in scr]))
    tot_vid_viewer = pma.aggregate(Count('person',distinct=True))['person__count']
    exp_ques_pract_count = pma.exclude(expressed_question_practice = None).values('expressed_question_practice__practice_name').annotate(count = Count('person'))
    tot_vid_adopt = run_query(video_analytics_sql.get_adoption_for_video(id))[0]['tot_adopt']
    
    actors = vid.farmers_shown.all()
    actor_data = dict(actors = actors.values('person_name'), tot_actors = len(actors))
    for ratio in actors.values('gender').annotate(count=Count('id')):
        actor_data[ratio['gender']] = ratio['count']
    
    #Many questions are irrelevant to the video. Ranking the questions by using the number of matches
    #in title and questionx
    title = vid.title
    x = title.split(' ')
    title_arr = []
    for elem in x:
         title_arr.extend(elem.split('_'))
    #title_arr is the final array of tokens from Title after splitting by ' ' and '_'
    
    ques = pma.exclude(expressed_question='').values_list('expressed_question',flat=True)
    if(ques):
        ques_arr = []
        for x in ques:
            ques_arr.append([x.split(' '), x])
            
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
    return render_to_response('videopage.html',dict(vid = vid, \
                                                     tot_vid_scr = tot_vid_scr, \
                                                     tot_vid_viewer = tot_vid_viewer, \
                                                     tot_vid_adopt = tot_vid_adopt, \
                                                     actors = actor_data, \
                                                     ques = ques, \
                                                     prac_shown = prac_shown))


def video_search(request):
    video_suitable_for = request.GET.get('videosuitable')
    video_uploaded = request.GET.get('videouploaded')
    season = request.GET.get('seaon')
    lang = request.GET.get('lang')
    prac_arr = request.GET.getlist('prac')
    
    vid = Video.objects.all();
    if(video_suitable_for):
        vid = vid.fitler(video_suitable_for = int(video_suitable_for))
    #if(video_uploaded):
    #
    if(season):
        vid = vid.filter(related_agricultural_practices__seasonality = season);
    if(lang):
        vid = vid.filter(language__id = int(lang))
    if(prac_arr):
        vid = vid.fitler(related_agricultural_practices__id__in = [int(i) for i in prac_arr])
        
        
    
    return render_to_response("searchvideo_result.html",dict())
                                                     
#Data generator for Month-wise Bar graph for Screening of videos
def video_screening_month_bar_data(request):
    id = int(request.GET['id'])
    return views.common.month_bar_data(video_analytics_sql.get_screening_month_bar_for_video, setting_from_date = None, setting_to_date = None, id = id);
