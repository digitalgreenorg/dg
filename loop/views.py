import json
import xlsxwriter
from django.http import JsonResponse
from io import BytesIO

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max, F

from tastypie.models import ApiKey, create_api_key
from models import LoopUser, CombinedTransaction, Village, Crop, Mandi, Farmer, DayTransportation, Gaddidar, \
    Transporter, Language, CropLanguage, GaddidarCommission, GaddidarShareOutliers, AggregatorIncentive, \
    AggregatorShareOutliers, IncentiveParameter, IncentiveModel

from loop_data_log import get_latest_timestamp
from loop.payment_template import *
import inspect
# Create your views here.
HELPLINE_NUMBER = "09891256494"
ROLE_AGGREGATOR = 2


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
                 'user_id': loop_user[0].user_id,
                 'mode': loop_user[0].mode, 'helpline': HELPLINE_NUMBER, 'phone_number': loop_user[0].phone_number,
                 'user_name': username,
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


@csrf_exempt
def download_data_workbook(request):
    if request.method == 'POST':
        # this will prepare the data
        formatted_post_data = format_web_request(request)
        # this will get combined web data and various formats
        data_dict = get_combined_data_and_sheets_formats(formatted_post_data)
        # accessing basic variables
        workbook = data_dict.get('workbook')
        name_of_sheets = data_dict.get('name_of_sheets')
        heading_format = data_dict.get('heading_format')
        header_format = data_dict.get('header_format')
        row_format = data_dict.get('row_format')
        total_cell_format = data_dict.get('total_cell_format')
        excel_output = data_dict.get('excel_output')
        combined_data = data_dict.get('combined_data')
        # now the sheet processes
        workbook = excel_processing(workbook, name_of_sheets, heading_format, row_format, total_cell_format,
                                    header_format, combined_data)
        # final closing the working
        workbook.close()
        excel_output.seek(0)
        response = HttpResponse(excel_output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response

@csrf_exempt
def farmer_payments(request):
    body = json.loads(request.body)
    if request.method == 'PATCH':
        for bundle in body.get("objects"):
            try:
                mandi = Mandi.objects.get(id=bundle["mandi"]["online_id"])
                attempt = DayTransportation.objects.get(date=bundle["date"], user_created=bundle["user_created_id"],
                                                        mandi=mandi)
                attempt.farmer_share = bundle["amount"]
                attempt.comment = bundle["comment"]
                attempt.user_modified_id = bundle["user_modified_id"]
                # attempt.time_modified = get_latest_timestamp().timestamp
                attempt.save()
            except:
                return HttpResponse(json.dumps({'message': 'error'}), status=500)
    return HttpResponse(json.dumps({'message': 'successfully edited'}), status=200)

def filter_data(request):
    language = request.GET.get('language')
    aggregators = LoopUser.objects.filter(role=ROLE_AGGREGATOR).values('user__id', 'name', 'name_en', 'id')
    villages = Village.objects.all().values('id', 'village_name', 'village_name_en')
    crops = Crop.objects.all().values('id', 'crop_name')
    crops_lang = CropLanguage.objects.values('crop__id', 'crop_name')
    crops_language = [{'id': obj['crop__id'],
                       'crop_name': obj['crop_name']} for obj in crops_lang]
    mandis = Mandi.objects.all().values('id', 'mandi_name', 'mandi_name_en')
    gaddidars = Gaddidar.objects.all().values(
        'id', 'gaddidar_name', 'gaddidar_name_en')
    transporters = Transporter.objects.values('id', 'transporter_name')
    data_dict = {'transporters': list(transporters), 'aggregators': list(aggregators), 'villages': list(villages),
                 'crops': list(crops),
                 'mandis': list(mandis), 'gaddidars': list(gaddidars), 'croplanguage': list(crops_language)}
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
        'crop__crop_name', 'user_created__id', 'date').distinct().annotate(amount=Sum('amount'),
                                                                           quantity=Sum('quantity'))
    for crop_aggregator in crops_aggregators:
        user = LoopUser.objects.get(
            user_id=crop_aggregator['user_created__id'])
        crop_aggregator['user_name'] = user.name
    dates = CombinedTransaction.objects.filter(**filter_args).values_list(
        'date', flat=True).distinct().order_by('date').annotate(Count('farmer', distinct=True))
    dates_farmer_count = CombinedTransaction.objects.filter(**filter_args).values(
        'date').distinct().order_by('date').annotate(Count('farmer', distinct=True))
    chart_dict = {'dates': list(dates), 'crops': list(crops), 'transactions': list(transactions), 'farmer_count': list(
        dates_farmer_count), 'crops_aggregators': list(crops_aggregators),
                  'crops_aggregators_transactions': list(crops_aggregators_transactions)}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def total_static_data(request):
    total_volume = CombinedTransaction.objects.all(
    ).aggregate(Sum('quantity'), Sum('amount'))
    total_repeat_farmers = len(CombinedTransaction.objects.values(
        'farmer').annotate(farmer_count=Count('farmer')).exclude(farmer_count=1))
    total_farmers_reached = len(
        CombinedTransaction.objects.values('farmer').distinct())
    total_cluster_reached = len(LoopUser.objects.filter(role=ROLE_AGGREGATOR))
    total_transportation_cost = DayTransportation.objects.values('date', 'user_created__id', 'mandi__id').annotate(
        Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    gaddidar_share = gaddidar_contribution_for_totat_static_data()

    aggregator_incentive = aggregator_incentive_for_total_static_data()

    chart_dict = {'total_volume': total_volume, 'total_farmers_reached': total_farmers_reached,
                  'total_transportation_cost': list(total_transportation_cost),
                  'total_gaddidar_contribution': gaddidar_share, 'total_cluster_reached': total_cluster_reached,
                  'total_repeat_farmers': total_repeat_farmers, 'total_aggregator_incentive': aggregator_incentive}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def aggregator_incentive_for_total_static_data():
    aggregator_incentive_list = calculate_aggregator_incentive()
    total_aggregator_incentive = 0
    for entry in aggregator_incentive_list:
        total_aggregator_incentive += entry['amount']
    return total_aggregator_incentive


def calculate_aggregator_incentive(start_date=None, end_date=None, mandi_list=None, aggregator_list=None):
    if aggregator_list is not None:
        user_qset = LoopUser.objects.filter(user__in=aggregator_list).values_list('id', flat=True)
    else:
        user_qset = LoopUser.objects.values_list('id', flat=True)

    parameters_dictionary = {'aggregator__in': user_qset}
    parameters_dictionary_for_outliers = {
        'mandi__in': mandi_list, 'aggregator__user__in': aggregator_list}
    parameters_dictionary_for_ct = {'date__gte': start_date, 'date__lte': end_date,
                                    'mandi__in': mandi_list, 'user_created__id__in': aggregator_list}

    arguments_for_ct = {}
    arguments_for_aggregator_incentive = {}
    arguments_for_aggregator_incentive_outliers = {}

    for k, v in parameters_dictionary.items():
        if v:
            arguments_for_aggregator_incentive[k] = v

    for k, v in parameters_dictionary_for_ct.items():
        if v:
            arguments_for_ct[k] = v

    for k, v in parameters_dictionary_for_outliers.items():
        if v:
            arguments_for_aggregator_incentive_outliers[k] = v

    ai_queryset = AggregatorIncentive.objects.filter(
        **arguments_for_aggregator_incentive)

    aso_queryset = AggregatorShareOutliers.objects.filter(
        **arguments_for_aggregator_incentive_outliers)
    combined_ct_queryset = CombinedTransaction.objects.filter(**arguments_for_ct).values(
        'date', 'user_created_id', 'mandi','mandi__mandi_name_en').order_by('-date').annotate(Sum('quantity'), Sum('amount'),
                                                                       Count('farmer_id', distinct=True))
    result = []

    incentive_param_queryset = IncentiveParameter.objects.all()

    for CT in combined_ct_queryset:
        sum = 0.0
        comment = ""
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [aso.date for aso in aso_queryset.filter(mandi=CT['mandi'], aggregator=user.id)]:
            try:
                ai_list_set = ai_queryset.filter(start_date__lte=CT['date'], aggregator=user.id).order_by('-start_date')
                if (ai_list_set.count() > 0):
                    exec (ai_list_set[0].incentive_model.calculation_method)
                    paramter_list = inspect.getargspec(calculate_inc)[0]
                    for param in paramter_list:
                        param_to_apply = incentive_param_queryset.get(notation=param)
                        print param_to_apply.notation_equivalent
                        x = calculate_inc(CT[param_to_apply.notation_equivalent])
                    sum += x
            except Exception as e:
                print e
        else:
            try:
                aso_share_date_aggregator = aso_queryset.filter(
                    date=CT['date'], aggregator=user.id, mandi=CT['mandi']).values('amount', 'comment')
                if aso_share_date_aggregator.count():
                    sum += aso_share_date_aggregator[0]['amount']
                    comment = aso_share_date_aggregator[0]['comment']
            except AggregatorShareOutliers.DoesNotExist:
                pass
        result.append(
            {'date': CT['date'], 'user_created__id': CT['user_created_id'], 'mandi__name' : CT['mandi__mandi_name_en'], 'mandi__id': CT['mandi'], 'amount': round(sum,2), 'quantity__sum': round(CT['quantity__sum'],2), 'comment' : comment})
    return result


def gaddidar_contribution_for_totat_static_data():
    gaddidar_share_list = calculate_gaddidar_share(None, None, None, None)
    total_share = 0
    for entry in gaddidar_share_list:
        total_share += entry['amount']
    return total_share


def calculate_gaddidar_share(start_date, end_date, mandi_list, aggregator_list):
    parameters_dictionary = {'mandi__in': mandi_list}
    parameters_dictionary_for_outliers = {'aggregator__user__in': aggregator_list, 'mandi__in': mandi_list}
    parameters_dictionary_for_ct = {'user_created__id__in': aggregator_list, 'mandi__in': mandi_list,
                                    'date__gte': start_date, 'date__lte': end_date}

    arguments_for_ct = {}
    arguments_for_gaddidar_commision = {}
    arguments_for_gaddidar_outliers = {}

    for k, v in parameters_dictionary.items():
        if v:
            arguments_for_gaddidar_commision[k] = v

    for k, v in parameters_dictionary_for_ct.items():
        if v:
            arguments_for_ct[k] = v

    for k, v in parameters_dictionary_for_outliers.items():
        if v:
            arguments_for_gaddidar_outliers[k] = v

    gc_queryset = GaddidarCommission.objects.filter(
        **arguments_for_gaddidar_commision)
    gso_queryset = GaddidarShareOutliers.objects.filter(
        **arguments_for_gaddidar_outliers)
    combined_ct_queryset = CombinedTransaction.objects.filter(**arguments_for_ct).values(
        'date', 'user_created_id', 'gaddidar', 'mandi', 'gaddidar__discount_criteria').order_by('-date').annotate(
        Sum('quantity'), Sum('amount'))
    result = []
    # gso_list = [gso.date for gso in gso_queryset.filter(gaddidar=CT['gaddidar'], aggregator=user.id)]
    for CT in combined_ct_queryset:
        sum = 0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [gso.date for gso in gso_queryset.filter(gaddidar=CT['gaddidar'], aggregator=user.id)]:
            try:
                gc_list_set = gc_queryset.filter(start_date__lte=CT['date'], gaddidar=CT[
                    'gaddidar']).order_by('-start_date')
                if CT['gaddidar__discount_criteria'] == 0 and gc_list_set.count() > 0:
                    sum += CT['quantity__sum'] * \
                           gc_list_set[0].discount_percent
                elif gc_list_set.count() > 0:
                    sum += CT['amount__sum'] * gc_list_set[0].discount_percent
            except GaddidarCommission.DoesNotExist:
                pass
        else:
            try:
                gso_gaddidar_date_aggregator = gso_queryset.filter(
                    date=CT['date'], aggregator=user.id, gaddidar=CT['gaddidar']).values_list('amount', flat=True)
                if gso_gaddidar_date_aggregator.count():
                    sum += gso_gaddidar_date_aggregator[0]
            except GaddidarShareOutliers.DoesNotExist:
                pass
        result.append({'date': CT['date'], 'user_created__id': CT['user_created_id'], 'gaddidar__id': CT[
            'gaddidar'], 'mandi__id': CT['mandi'], 'amount': round(sum,2), 'quantity__sum': round(CT['quantity__sum'],2)})
    return result


def crop_language_data(request):
    crops = CropLanguage.objects.filter(language=request.GET.get('language'))
    data = json.dumps(crops)

    return HttpResponse(data)


def recent_graphs_data(request):
    stats = CombinedTransaction.objects.values('farmer__id', 'date', 'user_created__id').order_by(
        '-date').annotate(Sum('quantity'), Sum('amount'))
    transportation_cost = DayTransportation.objects.values('date', 'mandi__id', 'user_created__id').order_by(
        '-date').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))
    dates = CombinedTransaction.objects.values_list(
        'date', flat=True).distinct().order_by('-date')

    gaddidar_contribution = calculate_gaddidar_share(None, None, None, None)

    chart_dict = {'stats': list(stats), 'transportation_cost': list(
        transportation_cost), 'dates': list(dates), "gaddidar_contribution": gaddidar_contribution}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def data_for_drilldown_graphs(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    gaddidar_ids = request.GET.getlist('gaddidar_ids[]')
    filter_args = {}
    filter_transportation = {}
    filter_args_no_crops = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
        filter_args_no_crops["date__gte"] = start_date
        filter_transportation["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
        filter_args_no_crops["date__lte"] = end_date
        filter_transportation["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids

    filter_args_no_crops["user_created__id__in"] = aggregator_ids
    filter_args_no_crops["mandi__id__in"] = mandi_ids
    filter_args_no_crops["gaddidar__id__in"] = gaddidar_ids

    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids

    total_repeat_farmers = CombinedTransaction.objects.filter(
        **filter_args).values('user_created__id', 'farmer').annotate(farmer_count=Count('farmer'))
    aggregator_mandi = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'mandi__id').annotate(Sum('quantity'), Sum('amount'),
                                                  mandi__id__count=Count('date', distinct=True))
    aggregator_gaddidar = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'gaddidar__id').annotate(Sum('quantity'), Sum('amount'))

    mandi_gaddidar = CombinedTransaction.objects.filter(
        **filter_args).values('mandi__id', 'gaddidar__id').annotate(Sum('quantity'), Sum('amount'))
    mandi_crop = CombinedTransaction.objects.filter(
        **filter_args).values('mandi__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))

    transportation_cost_mandi = DayTransportation.objects.filter(**filter_transportation).values('date',
                                                                                                 'mandi__id',
                                                                                                 'user_created__id').annotate(
        Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    crop_prices = list(CombinedTransaction.objects.filter(
        **filter_args).values('crop__crop_name', 'crop__id').annotate(Min('price'), Max('price'),
                                                                      Count('farmer', distinct=True)))
    for crop_obj in crop_prices:
        try:
            crop = CropLanguage.objects.get(crop=crop_obj['crop__id'])
            crop_obj['crop__crop_name_en'] = crop.crop_name
        except CropLanguage.DoesNotExist:
            pass

    mandi_crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'mandi__id').annotate(Min('price'), Max('price'))

    gaddidar_contribution = calculate_gaddidar_share(
        start_date, end_date, mandi_ids, aggregator_ids)

    aggregator_incentive_cost = calculate_aggregator_incentive(start_date,end_date,mandi_ids,aggregator_ids)

    transactions_details_without_crops = CombinedTransaction.objects.filter(**filter_args_no_crops).values(
        'user_created__id', 'mandi__id').annotate(Sum('quantity'), Sum('amount'),
                                                  mandi__id__count=Count('date', distinct=True))

    chart_dict = {"total_repeat_farmers": list(total_repeat_farmers), "crop_prices": crop_prices,
                  'aggregator_mandi': list(aggregator_mandi), 'aggregator_gaddidar': list(aggregator_gaddidar),
                  'mandi_gaddidar': list(
                      mandi_gaddidar), 'mandi_crop': list(mandi_crop),
                  'transportation_cost_mandi': list(transportation_cost_mandi),
                  "mandi_crop_prices": list(mandi_crop_prices), "gaddidar_contribution": gaddidar_contribution,
                  "aggregator_incentive_cost":aggregator_incentive_cost,
                  "transactions_details_without_crops": list(transactions_details_without_crops)}
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
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids

    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids

    transport_data = DayTransportation.objects.filter(**filter_transportation).values(
        'date').order_by('date').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    aggregator_data = CombinedTransaction.objects.filter(
        **filter_args).values('date').order_by('date').annotate(Sum('quantity'), Sum('amount'))

    dates = CombinedTransaction.objects.filter(**filter_args).values(
        'date').distinct().order_by('date').annotate(Count('farmer', distinct=True))

    crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'date').annotate(Min('price'), Max('price'), Sum('quantity'), Sum('amount'))

    aggregator_incentive_cost = calculate_aggregator_incentive(start_date, end_date, mandi_ids, aggregator_ids)

    chart_dict = {'transport_data': list(transport_data), 'crop_prices': list(
        crop_prices), 'dates': list(dates), 'aggregator_data': list(aggregator_data), 'aggregator_incentive_cost' : aggregator_incentive_cost}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def calculate_gaddidar_share_payments(start_date, end_date):
    parameters_dictionary_for_ct = {
        'date__gte': start_date, 'date__lte': end_date}
    arguments_for_ct = {}
    for k, v in parameters_dictionary_for_ct.items():
        if v:
            arguments_for_ct[k] = v

    gc_queryset = GaddidarCommission.objects.all()
    gso_queryset = GaddidarShareOutliers.objects.all()
    combined_ct_queryset = CombinedTransaction.objects.filter(**arguments_for_ct).values(
        'date', 'user_created_id', 'gaddidar', 'gaddidar__gaddidar_name_en', 'mandi', 'mandi__mandi_name_en',
        'gaddidar__discount_criteria').order_by('-date').annotate(Sum('quantity'), Sum('amount'))
    result = []
    # gso_list = [gso.date for gso in gso_queryset]
    for CT in combined_ct_queryset:
        sum = 0
        comment = ""
        gc_discount = 0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [gso.date for gso in gso_queryset.filter(gaddidar=CT['gaddidar'], aggregator=user.id)]:
            try:
                gc_list_set = gc_queryset.filter(start_date__lte=CT['date'], gaddidar=CT[
                    'gaddidar']).order_by('-start_date')
                if CT['gaddidar__discount_criteria'] == 0 and gc_list_set.count() > 0:
                    sum += CT['quantity__sum'] * \
                           gc_list_set[0].discount_percent
                    gc_discount = sum / CT['quantity__sum']
                elif gc_list_set.count() > 0:
                    sum += CT['amount__sum'] * gc_list_set[0].discount_percent
                    gc_discount = sum / CT['amount__sum']

            except GaddidarCommission.DoesNotExist:
                pass
        else:
            try:
                gso_gaddidar_date_aggregator = gso_queryset.filter(
                    date=CT['date'], aggregator=user.id, gaddidar=CT['gaddidar']).values('amount', 'comment')
                if gso_gaddidar_date_aggregator.count():
                    sum += gso_gaddidar_date_aggregator[0]['amount']
                    comment = gso_gaddidar_date_aggregator[0]['comment']
                    if CT['gaddidar__discount_criteria'] == 0:
                        gc_discount = sum / CT['quantity__sum']
                    else:
                        gc_discount = sum / CT['amount__sum']
            except GaddidarShareOutliers.DoesNotExist:
                pass
        result.append({'date': CT['date'], 'user_created__id': CT['user_created_id'], 'gaddidar__name': CT[
            'gaddidar__gaddidar_name_en'], 'mandi__name': CT['mandi__mandi_name_en'], 'amount': round(sum,2),
                       'gaddidar_discount': round(gc_discount,3), 'comment': comment})
    return result


def payments(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date

    aggregator_data = CombinedTransaction.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en'), gaddidar__gaddidar_name=F('gaddidar__gaddidar_name_en')).values(
        'date', 'user_created__id', 'mandi__mandi_name', 'gaddidar__gaddidar_name','mandi__id','gaddidar__id', 'gaddidar__discount_criteria').order_by('date').annotate(Sum('quantity'), Sum('amount'))

    outlier_data = CombinedTransaction.objects.filter(
        **filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en')).values('date', 'user_created__id',
                                                                                    'mandi__mandi_name').order_by(
        'date').annotate(Sum('quantity'), Count('farmer', distinct=True)).annotate(
        gaddidar__commission__sum=Sum(F('gaddidar__commission') * F("quantity")))

    outlier_transport_data = DayTransportation.objects.filter(**filter_args).annotate(
        mandi__mandi_name=F('mandi__mandi_name_en')).values(
        'date', 'mandi__id', 'mandi__mandi_name', 'user_created__id').order_by('date').annotate(
        Sum('transportation_cost'),
        farmer_share__sum=Avg(
            'farmer_share'))
    outlier_daily_data = CombinedTransaction.objects.filter(**filter_args).annotate(
        mandi__mandi_name=F('mandi__mandi_name_en'), gaddidar__gaddidar_name=F('gaddidar__gaddidar_name_en')).values(
        'date',
        'user_created__id',
        'mandi__mandi_name',
        'farmer__name',
        'crop__crop_name',
        'gaddidar__commission',
        'price',
        'gaddidar__gaddidar_name').order_by(
        'date').annotate(Sum('quantity'))

    transportation_data = DayTransportation.objects.filter(**filter_args).annotate(
        mandi__mandi_name=F('mandi__mandi_name_en'),
        transportation_vehicle__vehicle__vehicle_name=F('transportation_vehicle__vehicle__vehicle_name_en')).values(
        'date', 'user_created__id', 'transportation_vehicle__vehicle__vehicle_name',
        "transportation_vehicle__transporter__transporter_name", 'transportation_vehicle__vehicle_number',
        'mandi__mandi_name', 'farmer_share', 'id', 'comment').order_by('date').annotate(Sum('transportation_cost'))

    gaddidar_data = calculate_gaddidar_share_payments(start_date, end_date)

    aggregator_incentive = calculate_aggregator_incentive(start_date,end_date)

    # aggregator_outlier = AggregatorShareOutliers.objects.annotate(user_created__id=F('aggregator__user_id'),
    #                                                               mandi__name=F('mandi__mandi_name_en')).values("date",
    #                                                                                                             "mandi__name",
    #                                                                                                             "amount",
    #                                                                                                             "comment",
    #                                                                                                             "user_created__id")
    chart_dict = {'outlier_daily_data': list(outlier_daily_data), 'outlier_data': list(outlier_data),
                  'outlier_transport_data': list(
                      outlier_transport_data), 'gaddidar_data': gaddidar_data, 'aggregator_data': list(aggregator_data),
                  'transportation_data': list(transportation_data), 'aggregator_incentive': aggregator_incentive}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)
