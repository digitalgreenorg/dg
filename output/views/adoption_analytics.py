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
    
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog not in geog_list):
        raise Http404()
    
    #total adoptions, total distinct practice adopted, distinct farmer adopting
    main_stats = run_query(adoption_analytics_sql.adoption_tot_ado(geog, id, from_date, to_date, partners))[0]
    
    #Adoption rate
    if(to_date):
        date_var = to_date
    else:
        date_var = str(datetime.date.today())
    adopt_rate_data = run_query(shared_sql.adoption_rate(geog, id, date_var, partners))[0]
    if(adopt_rate_data and adopt_rate_data['tot_per']):
        main_stats.update(adopt_rate = (adopt_rate_data['tot_adopt_per']*100)/adopt_rate_data['tot_per'])
        main_stats.update(avg_ado_per_farmer = adopt_rate_data['tot_active_adop'] / adopt_rate_data['tot_per'])
    else:
        main_stats.update(adopt_rate = 0)
        main_stats.update(avg_ado_per_farmer = 0)
        
    #ratio of manifested expressed interest
    #ratio_exp_int_data = run_query(adoption_analytics_sql.adoption_exp_interest_to_adoption(geog, id, from_date, to_date, partners))[0]
    #if ratio_exp_int_data['tot_exp_int']:
    #    main_stats.update(ratio_exp_int = float(ratio_exp_int_data['tot_exp_int_ado'])/ratio_exp_int_data['tot_exp_int'])
    #else:
    #    main_stats.update(ratio_exp_int = 0)
        
    #Probability of Adoption
    tot_att = run_query_raw(shared_sql.tot_attendance(geog, id, from_date, to_date, partners))[0][0]
    if(tot_att != 0):
        main_stats.update(adopt_prob = float(main_stats['tot_ado'])/tot_att * 100)
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
    if tot_vids_seen:
        main_stats.update(avg_ado_per_vid = float(main_stats['tot_ado']) / tot_vids_seen)
    else:
        main_stats.update(avg_ado_per_vid = 0)
        
    #Avg adoption per Screening
    tot_scr = run_query(screening_analytics_sql.totAttendees_totScreening_datediff(geog, id, from_date, to_date, partners, values_to_fetch=['tot_scr']))[0]['tot_scr']
    if(tot_scr):
        main_stats.update(avg_ado_per_scr = float(main_stats['tot_ado']) / tot_scr)
    else:
        main_stats.update(avg_ado_per_scr = 0)
    
    search_box_params = views.common.get_search_box(request, adoption_analytics_sql.adoption_min_date)

    get_req_url = request.META['QUERY_STRING']
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(get_req_url): get_req_url = '&'+get_req_url

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
    geog_list = ['COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE', 'DUMMY']
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
        if(geog.upper()!= "VILLAGE"):
            temp_get_req_url = get_req_url[:]
            temp_get_req_url.append("id="+str(item['id']))
            return_val.append([geog_name[item['id']][0],item['tot_ado'],url+'&'.join(temp_get_req_url)])
        else:
            return_val.append([geog_name[item['id']][0],item['tot_ado'],''])

    return HttpResponse(json.dumps(return_val))


def adoption_practice_wise_scatter(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    return views.common.scatter_chart_data(adoption_analytics_sql.adoption_practice_wise_scatter, \
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
    
    return_val = [[str(date), float((active * 100)/tot)] for date, active, tot in adoption_rate_stats]
    return_val.insert(0,['Date','Adoption Rate'])
    return HttpResponse(json.dumps(return_val))
    

#===============================================================================
# def adoption_rate_line(request):
#    geog, id = get_geog_id(request)
#    from_date, to_date, partners = get_dates_partners(request)
#    sixty_days = datetime.timedelta(days=60)
#    
#    partners = map(int, partners)
#        
#    if partners and geog == "STATE":
#        #Refiltering the partners for the current state
#        partners = set(Partners.objects.filter(district__state__id = id).values_list('id', flat=True)).intersection(set(partners))
#        
#    if partners and geog in ("STATE", "COUNTRY"): #Recheck if filtered partners is not empty
#        pma_data = PersonMeetingAttendance.objects.filter(person__village__block__district__partner__in = partners)
#        pap_persons = PersonAdoptPractice.objects.filter(person__village__block__district__partner__in = partners)
#    else:
#       pma_data = PersonMeetingAttendance.objects.all()
#       pap_persons = PersonAdoptPractice.objects.all()
#       
#    if(geog == "STATE"):
#       pma_data = pma_data.filter(person__village__block__district__state__id = id)
#       pap_persons  = pap_persons.filter(person__village__block__district__state__id = id)
#    elif(geog == "DISTRICT"):
#        pma_data = pma_data.filter(person__village__block__district__id = id)
#        pap_persons = pap_persons.filter(person__village__block__district__id = id)
#    elif(geog == "BLOCK"):
#        pma_data = pma_data.filter(person__village__block__id = id)
#        pap_persons = pap_persons.filter(person__village__block__id = id)
#    elif(geog == "VILLAGE"):
#        pma_data = pma_data.filter(person__village__id = id)
#        pap_persons = pap_persons.filter(person__village__id = id)
#    elif(geog != "COUNTRY"):
#        raise Http404
#    
#    if from_date and to_date:
#        from_date = datetime.date(*[int(i) for i in from_date.split('-')])
#        to_date = datetime.date(*[int(i) for i in to_date.split('-')])
#        pma_data = pma_data.filter(screening__date__gte = (from_date - sixty_days), screening__date__lte = to_date)
#        date_struct = [[from_date + datetime.timedelta(days=i), 0, 0] for i in range((to_date - from_date).days + 1)]
#    else:
#        min_sc_date = pma_data.aggregate(Min('screening__date')).values()[0]
#        date_struct = [[min_sc_date + datetime.timedelta(days=i), 0, 0] for i in range((datetime.date.today() - min_sc_date).days + 1)]
#    
#    pma_data = pma_data.values_list('person__id', 'screening__date').order_by('person__id', 'screening__date')
#    pap_persons = set(pap_persons.values_list('person', flat=True).distinct())
#    
#    if len(pma_data) == 0:
#        return HttpResponse(";")
#            
#    def bin_search(ll, dd):
#        min = 0
#        max = len(ll) - 1
#        while max >= min:
#            mid = (min + max) / 2
#            if ll[mid][0] == dd:
#                return mid
#            elif ll[mid][0] > dd:
#                max = mid - 1
#            else:
#                min = mid + 1
#        return -1
#    
#    cur_person_id = pma_data[0][0]
#    min_date = pma_data[0][1]
#    max_date = min_date + sixty_days
#    for pma in pma_data[1:]:
#        if pma[1] > max_date or pma[0] != cur_person_id:
#            index = bin_search(date_struct, min_date)
#            if index == -1 and max_date >= date_struct[0][0] and min_date <= date_struct[0][0]:
#                index = 0
#                min_date = date_struct[0][0]
#            if index != -1:
#                is_adopted = cur_person_id in pap_persons
#                for i in range((max_date - min_date).days + 1):
#                    if(index + i >= len(date_struct)):
#                        break
#                    if is_adopted:
#                        date_struct[index + i][1] = date_struct[index + i][1] + 1
#                    date_struct[index + i][2] = date_struct[index + i][2] + 1
#            min_date = pma[1]
#            if pma[0] != cur_person_id:
#                cur_person_id = pma[0]
#        max_date = pma[1] + sixty_days
#    
#    return_val = []
#    for data in date_struct:
#        if(data[2] == 0):
#            rate = 0
#        else:
#            rate = float(data[1])/data[2] * 100
#        return_val.append(str(data[0]) + ';' + str(rate))
#        
#    return HttpResponse("\n".join(return_val))
#===============================================================================