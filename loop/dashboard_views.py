from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Sum, Avg, Max, F

import pandas as pd
from loop.models import CombinedTransaction, Farmer, Crop, Mandi, Gaddidar, LoopUser
from loop.utils.loop_etl.group_myisam_data import *

def graph_data(request):
    chart_name = request.GET['chartName']
    print chart_name
    if chart_name == 'volFarmerTS':
        result = vol_amount_farmer()
        return JsonResponse(result)
    else:
        return JsonResponse({"result":"success"})

def volume_aggregator(request):
    volume_per_aggregator = get_volume_aggregator(1)
    return JsonResponse(volume_per_aggregator)

def vol_amount_farmer():
    v_a_f_ts = volume_amount_farmers_ts(1,'20170401','20170601')
    return v_a_f_ts
