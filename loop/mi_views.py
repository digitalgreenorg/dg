import os
import json

import requests
from django.http import HttpResponse

from loop_ivr.outliers.removal import remove_crop_outliers
from loop_ivr.helper_function import run_query
from loop_ivr.utils.marketinfo import get_query

from mi_data_structure import *
from loop.models import *
import pandas as pd
from tastypie.models import ApiKey
from crop_price_structure import *

fileDir = os.path.dirname(os.path.realpath('__file__'))

def get_aggregator_mi_related_data(request):
    
    request_data = request.META.get('HTTP_AUTHORIZATION', '')
    username, apikey = request_data.split(':', 1)
    # Get User Id
    apikeyobj = ApiKey.objects.get(key=apikey)
    aggregator_id = [apikeyobj.user_id]
    agg_list = [4846, 4844, 4992, 5025]
    mandi_list = [134, 133, 152, 16, 150, 14, 5, 151, 188]
    agg_list_requested = list(set(aggregator_id) & set(agg_list))
    
    # Create Objects
    agg_data_obj = LoopUser.objects.filter(user__in=agg_list_requested).values('user', 'name_en')
    mandi_data_obj = Mandi.objects.filter(id__in=mandi_list).values('id', 'mandi_name_en')
    gaddidar_data_obj = Gaddidar.objects.filter(mandi__id__in=mandi_list)

    # Read CSV file and filter for requested Aggreagator
    filepath = os.path.join(fileDir, "/home/trionfo/Documents/dg/loop/utils/Transport Cost & Capacity Data - Sheet1.csv")
    print filepath
    transport_dataframe = pd.read_csv(filepath)
    transport_dataframe = transport_dataframe[transport_dataframe['Aggregator Id']==agg_list_requested[0]]

    # Store Json Result
    agg_res = []

    # Mandi Detail
    mandi_res = []    
    for mandiobj in mandi_data_obj:
        mandiobjdetail = MandiDetail(mandi_id=mandiobj['id'], mandi_name=mandiobj['mandi_name_en'], mandi_category='Chhoti Mandi',\
                    mandi_distance='590')
        gaddidar_obj= gaddidar_data_obj.filter(mandi__id=mandiobj['id']).values('id', 'gaddidar_name_en', 'gaddidar_phone')
        for gaddidarobj in gaddidar_obj:
            gaddidarobj = GaddidarDetail(gaddidar_id=gaddidarobj['id'], gaddidar_name=gaddidarobj['gaddidar_name_en'],\
                        gaddidar_phone_no=gaddidarobj['gaddidar_phone'])
            mandiobjdetail.gaddidar_list.append(gaddidarobj.__dict__)
        
        transport_dataframe_obj = transport_dataframe[transport_dataframe['Mandi Id'] == mandiobj['id']]
        for index, row in transport_dataframe_obj.iterrows():
            transportobj = TransportDetail(transport_id=row['Vehicle Id'], transport_name=row['Vehicle Name'], transport_cost=str(row['Cost']),\
                            transport_capacity=row['Capacity'])
            mandiobjdetail.transport_list.append(transportobj.__dict__)

        mandi_res.append(mandiobjdetail.__dict__)

    # Aggregator Details
    for aggobj in agg_data_obj:
        aggobj = AggregatorDetail(aggregator_id=aggobj['user'], aggregator_name=aggobj['name_en'])
        aggobj.mandi_list = mandi_res
        agg_res.append(aggobj.__dict__)

    data = json.dumps(agg_res)
    return HttpResponse(data)

def get_crop_prices(request):
    testing = 'Hi, want crop Prices?'
    data = json.dumps({"data": testing})
    cropobj = Crop.objects.values_list('id', flat=True)
    cropobj = map(int, cropobj)
    # Prepare data
    crop_list = tuple(cropobj)
    mandi_list = (134, 133, 152, 16, 150, 14, 5, 151, 188)

    query = get_query.query_for_rates(crop_list , mandi_list, date_range=3)
    
    result = run_query(query)
    dataframe = remove_crop_outliers(ct_data = result)

    print 'crop mandi date Av_Rate STD PriceMax PriceMin delta'
    df = dataframe.groupby(['Crop', 'Market_Real'])

    res = []
    for i, r in df:
        cropmandidata = CropMandiData(crop_id=i[0], mandi_id= i[1])
        for index, row in r.iterrows():
            crop, mandi, date, Av_Rate, STD, PriceMax, PriceMin = row['Crop'], row['Market_Real'], row['Date'], row['Av_Ratemean'], row['STDmean'], row['Pricemax'], row['Pricemin']
            delta = PriceMax - PriceMin
            priceobj = PriceDetails(date=str(date), std=round(STD, 2), min_price=round(PriceMin, 2), max_price=round(PriceMax, 2),\
                                delta=round(delta, 2), avg_price=round(Av_Rate, 2))
            cropmandidata.price_details.append(priceobj.__dict__)
        res.append(cropmandidata.__dict__)
    
    data = json.dumps(res)
    return HttpResponse(data)






# def getJSONObj(**kwargs):

#     aggobj = AggregatorDetail(aggregator_id=1, aggregator_name='Hello')
#     mandiobj = MandiDetail(mandi_id=1, mandi_name='Samastipur', mandi_category='Chhoti Mandi',\
#      mandi_distance='590')
#     transportobj = TransportDetail(transport_id=1, transport_name='Jugaad',  transport_cost=123,\
#      transport_capacity=1209)
#     gaddidarobj = GaddidarDetail(gaddidar_id=1, gaddidar_name='Gajodhar')

#     aggobj.mandi_list = [mandiobj.__dict__, mandiobj.__dict__]

#     mandiobj.transport_list = [transportobj.__dict__, ]
#     mandiobj.gaddidar_list = [gaddidarobj.__dict__, ]

#     return aggobj.__dict__


# def get_init_kwargs():
#     kwargs = {}
#     kwargs['aggregator_id'] = ''
#     kwargs['aggregator_name'] = ''
#     kwargs['mandi_id'] = ''
#     kwargs['mandi_name'] = ''
#     kwargs['mandi_category'] = ''
#     kwargs['mandi_distance'] = ''
#     kwargs['transport_id'] = ''
#     kwargs['transport_name'] = ''
#     kwargs['transport_cost'] = ''
#     kwargs['transport_capacity'] = ''
#     kwargs['gaddidar_id'] = ''
#     kwargs['gaddidar_name'] = ''
#     return kwargs
