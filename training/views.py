from dg.settings import DATABASES
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Sum, F
from django.core.serializers.json import DjangoJSONEncoder

import json
import MySQLdb
import pandas
import datetime
from models import Trainer, Assessment
from geographies.models import State

from tastypie.models import ApiKey
from training.management.databases.utility import multiprocessing_dict, multiprocessing_list
from training.management.databases.get_sql_queries import *
from training.log.training_log import get_latest_timestamp
from collections import OrderedDict

# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                api_key.save()
            log_obj = get_latest_timestamp()
            if log_obj == None:
                timestamp = datetime.datetime.utcnow()
            else:
                timestamp = log_obj.timestamp
            trainer = Trainer.objects.filter(training_user__user__id = user.id).first()
            return HttpResponse(json.dumps({'ApiKey':api_key.key,'timestamp':str(timestamp),'TrainerId':trainer.id}))
        else:
            return HttpResponse("0",status=401)
    else:
        return HttpResponse("0",status=403)
    return HttpResponse("0",status=404)

def extract_filters_request(request):
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = str(request.GET['start_date'])
        end_date = str(request.GET['end_date'])
    else:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        delta = datetime.timedelta(days=365)
        start_date = (datetime.datetime.today() - delta).strftime('%Y-%m-%d')
    if 'apply_filter' in request.GET:
        apply_filter = True if request.GET['apply_filter'] == 'true' else False
    else :
        apply_filter = False
    if 'chartType' in request.GET:
        chart_type =  str(request.GET.get('chartType'))
    else:
        chart_type = ''
    if 'chartName' in request.GET:
        chart_name = str(request.GET.get('chartName'))
    else:
        chart_name = ''
    trainers_list = request.GET.getlist('Trainer')
    states_list = request.GET.getlist('State')

    filter_args = {}
    filter_args['start_date'] = start_date
    filter_args['end_date'] = end_date
    filter_args['apply_filter'] = apply_filter
    filter_args['trainers_list'] = trainers_list
    filter_args['states_list'] = states_list
    filter_args['chart_name'] = chart_name
    filter_args['chart_type'] = chart_type

    return filter_args

def get_pandas_dataframe(sql_query):
    db_connection = MySQLdb.connect(host=DATABASES['default']['HOST'],
                                        user=DATABASES['default']['USER'],
                                        passwd=DATABASES['default']['PASSWORD'],
                                        db=DATABASES['default']['NAME'],
                                        charset='utf8',
                                        use_unicode=True)
    return pandas.read_sql_query(sql_query, con=db_connection)


@csrf_exempt
def get_filter_data(request):
    table_name =  parent_id_list = None
    try:
        table_name = request.GET['filter']
        parent = request.GET['parent']
        parent_id_list = request.GET.getlist(parent)
    except:
        pass
    response_list = []
    if table_name and table_name == 'Trainer' and parent_id_list and len(parent_id_list) > 0:
        trainers_list = Trainer.objects.filter(training_user__states__in = parent_id_list[0].split(',')).annotate(value=F('name')).values('id','value').distinct().order_by('value')
        trainer_dict = {'name':'Trainer', 'data':list(trainers_list)}
        response_list.extend([trainer_dict])
    elif table_name is None:
        states_list = State.objects.annotate(value=F('state_name')).values('id','value').order_by('value')
        state_dict = {'name':'State', 'data':list(states_list)}
        response_list.extend([state_dict])

    json_data = json.dumps(response_list)
    return HttpResponse(json_data)

@csrf_exempt
def get_overall_data(request):
    filter_args = extract_filters_request(request)
    query_list = []

    # No of Trainings
    training_query = get_training_data_sql(**filter_args)
    query_list.extend(training_query)

    # No of Mediators
    mediator_query = get_mediators_data_sql(**filter_args)
    query_list.extend(mediator_query)

    # Pass Percentage
    pass_percent_query = get_pass_perc_data_sql(**filter_args)
    query_list.extend(pass_percent_query)

    # Avg Score
    avg_score_query = get_avg_score_data_sql(**filter_args)
    query_list.extend(avg_score_query)

    results = multiprocessing_list(query_list = query_list)
    data = json.dumps({'data' : results})
    return HttpResponse(data)

def question_wise_data(chart_name, result):
    final_data_list = {}
    try:
        outer_data = {'outerData': {'series':[],'categories':result['Questions'].tolist()}}
        temp_dict_outer = {'name':'Questions','data':[]}
        for row in result.iterrows():
            temp_dict_outer['data'].append({'name':row[1].Questions,'y':int(row[1].Percentage)})

        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[chart_name] = outer_data
    except:
        final_data_list['error']="No data found for the filters applied"
    return final_data_list

def number_of_trainings(chart_name, result):
    final_data_list = {}
    state_grouped_data = result.groupby(['state']).sum().reset_index()
    try:
        outer_data = {'outerData': {'series':[],'categories':state_grouped_data['state'].tolist()}}

        temp_dict_outer = {'name':'Trainings','data':[]}
        for row in state_grouped_data.iterrows():
            temp_dict_outer['data'].append({'name':row[1].state,'y':int(row[1].trainings),'drilldown':row[1].state +' trainings'})

        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[chart_name] = outer_data
        inner_data = {'innerData': []}

        trainer_training_dict = {name:dict(zip(g['trainer'],g['trainings'])) for name,g in result.groupby('state')}
        for key,value in trainer_training_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = key + ' trainings'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append([k,v])
            inner_data['innerData'].append(temp_dict_inner)

        final_data_list[chart_name].update(inner_data)
    except:
        final_data_list['error']="No data found for the filters applied"
    return final_data_list

def pandas_default_aggregation(chart_name, result):
    final_data_list = {}
    state_grouped_data = result.groupby(['state']).sum().reset_index()
    try:
        outer_data = {'outerData': {'series':[],'categories':state_grouped_data['state'].tolist()}}
        temp_dict_outer = {'name':'Mediators','data':[]}
        for row in state_grouped_data.iterrows():
            temp_dict_outer['data'].append({'name':row[1].state,'y':int(row[1].mediators),'drilldown':row[1].state+' mediators'})
        outer_data['outerData']['series'].append(temp_dict_outer)

        temp_dict_outer = {'name':'Above70','data':[]}
        for row in state_grouped_data.iterrows():
            temp_dict_outer['data'].append({'name':row[1].state,'y':int(row[1].Above70),'drilldown':row[1].state+' above70'})

        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[chart_name] = outer_data
        inner_data = {'innerData': []}
        trainer_mediators_dict = {name: dict(zip(g['trainer'],g['mediators'])) for name,g in result.groupby('state')}
        trainer_pass_dict = {name: dict(zip(g['trainer'],g['Above70'])) for name,g in result.groupby('state')}
        for key, value in trainer_mediators_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = key + ' mediators'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append([k,v])
            inner_data['innerData'].append(temp_dict_inner)

        for key, value in trainer_pass_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = key
            temp_dict_inner['id'] = key + ' above70'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append([k,v])
            inner_data['innerData'].append(temp_dict_inner)

        final_data_list[chart_name].update(inner_data)
    except:
        final_data_list['error']="No data found for the filters applied"
    return final_data_list


def year_month_wise_data(chart_name, result):
    final_data_list = {}
    year_grouped_data = result.groupby(['year']).sum().reset_index()
    # sorting months
    months = {datetime.datetime(2000,i,1).strftime("%B"): i for i in range(1, 13)}
    result['month_number'] = result['month'].map(months)
    result = result.sort(columns=['month_number'])

    month_training_dict_test = {}

    try:
        outer_data = {'outerData': {'series':[],'categories':year_grouped_data['year'].tolist()}}
        temp_dict_outer = {'name':'Trainings','data':[]}
        for row in year_grouped_data.iterrows():
            temp_dict_outer['data'].append({'name':row[1].year,'y':int(row[1].trainings),'drilldown':str(row[1].year) +' trainings'})
        outer_data['outerData']['series'].append(temp_dict_outer)
        final_data_list[chart_name] = outer_data

        inner_data = {'innerData': []}
        month_training_dict = {name:OrderedDict(zip(g['month'],g['trainings'])) for name,g in result.groupby(['year'])}

        for key,value in month_training_dict.iteritems():
            temp_dict_inner = {'data':[]}
            temp_dict_inner['name'] = str(key)
            temp_dict_inner['id'] = str(key) + ' trainings'
            for k, v in value.iteritems():
                temp_dict_inner['data'].append([k,v])
            inner_data['innerData'].append(temp_dict_inner)
        final_data_list[chart_name].update(inner_data)
    except:
        final_data_list['error']="No data found for the filters applied"
    return final_data_list

def graph_data(request):
    filter_args = extract_filters_request(request)
    if filter_args['chart_name'] in ['state_trainer_#trainings', 'state_trainer_#mediators']:
        sql_query = trainings_mediators_query(**filter_args)
        result = get_pandas_dataframe(sql_query)

        if filter_args['chart_name'] == 'state_trainer_#mediators':
            data_to_send = pandas_default_aggregation(filter_args['chart_name'], result)
        elif filter_args['chart_name'] == 'state_trainer_#trainings':
            data_to_send = number_of_trainings(filter_args['chart_name'], result)

    elif filter_args['chart_name'] in ['question_wise_data']:
        sql_query = question_wise_data_query(**filter_args)
        result = get_pandas_dataframe(sql_query)
        data_to_send = question_wise_data(filter_args['chart_name'], result)

    elif filter_args['chart_name'] in ['year_month_wise_data']:
        sql_query = year_month_wise_data_query(**filter_args)
        result = get_pandas_dataframe(sql_query)
        data_to_send = year_month_wise_data(filter_args['chart_name'], result)

    return HttpResponse(json.dumps(data_to_send))

def dashboard(request):
    return render(request, 'analytics/dist/training/index.html')
    # return render(request, 'app_dashboards/training_dashboard.html')
