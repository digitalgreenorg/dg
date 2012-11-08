from django.shortcuts import *
from django.http import Http404, HttpResponse
from dashboard.models import *
import datetime
from output.database.SQL  import overview_analytics_sql, shared_sql, targets_sql, video_analytics_sql, screening_analytics_sql
from output import views
from output.views.common import get_geog_id
from output.database.utility import run_query, run_query_dict, run_query_dict_list, construct_query, get_dates_partners



def overview_module(request):
    geog, id = get_geog_id(request)
    from_date, to_date, partners = get_dates_partners(request)
    geog_list = [None,'COUNTRY','STATE','DISTRICT','BLOCK','VILLAGE']
    if(geog is not None and geog not in geog_list):
        raise Http404()
    geog_child = geog_par = "NULL"
    if geog != None:
        geog_par = geog_list[geog_list.index(geog)-1]
    if geog != "VILLAGE":
        geog_child = geog_list[geog_list.index(geog)+1]

    #Constructing table data
    vid_prod = run_query_dict(shared_sql.overview(type='production',geog=geog,id=id, from_date = from_date, to_date=to_date, partners=partners),'id');
    vid_screening = run_query_dict(shared_sql.overview(type='screening',geog=geog,id=id,from_date = from_date, to_date=to_date, partners=partners),'id');
    adoption = run_query_dict(shared_sql.overview(type='adoption',geog=geog,id=id,from_date = from_date, to_date=to_date, partners=partners),'id');
    tot_prac = run_query_dict(shared_sql.overview(type='practice',geog=geog,id=id,from_date = from_date, to_date=to_date, partners=partners),'id');
    tot_per = run_query_dict(shared_sql.overview(type='person',geog=geog,id=id,from_date = from_date, to_date=to_date, partners=partners),'id');
    tot_vil = run_query_dict(shared_sql.overview(type='village',geog=geog,id=id,from_date = from_date, to_date=to_date, partners=partners),'id');

    #Merging all dictionaries (vid_prod, tot_prac, etc) into one big one 'table_data'
    table_data = run_query(shared_sql.child_geog_list(geog=geog,id=id, from_date = from_date, to_date=to_date, partners=partners))
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
    par_geog_data = {}
    par_geog_data['tot_vid'] = reduce(lambda x,y: x+y, map(lambda x: x[0], vid_prod.values()), 0)
    par_geog_data['tot_scr'] = reduce(lambda x,y: x+y, map(lambda x: x[0], vid_screening.values()), 0)
    par_geog_data['tot_per'] = reduce(lambda x,y: x+y, map(lambda x: x[0], tot_per.values()), 0)
    par_geog_data['tot_pra'] = reduce(lambda x,y: x+y, map(lambda x: x[0], tot_prac.values()), 0)
    par_geog_data['tot_vil'] = reduce(lambda x,y: x+y, map(lambda x: x[0], tot_vil.values()), 0)
    par_geog_data['tot_ado'] = reduce(lambda x,y: x+y, map(lambda x: x[0], adoption.values()), 0)
    par_geog_data['name'], par_geog_data['id'] = get_parent_geog_id(geog, id)
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
    tot_val = views.screening_analytics.get_dist_attendees_avg_att_avg_sc(geog, id, from_date, to_date, partners, ['avg_sc_per_day', 'avg_att_per_sc']);
    #Average attendance 
    #Average Screening
    country_data.update(avg_att = tot_val['avg_att_per_sc'])
    country_data.update(avg_scr = tot_val['avg_sc_per_day'])
    
    #Adoption Rate
    country_data.update(adopt_rate = views.adoption_analytics.adoption_rate(geog, id, to_date, partners))
    #Distinct videos screened
    country_data.update(vid_screened = run_query(video_analytics_sql.video_tot_scr(geog=geog,id=id,from_date=from_date,to_date=to_date,partners=partners))[0]['count'])
    

    #search box params are the parameters for the search box i.e. dates, geography drop-down and partners if any
    search_box_params = views.common.get_search_box(request)

    get_req_url = request.META['QUERY_STRING']
    print get_req_url
    get_req_url = '&'.join([i for i in get_req_url.split('&') if i[:4]!='geog' and i[:2]!='id'])
    if(geog_child != "NULL"):
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

def get_parent_geog_id(geog, id):
    if geog is None:
        return "Total", None
    elif geog == "COUNTRY":
        return Country.objects.get(pk=id).country_name, None
    elif geog == "STATE":
        vls = State.objects.filter(pk=id).values_list('state_name','country')[0]
    elif geog == "DISTRICT":
        vls = District.objects.filter(pk=id).values_list("district_name", "state_id")[0]
    elif geog == "BLOCK":
        vls = Block.objects.filter(pk=id).values_list("block_name", "district_id")[0]
    elif geog == "VILLAGE":
        vls = Village.objects.filter(pk=id).values_list("village_name", "block_id")[0]
    else:
        return None, None
    return vls    
    