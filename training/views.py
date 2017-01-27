import json
import MySQLdb
import dg.settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max
from django.core.serializers.json import DjangoJSONEncoder

from tastypie.models import ApiKey, create_api_key
from models import Training, Score, Trainer, Question, Assessment
from activities.models import Screening, PersonAdoptPractice, PersonMeetingAttendance
from geographies.models import State
from django.db import connection
import datetime
from datetime import date

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
            return HttpResponse(api_key.key)
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("0")
    return HttpResponse("0")

def dashboard(request):
    return render(request, 'app_dashboards/training_dashboard.html')

def filter_data(request):
    assessments = Assessment.objects.values('id', 'name')
    trainers = Trainer.objects.values('id', 'name')
    states = State.objects.values('id','state_name')
    filter_args = {}
    filter_args['score__in'] = [0, 1]
    participants = Score.objects.filter(**filter_args).values('participant__id').distinct()
    num_trainings = Score.objects.filter(**filter_args).values('training_id').distinct().count()
    num_participants = len(participants)
    num_pass = Score.objects.filter(**filter_args).values('participant').annotate(Sum('score'), Count('score'))
    data_dict = {'assessments': list(assessments), 'trainers': list(trainers), 'states': list(states), 'num_trainings': num_trainings, 'num_participants': num_participants, 'num_pass': list(num_pass)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def date_filter_data(request):

    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    assessment_ids = request.GET.getlist('assessment_ids[]')
    trainer_ids = request.GET.getlist('trainer_ids[]') 
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args['training__assessment__id__in'] = assessment_ids
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args['score__in'] = [0, 1]
    participants = Score.objects.filter(**filter_args).values_list('participant__id', flat=True).distinct()
    num_trainings = Score.objects.filter(**filter_args).values('training_id').distinct().count()
    num_participants = len(participants)
    num_pass = Score.objects.filter(**filter_args).values('participant').annotate(Sum('score'), Count('score'))

    data_dict = {'num_trainings': num_trainings, 'num_participants': num_participants, 'num_pass': list(num_pass)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def trainer_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    assessment_ids = request.GET.getlist('assessment_ids[]')
    trainer_ids = request.GET.getlist('trainer_ids[]') 
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    trainer_wise_avg_score = {}
    trainer_wise_avg_score_list = []
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__assessment__id__in"] = assessment_ids
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]
    score_obj = Score.objects.filter(**filter_args).all()
    trainer_list_participant_training_count = score_obj.values('training__trainer__name').order_by('training__trainer__name').annotate(Count('participant', distinct=True) , Sum('score'), Count('score'), Count('training__id', distinct=True),all_participant_count=Count('participant', distinct=False))
    trainer_list_participant_count = score_obj.values('training__trainer__name', 'training_id').order_by('training__trainer__name').annotate(Count('participant', distinct=True ), Sum('score'))

    for trainer in trainer_list_participant_count :
        trainer_name = trainer['training__trainer__name']
        if(trainer_name not in trainer_wise_avg_score) :
            trainer_wise_avg_score[trainer_name] = {}
            trainer_wise_avg_score[trainer_name]['participant_count'] = trainer['participant__count']
            trainer_wise_avg_score[trainer_name]['score_sum'] = trainer['score__sum']
        else :
            trainer_wise_avg_score[trainer_name]['participant_count'] += trainer['participant__count']
            trainer_wise_avg_score[trainer_name]['score_sum'] += trainer['score__sum']

    for trainer_score in sorted(trainer_wise_avg_score) :
        json_obj = {}
        json_obj[trainer_score] = trainer_wise_avg_score[trainer_score]
        trainer_wise_avg_score_list.append(json_obj)
        
    mediator_list = Score.objects.filter(**filter_args).values('training__trainer__name', 'participant').order_by('training__trainer__name').annotate(Sum('score'), Count('score'))
    data_dict = {'trainer_list': list(trainer_list_participant_training_count), 'mediator_list': list(mediator_list), 'trainer_wise_average_score_data' : trainer_wise_avg_score_list}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def question_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    assessment_ids = request.GET.getlist('assessment_ids[]')
    trainer_ids = request.GET.getlist('trainer_ids[]')
    state_ids = request.GET.getlist('state_ids[]')
    question_data_dict = {}
    language_count = 0
    language_eng_id = 2
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__assessment__id__in"] = assessment_ids
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]
    question_list = Score.objects.filter(**filter_args).values('question__text', 'question__language__id', 'question__section', 'question__serial').order_by('question__language_id', 'question__section', 'question__serial').annotate(Sum('score'), Count('score'), Count('participant', distinct=True))
    language_text_eng = Question.objects.filter(language_id = language_eng_id, assessment_id__in=assessment_ids).values('text', 'section', 'serial').order_by('section', 'serial')
    question_data_dict = {'question_list' : list(question_list), 'question_language_text_eng':list(language_text_eng)}
    data = json.dumps(question_data_dict)
    return HttpResponse(data)

def state_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    assessment_ids = request.GET.getlist('assessment_ids[]')
    trainer_ids = request.GET.getlist('trainer_ids[]')
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    state_wise_avg_score = {}
    state_wise_avg_score_list = []
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__assessment__id__in"] = assessment_ids
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]

    score_obj = Score.objects.filter(**filter_args)
    state_list_participant_training_count = score_obj.values('participant__district__state__state_name').order_by('participant__district__state__state_name').annotate(Sum('score'), Count('score'), Count('participant', distinct=True), Count('training__id', distinct=True))
    state_list_participant_count = score_obj.values('participant__district__state__state_name', 'training_id').order_by('participant__district__state__state_name').annotate(Sum('score'), Count('score'), Count('participant', distinct=True))

    for state in state_list_participant_count :
        state_name = state['participant__district__state__state_name']
        if(state_name not in state_wise_avg_score) :
            state_wise_avg_score[state_name] = {}
            state_wise_avg_score[state_name]['participant_count'] = state['participant__count']
            state_wise_avg_score[state_name]['score_sum'] = state['score__sum']
        else :
            state_wise_avg_score[state_name]['participant_count'] += state['participant__count']
            state_wise_avg_score[state_name]['score_sum'] += state['score__sum']

    for state_score in sorted(state_wise_avg_score) :
        json_obj = {}
        json_obj[state_score] = state_wise_avg_score[state_score]
        state_wise_avg_score_list.append(json_obj)

    mediator_list = Score.objects.filter(**filter_args).values('participant__district__state__state_name', 'participant').order_by('participant__district__state__state_name').annotate(Sum('score'), Count('score'))
    data_dict = {'state_list': list(state_list_participant_training_count), 'mediator_list': list(mediator_list), 'state_wise_avg_score_data' : list(state_wise_avg_score_list)}
    data = json.dumps(data_dict)
    return HttpResponse(data)


def month_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    current_year = datetime.date.today().year
    start_date = datetime.date(current_year, 01, 01)
    end_date = datetime.date(current_year, 12, 31)
    assessment_ids = request.GET.getlist('assessment_ids[]')
    trainer_ids = request.GET.getlist('trainer_ids[]')
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__assessment__id__in"] = assessment_ids
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]

    month_data_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    truncate_date = connection.ops.date_trunc_sql('month', 'date')
    training_month_data = Training.objects.extra({'month':truncate_date})
    training_list = list(Score.objects.values_list('training_id', flat=True).distinct())
    month_wise_training_data = training_month_data.filter(id__in=training_list, date__gte=start_date, date__lte=end_date).values('month').annotate(Count('id')).order_by('month')

    maximum = -1
    for training_data in month_wise_training_data:
        month = training_data['month'].month
        training_count = training_data['id__count']
        month_data_list[month - 1] = training_count
        maximum = max(maximum, month)

    data_dict = {'trainings':'Number of Trainings','month_training_list':month_data_list[:maximum]}
    data = json.dumps(data_dict)
    return HttpResponse(data)
