import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max
from django.core.serializers.json import DjangoJSONEncoder

from tastypie.models import ApiKey, create_api_key
from models import Training, Score, Trainer, Question
from activities.models import Screening, PersonAdoptPractice

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
    trainers = Trainer.objects.values('id', 'name')
    questions = Question.objects.values('id', 'text')
    data_dict = {'trainers': list(trainers), 'questions': list(questions)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def training_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]')
    question_ids = request.GET.getlist('question_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["date__gte"] = start_date
    if(end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["trainer__id__in"] = trainer_ids
    # question filter
    training_list = Training.objects.filter(**filter_args).values('assessment','place','trainer__name','language__language_name').annotate(Count('participants'))
    data = json.dumps(list(training_list))
    return HttpResponse(data)

def trainer_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]')
    question_ids = request.GET.getlist('question_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["question__id__in"] = question_ids
    trainer_list = Score.objects.filter(**filter_args).values('training__trainer__name').annotate(Count('participant', distinct=True), Sum('score'), Count('score'))
    data = json.dumps(list(trainer_list))
    return HttpResponse(data)

def question_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]')
    question_ids = request.GET.getlist('question_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["question__id__in"] = question_ids
    question_list = Score.objects.filter(**filter_args).values('question__text').annotate(Sum('score'), Count('score'), Count('participant', distinct=True))
    data = json.dumps(list(question_list))
    return HttpResponse(data)

def mediator_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]')
    question_ids = request.GET.getlist('question_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["question__id__in"] = question_ids
    mediator_list = Score.objects.filter(**filter_args).values('participant').distinct()
    mediator_data = {}
    for i in mediator_list:
        screening_list = Screening.objects.filter(animator__id = i['participant'])
        #adoption_list = PersonAdoptPractice.objects.filter()
        mediator_data[i['participant']] = list(screening_list)
    print mediator_data
    data = json.dumps(mediator_data, cls= DjangoJSONEncoder)
    return HttpResponse(data)

