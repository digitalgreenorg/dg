from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
from dg.output.database.SQL  import screening_analytics_sql, shared_sql
from dg.output import views
from dg.output.views.common import get_geog_id
from dg.output.database.utility import run_query, run_query_raw, run_query_dict, run_query_dict_list, construct_query, get_dates_partners


def screening_module(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog not in geog_list):
        raise Http404()
    tot_val = run_query(screening_analytics_sql.totAttendees_totScreening_datediff(geog, id, from_date, to_date, partners))[0];
    tot_scr = tot_val['tot_scr']
    tot_att = tot_val['tot_dist_per']
    if(tot_val['tot_days']):
        avg_scr = float(tot_scr)/tot_val['tot_days']
    else:
        avg_scr = 0
    if(tot_scr):
        avg_att = float(tot_val['tot_per'])/tot_scr
    else:
        avg_att = 0

    search_box_params = views.common.get_search_box(request, screening_analytics_sql.screening_min_date)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url

    return render_to_response('screening_module.html',dict(search_box_params = search_box_params,\
                                                          tot_scr=tot_scr,\
                                                          tot_att=tot_att, \
                                                          avg_scr=avg_scr, \
                                                          avg_att=avg_att, \
                                                          get_req_url = get_req_url
                                                          ))

    ################
    ## LINE CHART ##
    ################

def screening_tot_lines(request):
    geog, id = get_geog_id(request)
    rows = run_query_raw(screening_analytics_sql.screening_raw_attendance(request, geog, id))
    return_val = []
    for row in rows:
        return_val.append(';'.join([str(x) for x in row]))

    if(return_val):
        return HttpResponse('\n'.join(return_val))

    return HttpResponse(';;;;')

def screening_percent_lines(request):
    geog, id = get_geog_id(request)
    rows = run_query_raw(screening_analytics_sql.screening_percent_attendance(request, geog, id))
    return_val = []
    for row in rows:
        return_val.append(';'.join([str(x) for x in row]))

    if(return_val):
        return HttpResponse('\n'.join(return_val))

    return HttpResponse(';;;;')

def screening_per_day_line(request):
    geog, id = get_geog_id(request)
    rows = run_query_raw(screening_analytics_sql.screening_per_day(request, geog, id))
    if (not rows):
        return HttpResponse(';')

    return_val = []
    prev_date = rows[0][0]
    return_val.append(';'.join([str(x) for x in rows[0]]))

    day_one_delta = datetime.timedelta(days=1)
    for row in rows[1:]:
        prev_date += day_one_delta;
        while (prev_date!=row[0]):
            return_val.append(str(prev_date)+';0')
            prev_date += day_one_delta;

        return_val.append(str(row[0])+';'+str(row[1]))

    return HttpResponse('\n'.join(return_val))


    ###############
    ## Bar Graph ##
    ###############

#Data generator for Month-wise Bar graph
def screening_monthwise_bar_data(request):
    return views.common.month_bar_data(request, screening_analytics_sql.screening_month_bar);

#Settings generator for Month-wise Bar graph
def screening_monthwise_bar_settings(request):
    return views.common.month_bar_settings(request,screening_analytics_sql.screening_month_bar, "Disseminations")

    ####################
    ## Scatter Chart  ##
    ####################


def screening_practice_wise_scatter_data(request):
    return views.common.scatter_chart_data(request,screening_analytics_sql.screening_practice_scatter)

def screening_mf_ratio(request):
    return views.common.pie_chart_data(request,screening_analytics_sql.screening_attendees_malefemaleratio, \
                                      {"M":"Male","F":"Female"}, 'Ratio of {{value}} attendees')

#Data generator to generate Geography Wise Pie.
def screening_geog_pie_data(request):
    geog, id = get_geog_id(request)
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
    if(geog not in geog_list[:-1]):
        raise Http404()
    
    get_req_url = request.META['QUERY_STRING']
    get_req_url = [i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id']
    get_req_url.append("geog="+geog_list[geog_list.index(geog)+1].lower())

    url = ";;;/analytics/screening_module?"

    scr_geog = run_query(shared_sql.overview(request,geog,id,'screening'))
    geog_name = run_query_dict(shared_sql.child_geog_list(request, geog, id),'id')

    return_val = []
    return_val.append('[title];[value];[pull_out];[color];[url];[description];[alpha];[label_radius]')
    for item in scr_geog:
        append_str = geog_name[item['id']][0]+';'+str(item['tot_scr'])
        if(geog.upper()!= "VILLAGE"):
            temp_get_req_url = get_req_url[:]
            temp_get_req_url.append("id="+str(item['id']))
            append_str += url+'&'.join(temp_get_req_url)
        append_str += ";Ratio of disseminations in "+geog_name[item['id']][0]
        return_val.append(append_str)

    return HttpResponse('\n'.join(return_val))
