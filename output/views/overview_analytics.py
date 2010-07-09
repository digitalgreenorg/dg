from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
from dg.output.database.SQL  import overview_analytics_sql, shared_sql, targets_sql, video_analytics_sql, screening_analytics_sql
from dg.output import views
from dg.output.views.common import get_geog_id
from dg.output.database.utility import run_query, run_query_dict, run_query_dict_list, construct_query, get_dates_partners



def overview_module(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = [None,'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE',None]
    if(geog not in geog_list):
        raise Http404()
    geog_par = geog_list[geog_list.index(geog)-1]
    geog_child = geog_list[geog_list.index(geog)+1]

    #Constructing table data
    vid_prod = run_query_dict(shared_sql.overview(type='production',geog=geog,id=id,request=request),'id');
    vid_screening = run_query_dict(shared_sql.overview(type='screening',geog=geog,id=id,request=request),'id');
    adoption = run_query_dict(shared_sql.overview(type='adoption',geog=geog,id=id,request=request),'id');
    tot_prac = run_query_dict(shared_sql.overview(type='practice',geog=geog,id=id,request=request),'id');
    tot_per = run_query_dict(shared_sql.overview(type='person',geog=geog,id=id,request=request),'id');
    tot_vil = run_query_dict(shared_sql.overview(type='village',geog=geog,id=id,request=request),'id');

    #Merging all dictionaries (vid_prod, tot_prac, etc) into one big one 'table_data'
    table_data = run_query(shared_sql.child_geog_list(request, geog, id))
    for i in table_data:
        if i['id'] in vid_prod:
            i['tot_pro'] = vid_prod[i['id']][0]
        else:
            i['tot_pro'] = 0

        if i['id'] in adoption:
            i['tot_ado'] = adoption[i['id']][0]
        else:
            i['tot_ado'] = 0

        if i['id'] in vid_screening:
            i['tot_scr'] = vid_screening[i['id']][0]
        else:
            i['tot_scr'] = 0

        if i['id'] in tot_prac:
            i['tot_pra'] = tot_prac[i['id']][0]
        else:
            i['tot_pra'] = 0

        if i['id'] in tot_per:
            i['tot_per'] = tot_per[i['id']][0]
        else:
            i['tot_per'] = 0
            
        if i['id'] in tot_vil:
            i['tot_vil'] = tot_vil[i['id']][0]
        else:
            i['tot_vil'] = 0

        i['geog'] =  geog_child


#par_geog is summed data in the below table
    par_geog_data= run_query(overview_analytics_sql.overview_sum_geog(geog, id, from_date, to_date, partners))[0]
    par_geog_data['geog'] = geog_par


#country data is the top-data    
    country_data = {}
    #Total Person Group
    country_data.update(run_query(overview_analytics_sql.overview_tot_pg(geog, id, from_date, to_date, partners))[0])
    
    if(to_date):
        date_var = to_date
    else:
        date_var = str(datetime.date.today())
    #Operational Village (Last 60 days)
    country_data.update(vil_oper = run_query(targets_sql.get_village_operational(geog, id, date_var, partners))[0]['count'])
    tot_val = run_query(screening_analytics_sql.totAttendees_totScreening_datediff(geog, id, from_date, to_date, partners))[0];
    if(tot_val['tot_scr']):
        #Average attendance 
        #Average Screening
        country_data.update(avg_att = float(tot_val['tot_per'])/tot_val['tot_scr'])
        country_data.update(avg_scr = float(tot_val['tot_scr'])/tot_val['tot_days'])
    else:
        country_data.update(avg_att = 0)
        country_data.update(avg_scr = 0)
    #Adoption Rate
    tot_att_60_days = float(run_query(shared_sql.tot_dist_attendees_60_days(geog, id, date_var, partners))[0]['tot_per'])
    if(tot_att_60_days):
        country_data.update(adopt_rate = float(run_query(shared_sql.tot_dist_adopt_60_days(geog,id, date_var, partners))[0]['tot_adop_per'])*100/tot_att_60_days)
    else:
        country_data.update(adopt_rate = 0)
    #Distinct videos screened
    country_data.update(vid_screened = run_query(video_analytics_sql.video_tot_scr(request,geog=geog,id=id))[0]['count'])
    

#search box params are the parameters for the search box i.e. dates, geography drop-down and partners if any
    search_box_params = views.common.get_search_box(request, overview_analytics_sql.overview_min_date)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url

    if(geog_child):
        header_geog = geog_child
    else:
        header_geog = "Village"

    return render_to_response('overview_module.html', dict(search_box_params = search_box_params, \
                                                                                                       country_data = country_data, \
                                                                                                       table_data = table_data, \
                                                                                                       par_geog_data = par_geog_data, \
                                                                                                       get_req_url = get_req_url, \
                                                                                                       header_geog = header_geog \
                                                                                                       ))
