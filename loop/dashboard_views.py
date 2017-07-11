from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Sum, Avg, Max, F

import pandas as pd
from loop.models import CombinedTransaction, Farmer, Crop, Mandi, Gaddidar, LoopUser
from loop.utils.loop_etl.group_myisam_data import *

def volume_aggregator(request):
    volume_per_aggregator = get_volume_aggregator(1)
    return JsonResponse(volume_per_aggregator)
