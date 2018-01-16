import os
import json
import xlsxwriter
import requests
from django.http import JsonResponse, HttpResponseBadRequest
from io import BytesIO
from threading import Thread

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max, F
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext

from tastypie.models import ApiKey, create_api_key
from models import LoopUser, CombinedTransaction, Village, Crop, Mandi, Farmer, DayTransportation, Gaddidar, \
    Transporter, Language, CropLanguage, GaddidarCommission, GaddidarShareOutliers, AggregatorIncentive, \
    AggregatorShareOutliers, IncentiveParameter, IncentiveModel, HelplineExpert, HelplineIncoming, HelplineOutgoing, \
    HelplineCallLog, HelplineSmsLog, LoopUserAssignedVillage, BroadcastAudience, AdminUser, District

import loop.utils.send_log.loop_data_log as loop_log
import loop.utils.send_log.loop_admin_log as admin_log
from loop.payment_template import *
from loop.utils.ivr_helpline.helpline_data import helpline_data, BROADCAST_S3_AUDIO_URL, BROADCAST_PENDING_TIME, \
    HELPLINE_LOG_FILE
from loop.forms import BroadcastForm, BroadcastTestForm
import csv
import time
import datetime
from datetime import timedelta
from pytz import timezone
import inspect

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, NO_EXPERT_GREETING_APP_ID, \
    OFF_HOURS_GREETING_APP_ID, \
    OFF_HOURS_VOICEMAIL_APP_ID, MEDIA_ROOT, BROADCAST_APP_ID, PERMISSION_DENIED_URL

from loop.helpline_view import write_log, save_call_log, save_sms_log, get_status, get_info_through_api, \
    update_incoming_acknowledge_user, make_helpline_call, send_helpline_sms, connect_to_app, \
    fetch_info_of_incoming_call, \
    update_incoming_obj, send_acknowledge, send_voicemail, start_broadcast, connect_to_broadcast, save_broadcast_audio, \
    redirect_to_broadcast, save_farmer_file
from loop.utils.loop_etl.group_myisam_data import get_data_from_myisam
from constants.constants import ROLE_CHOICE_AGGREGATOR, MODEL_TYPES_DAILY_PAY, DISCOUNT_CRITERIA_VOLUME, \
    INCORRECT_FARMER_PHONE_MODEL_APPLY_DATE

import pandas as pd
from training.management.databases.utility import *
from loop.management.commands.get_sql_queries import *
import MySQLdb
from dg.settings import DATABASES
# Create your views here.
HELPLINE_NUMBER = "01139595953"


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        loop_user = LoopUser.objects.filter(user=user)
        reg_token = None
        version = "0"
        if 'registration' in request.POST and request.POST['registration']:
            reg_token = request.POST['registration']
            LoopUser.objects.filter(registration=reg_token).update(registration=None)

        if 'version' in request.POST and request.POST['version']:
            version = request.POST['version']

        loop_user.update(registration=reg_token, version=version)

        if user is not None and user.is_active and loop_user.count() > 0:
            auth.login(request, user)

            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                api_key.save()
            log_object = loop_log.get_latest_timestamp()
            return HttpResponse(json.dumps(
                {'key': api_key.key, 'timestamp': str(log_object.timestamp), 'full_name': loop_user[0].name,
                 'user_id': loop_user[0].user_id,
                 'mode': loop_user[0].mode, 'phone_number': loop_user[0].phone_number, 'user_name': username,
                 'district': loop_user[0].village.block.district.id, 'days_count': loop_user[0].days_count,
                 'helpline': loop_user[0].village.block.district.state.helpline_number,
                 'crop_add': loop_user[0].village.block.district.state.crop_add,
                 'phone_digits': loop_user[0].village.block.district.state.phone_digit,
                 'phone_start': loop_user[0].village.block.district.state.phone_start,
                 'preferred_language': loop_user[0].preferred_language.notation,
                 'registration': loop_user[0].registration,
                 'country': loop_user[0].village.block.district.state.country.country_name, 'role': loop_user[0].role,
                 'farmer_phone_mandatory': loop_user[0].farmer_phone_mandatory,
                 'state': loop_user[0].village.block.district.state.state_name,
                 'show_farmer_share': loop_user[0].show_farmer_share,
                 'percent_farmer_share': loop_user[0].percent_farmer_share,
                 'server_sms': loop_user[0].village.block.district.state.server_sms}))
        else:
            admin_user = AdminUser.objects.filter(user=user)
            if user is not None and user.is_active and admin_user.count() > 0:
                auth.login(request, user)
                try:
                    api_key = ApiKey.objects.get(user=user)
                except ApiKey.DoesNotExist:
                    api_key = ApiKey.objects.create(user=user)
                    api_key.save()
                log_object = admin_log.get_latest_timestamp()
                return HttpResponse(json.dumps(
                    {'key': api_key.key, 'timestamp': str(log_object.timestamp), 'full_name': admin_user[0].name,
                     'user_id': admin_user[0].user_id,
                     'phone_number': admin_user[0].phone_number, 'user_name': username,
                     'state': admin_user[0].state.id,
                     'helpline': admin_user[0].state.helpline_number,
                     'phone_digits': admin_user[0].state.phone_digit,
                     'phone_start': admin_user[0].state.phone_start,
                     'preferred_language': admin_user[0].preferred_language.notation}))

                # return HttpResponse("0", status=401)
    else:
        return HttpResponse("0", status=403)
    return HttpResponse("0", status=400)


def home(request):
    return render_to_response(request, 'loop_base.html')


def dashboard(request):
    return render(request, 'analytics/dist/loop/index.html')
    # return render(request, 'app_dashboards/loop_dashboard.html')


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
        heading_of_sheets = data_dict.get('heading_of_sheets')
        heading_format = data_dict.get('heading_format')
        header_format = data_dict.get('header_format')
        row_format = data_dict.get('row_format')
        total_cell_format = data_dict.get('total_cell_format')
        excel_output = data_dict.get('excel_output')
        combined_data = data_dict.get('combined_data')
        combined_header = data_dict.get('combined_header')
        sheet_header = data_dict.get('sheet_header')
        sheet_footer = data_dict.get('sheet_footer')
        # now the sheet processes
        workbook = excel_processing(workbook, name_of_sheets, heading_of_sheets, heading_format,
                                    row_format, total_cell_format, header_format, combined_data, combined_header,
                                    sheet_header, sheet_footer)
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
                loop_user = LoopUser.objects.get(id=bundle["aggregator"]["online_id"])
                user = User.objects.get(id=loop_user.user_id)
                attempt = DayTransportation.objects.filter(date=bundle["date"], user_created=user, mandi=mandi)
                attempt.update(farmer_share=bundle["amount"])
                attempt.update(farmer_share_comment=bundle["comment"])
                attempt.update(user_modified_id=bundle["user_modified_id"])
                # attempt.time_modified = get_latest_timestamp().timestamp
            except:
                return HttpResponse(json.dumps({'message': 'error'}), status=500)
    return HttpResponse(json.dumps({'message': 'successfully edited'}), status=200)


def filter_data(request):
    language = request.GET.get('language')
    country_id = request.GET.get('country_id')
    state_id = request.GET.get('state_id')

    if (int(state_id) < 0):
        # country filter
        aggregators = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR,
                                              village__block__district__state__country=country_id).values('user__id',
                                                                                                          'name',
                                                                                                          'name_en',
                                                                                                          'id',
                                                                                                          'village__block__district__state__state_name_en',
                                                                                                          'village__block__district__state__country__country_name')
        mandis = Mandi.objects.filter(district__state__country=country_id).values('id', 'mandi_name', 'mandi_name_en')
        gaddidars = Gaddidar.objects.filter(mandi__district__state__country=country_id).values(
            'id', 'gaddidar_name', 'gaddidar_name_en')
    elif (int(state_id) > 0):
        # state filter
        aggregators = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR,
                                              village__block__district__state=state_id).values('user__id', 'name',
                                                                                               'name_en', 'id',
                                                                                               'village__block__district__state__state_name_en',
                                                                                               'village__block__district__state__country__country_name')
        mandis = Mandi.objects.filter(district__state=state_id).values('id', 'mandi_name', 'mandi_name_en')
        gaddidars = Gaddidar.objects.filter(mandi__district__state=state_id).values(
            'id', 'gaddidar_name', 'gaddidar_name_en')

    # villages = Village.objects.all().values('id', 'village_name', 'village_name_en')
    crops = Crop.objects.all().values('id', 'crop_name')
    crops_lang = CropLanguage.objects.values('crop_id', 'crop_name', 'language_id')
    crops_language = dict()
    for obj in crops_lang:
        if obj['language_id'] not in crops_language:
            crops_language[obj['language_id']] = list()
        crops_language[obj['language_id']].append({'id': obj['crop_id'],
                                                   'crop_name': obj['crop_name']})

    # transporters = Transporter.objects.values('id', 'transporter_name')
    data_dict = {'aggregators': list(aggregators), 'crops': list(crops),
                 'mandis': list(mandis), 'gaddidars': list(gaddidars), 'croplanguage': crops_language}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def admin_assigned_loopusers_data(request):
    user_id = request.GET.get('user_id')
    admin_user = AdminUser.objects.get(user__id = user_id)
    aggregators = admin_user.assigned_loopusers.all().values('user__id', 'name', 'name_en', 'id', 'village__block__district__state__state_name_en', 'village__block__district__state__country__country_name')
    data_dict = {'aggregators': list(aggregators)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def districts_for_state(request):
    state = request.GET.get('state')
    districts = District.objects.filter(state__state_name_en=state).values('id', 'district_name_en')
    data_dict = {'districts': list(districts)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def aggregator_data_for_districts(request):
    district_ids = request.GET.getlist('district_ids[]')
    aggregators = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR, village__block__district__in=district_ids).values('user__id', 'name', 'name_en', 'id', 'village__block__district__state__state_name_en', 'village__block__district__state__country__country_name')
    data_dict = {'aggregators': list(aggregators)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def jsonify(data):
    if isinstance(data, dict):
        json_data = dict()
        for key, value in data.items():
            if isinstance(value, list):  # for lists
                for i, item in enumerate(value):
                    value[i] = jsonify(value[i])
            if isinstance(value, unicode):
                value = value.encode("utf-8")
            if isinstance(value, dict):  # for nested lists
                value = jsonify(value)
            if type(value).__module__ == 'numpy':  # if value is numpy.*: > to python list
                value = value.tolist()
            json_data[str(key)] = value
        return json_data

    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[str(i)] = jsonify(data[i])
        return data

    elif type(data).__module__ == 'numpy':
        data = data.tolist()
        return data

    else:
        return data


def total_static_data(request):
    country_id = request.GET['country_id']  # To be fetched from request
    state_id = request.GET['state_id']
    if (int(state_id) < 0):
        # Only country filter
        total_farmers_reached = CombinedTransaction.objects.filter(mandi__district__state__country=country_id).values(
            'farmer').distinct().count()
        total_cluster_reached = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR,
                                                        village__block__district__state__country=country_id).count()
    elif (int(state_id) > 0):
        # state filter
        total_farmers_reached = CombinedTransaction.objects.filter(mandi__district__state=state_id).values(
            'farmer').distinct().count()
        total_cluster_reached = LoopUser.objects.filter(role=ROLE_CHOICE_AGGREGATOR,
                                                        village__block__district__state=state_id).count()

    aggregated_result, cum_vol_farmer = get_data_from_myisam(1, country_id, state_id)

    chart_dict = {'total_farmers_reached': total_farmers_reached,
                  'total_cluster_reached': total_cluster_reached,
                  'aggregated_result': aggregated_result}
    data = json.dumps(jsonify(chart_dict), cls=DjangoJSONEncoder)
    return HttpResponse(data)


def calculate_inc_default(V):
    return 0.25 * V


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
        'date', 'user_created_id', 'mandi', 'mandi__mandi_name_en').order_by('-date').annotate(Sum('quantity'),
                                                                                               Sum('amount'),
                                                                                               Count('farmer_id',
                                                                                                     distinct=True))

    # Checking if we need to apply incorrect farmer phone model on payment data
    date_start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if date_start >= INCORRECT_FARMER_PHONE_MODEL_APPLY_DATE:
        combined_ct_queryset = combined_ct_queryset.filter(date__gte=F('farmer__correct_phone_date'))

    result = []
    daily_pay_list = []

    incentive_param_queryset = IncentiveParameter.objects.all()

    for CT in combined_ct_queryset:
        amount_sum = 0.0
        comment = ""
        user = LoopUser.objects.get(user_id=CT['user_created_id'])

        ai_list_set = ai_queryset.filter(start_date__lte=CT['date'], aggregator=user.id).order_by('-start_date')
        if ai_list_set and ai_list_set[0].model_type == MODEL_TYPES_DAILY_PAY:
            # SEPARATE OUT ALL DAILY PAY CASES
            exec (ai_list_set[0].incentive_model.calculation_method)
            amount_sum = calculate_inc()
            daily_pay_list.append({'date': CT['date'], 'user_created__id': CT['user_created_id'],
                                   'mandi__name': CT['mandi__mandi_name_en'], 'mandi__id': CT['mandi'],
                                   'amount': amount_sum, 'quantity__sum': round(CT['quantity__sum'], 2),
                                   'comment': comment, 'aggregator_id': user.id})
            continue
        elif CT['date'] not in [aso.date for aso in aso_queryset.filter(mandi=CT['mandi'], aggregator=user.id)]:
            # IF NOT A CASE OF OUTLIER, GET LATEST START DATE AND COMPUTE ACCORDINGLY
            try:
                if ai_list_set.count() > 0:
                    exec (ai_list_set[0].incentive_model.calculation_method)
                    paramter_list = inspect.getargspec(calculate_inc)[0]
                    for param in paramter_list:
                        param_to_apply = incentive_param_queryset.get(notation=param)
                        amount_sum += calculate_inc(CT[param_to_apply.notation_equivalent])
                else:
                    amount_sum += calculate_inc_default(CT['quantity__sum'])
            except Exception:
                pass
        else:
            # HANDLE OUTLIERS FOR ALL MODELS EXCEPT DAILY PAY
            try:
                aso_share_date_aggregator = aso_queryset.filter(
                    date=CT['date'], aggregator=user.id, mandi=CT['mandi']).values('amount', 'comment')
                if aso_share_date_aggregator.count():
                    amount_sum += aso_share_date_aggregator[0]['amount']
                    comment = aso_share_date_aggregator[0]['comment']
            except AggregatorShareOutliers.DoesNotExist:
                pass
        result.append(
            {'date': CT['date'], 'user_created__id': CT['user_created_id'], 'mandi__name': CT['mandi__mandi_name_en'],
             'mandi__id': CT['mandi'], 'amount': round(amount_sum, 2), 'quantity__sum': round(CT['quantity__sum'], 2),
             'comment': comment})

    try:
        daily_pay_df = pd.DataFrame(daily_pay_list)
        daily_pay_mandi_count = daily_pay_df.groupby(['date', 'user_created__id']).agg(
            {'mandi__id': 'count'}).reset_index()
        daily_pay_mandi_count.rename(columns={"mandi__id": "mandi__count"}, inplace=True)
        daily_pay_df = pd.merge(daily_pay_df, daily_pay_mandi_count, on=['date', 'user_created__id'], how='left')
        daily_pay_df['amount'] = daily_pay_df['amount'] / daily_pay_df['mandi__count']

        for index, row in daily_pay_df.iterrows():
            outlier = aso_queryset.filter(date=row['date'], aggregator=row['aggregator_id'],
                                          mandi=row['mandi__id']).values('amount', 'comment')
            if outlier.count():
                daily_pay_df.loc[index, 'amount'] = outlier[0]['amount']
                daily_pay_df.loc[index, 'comment'] = outlier[0]['comment']

        daily_pay_df.drop(['mandi__count', 'aggregator_id'], axis=1, inplace=True)
        daily_pay_df = daily_pay_df.round({'amount': 2})

        daily_pay = daily_pay_df.to_dict(orient='records')

        result.extend(daily_pay)
    except Exception:
        pass
    return result


def crop_language_data(request):
    crops = CropLanguage.objects.filter(language=request.GET.get('language'))
    data = json.dumps(crops)

    return HttpResponse(data)


# def recent_graphs_data(request):
# country_id = request.GET['country_id'] #To be fetched from request
#     aggregated_result, cummulative_vol_farmer = get_data_from_myisam(0, country_id)

#     chart_dict = {'aggregated_result': aggregated_result, 'cummulative_vol_farmer': cummulative_vol_farmer}
#     data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
#     return HttpResponse(data)


def data_for_drilldown_graphs(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('a_id[]')
    crop_ids = request.GET.getlist('c_id[]')
    mandi_ids = request.GET.getlist('m_id[]')
    gaddidar_ids = request.GET.getlist('g_id[]')
    country_id = request.GET['country_id']  #To be fetched from request
    state_id = request.GET['state_id']

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
    filter_args["mandi__district__state__country"] = country_id

    filter_args_no_crops["user_created__id__in"] = aggregator_ids
    filter_args_no_crops["mandi__id__in"] = mandi_ids
    filter_args_no_crops["gaddidar__id__in"] = gaddidar_ids
    filter_args_no_crops["mandi__district__state__country"] = country_id

    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids
    filter_transportation["mandi__district__state__country"] = country_id
    if (int(state_id) > 0):
        #set state filter also
        filter_args["mandi__district__state"] = state_id
        filter_args_no_crops["mandi__district__state"] = state_id
        filter_transportation["mandi__district__state"] = state_id

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

    crop_language_data = CropLanguage.objects.values('crop_id', 'crop_name', 'language_id')
    language_wise_crop_name = dict()
    for crop in crop_language_data:
        if crop['language_id'] not in language_wise_crop_name:
            language_wise_crop_name[crop['language_id']] = dict()
        language_wise_crop_name[crop['language_id']][crop['crop_id']] = crop['crop_name']
    for crop_obj in crop_prices:
        # For Hindi Language
        if crop_obj['crop__id'] in language_wise_crop_name[1]:
            crop_obj['crop__crop_name_hi'] = language_wise_crop_name[1][crop_obj['crop__id']]
        else:
            crop_obj['crop__crop_name_hi'] = crop_obj['crop__crop_name']
        # For Bangla Language
        if crop_obj['crop__id'] in language_wise_crop_name[3]:
            crop_obj['crop__crop_name_bn'] = language_wise_crop_name[3][crop_obj['crop__id']]
        else:
            crop_obj['crop__crop_name_bn'] = crop_obj['crop__crop_name']
        # For Marathi Language
        if crop_obj['crop__id'] in language_wise_crop_name[4]:
            crop_obj['crop__crop_name_mr'] = language_wise_crop_name[4][crop_obj['crop__id']]
        else:
            crop_obj['crop__crop_name_mr'] = crop_obj['crop__crop_name']

    mandi_crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'mandi__id').annotate(Min('price'), Max('price'))

    gaddidar_contribution = calculate_gaddidar_share_payments(
        start_date, end_date, mandi_ids, aggregator_ids)

    aggregator_incentive_cost = calculate_aggregator_incentive(start_date, end_date, mandi_ids, aggregator_ids)

    transactions_details_without_crops = CombinedTransaction.objects.filter(**filter_args_no_crops).values(
        'user_created__id', 'mandi__id').annotate(Sum('quantity'), Sum('amount'),
                                                  mandi__id__count=Count('date', distinct=True))

    chart_dict = {"total_repeat_farmers": list(total_repeat_farmers), "crop_prices": crop_prices,
                  'aggregator_mandi': list(aggregator_mandi), 'aggregator_gaddidar': list(aggregator_gaddidar),
                  'mandi_gaddidar': list(
                      mandi_gaddidar), 'mandi_crop': list(mandi_crop),
                  'transportation_cost_mandi': list(transportation_cost_mandi),
                  "mandi_crop_prices": list(mandi_crop_prices), "gaddidar_contribution": gaddidar_contribution,
                  "aggregator_incentive_cost": aggregator_incentive_cost,
                  "transactions_details_without_crops": list(transactions_details_without_crops)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def data_for_line_graph(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('a_id[]')
    crop_ids = request.GET.getlist('c_id[]')
    mandi_ids = request.GET.getlist('m_id[]')
    gaddidar_ids = request.GET.getlist('g_id[]')
    country_id = request.GET['country_id']  #To be fetched from request
    state_id = request.GET['state_id']
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
    filter_args["mandi__district__state__country"] = country_id

    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids
    filter_transportation["mandi__district__state__country"] = country_id

    if (int(state_id) > 0):
        filter_args["mandi__district__state"] = state_id
        filter_transportation["mandi__district__state"] = state_id

    transport_data = DayTransportation.objects.filter(**filter_transportation).values(
        'date').order_by('date').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    aggregator_data = CombinedTransaction.objects.filter(
        **filter_args).values('date').order_by('date').annotate(Sum('quantity'), Sum('amount'))

    dates = CombinedTransaction.objects.filter(**filter_args).values(
        'date').distinct().order_by('date').annotate(Count('farmer', distinct=True))

    crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'date').annotate(Min('price'), Max('price'), Sum('quantity'), Sum('amount'))

    # aggregator_incentive_cost = calculate_aggregator_incentive(start_date, end_date, mandi_ids, aggregator_ids)

    chart_dict = {'transport_data': list(transport_data), 'crop_prices': list(
        crop_prices), 'dates': list(dates), 'aggregator_data': list(aggregator_data)}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def calculate_gaddidar_share_payments(start_date, end_date, mandi_list=None, aggregator_list=None):
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

    gc_queryset = GaddidarCommission.objects.filter(**arguments_for_gaddidar_commision)
    gso_queryset = GaddidarShareOutliers.objects.filter(**arguments_for_gaddidar_outliers)
    combined_ct_queryset = CombinedTransaction.objects.filter(**arguments_for_ct).values(
        'date', 'user_created_id', 'gaddidar', 'gaddidar__gaddidar_name_en', 'mandi', 'mandi__mandi_name_en',
        'gaddidar__discount_criteria').order_by('-date').annotate(Sum('quantity'), Sum('amount'))
    result = []

    # gso_list = [gso.date for gso in gso_queryset]
    for CT in combined_ct_queryset:
        amount_sum = 0
        comment = ""
        gc_discount = 0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [gso.date for gso in gso_queryset.filter(gaddidar=CT['gaddidar'], aggregator=user.id)]:
            try:
                gc_list_set = gc_queryset.filter(start_date__lte=CT['date'], gaddidar=CT[
                    'gaddidar']).order_by('-start_date')
                if CT['gaddidar__discount_criteria'] == DISCOUNT_CRITERIA_VOLUME and gc_list_set.count() > 0:
                    amount_sum += CT['quantity__sum'] * \
                                  gc_list_set[0].discount_percent
                    gc_discount = amount_sum / CT['quantity__sum']
                elif gc_list_set.count() > 0:
                    amount_sum += CT['amount__sum'] * gc_list_set[0].discount_percent
                    gc_discount = amount_sum / CT['amount__sum']

            except GaddidarCommission.DoesNotExist:
                pass
        else:
            try:
                gso_gaddidar_date_aggregator = gso_queryset.filter(
                    date=CT['date'], aggregator=user.id, gaddidar=CT['gaddidar']).values('amount', 'comment')
                if gso_gaddidar_date_aggregator.count():
                    amount_sum += gso_gaddidar_date_aggregator[0]['amount']
                    comment = gso_gaddidar_date_aggregator[0]['comment']
                    if CT['gaddidar__discount_criteria'] == DISCOUNT_CRITERIA_VOLUME:
                        gc_discount = amount_sum / CT['quantity__sum']
                    else:
                        gc_discount = amount_sum / CT['amount__sum']
            except GaddidarShareOutliers.DoesNotExist:
                pass
        result.append({'date': CT['date'], 'user_created__id': CT['user_created_id'], 'gaddidar__id': CT[
            'gaddidar'], 'mandi__id': CT['mandi'], 'gaddidar__name': CT[
            'gaddidar__gaddidar_name_en'], 'mandi__name': CT['mandi__mandi_name_en'], 'amount': round(amount_sum, 2),
                       'gaddidar_discount': round(gc_discount, 3), 'comment': comment,
                       'quantity__sum': round(CT['quantity__sum'], 2)})
    return result


def payments(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_id = request.GET['aggregator_id']
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    if (aggregator_id != ""):
        filter_args["user_created__id"] = aggregator_id

    aggregator_data = CombinedTransaction.objects.filter(**filter_args).annotate(
        mandi__mandi_name=F('mandi__mandi_name_en'), gaddidar__gaddidar_name=F('gaddidar__gaddidar_name_en')).values(
        'date', 'user_created__id', 'mandi__mandi_name', 'gaddidar__gaddidar_name', 'mandi__id', 'gaddidar__id',
        'gaddidar__discount_criteria').order_by('date').annotate(Sum('quantity'), Sum('amount'))

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
        'transportation_vehicle__transporter__transporter_phone',
        'mandi__mandi_name', 'farmer_share', 'id', 'farmer_share_comment', 'transportation_cost_comment', 'mandi__id',
        'transportation_vehicle__id', 'timestamp').order_by('date').annotate(Sum('transportation_cost'))

    gaddidar_data = calculate_gaddidar_share_payments(start_date, end_date, None, [aggregator_id])

    aggregator_incentive = calculate_aggregator_incentive(start_date, end_date, None, [aggregator_id])

    chart_dict = {'outlier_daily_data': list(outlier_daily_data), 'outlier_data': list(outlier_data),
                  'outlier_transport_data': list(
                      outlier_transport_data), 'gaddidar_data': gaddidar_data, 'aggregator_data': list(aggregator_data),
                  'transportation_data': list(transportation_data), 'aggregator_incentive': aggregator_incentive}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


@login_required()
@user_passes_test(
    lambda u: u.groups.filter(name='Loop Payment').count() > 0 and AdminUser.objects.filter(user_id=u.id).count() > 0,
    login_url=PERMISSION_DENIED_URL)
def dashboard_payments(request):
    if request.method == 'GET':
        context = RequestContext(request)
        user = request.user
        try:
            api_key = ApiKey.objects.get(user=user)
        except ApiKey.DoesNotExist:
            api_key = ApiKey.objects.create(user=user)
            api_key.save()
        admin_user = AdminUser.objects.get(user = user)
        login_data = dict()
        login_data['user_name'] = user.username
        login_data['user_id'] = user.id
        login_data['key'] = api_key.key
        login_data['state'] = admin_user.state
        return render_to_response('app_dashboards/loop_dashboard_payment.html', login_data, context_instance=context)
    else:
        return HttpResponse(status=404)


def helpline_incoming(request):
    if request.method == 'GET':
        call_id, farmer_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        save_call_log(call_id, farmer_number, dg_number, 0, incoming_time)
        # Check if Any broadcast is pending for this number
        # If yes then redirect user to pending broadcast for this misscall.
        # Behaviour of helpline will be normal if no pending broadcast.
        farmer_number_possibilities = [farmer_number, '0' + farmer_number, farmer_number.lstrip('0'),
                                       '91' + farmer_number.lstrip('0'), '+91' + farmer_number.lstrip('0')]
        # check if any broadcast pending after this time period.
        time_period = (
            datetime.datetime.now(timezone('Asia/Kolkata')) - timedelta(days=BROADCAST_PENDING_TIME)).replace(
            tzinfo=None)
        # Check if a pending (0) or DND-faild (2) broadcast exist.
        if BroadcastAudience.objects.filter(to_number__in=farmer_number_possibilities, status__in=[0, 2],
                                            start_time__gte=time_period).exists():
            # Create thread for redirect helpline flow to play broadcast.
            Thread(target=redirect_to_broadcast, args=[farmer_number, dg_number]).start()
            return HttpResponse(status=200)
        # If no pending broadcast, then normal helpline flow.
        incoming_call_obj = HelplineIncoming.objects.filter(from_number=farmer_number, call_status=0).order_by('-id')
        # If No pending call with this number
        if len(incoming_call_obj) == 0:
            incoming_call_obj = HelplineIncoming(call_id=call_id, from_number=farmer_number, to_number=dg_number,
                                                 incoming_time=incoming_time, last_incoming_time=incoming_time)
            try:
                incoming_call_obj.save()
            except Exception as e:
                # Write Exception to Log file
                module = 'helpline_incoming (New Call)'
                write_log(HELPLINE_LOG_FILE, module, str(e))
                return HttpResponse(status=500)
            # expert_obj = HelplineExpert.objects.filter(expert_status=1, state__helpline_number=dg_number)[:1]
            # # Initiate Call if Expert is available
            # if len(expert_obj) > 0:
            #     make_helpline_call(incoming_call_obj, expert_obj[0], farmer_number)
            expert_number = get_expert_number(dg_number)
            # Initiate Call if Expert is available
            if expert_number != '':
                make_helpline_call(incoming_call_obj, expert_number, farmer_number)
            # Send Greeting and Sms if No Expert is available
            else:
                sms_body = helpline_data['sms_body']
                send_helpline_sms(EXOTEL_HELPLINE_NUMBER, farmer_number, sms_body)
                # Send greeting to user for notify about no expert available at this time.
                connect_to_app(farmer_number, NO_EXPERT_GREETING_APP_ID)
            return HttpResponse(status=200)
        # If pending call exist for this number
        else:
            # Update last incoming time for this pending call
            incoming_call_obj = incoming_call_obj[0]
            incoming_call_obj.last_incoming_time = incoming_time
            try:
                incoming_call_obj.save()
            except Exception as e:
                # Write Exception to Log file
                module = 'helpline_incoming (Old Call)'
                write_log(HELPLINE_LOG_FILE, module, str(e))
            latest_outgoing_of_incoming = HelplineOutgoing.objects.filter(incoming_call=incoming_call_obj).order_by(
                '-id').values_list('call_id', flat=True)[:1]
            if len(latest_outgoing_of_incoming) != 0:
                call_status = get_status(latest_outgoing_of_incoming[0])
            else:
                call_status = ''
            # Check If Pending call is already in-progress
            if call_status != '' and call_status['response_code'] == 200 and (
                        call_status['status'] in ('ringing', 'in-progress')):
                return HttpResponse(status=200)
            expert_number = get_expert_number(dg_number)
            # expert_obj = HelplineExpert.objects.filter(expert_status=1, state__helpline_number=dg_number)[:1]

            # # Initiate Call if Expert is available
            if expert_number != '':
                make_helpline_call(incoming_call_obj, expert_number, farmer_number)
            # Send Greeting and Sms if No Expert is available
            else:

                sms_body = helpline_data['sms_body']
                send_helpline_sms(EXOTEL_HELPLINE_NUMBER, farmer_number, sms_body)
                # Send greeting to user for notify about no expert available at this time.
                connect_to_app(farmer_number, NO_EXPERT_GREETING_APP_ID)
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

def get_expert_number(dg_number):
    expert_number = ''
    expert_obj = HelplineExpert.objects.filter(expert_status=1, state__helpline_number=dg_number)[:1]

    if len(expert_obj) > 0:
        expert_number = expert_obj[0]
    else :
        # Search in partner helpline number
        expert_partner_obj = HelplineExpert.objects.filter(partner__helpline_number=dg_number)[:1]
        if len(expert_partner_obj) > 0 :
            expert_number = expert_partner_obj[0]
    
    return expert_number

@csrf_exempt
def helpline_call_response(request):
    if request.method == 'POST':
        status = str(request.POST.getlist('Status')[0])
        outgoing_call_id = str(request.POST.getlist('CallSid')[0])
        outgoing_obj = HelplineOutgoing.objects.filter(call_id=outgoing_call_id).select_related('incoming_call',
                                                                                                'from_number').order_by(
            '-id')
        outgoing_obj = outgoing_obj[0] if len(outgoing_obj) > 0 else ''
        # If call Successfully completed then mark call as resolved
        if status == 'completed':
            recording_url = str(request.POST.getlist('RecordingUrl')[0])
            resolved_time = str(request.POST.getlist('DateUpdated')[0])
            if outgoing_obj:
                incoming_obj = outgoing_obj.incoming_call
                expert_obj = outgoing_obj.from_number
                update_incoming_obj(incoming_obj, 1, recording_url, expert_obj, resolved_time)
            else:
                # if outgoing object not found then get detail by call Exotel API
                call_detail = get_info_through_api(outgoing_call_id)
                if call_detail != '':
                    incoming_obj = call_detail[0]
                    expert_obj = call_detail[1]
                    update_incoming_obj(incoming_obj, 1, recording_url, expert_obj, resolved_time)
        elif status == 'failed':
            if outgoing_obj:
                farmer_number = outgoing_obj.to_number
                # send sms to Notify User about Later Call
                sms_body = helpline_data['sms_body']
                send_helpline_sms(EXOTEL_HELPLINE_NUMBER, farmer_number, sms_body)
            else:
                call_detail = get_info_through_api(outgoing_call_id)
                if call_detail != '':
                    farmer_number = call_detail[2]
                    # send sms to Notify User about Later Call
                    sms_body = helpline_data['sms_body']
                    send_helpline_sms(EXOTEL_HELPLINE_NUMBER, farmer_number, sms_body)
        elif status == 'no-answer' or status == 'busy':
            call_status = get_status(outgoing_call_id)
            if call_status['response_code'] == 200:
                # if expert pick call and (not farmer or farmer busy)
                if call_status['from_status'] == 'completed':
                    if outgoing_obj:
                        farmer_number = outgoing_obj.to_number
                    else:
                        farmer_number = call_status['to']
                    # send sms to Notify User about Later Call
                    sms_body = helpline_data['sms_body']
                    send_helpline_sms(EXOTEL_HELPLINE_NUMBER, farmer_number, sms_body)
                    return HttpResponse(status=200)
            make_call = 0
            if outgoing_obj:
                incoming_obj = outgoing_obj.incoming_call
                expert_obj = outgoing_obj.from_number
                to_number = outgoing_obj.to_number
                make_call = 1
            else:
                call_detail = get_info_through_api(outgoing_call_id)
                if call_detail != '':
                    incoming_obj = call_detail[0]
                    expert_obj = call_detail[1]
                    to_number = call_detail[2]
                    make_call = 1
            if make_call == 1:
                # Find next expert
                expert_numbers = list(HelplineExpert.objects.filter(expert_status=1, state__helpline_number=dg_number))
                try:
                    expert_numbers = expert_numbers[expert_numbers.index(expert_obj) + 1:]
                except Exception as e:
                    expert_numbers = []
                    pass
                # Make a call if next expert found
                if len(expert_numbers) > 0:
                    # if call initiate by queue module or in the chain of call initiate by queue module
                    if send_acknowledge(incoming_obj) == 0:
                        make_helpline_call(incoming_obj, expert_numbers[0], to_number)
                    else:
                        make_helpline_call(incoming_obj, expert_numbers[0], to_number, 1)
                # Send greeting and Sms if no expert is available
                else:
                    # if call not initiate by queue module or not in the chain of call initiate by queue module
                    # then send acknowledgement of future call to user
                    if send_acknowledge(incoming_obj) == 0:
                        sms_body = helpline_data['sms_body']
                        send_helpline_sms(EXOTEL_HELPLINE_NUMBER, to_number, sms_body)
                        # Send greeting to user for notify about no expert available at this time.
                        connect_to_app(to_number, NO_EXPERT_GREETING_APP_ID)
        else:
            # For other conditions write Logs
            module = 'helpline_call_response'
            log = 'Status: %s (outgoing_call_id: %s)' % (str(status), str(outgoing_call_id))
            write_log(HELPLINE_LOG_FILE, module, log)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def helpline_offline(request):
    if request.method == 'GET':
        call_id, farmer_number, dg_number, incoming_time = fetch_info_of_incoming_call(request)
        save_call_log(call_id, farmer_number, dg_number, 0, incoming_time)
        incoming_call_obj = HelplineIncoming.objects.filter(from_number=farmer_number, call_status=0).order_by('-id')
        if len(incoming_call_obj) == 0:
            incoming_call_obj = HelplineIncoming(call_id=call_id, from_number=farmer_number, to_number=dg_number,
                                                 incoming_time=incoming_time, last_incoming_time=incoming_time)
            try:
                incoming_call_obj.save()
            except Exception as e:
                # Write Exception to Log file
                module = 'helpline_offline'
                write_log(HELPLINE_LOG_FILE, module, str(e))
                return HttpResponse(status=500)
        else:
            # Update last incoming time for this pending call
            incoming_call_obj = incoming_call_obj[0]
            incoming_call_obj.last_incoming_time = incoming_time
            try:
                incoming_call_obj.save()
            except Exception as e:
                # Write Exception to Log file
                module = 'helpline_offline'
                write_log(HELPLINE_LOG_FILE, module, str(e))
        # Create thread for Notify User about off hours and record voicemail.
        Thread(target=send_voicemail, args=[farmer_number, OFF_HOURS_VOICEMAIL_APP_ID]).start()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Broadcast').count() > 0,
                  login_url=PERMISSION_DENIED_URL)
def broadcast(request):
    context = RequestContext(request)
    template_data = dict()
    template_data['broadcast_test_form'] = BroadcastTestForm()
    template_data['broadcast_form'] = BroadcastForm()
    # This will check on template whether to show forms (0) or message(1).
    template_data['acknowledge'] = 0
    # By default 0 for select Test Broadcast tab.
    template_data['active_tab'] = 0
    if request.method == 'POST':
        if 'broadcast_test_submit' in request.POST:
            broadcast_test_form = BroadcastTestForm(request.POST, request.FILES)
            if broadcast_test_form.is_valid():
                broadcast_title = 'admin_test'
                cluster_id_list = []
                audio_file = broadcast_test_form.cleaned_data.get('audio_file')
                to_number = broadcast_test_form.cleaned_data.get('to_number')
                farmer_contact_detail = [{'id': None, 'phone': to_number}]
            else:
                template_data['broadcast_test_form'] = broadcast_test_form
                return render_to_response('loop/broadcast.html', template_data, context_instance=context)
        elif 'submit' in request.POST:
            broadcast_form = BroadcastForm(request.POST, request.FILES)
            if broadcast_form.is_valid():
                broadcast_title = str(broadcast_form.cleaned_data.get('title'))
                cluster_id_list = broadcast_form.cleaned_data.get('cluster')
                audio_file = broadcast_form.cleaned_data.get('audio_file')
                farmer_file = broadcast_form.cleaned_data.get('farmer_file')
                farmer_contact_detail = []
                if cluster_id_list:
                    village_list = LoopUserAssignedVillage.objects.filter(loop_user_id__in=cluster_id_list).values_list(
                        'village', flat=True)
                    farmer_contact_detail = list(
                        Farmer.objects.filter(village_id__in=village_list).values('id', 'phone'))
                if farmer_file:
                    farmer_file_name = save_farmer_file(broadcast_title, farmer_file)
                    # Fetch cantact from csv file
                    with open(farmer_file_name, 'rb') as csvfile:
                        csv_header = ['id', 'phone']
                        customreader = csv.reader(csvfile)
                        # If csv file is not in correct format
                        if customreader.next() != csv_header:
                            broadcast_form.errors['farmer_file'] = ['Please upload csv file in correct format']
                            template_data['broadcast_form'] = broadcast_form
                            # Change to 1 for select Broadcast tab.
                            template_data['active_tab'] = 1
                            return render_to_response('loop/broadcast.html', template_data, context_instance=context)
                        for row in customreader:

                            farmer_id = int(row[0].strip()) if row[0].strip() else None
                            farmer_no = row[1].strip()
                            farmer_contact = {'id': farmer_id, 'phone': farmer_no}
                            if farmer_contact not in farmer_contact_detail:
                                farmer_contact_detail.append(farmer_contact)
                    # Remove csv file from server
                    os.remove(farmer_file_name)
            else:
                template_data['broadcast_form'] = broadcast_form
                # Change to 1 for select Broadcast tab.
                template_data['active_tab'] = 1
                return render_to_response('loop/broadcast.html', template_data, context_instance=context)
        else:
            HttpResponseBadRequest("<h2>Something is wrong, Please Try Again</h2>")
        audio_file_name = save_broadcast_audio(broadcast_title, audio_file)
        s3_audio_url = BROADCAST_S3_AUDIO_URL % (audio_file_name,)
        # Start thread for begin broadcast.

        Thread(target=start_broadcast,
               args=[broadcast_title, s3_audio_url, farmer_contact_detail, cluster_id_list, EXOTEL_HELPLINE_NUMBER,
                     BROADCAST_APP_ID]).start()

        template_data['acknowledge'] = 1
    elif request.method != 'GET':
        HttpResponseBadRequest("<h2>Only GET and POST requests is allow</h2>")
    return render_to_response('loop/broadcast.html', template_data, context_instance=context)


# BROADCAST_STATUS = ((0, "Pending"), (1, "Done"), (2, "DND-Failed"), (3, "Declined"))
@csrf_exempt
def broadcast_call_response(request):
    if request.method == 'POST':
        status = str(request.POST.getlist('Status')[0])
        outgoing_call_id = str(request.POST.getlist('CallSid')[0])
        audience_obj = BroadcastAudience.objects.filter(call_id=outgoing_call_id).order_by('-id')
        audience_obj = audience_obj[0] if len(audience_obj) > 0 else ''
        # if call found in our database, then update status accordingly
        if audience_obj != '':
            if status == 'completed':
                end_time = str(request.POST.getlist('DateUpdated')[0])
                audience_obj.end_time = end_time
                # if call completed then set status done if user has
                # listened the broadcast.
                audience_obj.status = 1
            else:
                # If call is not completed then set status pending
                # so if user call on halpline number then he will redirected to
                # broadcast message.
                audience_obj.status = 0
            try:
                audience_obj.save()
            except Exception as e:
                module = 'broadcast_call_response'
                write_log(HELPLINE_LOG_FILE, module, str(e))
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


# Make sure adding a forward slash (i.e. /) at the end of URL
# when putting this URL on exotel app.
def broadcast_audio_request(request):
    if request.method == 'GET':
        outgoing_call_id = str(request.GET.getlist('CallSid')[0])
        broadcast_audio_url = list(
            BroadcastAudience.objects.filter(call_id=outgoing_call_id).values_list('broadcast__audio_url',
                                                                                   flat=True).order_by('-id'))
        broadcast_audio_url = broadcast_audio_url[0] if len(broadcast_audio_url) > 0 else ''
        audio_url_response = HttpResponse(broadcast_audio_url, content_type='text/plain')
        return audio_url_response
    else:
        return HttpResponse(status=200)
