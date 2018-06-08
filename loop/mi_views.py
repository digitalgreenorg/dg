import os
import json

import requests
import pandas as pd

from django.http import HttpResponse

from loop_ivr.outliers.removal import remove_crop_outliers
from loop_ivr.helper_function import run_query
from loop_ivr.utils.marketinfo import get_query
from loop.models import *
from tastypie.models import ApiKey

from mi_data_structure import *
from crop_price_structure import *
from loop.utils.mi_pilot_var import mandi_list, agg_list, transport_detail_filepath

fileDir = os.path.dirname(os.path.realpath('__file__'))

def get_aggregator_mi_related_data(request):
    
    agg_list_requested = is_authenticated(request)

    if agg_list_requested :
        
        # Create Objects
        agg_data_obj = LoopUser.objects.filter(user__in=agg_list_requested).values('user', 'name_en', 'preferred_language_id')

        # get Dict from Single Obj
        agg_obj = agg_data_obj[0]
        preferred_lang_suffix = '_en' if agg_obj['preferred_language_id'] == 2 else ''

        # Mandi Name in preferred lang of aggregator
        mandi_name_label = 'mandi_name' + preferred_lang_suffix
        mandi_data_obj = Mandi.objects.filter(id__in=mandi_list).values('id', mandi_name_label)

        #Gaddidar Name in preferred lang of aggregator
        gaddidar_name_label = 'gaddidar_name' + preferred_lang_suffix
        gaddidar_data_obj = Gaddidar.objects.filter(mandi__id__in=mandi_list)

        # Read CSV file and filter for requested Aggreagator
        filepath = fileDir + transport_detail_filepath
        transport_dataframe = pd.read_csv(filepath)
        transport_dataframe = transport_dataframe[transport_dataframe['Aggregator Id']==agg_list_requested[0]]

        # Store Json Result
        agg_res = []

        # Mandi Detail
        mandi_res = []    
        for mandiobj in mandi_data_obj:
            mandiobjdetail = MandiDetail(mandi_id=mandiobj['id'], mandi_name=mandiobj[mandi_name_label], mandi_category='Chhoti Mandi',\
                        mandi_distance='590')
            gaddidar_obj= gaddidar_data_obj.filter(mandi__id=mandiobj['id']).values('id', gaddidar_name_label, 'gaddidar_phone')
            for gaddidarobj in gaddidar_obj:
                gaddidarobj = GaddidarDetail(gaddidar_id=gaddidarobj['id'], gaddidar_name=gaddidarobj[gaddidar_name_label],\
                            gaddidar_phone_no=gaddidarobj['gaddidar_phone'])
                mandiobjdetail.gaddidar_list.append(gaddidarobj.__dict__)
            
            transport_dataframe_obj = transport_dataframe[transport_dataframe['Mandi Id'] == mandiobj['id']]
            for index, row in transport_dataframe_obj.iterrows():
                transportobj = TransportDetail(transport_id=row['Vehicle Id'], transport_name=row['Vehicle Name'], transport_cost=str(row['Cost']),\
                                transport_capacity=row['Capacity'])

                mandiobjdetail.distance = row['Mandi Distance'] 
                mandiobjdetail.category = row['Mandi Category']
                mandiobjdetail.transport_list.append(transportobj.__dict__)

            mandi_res.append(mandiobjdetail.__dict__)

        # Aggregator Details
        for aggobj in agg_data_obj:
            aggobj = AggregatorDetail(aggregator_id=aggobj['user'], aggregator_name=aggobj['name_en'])
            aggobj.mandi_list = mandi_res
            agg_res.append(aggobj.__dict__)

        data = json.dumps(agg_res)
        return HttpResponse(data)
    else :
        return HttpResponse(status=401)
    

def get_crop_prices(request):

    agg_list_requested = is_authenticated(request)
    
    if agg_list_requested :
        # Handling Request Params
        kwargs = read_params(request)

        cropobj = Crop.objects.values_list('id', flat=True)
        cropobj = map(int, cropobj)
        # Prepare data
        crop_list = tuple(cropobj)

        query = get_query.query_for_rates(crop_list , mandi_list, date_range=kwargs['day_limit'])
        
        result = run_query(query)
        dataframe = remove_crop_outliers(ct_data = result)

        # Grouping Raw Data to Crop & Mandi wise.
        df = dataframe.groupby(['Crop', 'Market_Real'])

        # Creation of JSON
        res = []
        for i, r in df:
            # Assigning min date
            latest_price_date = pd.Timestamp('2015-01-01')
            cropmandidata = CropMandiData(crop_id=i[0], mandi_id= i[1])
            for index, row in r.iterrows():
                crop, mandi, date, Av_Rate, STD, PriceMax, PriceMin = row['Crop'], row['Market_Real'], row['Date'], row['Av_Ratemean'], row['STDmean'], row['Pricemax'], row['Pricemin']
                delta = PriceMax - PriceMin
                latest_price_date = max(latest_price_date, date)
                priceobj = PriceDetails(date=str(date), std=round(STD, 2), min_price=round(PriceMin, 2), max_price=round(PriceMax, 2),\
                                    delta=round(delta, 2), avg_price=round(Av_Rate, 2))
                cropmandidata.price_details.append(priceobj.__dict__)
            cropmandidata.latest_price_date = str(latest_price_date)
            res.append(cropmandidata.__dict__)
        
        data = json.dumps(res)
        return HttpResponse(data)
    else:
        return HttpResponse(status=401)

def read_params(request):
    kwargs = {}
    
    kwargs['day_limit'] = int(request.GET.get('day_limit', 3))
    kwargs['start_date'] = request.GET.get('start_date', None)
    kwargs['end_date'] = request.GET.get('end_date', None)
    kwargs['crop_id'] = tuple(request.GET.getlist('crop_id', None))
    kwargs['mandi_id'] = tuple(request.GET.getlist('mandi_id', None))
    kwargs['range'] = request.GET.get('range', None)
    kwargs['absolute'] = request.GET.get('absolute', None)
    
    return kwargs


def is_authenticated(request):

    try:
        # Mobile App Authentication
        request_data = request.META.get('HTTP_AUTHORIZATION', '')
        username, apikey = request_data.split(':', 1)
        # Get User Id
        apikeyobj = ApiKey.objects.get(key=apikey)
        aggregator_id = [apikeyobj.user_id]
        agg_list_requested = list(set(aggregator_id) & set(agg_list))
    except Exception:
        agg_list_requested = []
    
    return agg_list_requested
