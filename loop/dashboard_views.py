from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Sum, Avg, Max, F
from django.core.serializers.json import DjangoJSONEncoder
import json
import math
import pandas as pd

from loop.models import CombinedTransaction, Farmer, Crop, Mandi, Gaddidar, LoopUser
from loop.utils.loop_etl.group_myisam_data import *
from constants.constants import ROLE_CHOICE_AGGREGATOR

# def cpk_spk_timeseries(country_id, start_date, end_date):
#     cpk_spk = cpk_spk_ts(country_id, start_date, end_date)
#     return cpk_spk
#
# def vol_amount_farmer(country_id, start_date, end_date):
#     v_a_f_ts = volume_amount_farmers_ts(country_id, start_date, end_date)
#     return v_a_f_ts

def volume_aggregator(request):
    volume_per_aggregator = get_volume_aggregator(1)
    return JsonResponse(volume_per_aggregator)

def recent_graphs_data(request):
    # country_id = request.GET['country_id'] #To be fetched from request
    country_id = 1
    aggregated_result, cummulative_vol_farmer = get_data_from_myisam(0, country_id)

    chart_dict = {'aggregated_result': aggregated_result}

    # algorithm to store column wise grouped data

    res = {}
    for key, aggregated_value in aggregated_result.iteritems():
        for data in aggregated_value:
            for k, v in data.iteritems():
                if k not in res:
                    res[k] = {}
                    res[k]['placeHolder'] = 'recentcardGraphs'
                    res[k]['tagName'] = k
                    res[k]['value'] = {}
                if key not in res[k]['value']:
                        res[k]['value'][key] = []
                if type(v) is float:
                    if(math.isnan(float(v))) :
                        v = 0
                res[k]['value'][key].append(v)

    data = []
    data.append(res['cpk']);
    data.append(res['quantity__sum'])
    data.append(res['amount__sum'])
    data.append(res['distinct_farmer_count'])
    data.append(res['spk'])
    data.append(res['active_cluster'])
    return data


def get_cluster_related_data(filter_args) :
    country_id = filter_args['country_id'] #To be fetched from request
    total_farmers_reached = CombinedTransaction.objects.filter(mandi__district__state__country=country_id).values('farmer').distinct().count()
    total_cluster_reached = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR, village__block__district__state__country=country_id).count()

    aggregated_result, cum_vol_farmer = get_data_from_myisam(1, country_id)
    volume = round(aggregated_result['quantity'][0], 2)
    amount = round(aggregated_result['amount'][0], 2)
    aggregator_incentive = aggregated_result['aggregator_incentive'][0]
    transportation_cost = aggregated_result['transportation_cost'][0]
    farmer_share = aggregated_result['farmer_share'][0]
    gaddidar_share = aggregated_result['gaddidar_share'][0]
    cpk = round((aggregator_incentive + transportation_cost) / volume, 2)
    spk = round((farmer_share + gaddidar_share) * 100 / volume, 2)

    data = []
    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'No_of_clusters_overall',
        'value': total_cluster_reached
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'No_of_farmers_overall',
        'value': total_farmers_reached
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Volume_overall',
        'value': volume
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Payments_overall',
        'value': amount
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Cost_per_kg_overall',
        'value':-cpk
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Sustainability_overall',
        'value':spk
    })

    return data

def get_card_graph_data(request):

    query_list = []
    filter_args = extract_filters_request(request)

    if filter_args['cardName'] in ['No_of_clusters_overall']:
        data_to_send = get_cluster_related_data(filter_args)

    if filter_args['cardName'] in ['active_cluster']:
        data_to_send = recent_graphs_data(filter_args)

    data = json.dumps({'data' : data_to_send}, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def extract_filters_request(request):
    if 'cardName' in request.GET:
        cardName = str(request.GET.get('cardName'))
    else:
        cardName = ''

    if 'country_id' in request.GET:
        country_id = str(request.GET.get('country_id'))
    else:
        country_id = 1

    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = str(request.GET['start_date'])
        end_date = str(request.GET['end_date'])
    else:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        delta = datetime.timedelta(days=30)
        start_date = (datetime.datetime.today() - delta).strftime('%Y-%m-%d')

    aggregators_list = request.GET.getlist('Aggregator')
    mandis_list = request.GET.getlist('Mandi')
    crops_list = request.GET.getlist('Crops')
    gaddidars_list = request.GET.getlist('Gaddidar')

    filter_args = {}
    filter_args['cardName'] = cardName
    filter_args['country_id'] = country_id
    filter_args['start_date'] = start_date
    filter_args['end_date'] = end_date
    filter_args['country_id'] = country_id
    filter_args['aggregators_list'] = aggregators_list
    filter_args['mandis_list'] = mandis_list
    filter_args['crops_list'] = crops_list
    filter_args['gaddidars_list'] = gaddidars_list

    return filter_args

def get_pandas_dataframe(sql_query):
    db_connection = MySQLdb.connect(host=DATABASES['default']['HOST'],
                                        user=DATABASES['default']['USER'],
                                        passwd=DATABASES['default']['PASSWORD'],
                                        db=DATABASES['default']['NAME'],
                                        charset='utf8',
                                        use_unicode=True)
    return pd.read_sql_query(sql_query, con=db_connection)

# def cumm_vol_farmer(country_id):
#     c_v_f = get_cummulative_vol_farmer(country_id)
#     return c_v_f

def graph_data(request):
    filter_args = extract_filters_request(request)

    chart_name = request.GET['chartName']
    if chart_name == 'volFarmerTS':
        result = volume_amount_farmers_ts(**filter_args)
    elif chart_name == 'cpkSpkTS':
        result = cpk_spk_ts(**filter_args)
    elif chart_name == 'cummulativeCount':
        result = get_cummulative_vol_farmer(**filter_args)
    elif chart_name == 'aggrvol':
        result = aggregator_volume(**filter_args)
    elif chart_name == 'aggrvisit':
        result = aggregator_visits(**filter_args)
    elif chart_name == 'mandivolume':
        result = mandi_volume(**filter_args)
    elif chart_name == 'mandivisit':
        result = mandi_visits(**filter_args)
    elif chart_name == 'cropvolume':
        result = crop_volume(**filter_args)
    elif chart_name == 'cropfarmercount':
        result = crop_farmer_count(**filter_args)
    elif chart_name == 'cropprices':
        result = crop_prices(**filter_args)
    elif chart_name == 'aggrspkcpk':
        result = agg_spk_cpk(**filter_args)
    elif chart_name == 'aggrrecoveredtotal':
        result = agg_cost(**filter_args)
    elif chart_name == 'aggrfarmercount':
        result = agg_farmer_count(**filter_args)
    elif chart_name == 'mandispkcpk':
        result = mandi_spk_cpk(**filter_args)
    elif chart_name == 'mandirecoveredtotal':
        result = mandi_cost(**filter_args)
    elif chart_name == 'mandifarmercount':
        result = mandi_farmer_count(**filter_args)
    else:
        result = {"result":"success"}
    return JsonResponse(result)

def send_filter_data(request):
    # language = request.GET.get('language')
    # country_id = request.GET.get('country_id')
    country_id = 1
    response_list = []
    aggregator_data = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR, village__block__district__state__country=country_id).annotate(value=F('name_en')).values('user_id', 'value').distinct().order_by('value')
    aggregator_list = aggregator_data.annotate(id=F('user_id')).values('id', 'value')

    aggregator_dict = {'name':'Aggregator', 'data':list(aggregator_list)}

    crop_list = Crop.objects.annotate(value=F('crop_name')).values('id', 'value').order_by('value')
    crop_dict = {'name':'Crops', 'data':list(crop_list)}

    mandi_list = Mandi.objects.filter(district__state__country=country_id).annotate(value=F('mandi_name_en')).values('id', 'value').order_by('value')
    mandi_dict = {'name':'Mandi', 'data':list(mandi_list)}

    gaddidar_list = Gaddidar.objects.filter(mandi__district__state__country=country_id).annotate(value=F('gaddidar_name_en')).values(
        'id', 'value').order_by('value')
    gaddidar_dict = {'name':'Gaddidar','data':list(gaddidar_list)}

    response_list.extend([aggregator_dict, crop_dict, mandi_dict, gaddidar_dict])
    data = json.dumps(response_list)
    return HttpResponse(data)
