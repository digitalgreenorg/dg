import json

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
    participants = Score.objects.filter(assessment__id=1).values_list('participant__id', flat=True).distinct()
    num_trainings = Training.objects.filter(assessment__id=1).values('date', 'place', 'trainer').distinct().count()
    num_participants = len(participants)
    num_pass = Score.objects.filter(score__in=[0,1], assessment__id=1).values('participant').annotate(Sum('score'), Count('score'))
    #num_farmers = len(PersonMeetingAttendance.objects.filter(screening__animator__in=participants).values_list('person', flat=True).distinct())
    data_dict = {'assessments': list(assessments), 'trainers': list(trainers), 'states': list(states), 'num_trainings': num_trainings, 'num_participants': num_participants, 'num_pass': list(num_pass)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def trainer_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]') 
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    # Check for module (Pico Seekho OR Documentation)
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]
    filter_args["training__assessment__id__in"] = assessment_ids
    trainer_list = Score.objects.filter(**filter_args).values('training__trainer__name').annotate(Count('participant', distinct=True), Sum('score'), Count('score'), Count('training__id', distinct=True))
    data = json.dumps(list(trainer_list))
    return HttpResponse(data)

def question_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]')
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]
    filter_args["training__assessment__id__in"] = assessment_ids
    question_list = Score.objects.filter(**filter_args).values('question__text', 'question__language__id').order_by('-question__id').annotate(Sum('score'), Count('score'), Count('participant', distinct=True))
    data = json.dumps(list(question_list))
    return HttpResponse(data)

def mediator_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]')
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]
    filter_args["training__assessment__id__in"] = assessment_ids
    mediator_list = Score.objects.filter(**filter_args).values('participant').distinct()
    mediator_data = {}
    for i in mediator_list:
        screening_list = Screening.objects.filter(animator__id = i['participant'])
        #adoption_list = PersonAdoptPractice.objects.filter()
        mediator_data[i['participant']] = list(screening_list)
    #print mediator_data
    data = json.dumps(mediator_data, cls= DjangoJSONEncoder)
    return HttpResponse(data)

def state_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    trainer_ids = request.GET.getlist('trainer_ids[]')
    state_ids = request.GET.getlist('state_ids[]')
    filter_args = {}
    if(start_date !=""):
        filter_args["training__date__gte"] = start_date
    if(end_date != ""):
        filter_args["training__date__lte"] = end_date
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]
    filter_args["training__assessment__id__in"] = assessment_ids
    state_list = Score.objects.filter(**filter_args).values('participant__district__state__state_name').annotate(Sum('score'), Count('score'), Count('participant', distinct=True), Count('training__id', distinct=True))
    data = json.dumps(list(state_list))
    return HttpResponse(data)
