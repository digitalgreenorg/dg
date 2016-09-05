import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max, F

from tastypie.models import ApiKey, create_api_key
from models import LoopUser, CombinedTransaction, Village, Crop, Mandi, Farmer, DayTransportation, Gaddidar, Transporter, Language, Croplanguage, GaddidarCommission, GaddidarShareOutliers

from loop_data_log import get_latest_timestamp

# Create your views here.
HELPLINE_NUMBER = "09891256494"


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        loop_user = LoopUser.objects.filter(user=user)
        if user is not None and user.is_active and loop_user.count() > 0:
            auth.login(request, user)
            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                api_key.save()
            log_object = get_latest_timestamp()
            return HttpResponse(json.dumps(
                {'key': api_key.key, 'timestamp': str(log_object.timestamp), 'full_name': loop_user[0].name,
                 'mode': loop_user[0].mode, 'helpline': HELPLINE_NUMBER, 'phone_number': loop_user[0].phone_number,
                 'district': loop_user[0].village.block.district.id}))
        else:
            return HttpResponse("0", status=401)
    else:
        return HttpResponse("0", status=403)
    return HttpResponse("0", status=400)


def home(request):
    return render_to_response(request, 'loop_base.html')


def dashboard(request):
    return render(request, 'app_dashboards/loop_dashboard.html')


def filter_data(request):
    aggregators = LoopUser.objects.all().values('user__id','name','name_en')
    villages = Village.objects.all().values('id','village_name','village_name_en')
    crops = Crop.objects.extra(select={'crop_name':'crop_name_en'}).values('id', 'crop_name')
    mandis = Mandi.objects.all().values('id','mandi_name','mandi_name_en')
    gaddidars = Gaddidar.objects.all().values('id','gaddidar_name','gaddidar_name_en')
    transporters = Transporter.objects.values('id', 'transporter_name')
    data_dict = {'transporters': list(transporters), 'aggregators': list(aggregators), 'villages': list(villages), 'crops': list(crops),
                 'mandis': list(mandis), 'gaddidars': list(gaddidars)}
    data = json.dumps(data_dict)
    return HttpResponse(data)


def village_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    village_ids = request.GET.getlist('village_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["farmer__village__id__in"] = village_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    transactions = CombinedTransaction.objects.filter(**filter_args).values(
        'farmer__village__village_name').distinct().annotate(Count('farmer', distinct=True), Sum('amount'),
                                                             Sum('quantity'), Count(
                                                                 'date', distinct=True),
                                                             total_farmers=Count('farmer'))
    data = json.dumps(list(transactions))
    return HttpResponse(data)


def aggregator_wise_data(request):

    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    village_ids = request.GET.getlist('village_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["farmer__village__id__in"] = village_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    transactions = list(
        CombinedTransaction.objects.filter(**filter_args).values('user_created__id').distinct().annotate(
            Count('farmer', distinct=True), Sum('amount'), Sum(
                'quantity'), Count('date', distinct=True),
            total_farmers=Count('farmer')))
    for i in transactions:
        user = LoopUser.objects.get(user_id=i['user_created__id'])
        i['user_name'] = user.name
    data = json.dumps(transactions)
    return HttpResponse(data)


def crop_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    village_ids = request.GET.getlist('village_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["farmer__village__id__in"] = village_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    # crop wise data here
    crops = CombinedTransaction.objects.filter(
        **filter_args).values_list('crop__crop_name', flat=True).distinct()

    transactions = CombinedTransaction.objects.filter(**filter_args).values(
        'crop__crop_name', 'date').distinct().annotate(Sum('amount'), Sum('quantity'))
    # crop and aggregator wise data
    crops_aggregators = CombinedTransaction.objects.filter(**filter_args).values(
        'crop__crop_name', 'user_created__id').distinct().annotate(amount=Sum('amount'), quantity=Sum('quantity'))
    crops_aggregators_transactions = CombinedTransaction.objects.filter(**filter_args).values(
        'crop__crop_name', 'user_created__id', 'date').distinct().annotate(amount=Sum('amount'), quantity=Sum('quantity'))
    for crop_aggregator in crops_aggregators:
        user = LoopUser.objects.get(
            user_id=crop_aggregator['user_created__id'])
        crop_aggregator['user_name'] = user.name
    dates = CombinedTransaction.objects.filter(**filter_args).values_list(
        'date', flat=True).distinct().order_by('date').annotate(Count('farmer', distinct=True))
    dates_farmer_count = CombinedTransaction.objects.filter(**filter_args).values(
        'date').distinct().order_by('date').annotate(Count('farmer', distinct=True))
    chart_dict = {'dates': list(dates), 'crops': list(crops), 'transactions': list(transactions), 'farmer_count': list(
        dates_farmer_count), 'crops_aggregators': list(crops_aggregators), 'crops_aggregators_transactions': list(crops_aggregators_transactions)}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def total_static_data(request):
    total_volume = CombinedTransaction.objects.all(
    ).aggregate(Sum('quantity'), Sum('amount'))
    # remove total_volume_for_transport after entering past data and make
    # changes in js accordingly (filter for june dates)
    # total_volume_for_transport = CombinedTransaction.objects.aggregate(Sum('quantity'))
    total_repeat_farmers = len(CombinedTransaction.objects.values(
        'farmer').annotate(farmer_count=Count('farmer')).exclude(farmer_count=1))
    total_farmers_reached = len(
        CombinedTransaction.objects.values('farmer').distinct())
    total_cluster_reached = len(LoopUser.objects.all())

    # remove date from filter
    # filter(date__gte="2016-06-01")
    total_transportation_cost = DayTransportation.objects.values('date', 'user_created__id', 'mandi__id').annotate(
        Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    gaddidar_share = gaddidar_contribution_for_totat_static_data()

    chart_dict = {'total_volume': total_volume, 'total_farmers_reached': total_farmers_reached,
                  'total_transportation_cost': list(total_transportation_cost), 'total_gaddidar_contribution': gaddidar_share, 'total_cluster_reached': total_cluster_reached, 'total_repeat_farmers': total_repeat_farmers}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)

def gaddidar_contribution_for_totat_static_data():
    gaddidar_share_list = calculate_gaddidar_share(None, None, None, None)
    total_share = 0
    for entry in gaddidar_share_list:
        total_share += entry['amount']
    return total_share

def calculate_gaddidar_share(start_date, end_date, mandi_list, aggregator_list):

    parameters_dictionary = {'mandi__in' : mandi_list}
    parameters_dictionary_for_outliers = {'mandi__in':mandi_list, 'aggregator__user__in':aggregator_list}
    parameters_dictionary_for_ct = {'date__gte' : start_date, 'date__lte':end_date, 'mandi__in' : mandi_list, 'user_created__id__in':aggregator_list}

    arguments_for_ct = {}
    arguments_for_gaddidar_commision={}
    arguments_for_gaddidar_outliers ={}

    for k, v in parameters_dictionary.items():
        if v:
            arguments_for_gaddidar_commision[k]=v

    for k, v in parameters_dictionary_for_ct.items():
        if v:
            arguments_for_ct[k] = v

    for k, v in parameters_dictionary_for_outliers.items():
        if v:
            arguments_for_gaddidar_outliers[k]=v

    gc_queryset = GaddidarCommission.objects.filter(**arguments_for_gaddidar_commision)
    gso_queryset = GaddidarShareOutliers.objects.filter(**arguments_for_gaddidar_outliers)
    combined_ct_queryset = CombinedTransaction.objects.filter(**arguments_for_ct).values(
        'date', 'user_created_id', 'gaddidar', 'mandi' ,'gaddidar__discount_criteria').annotate(Sum('quantity'), Sum('amount'))
    result = []
    for CT in combined_ct_queryset:
        sum=0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [x.date for x in gso_queryset]:
            try:
                gc_list_set = gc_queryset.filter(start_date__lte=CT['date'], gaddidar=CT[
                                                 'gaddidar']).order_by('-start_date')
                if CT['gaddidar__discount_criteria'] == 0 and len(gc_list_set) > 0:
                    sum += CT['quantity__sum'] * \
                        gc_list_set[0].discount_percent
                elif len(gc_list_set) > 0:
                    sum += CT['amount__sum'] * gc_list_set[0].discount_percent
            except GaddidarCommission.DoesNotExist:
                pass
        else:
            try:
                gso_gaddidar_date_aggregator = gso_queryset.filter(
                    date=CT['date'], aggregator=user.id,gaddidar=CT['gaddidar']).values_list('amount', flat=True)
                if len(gso_gaddidar_date_aggregator):
                    sum += gso_gaddidar_date_aggregator[0]
            except GaddidarShareOutliers.DoesNotExist:
                pass
        result.append({'date':CT['date'], 'user_created__id':CT['user_created_id'], 'gaddidar__id':CT['gaddidar'], 'mandi__id':CT['mandi'], 'amount':sum})
    return result

def crop_language_data(request):
    crops = Croplanguage.objects.filter(language=request.GET.get('language'))
    data = json.dumps(crops)
    
    return HttpResponse(data)

def recent_graphs_data(request):

    stats = CombinedTransaction.objects.values('farmer__id', 'date', 'user_created__id').order_by(
        '-date').annotate(Sum('quantity'), Sum('amount'))
    aggregators = LoopUser.objects.all().values('name','user_id','name_en')
    mandis = Mandi.objects.all().values('id','mandi_name','mandi_name_en')
    transportation_cost = DayTransportation.objects.values('date').order_by(
        '-date').annotate(Sum('transportation_cost'), Sum('farmer_share'))
    dates = CombinedTransaction.objects.values_list(
        'date', flat=True).distinct().order_by('-date')
    # crops = Crop.objects.all().extra(
        # select={'crop_name': 'crop_name_en'}).values('id', 'crop_name')

    chart_dict = {'stats': list(stats), 'transportation_cost': list(transportation_cost), 'dates': list(dates)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)

def new_aggregator_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    gaddidar_ids = request.GET.getlist('gaddidar_ids[]')
    filter_args = {}
    filter_transportation = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
        filter_transportation["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
        filter_transportation["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids
    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids

    total_repeat_farmers = CombinedTransaction.objects.filter(
        **filter_args).values('user_created__id', 'farmer').annotate(farmer_count=Count('farmer'))
    aggregator_mandi = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'mandi__id').annotate(Sum('quantity'), Sum('amount'), mandi__id__count=Count('date', distinct=True))
    aggregator_gaddidar = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'gaddidar__id').annotate(Sum('quantity'), Sum('amount'))

    mandi_gaddidar = CombinedTransaction.objects.filter(
        **filter_args).values('mandi__id', 'gaddidar__id').annotate(Sum('quantity'), Sum('amount'))
    mandi_crop = CombinedTransaction.objects.filter(
        **filter_args).values('mandi__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))

    transportation_cost_mandi = DayTransportation.objects.filter(**filter_transportation).values('date',
        'mandi__id', 'user_created__id').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    crop_prices = CombinedTransaction.objects.filter(
        **filter_args).annotate(crop__crop_name=F('crop__crop_name_en')).values('crop__crop_name','crop__id').annotate(Min('price'), Max('price'), Count('farmer', distinct=True))
    #TODO:mandi_crop_prices
    mandi_crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'mandi__id').annotate(Min('price'), Max('price'))

    gaddidar_contribution = calculate_gaddidar_share(start_date, end_date, mandi_ids,aggregator_ids)

    # stats = CombinedTransaction.objects.filter(**filter_args).values('user_created__id', 'mandi__id', 'crop__crop_name', 'date', 'farmer__id', 'quantity', 'amount', 'gaddidar__id').order_by('-date')
    # aggregator_crop = CombinedTransaction.objects.filter(**filter_args).values(
    #     'user_created__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))
    # gaddidar_crop = CombinedTransaction.objects.filter(
    #     **filter_args).values('gaddidar__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))

    # visits={}
    #
    # aggregators_mandis = CombinedTransaction.objects.filter(**filter_args).values('user_created__id', 'date', 'mandi__id').distinct()
    #
    # for aggregator in  aggregator_ids:
    #     for mandi in mandi_ids:
    #         visits[(int(aggregator),int(mandi))] = 0
    #
    # for agg_man in aggregators_mandis:
    #     for mandi in mandi_ids:
    #         for aggregator in aggregator_ids:
    #             if agg_man['mandi__id'] == int(mandi) and agg_man['user_created__id'] == int(aggregator):
    #                 visits[(int(aggregator), int(mandi))]+=1
    #
    # for agg_man in aggregator_mandi:
    #     for visit in visits:
    #         if (agg_man['user_created__id'], agg_man['mandi__id']) == visit:
    #             agg_man['mandi__id__count'] = visits[(agg_man['user_created__id'], agg_man['mandi__id'])]

    chart_dict = {"total_repeat_farmers": list(total_repeat_farmers), "crop_prices": list(crop_prices), 'aggregator_mandi': list(aggregator_mandi), 'aggregator_gaddidar': list(aggregator_gaddidar), 'mandi_gaddidar': list(mandi_gaddidar), 'mandi_crop': list(mandi_crop),  'transportation_cost_mandi': list(transportation_cost_mandi), "mandi_crop_prices": list(mandi_crop_prices), "gaddidar_contribution":gaddidar_contribution}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def data_for_line_graph(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    gaddidar_ids = request.GET.getlist('gaddidar_ids[]')
    filter_args = {}
    filter_transportation = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
        filter_transportation["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
        filter_transportation["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids

    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids

    transport_data = DayTransportation.objects.filter(**filter_transportation).values(
        'date').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    aggregator_data = CombinedTransaction.objects.filter(**filter_args).values('date').order_by('date').annotate(Sum('quantity'), Sum('amount'))

    # crop_data = CombinedTransaction.objects.filter(
        # **filter_args).values('crop__id', 'date').order_by('date').annotate(Sum('quantity'))

    # gaddidar_data = CombinedTransaction.objects.filter(
        # **filter_args).values('gaddidar__id', 'date').order_by('date').annotate(Sum('quantity'))
    # mandi_data = CombinedTransaction.objects.filter(
        # **filter_args).values('mandi__id', 'date').order_by('date').annotate(Sum('quantity'))
    # farmer = CombinedTransaction.objects.filter(
        # **filter_args).values('date').annotate(Count('farmer'))

    dates = CombinedTransaction.objects.filter(**filter_args).values(
        'date').distinct().order_by('date').annotate(Count('farmer'))

    crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'date').annotate(Min('price'), Max('price'), Sum('quantity'), Sum('amount'))

    chart_dict = {'transport_data': list(transport_data), 'crop_prices': list(crop_prices), 'dates': list(dates), 'aggregator_data': list(aggregator_data)}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


# def data_for_time_chart(request):
#     start_date = request.GET['start_date']
#     end_date = request.GET['end_date']
#     aggregator_ids = request.GET.getlist('aggregator_ids[]')
#     village_ids = request.GET.getlist('village_ids[]')
#     crop_ids = request.GET.getlist('crop_ids[]')
#     mandi_ids = request.GET.getlist('mandi_ids[]')
#     gaddidar_ids = request.GET.getlist('gaddidar_ids[]')
#     filter_args = {}
#     if (start_date != ""):
#         filter_args["date__gte"] = start_date
#     if (end_date != ""):
#         filter_args["date__lte"] = end_date
#     filter_args["user_created__id__in"] = aggregator_ids
#     filter_args["farmer__village__id__in"] = village_ids
#     filter_args["crop__id__in"] = crop_ids
#     filter_args["mandi__id__in"] = mandi_ids
#     filter_args["gaddidar__id__in"] = gaddidar_ids
#
#     total_data = CombinedTransaction.objects.filter(
#         **filter_args).values('date').order_by('date').annotate(Sum('quantity'), Sum('amount'))
#     dates = CombinedTransaction.objects.filter(**filter_args).values_list(
#         'date', flat=True).distinct().order_by('date')
#     chart_dict = {'total_data': list(total_data), 'dates': list(dates)}
#     data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
#     return HttpResponse(data)


def payments(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date

    aggregator_data = CombinedTransaction.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en'), gaddidar__gaddidar_name=F('gaddidar__gaddidar_name_en')).values(
        'date', 'user_created__id', 'mandi__mandi_name', 'gaddidar__gaddidar_name', 'gaddidar__commission').annotate(Sum('quantity'), Count('farmer',distinct=True))

    outlier_data = CombinedTransaction.objects.filter(
        **filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en')).values('date', 'user_created__id', 'mandi__mandi_name').annotate(Sum('quantity'), Count('farmer', distinct=True)).annotate(gaddidar__commission__sum=Sum(F('gaddidar__commission') * F("quantity")))

    outlier_transport_data = DayTransportation.objects.filter(**filter_args).values(
        'date', 'mandi__id', 'user_created__id').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    outlier_daily_data = CombinedTransaction.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en'), gaddidar__gaddidar_name=F('gaddidar__gaddidar_name_en'), crop__crop_name=F('crop__crop_name_en')).values('date', 'user_created__id', 'mandi__mandi_name',
                                                                                                                                                                                                                                          'farmer__name', 'crop__crop_name', 'gaddidar__commission', 'price', 'gaddidar__gaddidar_name').annotate(Sum('quantity'))

    transportation_data = DayTransportation.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en'), transportation_vehicle__vehicle__vehicle_name=F('transportation_vehicle__vehicle__vehicle_name_en')).values(
        'date', 'user_created__id', 'transportation_vehicle__vehicle__vehicle_name', "transportation_vehicle__transporter__transporter_name", 'transportation_vehicle__vehicle_number', 'mandi__mandi_name', 'farmer_share').annotate(Sum('transportation_cost'))

    gaddidar_data = CombinedTransaction.objects.filter(**filter_args).values(
        'date', 'user_created__id', 'mandi__id', 'gaddidar__id', 'gaddidar__commission').annotate(Sum('quantity'))

    chart_dict = {'outlier_daily_data': list(outlier_daily_data), 'outlier_data': list(outlier_data), 'outlier_transport_data': list(outlier_transport_data),  'gaddidar_data': list(
        gaddidar_data), 'aggregator_data': list(aggregator_data), 'transportation_data': list(transportation_data)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)
