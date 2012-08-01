from django.shortcuts import *
from django.http import Http404, HttpResponse
from output.database.SQL  import screening_analytics_sql, shared_sql, overview_analytics_sql, adoption_analytics_sql, video_analytics_sql
from output.database.SQL.targets_sql import *
from output.views.common import get_geog_id
from output.views.overview_analytics import get_parent_geog_id
from output import views
from output.database.utility import run_query, run_query_raw, run_query_dict, run_query_dict_list, construct_query, get_dates_partners
import datetime

def target_table(request):
    geog, id = get_geog_id(request);
    from_date, to_date, partners = get_dates_partners(request)
    
    today_date = datetime.date.today()
    if(not from_date):
        from_date = str(datetime.date(today_date.year,today_date.month,1))
    if(not to_date):
        to_date = str(datetime.date(today_date.year+(today_date.month+1)/12,(today_date.month+1)%12, 1) - datetime.timedelta(days=1))
    
    if(datetime.date(*[int(i) for i in str(from_date).split('-')]) > datetime.date(*[int(i) for i in str(to_date).split('-')])):
        raise Http404; 
    achieved_vals = {}
    achieved_vals['csp_identified'] = run_query(get_csp_identified(geog, id, from_date, to_date, partners))[0]['count']
    
    vil_operation_from_date = run_query(get_village_operational(geog, id, from_date, partners))[0]['count']
    vil_operation_to_date = run_query(get_village_operational(geog, id, to_date, partners))[0]['count'] 
    if(vil_operation_from_date!=None and vil_operation_to_date!=None):
        achieved_vals['village_operational'] = vil_operation_to_date - vil_operation_from_date
    
    achieved_vals['storyboard'] = run_query(get_storyboard_prepared(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['video_edited'] = run_query(get_video_edited(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['quality_check'] = run_query(get_quality_check(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['inter_per_dissemination'] = run_query(get_interest_per_dissemination(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['new_csp_training'] = run_query(get_fresh_csp_tot_training(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['refresher_csp_traing'] = run_query(get_csp_tot_training(geog, id, from_date, to_date, partners))[0]['count'] - achieved_vals['new_csp_training'] 
    achieved_vals['new_crp_training'] = run_query(get_fresh_crp_tot_training(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['refresher_crp_traing'] = run_query(get_crp_tot_training(geog, id, from_date, to_date, partners))[0]['count'] - achieved_vals['new_crp_training']
    achieved_vals['vil_identified'] = run_query(get_village_identified(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['geog_name'] = get_parent_geog_id(geog, id)[0]
    tot_val = run_query(shared_sql.get_totals(geog, id, from_date, to_date, partners, ['tot_vid', 'tot_ado', 'tot_att', 'tot_scr']))[0]
    achieved_vals['video_production'] = tot_val['tot_vid']
    achieved_vals['disseminations'] = tot_val['tot_scr']
    if(tot_val['tot_scr']):
        achieved_vals['att_per_diss'] = tot_val['tot_att']/tot_val['tot_scr']
        achieved_vals['avg_adoption'] = tot_val['tot_ado']/tot_val['tot_scr']
    else:
        achieved_vals['att_per_diss'] = 0
        achieved_vals['avg_adoption'] = 0
        
    achieved_vals['vids_uploaded'] = run_query(get_videos_uploaded(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['csp_identified'] = run_query(get_csp_identified(geog, id, from_date, to_date, partners))[0]['count']
    
    target_vals = run_query(get_targets(geog, id, from_date, to_date, partners))[0]
    
    search_box_params = views.common.get_search_box(request)
    #overrider search_box from_date and to_date 
    search_box_params['from_date'] = str(from_date)
    search_box_params['to_date'] = str(to_date)
    
    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url
    
    return render_to_response('targets_table.html',dict(search_box_params = search_box_params,\
                                                          achieved_vals=achieved_vals,\
                                                          target_vals=target_vals, \
                                                          get_req_url = get_req_url
                                                          ))

