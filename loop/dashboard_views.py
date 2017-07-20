from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Sum, Avg, Max, F

import pandas as pd
from loop.models import CombinedTransaction, Farmer, Crop, Mandi, Gaddidar, LoopUser
from loop.utils.loop_etl.group_myisam_data import *

def graph_data(request):
    chart_name = request.GET['chartName']
    country_id = 1
    start_date = 20170401
    end_date = 20170601
    if chart_name == 'volFarmerTS':
        result = vol_amount_farmer(country_id, start_date, end_date)
        return JsonResponse(result)
    elif chart_name == 'cpkSpkTS':
        result = cpk_spk_timeseries(country_id, start_date, end_date)
        return JsonResponse(result)
    elif chart_name == 'cummulativeCount':
        result = cumm_vol_farmer(country_id)
        return JsonResponse(result)
    else:
        return JsonResponse({"result":"success"})

def cpk_spk_timeseries(country_id, start_date, end_date):
    cpk_spk = cpk_spk_ts(country_id, start_date, end_date)
    return cpk_spk

def vol_amount_farmer(country_id, start_date, end_date):
    v_a_f_ts = volume_amount_farmers_ts(country_id, start_date, end_date)
    return v_a_f_ts

def volume_aggregator(request):
    volume_per_aggregator = get_volume_aggregator(1)
    return JsonResponse(volume_per_aggregator)

def cumm_vol_farmer(country_id):
    c_v_f = get_cummulative_vol_farmer(country_id)
    return c_v_f
