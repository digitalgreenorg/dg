from dashboard.models import *
from django.db.models import Min
from django.http import Http404, HttpResponse
from django.shortcuts import *
from output import views
from output.database.SQL  import adoption_analytics_sql, video_analytics_sql, screening_analytics_sql, shared_sql
from output.database.utility import run_query, run_query_dict, run_query_dict_list, run_query_raw, construct_query, get_dates_partners
from output.views.common import get_geog_id
import datetime, json


def adoption_module(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    
    geog_list = [None,'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog not in geog_list):
        raise Http404()
    
    totals = run_query(shared_sql.get_totals(geog, id, from_date, to_date, partners, values_to_fetch=['tot_att', 'tot_ado', 'tot_scr']))[0]
    #total adoptions, total distinct practice adopted, distinct farmer adopting
    main_stats = run_query(adoption_analytics_sql.adoption_tot_ado(geog, id, from_date, to_date, partners))[0]
    main_stats['tot_ado'] = totals['tot_ado'] if totals['tot_ado'] is not None else 0
    
    #Adoption rate
    date_var = to_date if to_date else str(datetime.date.today())
    adopt_rate_data = run_query(shared_sql.adoption_rate_totals(geog, id, date_var, partners))[0]
    if(adopt_rate_data and adopt_rate_data['tot_per']):
        main_stats.update(adopt_rate = (adopt_rate_data['tot_adopt_per']*100)/adopt_rate_data['tot_per'])
        main_stats.update(avg_ado_per_farmer = adopt_rate_data['tot_active_adop'] / adopt_rate_data['tot_per'])
    else:
        main_stats.update(adopt_rate = 0)
        main_stats.update(avg_ado_per_farmer = 0)
        
    #Probability of Adoption
    if(totals['tot_att'] and main_stats['tot_ado']):
        main_stats.update(adopt_prob = float(main_stats['tot_ado'])/float(totals['tot_att']) * 100)
    else:
        main_stats.update(adopt_prob = 0)
    
    #Number of practices repeated adopted by same farmer
    repeat_pract_per = run_query_raw(adoption_analytics_sql.adoption_repeat_adoption_practice_count(geog, id, from_date, to_date, partners))
    if repeat_pract_per != None and main_stats['tot_farmers']:
        main_stats.update(repeat_pract = float(repeat_pract_per[0][0] * 100)/main_stats['tot_farmers'])
    else:
        main_stats.update(repeat_pract = 0)
        
    #Avg adoption per Video
    tot_vids_seen = run_query(video_analytics_sql.video_tot_scr(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners))[0]['count']
    if tot_vids_seen and main_stats['tot_ado']:
        main_stats.update(avg_ado_per_vid = float(main_stats['tot_ado']) / tot_vids_seen)
    else:
        main_stats.update(avg_ado_per_vid = 0)
        
    #Avg adoption per Screening
    if(totals['tot_scr'] and main_stats['tot_ado']):
        main_stats.update(avg_ado_per_scr = float(main_stats['tot_ado']) / float(totals['tot_scr']))
    else:
        main_stats.update(avg_ado_per_scr = 0)
    
    search_box_params = views.common.get_search_box(request)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])

    return render_to_response('adoption_module.html', dict(search_box_params = search_box_params,
                                                          get_req_url = get_req_url,
                                                          **main_stats
                                                          ))

# Pie chart for male-female ratio in video module
def adoption_pie_graph_mf_ratio(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.pie_chart_data(adoption_analytics_sql.adoption_malefemale_ratio, \
                                      {"M":"Male","F":"Female"}, 'Ratio of Adoption for {{value}} farmers', \
                                      geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)

#Data generator to generate Geography Wise Pie.
def adoption_geog_pie_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = [None,'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
    if(geog not in geog_list[:-1]):
        raise Http404()
    
    get_req_url = request.META['QUERY_STRING']
    get_req_url = [i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id']
    get_req_url.append("geog="+geog_list[geog_list.index(geog)+1].lower())

    url = "/analytics/adoption_module?"


    ado_prod = run_query(shared_sql.overview(geog,id, from_date, to_date, partners, 'adoption'))
    geog_name = run_query_dict(shared_sql.child_geog_list(geog, id, from_date, to_date, partners),'id')

    return_val = []
    return_val.append(['name','value','url'])
    for item in ado_prod:
        if(geog is None or geog.upper()!= "VILLAGE"):
            temp_get_req_url = get_req_url[:]
            temp_get_req_url.append("id="+str(item['id']))
            return_val.append([geog_name[item['id']][0], float(item['tot_ado']) ,url+'&'.join(temp_get_req_url)])
        else:
            return_val.append([geog_name[item['id']][0], float(item['tot_ado']), ''])

    return HttpResponse(json.dumps(return_val))


def adoption_practice_wise_scatter(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.practice_scatter_chart_data(adoption_analytics_sql.adoption_practice_wise_scatter, \
                                           geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners)
    
def adoption_monthwise_bar_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.month_bar_data(adoption_analytics_sql.adoption_month_bar, setting_from_date = from_date, setting_to_date = to_date, \
                                       geog = geog, id = id, from_date=from_date, to_date = to_date, partners= partners);

#Settings generator for Month-wise Bar graph


def adoption_rate_line(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    adoption_rate_stats = run_query_raw(adoption_analytics_sql.adoption_rate_line(geog, id, from_date, to_date, partners))
    return_val = []
    for date, active, tot in adoption_rate_stats:
        if tot:
            return_val.append([str(date), round(float((active * 100)/tot),1)])
        else:
            return_val.append([str(date), 0])   
    return_val.insert(0,['Date','Adoption Rate'])
    return HttpResponse(json.dumps(return_val))
    

def adoption_rate(geog, id, to_date, partners):
    if not to_date:
        to_date = datetime.date.today()
    adopt_rate_data = run_query(shared_sql.adoption_rate_totals(geog, id, to_date, partners))[0]
    if(adopt_rate_data and adopt_rate_data['tot_per']):
        return (adopt_rate_data['tot_adopt_per']*100)/adopt_rate_data['tot_per']
    else:
        return 0
