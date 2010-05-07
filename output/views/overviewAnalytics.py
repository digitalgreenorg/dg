from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
from dg.output.database.SQL  import overviewAnalyticsSQL, sharedSQL
from dg.output import views
from dg.output.database.utility import run_query, run_query_dict, run_query_dict_list, construct_query, getDatesPartners


def overview_module(request,geog,id):
    id = int(id)
    from_date, to_date, partners = getDatesPartners(request)
    geog_list = [None,'country','state','district','block','village',None]
    if(geog not in geog_list):
        raise Http404()
    geog_par = geog_list[geog_list.index(geog)-1]
    geog_child = geog_list[geog_list.index(geog)+1]
    
    #Constructing table data 
    vid_prod = run_query_dict(sharedSQL.overview(type='production',geog=geog,id=id,request=request),'id');
    vid_screening = run_query_dict(sharedSQL.overview(type='screening',geog=geog,id=id,request=request),'id');
    adoption = run_query_dict(sharedSQL.overview(type='adoption',geog=geog,id=id,request=request),'id');
    tot_prac = run_query_dict(sharedSQL.overview(type='practice',geog=geog,id=id,request=request),'id');
    tot_per = run_query_dict(sharedSQL.overview(type='person',geog=geog,id=id,request=request),'id');
    
    #Merging all dictionaries (vid_prod, tot_prac, etc) into one big one 'table_data'
    table_data = run_query(sharedSQL.child_geog_list(request, geog, id))
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
        
        i['geog'] =  geog_child
            
      
#par_geog is summed data in the below table  
    par_geog_data= run_query(overviewAnalyticsSQL.overview_sum_geog(request ,geog, id))[0]
    par_geog_data['geog'] = geog_par
    

#country data is the top-data   
    country_data = run_query(overviewAnalyticsSQL.overview_sum_geog(None ,'country', 1))[0]
    country_data.update(run_query(overviewAnalyticsSQL.overview_nation_pg_vil_total())[0])
    
#search box params are the parameters for the search box i.e. dates, geography drop-down and partners if any
    search_box_params = views.common.get_search_box(request,geog,id, overviewAnalyticsSQL.overview_min_date)
    
    get_req_url = request.META['QUERY_STRING']
    if(get_req_url): get_req_url = '?'+get_req_url


    return render_to_response('base_overview.html', dict(search_box_params = search_box_params, \
                                                       country_data = country_data, \
                                                       table_data = table_data, \
                                                       par_geog_data = par_geog_data, \
                                                       get_req_url = get_req_url \
                                                       ))

