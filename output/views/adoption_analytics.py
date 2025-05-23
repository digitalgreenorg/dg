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

    totals = run_query(shared_sql.get_totals(geog, id, from_date, to_date, partners, values_to_fetch=['tot_att']))[0]
    tot_ado = run_query(shared_sql.get_totals(geog, id, from_date, to_date, partners, values_to_fetch=['tot_ado']))[0]
    tot_scr = run_query(shared_sql.get_totals(geog, id, from_date, to_date, partners, values_to_fetch=['tot_scr']))[0]
    tot_nonunique_ado = run_query(shared_sql.get_totals(geog, id, from_date, to_date, partners, values_to_fetch=['tot_nonunique_ado']))[0]
    totals.update(tot_ado)
    totals.update(tot_scr)
    totals.update(tot_nonunique_ado)

    # Total adoptions, total distinct practice adopted, distinct farmer adopting
    main_stats = run_query(adoption_analytics_sql.adoption_tot_ado(geog, id, from_date, to_date, partners))[0]
    main_stats['tot_ado'] = totals['tot_ado'] if totals['tot_ado'] is not None else 0
    main_stats['tot_nonunique_ado'] = totals['tot_nonunique_ado'] if totals['tot_nonunique_ado'] is not None else 0

    # Adoption rate
    date_var = to_date if to_date else (datetime.datetime.utcnow() - datetime.timedelta(1)).strftime('%Y-%m-%d')

    if type(to_date) != datetime.datetime:
        sixty_days_past = (datetime.datetime.strptime(date_var, '%Y-%m-%d') - datetime.timedelta(60)).strftime('%Y-%m-%d')
    else:
        sixty_days_past = (date_var - datetime.timedelta(60)).strftime('%Y-%m-%d')

    adopt_rate_data = run_query(shared_sql.get_total_active_attendees(geog, id, sixty_days_past, date_var, partners))[0]
    tot_adopt_per = run_query(shared_sql.get_total_adopted_attendees(geog, id, sixty_days_past, date_var, partners))[0]
    tot_active_adop = run_query(shared_sql.get_total_adoption_by_active_attendees(geog, id, from_date, date_var, partners))[0]
    adopt_rate_data.update(tot_adopt_per)
    adopt_rate_data.update(tot_active_adop)

    # Adoption rate
    if(adopt_rate_data['tot_adopt_per'] and adopt_rate_data['tot_per']):
        main_stats.update(adopt_rate = (adopt_rate_data['tot_adopt_per']*100)/adopt_rate_data['tot_per'])
    else:
        main_stats.update(adopt_rate = 0)
    
    # Average adoption per active viewer
    if(adopt_rate_data['tot_active_adop_nonunique'] and adopt_rate_data['tot_active_adop']):
        main_stats.update(avg_ado_per_farmer = adopt_rate_data['tot_active_adop_nonunique'] / adopt_rate_data['tot_active_adop'])
    else:
        main_stats.update(avg_ado_per_farmer = 0)

    # Probability of Adoption
    if(totals['tot_att'] and main_stats['tot_ado']):
        main_stats.update(adopt_prob = float(main_stats['tot_ado'])/float(totals['tot_att']) * 100)
    else:
        main_stats.update(adopt_prob = 0)

    # Number of practices repeated adopted by same farmer
    repeat_pract_per = run_query_raw(adoption_analytics_sql.adoption_repeat_adoption_practice_count(geog, id, from_date, to_date, partners))
    if repeat_pract_per != None and main_stats['tot_farmers']:
        main_stats.update(repeat_pract = float(repeat_pract_per[0][0] * 100)/main_stats['tot_farmers'])
    else:
        main_stats.update(repeat_pract = 0)

    # Average adoption per Video
    tot_vids_seen = run_query(video_analytics_sql.video_tot_scr(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners))[0]['count']
    if tot_vids_seen and main_stats['tot_ado']:
        main_stats.update(avg_ado_per_vid = float(main_stats['tot_nonunique_ado']) / tot_vids_seen)
    else:
        main_stats.update(avg_ado_per_vid = 0)

    # Average adoption per Screening
    if(totals['tot_scr'] and main_stats['tot_nonunique_ado']):
        main_stats.update(avg_ado_per_scr = float(main_stats['tot_nonunique_ado']) / float(totals['tot_scr']))
    else:
        main_stats.update(avg_ado_per_scr = 0)
    
    # Average adoption per adopter
    if(main_stats['tot_ado'] and main_stats['tot_nonunique_ado']):
        main_stats.update(avg_ado_per_adop = float(main_stats['tot_nonunique_ado']) / float(main_stats['tot_ado']))
    else:
        main_stats.update(avg_ado_per_adop = 0)

    search_box_params = views.common.get_search_box(request)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
 
    if  "/coco/jslps/analytics/" in request.get_full_path():
        template = 'jslps_adoption_module.html'
    elif  "/coco/brlps/analytics/" in request.get_full_path():
        template = 'brlps_adoption_module.html'
    elif "/coco/ethiopia/analytics/" in request.get_full_path():
        template = 'ethiopia_adoption_module.html'
    else:
        template = 'adoption_module.html'
    
    return render(request, template, dict(search_box_params = search_box_params,
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

# Data generator to generate Geography Wise Pie
def adoption_geog_pie_data(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = [None,'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
    if(geog not in geog_list[:-1]):
        raise Http404()

    get_req_url = request.META['QUERY_STRING']
    get_req_url = [i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id']
    get_req_url.append("geog="+geog_list[geog_list.index(geog)+1].lower())

    url = "/coco/analytics/adoption_module?"


    ado_prod = run_query(shared_sql.overview(geog,id, from_date, to_date, partners, 'adoption'))
    geog_name = run_query_dict(shared_sql.child_geog_list(geog, id, from_date, to_date),'id')

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

# Settings generator for Month-wise Bar graph


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


def adoption_rate(geog, id,from_date, to_date, partners):
    if not to_date:
        to_date = datetime.date.today()

    if type(to_date) != datetime.datetime:
        sixty_days_past = (datetime.datetime.strptime(to_date, '%Y-%m-%d') - datetime.timedelta(60)).strftime('%Y-%m-%d')
    else:
        sixty_days_past = (to_date - datetime.timedelta(60)).strftime('%Y-%m-%d')

    adopt_rate_data = run_query(shared_sql.get_total_adopted_attendees(geog, id, sixty_days_past, to_date, partners))[0]
    adopt_rate_data_tot_per = run_query(shared_sql.get_total_active_attendees(geog, id, sixty_days_past, to_date, partners))[0]
    adopt_rate_data.update(adopt_rate_data_tot_per)
    
    if(adopt_rate_data and adopt_rate_data['tot_per']):
        return (adopt_rate_data['tot_adopt_per']*100)/adopt_rate_data['tot_per']
    else:
        return 0
