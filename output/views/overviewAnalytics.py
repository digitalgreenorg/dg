from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
from dg.output.database  import overviewAnalyticsSQL, common
from dg.output import views
from dg.output.database.common import run_query, run_query_dict, run_query_dict_list, construct_query

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
        to_date = request.GET['to_date']
        
                
        par_geog = run_query(overviewAnalyticsSQL.overview_sum_geog(dict(geog=geog,from_date=from_date,to_date=to_date,id=id)))
        vid_prod = run_query(construct_query(common.overview,dict(type='production',geography=geog,geog_child=geog_child,from_date=from_date,to_date=to_date,id=id)));
        vid_screening = run_query(construct_query(common.overview,dict(type='screening',geography=geog,geog_child=geog_child,from_date=from_date,to_date=to_date,id=id)));
        adoption = run_query(construct_query(common.overview,dict(type='adoption',geography=geog,geog_child=geog_child,from_date=from_date,to_date=to_date,id=id)));
        tot_prac = run_query(construct_query(common.overview,dict(type='practice',geography=geog,geog_child=geog_child,from_date=from_date,to_date=to_date,id=id)));
        tot_per = run_query(construct_query(common.overview,dict(type='person',geography=geog,geog_child=geog_child,from_date=from_date,to_date=to_date,id=id)));

    else:
        date_range = 0
        par_geog = run_query(overviewAnalyticsSQL.overview_sum_geog(dict(geog=geog,id=id)))
        vid_prod = run_query(construct_query(common.overview,dict(type='production',geography=geog,geog_child=geog_child,id=id)));
        vid_screening = run_query(construct_query(common.overview,dict(type='screening',geography=geog,geog_child=geog_child,id=id)));
        adoption = run_query(construct_query(common.overview,dict(type='adoption',geography=geog,geog_child=geog_child,id=id)));
        tot_prac = run_query(construct_query(common.overview,dict(type='practice',geography=geog,geog_child=geog_child,id=id)));
        tot_per = run_query(construct_query(common.overview,dict(type='person',geography=geog,geog_child=geog_child,id=id)));
                
        min_date = run_query(overviewAnalyticsSQL.overview_min_date(geog = geog, id=id))
        start_date = min_date[0]['date']
        if not start_date:
            start_date = datetime.date.today()
               
    # Return static country data            
    country_data = run_query(overviewAnalyticsSQL.overview_sum_geog(dict(geog='country',id='1')))
    country_data[0].update(run_query(overviewAnalyticsSQL.overview_nation_pg_vil_total())[0])    
    #written by sreenivas to return parent id
    parent_id = run_query(overviewAnalyticsSQL.overview_parent_id(dict(geog = geog, id = id)))
    par_id = parent_id [0]['id']
    block_name = 'block'
    if geog == 'village':
        block_name = parent_id[0]['name']
        if date_range == 0:            
            par_geog = run_query(overviewAnalyticsSQL.overview_sum_geog(dict(geog='block',id=par_id)))
        else:
            par_geog = run_query(overviewAnalyticsSQL.overview_sum_geog(dict(geog='block',from_date=from_date,to_date=to_date,id=par_id)))
    
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
        return render_to_response('overview.html',{'item_list':return_val,'country_data':country_data[0],\
                                                   'block_name':block_name,'par_id':par_id,'geography':geog_child,'geog':geog,'id':id,\
                                                   'from_date':from_date,'to_date':to_date,\
                                                   'par_geog':par_geog[0],'sel_val': views.common.breadcrumbs_options(geog,id)})
    else:
        return render_to_response('overview.html',{'item_list':return_val,'country_data':country_data[0],'par_id':par_id,'geography':geog_child,\
                                                   'block_name':block_name,'start_date':start_date,'geog':geog,'id':id,'par_geog':par_geog[0], \
                                                   'sel_val': views.common.breadcrumbs_options(geog,id)})
        
        
