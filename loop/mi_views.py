import json

import requests
from django.http import HttpResponse

from mi_data_structure import *
from loop.models import *

def get_aggregator_mi_related_data(request):
    agg_list = [4846, 4844, 4992, 5025]
    mandi_list = [134, 133, 152, 16, 150, 14, 5, 151, 188]
    agg_data_obj = LoopUser.objects.filter(user__in=agg_list).values('user', 'name_en')
    mandi_data_obj = Mandi.objects.filter(id__in=mandi_list).values('id', 'mandi_name_en')
    gaddidar_data_obj = Gaddidar.objects.filter(mandi__id__in=mandi_list)
    transport_data_obj = Vehicle.objects.values('id', 'name')
    # Store Json Result
    agg_res = []
    # Mandi Detail
    mandi_res = []
    for mandiobj in mandi_data_obj:
        mandiobjdetail = MandiDetail(mandi_id=mandiobj['id'], mandi_name=mandiobj['mandi_name_en'], mandi_category='Chhoti Mandi',\
                    mandi_distance='590')
        gaddidar_obj= gaddidar_data_obj.filter(mandi__id=mandiobj['id']).values('id', 'gaddidar_name_en')
        for gaddidarobj in gaddidar_obj:
            gaddidarobj = GaddidarDetail(gaddidar_id=gaddidarobj['id'], gaddidar_name=gaddidarobj['gaddidar_name_en'])
            mandiobjdetail.gaddidar_list.append(gaddidarobj.__dict__)

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