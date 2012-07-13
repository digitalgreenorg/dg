from django.shortcuts import *
from django.db.models import Count, Min, Max
from django.http import Http404, HttpResponse
from dashboard.models import *
import datetime,json
from output.database.SQL  import screening_analytics_sql, shared_sql
from output import views
from output.views.common import get_geog_id
from output.database.utility import run_query, run_query_raw, run_query_dict, run_query_dict_list, construct_query, get_dates_partners


def screening_module(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog not in geog_list):
        raise Http404()
    tot_val = get_dist_attendees_avg_att_avg_sc(geog, id, from_date, to_date, partners)
    
    search_box_params = views.common.get_search_box(request, screening_analytics_sql.screening_min_date)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url

    return render_to_response('screening_module.html',dict(search_box_params = search_box_params,\
                                                          tot_scr=tot_val['tot_scr'],\
                                                          tot_att=tot_val['dist_att'], \
                                                          avg_scr=tot_val['avg_sc_per_day'], \
                                                          avg_att=tot_val['avg_att_per_sc'], \
                                                          get_req_url = get_req_url
                                                          ))

    ################
    ## LINE CHART ##
    ################

def screening_tot_lines(request):
    geog, id = get_geog_id(request);
    from_date, to_date, partners = get_dates_partners(request);
    rows = run_query_raw(screening_analytics_sql.screening_raw_attendance(geog, id, from_date, to_date, partners))
    return_val = []
    for row in rows:
        return_val.append([str(row[0])] + map(float, list(row)[1:]))

    return_val.insert(0,["Date","Total Attendance","Total Expressed Interest","Total Expressed Adoption","Total Expressed Question"])
    if(return_val):
        return HttpResponse(json.dumps(return_val))

    return HttpResponse(';;;;')

def screening_percent_lines(request):
    geog, id = get_geog_id(request);
    from_date, to_date, partners = get_dates_partners(request);
    
    rows = run_query_raw(screening_analytics_sql.screening_percent_attendance(geog, id, from_date, to_date, partners))
    return_val = []
    for row in rows:
        return_val.append([str(row[0])]+[float(x) for x in list(row)[1:]])
    return_val.insert(0,["Date","Relative Attendance","Relative Expressed Interest","Relative Expressed Adoption","Relative Expressed Question"])
    if(return_val):
        return HttpResponse(json.dumps(return_val)  )

    return HttpResponse(';;;;')

def screening_per_day_line(request):
    geog, id = get_geog_id(request);
    from_date, to_date, partners = get_dates_partners(request);
    rows = run_query_raw(screening_analytics_sql.screening_per_day(geog, id, from_date, to_date, partners))
    if (not rows):
        return HttpResponse(';')
    return_val = []
    prev_date = rows[0][0]
    return_val.append([str(rows[0][0]),int(rows[0][1])])
    day_one_delta = datetime.timedelta(days=1)
    for row in rows[1:]:
        prev_date += day_one_delta;
        while (prev_date!=row[0]):
            return_val.append([str(prev_date),0])
            prev_date += day_one_delta;

        return_val.append([str(row[0]),int(row[1])])
        
    return_val.insert(0,["Date","Total Disseminations"])
    return HttpResponse(json.dumps(return_val))


    ###############
    ## Bar Graph ##
    ###############

#Data generator for Month-wise Bar graph
def screening_monthwise_bar_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.month_bar_data(screening_analytics_sql.screening_month_bar, setting_from_date = from_date, setting_to_date = to_date, \
                                       geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners);


    ####################
    ## Scatter Chart  ##
    ####################


def screening_practice_wise_scatter_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.scatter_chart_data(screening_analytics_sql.screening_practice_scatter, \
                                            geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)


    ################
    ## PIE CHARTS ##
    ################
    
def screening_mf_ratio(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.pie_chart_data(screening_analytics_sql.screening_attendees_malefemaleratio, \
                                      {"M":"Male","F":"Female"}, 'Ratio of {{value}} attendees', \
                                      geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)

#Data generator to generate Geography Wise Pie.
def screening_geog_pie_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
    if(geog not in geog_list[:-1]):
        raise Http404()
    
    get_req_url = request.META['QUERY_STRING']
    get_req_url = [i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id']
    get_req_url.append("geog="+geog_list[geog_list.index(geog)+1].lower())

    url = "/analytics/screening_module?"

    scr_geog = run_query(shared_sql.overview(geog,id, from_date, to_date, partners,'screening'))
    geog_name = run_query_dict(shared_sql.child_geog_list(geog,id, from_date, to_date, partners,),'id')
    
    return_val = []
    return_val.append(['title','value','url'])
    for item in scr_geog:
        if(geog.upper()!= "VILLAGE"):
            temp_get_req_url = get_req_url[:]
            temp_get_req_url.append("id="+str(item['id']))
            return_val.append([geog_name[item['id']][0],item['tot_scr'],url+'&'.join(temp_get_req_url)])
        else:
            return_val.append([geog_name[item['id']][0],item['tot_scr'],''])       
    return HttpResponse(json.dumps(return_val))


#Returns total distinct attendees, average attendance per screening, average screening per day
#        during the given period and for the given geography/partners
#        return values and calculation can be restricted using 'values_to_fetch'
#        values_to_fetch is a list of combination of 'tot_scr', 'dist_att, 'avg_att_per_sc', 'avg_sc_per_day'
#        values_to_fetch can be None, which will fetch all
def get_dist_attendees_avg_att_avg_sc(geog, id, from_date, to_date, partners, values_to_fetch=None):
    return_dict = {}
    if geog == 'COUNTRY' and not(from_date or to_date or partners):
        if values_to_fetch == None or ('dist_att' in values_to_fetch and 'avg_att_per_sc' in values_to_fetch):
            pma_data = PersonMeetingAttendance.objects.aggregate(tot_dist_per=Count('person', distinct=True), tot_per=Count('id'))
        elif 'dist_att' in values_to_fetch:
            pma_data = PersonMeetingAttendance.objects.aggregate(tot_dist_per=Count('person', distinct=True))
        elif 'avg_att_per_sc' in values_to_fetch:
            pma_data = dict(tot_per=PersonMeetingAttendance.objects.count())

        if values_to_fetch == None or 'avg_sc_per_day' in values_to_fetch:
            sc_data = Screening.objects.aggregate(tot_scr=Count("id"), max_date=Max('date'), min_date=Min('date'))
        elif 'avg_att_per_sc' in values_to_fetch or 'tot_scr' in values_to_fetch:
            sc_data = Screening.objects.aggregate(tot_scr=Count("id"))
        
        if(values_to_fetch==None or 'dist_att' in values_to_fetch):
            return_dict['dist_att'] = pma_data['tot_dist_per']
        if(values_to_fetch==None or 'tot_scr' in values_to_fetch):
            return_dict['tot_scr'] = sc_data['tot_scr']
        if(values_to_fetch==None or 'avg_att_per_sc' in values_to_fetch):
            if sc_data['tot_scr'] != 0:
                return_dict['avg_att_per_sc'] = float(pma_data['tot_per'])/sc_data['tot_scr']
            else:
                return_dict['avg_att_per_sc'] = 0
        if(values_to_fetch==None or 'avg_sc_per_day' in values_to_fetch):
            if(sc_data['max_date'] and sc_data['min_date']):
                tot_days = (sc_data['max_date'] - sc_data['min_date']).days + 1
            else:
                tot_days = 0
            if(tot_days):
                return_dict['avg_sc_per_day'] = sc_data['tot_scr']/tot_days
            else:
                return_dict['avg_sc_per_day'] = 0
    else:
        if values_to_fetch == None:
            sql_values_to_fetch = None
        else:
            sql_values_to_fetch = []
            if 'dist_att' in values_to_fetch:
                sql_values_to_fetch.append("tot_dist_per")
            if 'avg_att_per_sc' in values_to_fetch:
                sql_values_to_fetch.extend(["tot_scr", "tot_per"])
            if 'avg_sc_per_day' in values_to_fetch:
                sql_values_to_fetch.append("tot_scr")
                if not(from_date and to_date):
                    sql_values_to_fetch.append('dates')
            if 'tot_scr' in values_to_fetch and 'tot_scr' in sql_values_to_fetch:
                sql_values_to_fetch.append('tot_scr')
        tot_val = run_query(screening_analytics_sql.totAttendees_totScreening_datediff(geog, id, from_date, to_date, partners, sql_values_to_fetch))[0];
        
        if(values_to_fetch==None or 'dist_att' in values_to_fetch):
            return_dict['dist_att'] = tot_val['tot_dist_per']
        if(values_to_fetch==None or 'tot_scr' in values_to_fetch):
            return_dict['tot_scr'] = tot_val['tot_scr']
        if(values_to_fetch==None or 'avg_att_per_sc' in values_to_fetch):
            if tot_val['tot_scr'] != 0:
                return_dict['avg_att_per_sc'] = float(tot_val['tot_per'])/tot_val['tot_scr']
            else:
                return_dict['avg_att_per_sc'] = 0
        if(values_to_fetch==None or 'avg_sc_per_day' in values_to_fetch):
            if from_date and to_date:
                tot_days = (datetime.date(*[int(i) for i in to_date.split('-')]) - datetime.date(*[int(i) for i in from_date.split('-')])).days + 1;
            else:
                tot_days = tot_val['tot_days']
            if(tot_days):
                return_dict['avg_sc_per_day'] = float(tot_val['tot_scr'])/tot_days
            else:
                return_dict['avg_sc_per_day'] = 0
    
    return return_dict
