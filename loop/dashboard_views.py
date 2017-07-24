from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Sum, Avg, Max, F

import pandas as pd
from loop.models import CombinedTransaction, Farmer, Crop, Mandi, Gaddidar, LoopUser
from loop.utils.loop_etl.group_myisam_data import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from constants.constants import ROLE_CHOICE_AGGREGATOR

def graph_data(request):
    chart_name = request.GET['chartName']
    if chart_name == 'volFarmerTS':
        result = vol_amount_farmer()
        return JsonResponse(result)
    if chart_name == 'cpkSpkTS':
        result = cpk_spk_timeseries()
        return JsonResponse(result)
    else:
        return JsonResponse({"result":"success"})

def cpk_spk_timeseries():
    cpk_spk = cpk_spk_ts(1,'20170401','20170601')
    return cpk_spk

def volume_aggregator(request):
    volume_per_aggregator = get_volume_aggregator(1)
    return JsonResponse(volume_per_aggregator)

def vol_amount_farmer():
    v_a_f_ts = volume_amount_farmers_ts(1,'20170401','20170601')
    return v_a_f_ts

def recent_graphs_data(request):
    # country_id = request.GET['country_id'] #To be fetched from request
    country_id = 1
    aggregated_result, cummulative_vol_farmer = get_data_from_myisam(0, country_id)

    chart_dict = {'aggregated_result': aggregated_result}
    # 'cummulative_vol_farmer': cummulative_vol_farmer}
    # data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    # algorithm to store column wise grouped data
    # print '*******************   ' + str(type(aggregated_result)) + '  ************************'
    res = {}
    for key, aggregated_value in aggregated_result.iteritems():
        for data in aggregated_value:
            for k, v in data.iteritems():
                if k not in res:
                    res[k] = {}
                    res[k]['placeHolder'] = 'cardData'
                    res[k]['tagName'] = k
                    res[k]['value'] = {}
                if key not in res[k]['value']:
                        res[k]['value'][key] = []
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
        'placeHolder':'cardGraphs',
        'tagName':'#Clusters',
        'value': total_cluster_reached
    })

    data.append({
        'placeHolder':'cardGraphs',
        'tagName':'#Farmers',
        'value': total_farmers_reached
    })

    data.append({
        'placeHolder':'cardGraphs',
        'tagName':'Volume',
        'value': volume
    })

    data.append({
        'placeHolder':'cardGraphs',
        'tagName':'Payments',
        'value': amount
    })

    data.append({
        'placeHolder':'cardGraphs',
        'tagName':'Cost per Kg',
        'value':-cpk
    })
    
    data.append({
        'placeHolder':'cardGraphs',
        'tagName':'Sustainability',
        'value':spk
    })
 
    return data

def get_card_graph_data(request):

    query_list = []
    filter_args = extract_filters_request(request)

    if filter_args['cardName'] in ['No_of_clusters_overall']:
        data_to_send = get_cluster_related_data(filter_args)
    
    if filter_args['cardName'] in ['No_of_clusters_spark_recent']:
        data_to_send = recent_graphs_data(filter_args)
        # data_to_send = []
        # data_to_send.append({
        #     'placeHolder':'cardGraphs',
        #     'tagName':'#Clusters_spark',
        #     'value':[1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 12, 34, 72, 23, 83]
        # })

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

    filter_args = {}
    filter_args['cardName'] = cardName
    filter_args['country_id'] = country_id
    return filter_args

def get_pandas_dataframe(sql_query):
    db_connection = MySQLdb.connect(host=DATABASES['default']['HOST'],
                                        user=DATABASES['default']['USER'],
                                        passwd=DATABASES['default']['PASSWORD'],
                                        db=DATABASES['default']['NAME'],
                                        charset='utf8',
                                        use_unicode=True)
    return pd.read_sql_query(sql_query, con=db_connection)