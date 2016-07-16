import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max

from tastypie.models import ApiKey, create_api_key
from models import LoopUser, CombinedTransaction, Village, Crop, Mandi, Farmer, DayTransportation, Gaddidar

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
    print request
    return render_to_response(request, 'loop_base.html')


def dashboard(request):
    return render(request, 'app_dashboards/loop_dashboard.html')


def second_loop_page(request):
    return render(request, 'app_dashboards/second_loop_page.html')


def filter_data(request):
    aggregators = LoopUser.objects.values('user__id', 'name')
    villages = Village.objects.values('id', 'village_name')
    crops = Crop.objects.values('id', 'crop_name')
    mandis = Mandi.objects.values('id', 'mandi_name')
    gaddidars = Gaddidar.objects.values('id', 'gaddidar_name')
    data_dict = {'aggregators': list(aggregators), 'villages': list(villages), 'crops': list(crops),
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
    total_volume = CombinedTransaction.objects.all().aggregate(Sum('quantity'), Sum('amount'))
    total_volume_for_transport = CombinedTransaction.objects.filter(date__gte="2016-06-01").aggregate(Sum('quantity'))
    total_repeat_farmers = len(CombinedTransaction.objects.values('farmer').annotate(farmer_count=Count('farmer')).exclude(farmer_count=1))
    total_farmers_reached = len(CombinedTransaction.objects.values('farmer').distinct())
    total_cluster_reached = len(LoopUser.objects.all())
    total_transportation_cost = DayTransportation.objects.filter(date__gte="2016-06-01").aggregate(
        Sum('transportation_cost'), Sum('farmer_share'))

    chart_dict = {'total_volume': total_volume, 'total_farmers_reached': total_farmers_reached,
                  'total_transportation_cost': total_transportation_cost, 'total_cluster_reached':total_cluster_reached, 'total_volume_for_transport':total_volume_for_transport, 'total_repeat_farmers':total_repeat_farmers}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def recent_graphs_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date

    stats = CombinedTransaction.objects.filter(**filter_args).values('farmer__id', 'date').order_by(
        '-date').annotate(Sum('quantity'), Sum('amount'))
    aggregators = LoopUser.objects.all().values('name', 'user_id')
    mandis = Mandi.objects.all().values('id', 'mandi_name')
    transportation_cost = DayTransportation.objects.filter(**filter_args).values(
                                                                 'date').order_by('-date').annotate(Sum('transportation_cost'), Sum('farmer_share'))
    dates = CombinedTransaction.objects.values_list(
        'date', flat=True).distinct().order_by('-date')
    crops = Crop.objects.all().values('id', 'crop_name')

    chart_dict = {'stats': list(stats), 'aggregators': list(aggregators), 'mandis': list(
        mandis), 'transportation_cost': list(transportation_cost), 'dates': list(dates), 'crops': list(crops)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def farmer_count_aggregator_wise(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    farmers_count = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id').annotate(Count('farmer', distinct=True))

    chart_dict = {'farmers_count': list(farmers_count)}
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
    filter_transportation["mandi__id__in"]=mandi_ids

    total_repeat_farmers = CombinedTransaction.objects.filter(**filter_args).values('user_created__id','farmer').annotate(farmer_count=Count('farmer'))
    # stats = CombinedTransaction.objects.filter(**filter_args).values('user_created__id', 'mandi__id', 'crop__crop_name', 'date', 'farmer__id', 'quantity', 'amount', 'gaddidar__id').order_by('-date')
    aggregator_mandi = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'mandi__id').annotate(Sum('quantity'), Sum('amount'),mandi__in__count=Count('date',distinct=True))
    aggregator_gaddidar = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'gaddidar__id', 'date', 'gaddidar__mandi__id').annotate(Sum('quantity'), Sum('amount'))
    aggregator_crop = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))
    mandi_gaddidar = CombinedTransaction.objects.filter(**filter_args).values('mandi__id', 'gaddidar__id').annotate(Sum('quantity'), Sum('amount'))
    mandi_crop = CombinedTransaction.objects.filter(
        **filter_args).values('mandi__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))
    gaddidar_crop = CombinedTransaction.objects.filter(
        **filter_args).values('gaddidar__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))
    transportation_cost_mandi = DayTransportation.objects.filter(**filter_transportation).values(
        'date','mandi__id','user_created__id').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__crop_name').annotate(Min('price'), Max('price'), Count('farmer', distinct=True))




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


    chart_dict = {"total_repeat_farmers": list(total_repeat_farmers),"crop_prices": list(crop_prices),'aggregator_mandi': list(aggregator_mandi), 'aggregator_gaddidar': list(aggregator_gaddidar), 'aggregator_crop': list(
        aggregator_crop), 'mandi_gaddidar':list(mandi_gaddidar), 'mandi_crop': list(mandi_crop), 'gaddidar_crop': list(gaddidar_crop), 'transportation_cost_mandi': list(transportation_cost_mandi)}
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
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids

    farmer = CombinedTransaction.objects.filter(**filter_args).values('date').annotate(Count('farmer'))

    mandi_data = CombinedTransaction.objects.filter(**filter_args).values('mandi__id','date').order_by('date').annotate(Sum('quantity'))

    aggregator_data = CombinedTransaction.objects.filter(**filter_args).values('user_created__id','date').order_by('date').annotate(Sum('quantity'), Sum('amount'))

    crop_data = CombinedTransaction.objects.filter(**filter_args).values('crop__id','date').order_by('date').annotate(Sum('quantity'))

    gaddidar_data = CombinedTransaction.objects.filter(**filter_args).values('gaddidar__id','date').order_by('date').annotate(Sum('quantity'))

    dates = CombinedTransaction.objects.filter(**filter_args).values_list(
        'date', flat=True).distinct().order_by('date')

    crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'date').annotate(Min('price'), Avg('price') ,Max('price'), Sum('quantity'), Sum('amount'))

    chart_dict = {'crop_prices':list(crop_prices), 'farmer': list(farmer), 'mandi_data':list(mandi_data), 'dates':list(dates), 'aggregator_data':list(aggregator_data), 'crop_data':list(crop_data), 'gaddidar_data':list(gaddidar_data)}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)

def data_for_time_chart(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    village_ids = request.GET.getlist('village_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    gaddidar_ids = request.GET.getlist('gaddidar_ids[]')
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["farmer__village__id__in"] = village_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids

    total_data = CombinedTransaction.objects.filter(**filter_args).values('date').order_by('date').annotate(Sum('quantity'), Sum('amount'))
    dates = CombinedTransaction.objects.filter(**filter_args).values_list(
        'date', flat=True).distinct().order_by('date')
    chart_dict = {'total_data':list(total_data), 'dates':list(dates)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)



def payments(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date

    aggregator_data = CombinedTransaction.objects.filter(**filter_args).values('date', 'user_created__id', 'mandi__mandi_name').annotate(Sum('quantity'), Count('farmer'))

    transportation_data = DayTransportation.objects.filter(**filter_args).values('date', 'user_created__id', 'transportation_vehicle__vehicle_number', 'mandi__mandi_name').annotate(Sum('transportation_cost'))

    gaddidar_data = CombinedTransaction.objects.filter(**filter_args).values('date', 'user_created__id', 'gaddidar__id', 'gaddidar__commission').annotate(Sum('quantity'))

    chart_dict = {'gaddidar_data':list(gaddidar_data) ,'aggregator_data':list(aggregator_data), 'transportation_data':list(transportation_data)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)
