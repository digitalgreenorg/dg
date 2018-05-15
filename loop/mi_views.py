import requests
from django.http import HttpResponse
import json

def get_aggregator_mi_related_data(request):
    testing = 'Hi Testing'
    print request.GET.get('aggId')
    data = json.dumps({'data': testing})
    return HttpResponse(data)

def get_crop_prices(request):
    testing = 'Hi, want crop Prices?'
    data = json.dumps({"data": testing})
    return HttpResponse(data)
