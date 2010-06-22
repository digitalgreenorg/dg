from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.output.database.SQL  import screening_analytics_sql, shared_sql, overview_analytics_sql
from dg.output.database.SQL.targets_sql import *
from dg.output.views.common import get_geog_id
from dg.output import views
from dg.output.database.utility import run_query, run_query_raw, run_query_dict, run_query_dict_list, construct_query, get_dates_partners
import datetime

def target_table(request):
    geog, id = get_geog_id(request);
    from_date, to_date, partners = get_dates_partners(request)
    
    today_date = datetime.date.today()
    if(not from_date):
        from_date = str(datetime.date(today_date.year,today_date.month,1))
    if(not to_date):
        to_date = str(datetime.date(today_date.year+(today_date.month+1)/12,(today_date.month+1)%12,1) - datetime.timedelta(days=1))
    
    if(datetime.date(*[int(i) for i in str(from_date).split('-')]) > datetime.date(*[int(i) for i in str(to_date).split('-')])):
        raise Http404; 
    achieved_vals = {}
    achieved_vals['csp_identified'] = run_query(get_csp_identified(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['village_operational'] = run_query(get_village_operational(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['storyboard'] = run_query(get_storyboard_prepared(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['video_edited'] = run_query(get_video_edited(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['quality_check'] = run_query(get_quality_check(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['inter_per_dissemination'] = run_query(get_interest_per_dissemination(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['new_csp_training'] = run_query(get_fresh_csp_tot_training(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['refresher_csp_traing'] = run_query(get_csp_tot_training(geog, id, from_date, to_date, partners))[0]['count'] - achieved_vals['new_csp_training'] 
    achieved_vals['new_crp_training'] = run_query(get_fresh_crp_tot_training(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['refresher_crp_traing'] = run_query(get_crp_tot_training(geog, id, from_date, to_date, partners))[0]['count'] - achieved_vals['new_crp_training']
    achieved_vals['vil_identified'] = run_query(get_village_identified(geog, id, from_date, to_date, partners))[0]['count']
    overview_vals = run_query(overview_analytics_sql.overview_sum_geog(geog, id, from_date, to_date, partners, ['adoption', 'production']))[0]
    achieved_vals['geog_name'] = overview_vals['name']
    achieved_vals['video_production'] = overview_vals['tot_vid']
    
    tot_val = run_query(screening_analytics_sql.totAttendees_totScreening_datediff(geog, id, from_date, to_date, partners))[0];
    achieved_vals['disseminations'] = tot_val['tot_scr']
    if(tot_val['tot_dist_per']):
        achieved_vals['att_per_diss'] = float(tot_val['tot_dist_per'])/tot_val['tot_scr']
    else:
        achieved_vals['att_per_diss'] = 0
        
    if(tot_val['tot_scr'] == 0):
        achieved_vals['avg_adoption'] = 0
    else:
        achieved_vals['avg_adoption'] = float(overview_vals['tot_ado'])/tot_val['tot_scr']
        
    achieved_vals['vids_uploaded'] = run_query(get_videos_uploaded(geog, id, from_date, to_date, partners))[0]['count']
    achieved_vals['csp_identified'] = run_query(get_csp_identified(geog, id, from_date, to_date, partners))[0]['count']
    
    target_vals = run_query(get_targets(geog, id, from_date, to_date, partners))[0]
    
    search_box_params = views.common.get_search_box(request)
    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url
    
    return render_to_response('targets_table.html',dict(search_box_params = search_box_params,\
                                                          achieved_vals=achieved_vals,\
                                                          target_vals=target_vals, \
                                                          get_req_url = get_req_url
                                                          ))

