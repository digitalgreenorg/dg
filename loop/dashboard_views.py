from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Min, Sum, Avg, Max, F, Value
from django.db.models.fields import CharField
import json
import math
import pandas as pd

from loop.models import CombinedTransaction, Farmer, Crop, Mandi, Gaddidar, LoopUser, Country, State
from loop.utils.loop_etl.group_myisam_data import *
from loop.dashboard.home_statistics import *
from loop.dashboard.analytics_statistics import *
from loop.dashboard.timeseries_statistics import *
from constants.constants import ROLE_CHOICE_AGGREGATOR

def extract_filters_request(request):
    if 'cardName' in request.GET:
        cardName = str(request.GET.get('cardName'))
    else:
        cardName = ''

    if 'country_id' in request.GET:
        country_id = str(request.GET.get('country_id'))
    else:
        country_id = 1
    if 'state_id' in request.GET:
        state_id = str(request.GET.get('state_id'))
    else :
        state_id = None

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
    filter_args['aggregators_list'] = aggregators_list
    filter_args['mandis_list'] = mandis_list
    filter_args['crops_list'] = crops_list
    filter_args['gaddidars_list'] = gaddidars_list
    filter_args['state_id'] = state_id

    return filter_args

def volume_aggregator(request):
    volume_per_aggregator = get_volume_aggregator(1)
    return JsonResponse(volume_per_aggregator)

def recent_graphs_data(**kwargs):
    kwargs['start_date'] = None
    kwargs['end_date'] = None
    kwargs['aggregator_list'] = []
    kwargs['gaddidar_list'] = []
    kwargs['mandi_list'] = []

    aggregated_result = get_data_from_myisam(0, **kwargs)
    # aggregated_result, cummulative_vol_farmer = get_data_from_myisam(0, **kwargs)
    chart_dict = {'aggregated_result': aggregated_result}

    # algorithm to store column wise grouped data
    res = {}
    res['cpk'] = generate_res_recent('cpk', 'recentcardGraphs', 'Cpk' , {})
    res['quantity__sum'] = generate_res_recent('quantity__sum', 'recentcardGraphs', 'Volume' , {})
    res['amount__sum'] = generate_res_recent('amount__sum','recentcardGraphs', 'Amount' , {})
    res['distinct_farmer_count'] = generate_res_recent('distinct_farmer_count', 'recentcardGraphs', 'Farmers' , {})
    res['spk'] = generate_res_recent('spk', 'recentcardGraphs', 'Spk' , {})
    res['active_cluster'] = generate_res_recent( 'active_cluster','recentcardGraphs', 'Clusters' , {})
    for key, aggregated_value in aggregated_result.iteritems():
        for data in reversed(aggregated_value):
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

def generate_res_recent(key, placeHolder, tagName, value):
    res = {}
    res['placeHolder'] = placeHolder
    res['tagName'] = tagName
    res['value'] = {}
    res['value']['15'] = []
    res['value']['30'] = []
    res['value']['60'] = []
    return res


def overall_graph_data(**filter_args):
    country_id = filter_args['country_id'] #To be fetched from request
    state_id = filter_args['state_id']
    filter_args['start_date'] = None
    filter_args['end_date'] = None
    filter_args['aggregator_list'] = []
    filter_args['gaddidar_list'] = []
    filter_args['mandi_list'] = []
    combinedTransactionData = CombinedTransaction.objects.filter(mandi__district__state__country=country_id)
    loopUserData = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR, village__block__district__state__country=country_id)

    if state_id:
        combinedTransactionData = combinedTransactionData.filter(mandi__district__state=state_id)
        loopUserData = loopUserData.filter(village__block__district__state=state_id)

    total_farmers_reached = combinedTransactionData.values('farmer').distinct().count()
    total_cluster_reached = loopUserData.count()

    aggregated_result = get_data_from_myisam(1, **filter_args)
    # aggregated_result, cum_vol_farmer = get_data_from_myisam(1, **filter_args)
    # if((len(aggregated_result) > 0) and (len(cum_vol_farmer) > 0)):
    volume = round(aggregated_result['quantity'][0])
    amount = round(aggregated_result['amount'][0])
    aggregator_incentive = aggregated_result['aggregator_incentive'][0]
    transportation_cost = aggregated_result['transportation_cost'][0]
    farmer_share = aggregated_result['farmer_share'][0]
    gaddidar_share = aggregated_result['gaddidar_share'][0]
    cpk = round((aggregator_incentive + transportation_cost) / volume, 2)
    spk = round((farmer_share + gaddidar_share) * 100 / (aggregator_incentive + transportation_cost), 2)

    data = []
    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'No_of_clusters_overall',
        'value': 0 if(isNAN(total_cluster_reached)) else total_cluster_reached
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'No_of_farmers_overall',
        'value': 0 if(isNAN(total_farmers_reached)) else total_farmers_reached
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Volume_overall',
        'value': 0 if(isNAN(volume)) else  volume
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Payments_overall',
        'value':  0 if(isNAN(amount)) else amount
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Cost_per_kg_overall',
        'value': -1 if(isNAN(cpk)) else -cpk
    })

    data.append({
        'placeHolder':'overallcardGraphs',
        'tagName':'Sustainability_overall',
        'value': 0 if(isNAN(spk)) else spk
    })

    return data

def isNAN(v) :
    if type(v) is float:
        if(math.isnan(float(v))) :
            return True
    return False

def get_card_graph_data(request):
    query_list = []
    filter_args = extract_filters_request(request)
    data_to_send = {}

    if filter_args['cardName'] in ['No_of_clusters_overall']:
        data_to_send = overall_graph_data(**filter_args)
    elif filter_args['cardName'] in ['Clusters']:
        data_to_send = recent_graphs_data(**filter_args)

    data = json.dumps({'data' : data_to_send}, cls=DjangoJSONEncoder)
    return HttpResponse(data)

def get_pandas_dataframe(sql_query):
    db_connection = MySQLdb.connect(host=DATABASES['default']['HOST'],
                                        user=DATABASES['default']['USER'],
                                        passwd=DATABASES['default']['PASSWORD'],
                                        db=DATABASES['default']['NAME'],
                                        charset='utf8',
                                        use_unicode=True)
    return pd.read_sql_query(sql_query, con=db_connection)

def graph_data(request):
    filter_args = extract_filters_request(request)

    chart_name = request.GET['chartName']
    if chart_name == 'volFarmerTS':
        result = volume_amount_farmers_ts(**filter_args)
    elif chart_name == 'cpkSpkTS':
        result = cpk_spk_ts(**filter_args)
    elif chart_name == 'cummulativeCount':
        filter_args['start_date'] = None
        filter_args['end_date'] = None
        result = get_cummulative_vol_farmer(**filter_args)
    elif chart_name == 'aggrvol':
        result = aggregator_volume(**filter_args)
    elif chart_name == 'aggramt':
        result = aggregator_amount(**filter_args)
    elif chart_name == 'aggrvisit':
        result = aggregator_visits(**filter_args)
    elif chart_name == 'aggrspkcpk':
        result = agg_spk_cpk(**filter_args)
    elif chart_name == 'aggrrecoveredtotal':
        result = agg_cost(**filter_args)
    elif chart_name == 'aggrfarmercount':
        result = agg_farmer_count(**filter_args)
    elif chart_name == 'mandivolume':
        result = mandi_volume(**filter_args)
    elif chart_name == 'mandivisit':
        result = mandi_visits(**filter_args)
    elif chart_name == 'mandispkcpk':
        result = mandi_spk_cpk(**filter_args)
    elif chart_name == 'mandirecoveredtotal':
        result = mandi_cost(**filter_args)
    elif chart_name == 'mandifarmercount':
        result = mandi_farmer_count(**filter_args)
    elif chart_name == 'cropvolume':
        result = crop_volume(**filter_args)
    elif chart_name == 'cropfarmercount':
        result = crop_farmer_count(**filter_args)
    elif chart_name == 'cropprices':
        result = crop_prices(**filter_args)
    elif chart_name == 'crop_price_range_ts':
        result = crop_price_range_ts(**filter_args)
    else:
        result = {"result":"success"}
    return JsonResponse(result)

def send_filter_data(request):
    # language = request.GET.get('language')
    filter_args = extract_filters_request(request)
    country_id = filter_args['country_id']
    state_id = filter_args['state_id']
    response_list = []

    aggregator_data = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR, village__block__district__state__country=country_id)
    if state_id != None:
        aggregator_data = aggregator_data.filter(village__block__district__state=state_id)
    aggregator_data = aggregator_data.annotate(value=F('name_en')).values('user_id', 'value').distinct().order_by('value')
    aggregator_list = aggregator_data.annotate(id=F('user_id')).values('id', 'value')

    aggregator_dict = {'name':'Aggregator', 'data':list(aggregator_list)}

    crop_list = Crop.objects.annotate(value=F('crop_name')).values('id', 'value').order_by('value')
    crop_dict = {'name':'Crops', 'data':list(crop_list)}

    mandi_list = Mandi.objects.filter(district__state__country=country_id)
    if state_id != None:
        mandi_list = mandi_list.filter(district__state=state_id)
    mandi_list = mandi_list.annotate(value=F('mandi_name_en')).values('id', 'value').order_by('value')

    mandi_dict = {'name':'Mandi', 'data':list(mandi_list)}

    gaddidar_list = Gaddidar.objects.filter(mandi__district__state__country=country_id)
    if state_id != None:
        gaddidar_list = gaddidar_list.filter(mandi__district__state=state_id)
    gaddidar_list = gaddidar_list.annotate(value=F('gaddidar_name_en')).values('id', 'value').order_by('value')
    gaddidar_dict = {'name':'Gaddidar','data':list(gaddidar_list)}

    response_list.extend([aggregator_dict, crop_dict, mandi_dict, gaddidar_dict])
    data = json.dumps(response_list)
    return HttpResponse(data)

def get_global_filter(request) :
    country_list = Country.objects.annotate(value=F('country_name'), isSelected=F('is_visible'), tagName=Value('country_id', output_field=CharField())).values('id', 'value', 'isSelected', 'tagName')

    for obj in country_list:
        obj['dropDown'] = True
        state_list = State.objects.filter(country_id = obj['id']).annotate(value=F('state_name_en'), isSelected=F('is_visible'), parentId=F('country_id'), parentTag=Value('country_id', output_field=CharField()),\
         tagName=Value('state_id', output_field=CharField())).values('id', 'value', 'isSelected', 'parentId', 'parentTag', 'tagName')
        obj['dropDownData'] = list(state_list)
    data = json.dumps(list(country_list))
    return HttpResponse(data)
