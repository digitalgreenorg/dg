from dashboard.models import *
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import *
from output import views
from output.database.SQL import video_analytics_sql, shared_sql
from output.database.utility import run_query, run_query_dict, \
    run_query_dict_list, run_query_raw, construct_query, get_dates_partners
from output.views.common import get_geog_id
import datetime
import json
import math


#Main view for the video module. Render's the main HTML page.
#Views below this, serve the AJAX calls from the graphs.
def video_module(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    
    geog_list = [None, 'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog not in geog_list):
        raise Http404()

    tot_vid = run_query_raw(shared_sql.get_totals(geog, id, from_date, to_date, partners, "tot_vid"))[0][0];
    tot_vid = 0 if tot_vid is None else tot_vid 
    tot_vids_screened = run_query(video_analytics_sql.video_tot_scr(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners))[0]['count']
    prod_duration_ls = map(lambda x: x[0], run_query_raw(video_analytics_sql.video_prod_duration(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners)))
    tot_avg =  float(sum(prod_duration_ls))/len(prod_duration_ls) if prod_duration_ls else 0
    search_box_params = views.common.get_search_box(request)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url

    return render_to_response('video_module.html',dict(search_box_params = search_box_params,\
                                                          tot_video=tot_vid,\
                                                          tot_vids_screened=tot_vids_screened, \
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
    geog_list = [None, 'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
    if(geog not in geog_list[:-1]):
        raise Http404()
    
    get_req_url = request.META['QUERY_STRING']
    get_req_url = [i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id']
    get_req_url.append("geog="+geog_list[geog_list.index(geog)+1].lower())

    url = "/analytics/video_module?"


    vid_prod = run_query(shared_sql.overview(geog,id, from_date, to_date, partners, 'production'))
    geog_name = run_query_dict(shared_sql.child_geog_list(geog, id, from_date, to_date, partners),'id')

    return_val = []
    return_val.append(["title","val",'url'])
    for item in vid_prod:
        if(geog is None or geog.upper()!= "VILLAGE"):
            temp_get_req_url = get_req_url[:]
            temp_get_req_url.append("id="+str(item['id']))
            return_val.append([geog_name[item['id']][0], float(item['tot_pro']), url+'&'.join(temp_get_req_url)])
        else:
            return_val.append([geog_name[item['id']][0], float(item['tot_pro']), ''])

    return HttpResponse(json.dumps(return_val))

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


###########################
##     VIDEO PAGE        ##
###########################

def video(request):
    id = int(request.GET['id'])
    vid = Video.objects.select_related().get(pk=id)
    vid.prod_duration = vid.video_production_end_date+datetime.timedelta(days=1) - vid.video_production_start_date
    
    tot_vid_scr = vid.screening_set.count()
    tot_vid_adopt = vid.personadoptpractice_set.count()
    
    actors = vid.farmers_shown.values('person_name')
    actor_data = dict(actors = actors, tot_actors = len(actors))
    
    #Many questions are irrelevant to the video. Ranking the questions by using the number of matches
    #in title and question
    title_arr = [i for j in map(lambda x: x.split('_'), vid.title.split(' ')) for i in j]
    #title_arr is the final array of tokens from Title after splitting by ' ' and '_'
    
    ques = PersonMeetingAttendance.objects.filter(screening__videoes_screened = vid).exclude(expressed_question =  '')
    ques = ques.values('expressed_question','person__person_name','person__village__block__district__district_name',
                       'person__village__block__district__state__state_name','screening__date')
    if(len(ques) > 0):
        ques_arr = []
        for x in ques:
            ques_arr.append([x['expressed_question'].split(' '), x])
            
        scores = []
        for ques in ques_arr:
            count = 0
            for tok in title_arr:
                if tok in ques[0]:
                    count = count + 1
            scores.append([count, ques[1]])
        scores.sort(key = (lambda x: x[0]), reverse = True)
        ques = scores
    #ques is the final array of Question. It is SORTED list of lists, each list of the form [scores, pma object]
    
    
    rel_vids_all = Video.objects.exclude(pk=vid.pk).order_by('-viewers')
    rel_vids_prac = rel_vids_all.filter(related_agricultural_practices__in = vid.related_agricultural_practices.all())
    if(rel_vids_prac.count()>= 9):
        rel_vids = rel_vids_prac[:9]
    else:
        rel_vids = set(rel_vids_prac)
        rel_vids_lang = rel_vids_all.exclude(pk__in=rel_vids_prac.values_list('pk',flat=True)).filter(language = vid.language)
        rel_vids.update(list(rel_vids_lang[:9-len(rel_vids)]))
        if(len(rel_vids)< 9):
            rel_vids.update(list((rel_vids_all.filter(village__block__district__state = vid.village.block.district.state))[:9-len(rel_vids)]))

    rel_vids = sorted(list(rel_vids), key=lambda x: x.viewers, reverse=True)        
    return render_to_response('videopage.html',dict(vid = vid, \
                                                     tot_vid_scr = tot_vid_scr, \
                                                     tot_vid_adopt = tot_vid_adopt, \
                                                     actors = actor_data, \
                                                     ques = ques, \
                                                     rel_vids = rel_vids))


def video_search(request):
    video_suitable_for = request.GET.get('videosuitable')
    video_uploaded = request.GET.get('videouploaded')
    season = request.GET.getlist('season')
    lang = request.GET.get('lang')
    prac_arr = request.GET.getlist('prac')
    query = request.GET.get('query')
    page = request.GET.get('page')
    geog = request.GET.get('geog')
    id = request.GET.get('id')
    partners = request.GET.getlist('partner')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    sort = request.GET.get('sort')
    sort_order = request.GET.get('sort_order')
    search_box_params = {}

    vids = Video.objects.annotate(adoptions=Count('personadoptpractice'))
    
    if(query):
        vids = vids.filter(title__icontains = query)
        search_box_params['query'] = query
    if(video_suitable_for):
        if(int(video_suitable_for) != -1):
            vids = vids.filter(video_suitable_for = int(video_suitable_for))
    else:
        vids = vids.filter(video_suitable_for = 1)
    search_box_params['video_suitable_for'] = video_suitable_for
    if(from_date):
        search_box_params['from_date'] = from_date;
        from_date = datetime.date(*map(int,from_date.split('-')))
        vids = vids.filter(video_production_end_date__gte = from_date)
    if(to_date):
        search_box_params['to_date'] = to_date;
        to_date = datetime.date(*map(int,to_date.split('-')))
        vids = vids.filter(video_production_end_date__lte = to_date)
    if(video_uploaded == '1'):
        vids = vids.exclude(youtubeid = '')
        search_box_params['video_uploaded'] = video_uploaded
    elif(video_uploaded == '0'):
        vids = vids.filter(youtubeid = '')
        search_box_params['video_uploaded'] = video_uploaded
    
    if(season):
        vids = vids.filter(related_agricultural_practices__seasonality__in = season);
        search_box_params['season'] = season
    if(lang):
        vids = vids.filter(language__id = int(lang))
        search_box_params['sel_lang'] = lang
    search_box_params['langs'] = Language.objects.all().values('id','language_name')
    if(prac_arr):
        vids = vids.filter(related_agricultural_practices__id__in = map(int,prac_arr))
        search_box_params['prac'] = prac_arr
    search_box_params['all_pracs'] = Practices.objects.all().values('id','practice_name')
    if(geog):
        geog = geog.upper();
        if(geog=="COUNTRY"):
            vids = vids.filter(village__block__district__state__country__id = int(id))
        if(geog=="STATE"):
            vids = vids.filter(village__block__district__state__id = int(id))
        elif(geog=="DISTRICT"):
            vids = vids.filter(village__block__district__id = int(id))
        elif(geog=="BLOCK"):
            vids = vids.filter(village__block__id = int(id))
        elif(geog=="VILLAGE"):
            vids = vids.filter(village__id = int(id))
    search_box_params['geog_val'] = views.common.breadcrumbs_options(geog,id)
    
    if(partners):
        vids = vids.filter(village__block__district__partner__id__in = map(int,partners))
        search_box_params['sel_partners'] = partners
    search_box_params['all_partners'] = Partners.objects.all().values('id','partner_name')
    
    if(sort == None):
        vids  = vids.order_by('id')
    elif(sort == "viewers"):
        search_box_params['sort'] = sort
        if(sort_order == "asc"):
            search_box_params['sort_order'] = sort_order
            vids = vids.order_by("viewers",'id')
        else:
            vids = vids.order_by('-viewers', 'id')
    elif(sort == "prod_date"):
        search_box_params['sort'] = sort
        if(sort_order == "asc"):
            search_box_params['sort_order'] = sort_order
            vids = vids.order_by('video_production_end_date', 'id')
        else:
            vids = vids.order_by('-video_production_end_date', 'id')
    elif(sort == 'adoptions'):
        search_box_params['sort'] = sort
        if(sort_order == "asc"):
            search_box_params['sort_order'] = sort_order
            vids = vids.order_by('adoptions', 'id')
        else:
            vids = vids.order_by('-adoptions', 'id')
        
    
    #for paging
    vid_count = vids.count()
    vid_per_page = 10
    tot_pages = int(math.ceil(float(vid_count)/vid_per_page))
    if(not page or int(page) > tot_pages): 
        page = 1
    page = int(page)
    vids = vids[(page-1)*vid_per_page:(page*vid_per_page)]
    paging = dict(tot_pages = range(1,tot_pages+1), vid_count = vid_count, cur_page = page)
    
    return render_to_response("searchvideo_result.html",dict(vids = vids, paging=paging, search_box_params = search_box_params))
                                            

#Data generator for Month-wise Bar graph for Screening of videos
def video_screening_month_bar_data(request):
    video_id = int(request.GET['id'])
    return views.common.month_bar_data(video_analytics_sql.get_screening_month_bar_for_video, setting_from_date = None, setting_to_date = None, id = video_id);
