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
    
def sidenavtest(request):
    return render(request, 'app_dashboards/sidenavtest.html')

def filter_data(request):
    assessments = Assessment.objects.values('id', 'name')
    trainers = Trainer.objects.values('id', 'name')
    states = State.objects.values('id','state_name')
    participants = Score.objects.filter(training__assessment__id=1).values('participant__id').distinct()
    num_trainings = Score.objects.filter(score__in=[0,1], training__assessment__id=1).values('training_id').distinct().count()
    num_participants = len(participants)
    num_pass = Score.objects.filter(score__in=[0,1], training__assessment__id=1).values('participant').annotate(Sum('score'), Count('score'))
    # training_objs = Training.objects.filter(assessment__id = 1).values('participants__id','date')
    # for item in training_objs :
    #     if(item['participants__id'] is not None) :
    #         item['participants__id'] = int(item['participants__id'])
    #     else :
    #         del item
            
    # print training_objs    
    # count = 0           
    # for item in training_objs:
    #     count += Screening.objects.filter(animator_id=item['participants__id'], date__gte=item['date']).values('village_id').distinct().count()
    # num_villages = count
    # num_beneficiaries = 0
    # for item in training_objs:
    #     num_beneficiaries += Screening.objects.filter(animator_id= item['participants__id'], date__gte=item['date']).values('farmers_attendance__id').distinct().count()


                    

    # mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root',
    #                                passwd=dg.settings.DATABASES['default']['PASSWORD'],
    #                                db=dg.settings.DATABASES['default']['NAME'],
    #                                 charset = 'utf8',
    #                                  use_unicode = True)
    # query = 'Select count(distinct(person_id)) as viewers from person_meeting_attendance_myisam'
    # cur = mysql_cn.cursor()
    # cur.execute(query)
    # result = cur.fetchall()
    # for row in result:
    #     num_beneficiaries = row[0]
    # mysql_cn.close()


    # print "******* Num villages"
    # print num_villages
    # print "*********"

    # print "******* Beneficiaries"
    # print num_beneficiaries
    # print "*********"
    #num_farmers = len(PersonMeetingAttendance.objects.filter(screening__animator__in=participants).values_list('person', flat=True).distinct())
    data_dict = {'assessments': list(assessments), 'trainers': list(trainers), 'states': list(states), 'num_trainings': num_trainings, 'num_participants': num_participants, 'num_pass': list(num_pass)}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def date_filter_data(request):

    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    print "**********************************************"
    print start_date
    print end_date
    print "**********************************************"
    assessments = Assessment.objects.values('id', 'name')
    trainers = Trainer.objects.values('id', 'name')
    states = State.objects.values('id','state_name')
    participants = Score.objects.filter(training__assessment__id=1, training__date__gte=start_date, training__date__lte=end_date).values_list('participant__id', flat=True).distinct()
    num_trainings = Score.objects.filter(score__in=[0,1], training__assessment__id=1, training__date__gte = start_date, training__date__lte = end_date).values('training_id').distinct().count()
    # Training.objects.filter(assessment__id = 1, date__gte = start_date, date__lte = end_date).values('date', 'place', 'trainer').distinct().count()
    num_participants = len(participants)
    num_pass = Score.objects.filter(score__in=[0,1], training__assessment__id=1, training__date__gte = start_date, training__date__lte = end_date).values('participant').annotate(Sum('score'), Count('score'))


    # Start

    # training_objs = Training.objects.filter(assessment__id = 1, date__gte = start_date, date__lte = end_date).values('participants__id','date')
    # for item in training_objs:
    #     if(item['participants__id'] is not None) :
    #         item['participants__id'] = int(item['participants__id'])
    #     else :
    #         del item
    # print training_objs    
    # count = 0           
    # for item in training_objs:
    #     count += Screening.objects.filter(animator_id=item['participants__id'], date__gte = item['date'], date__lte = end_date).values('village_id').distinct().count()
    # num_villages = count
    # num_beneficiaries = 0
    # for item in training_objs:
    #     num_beneficiaries += Screening.objects.filter(animator_id= item['participants__id'], date__gte = item['date'], date__lte = end_date).values('farmers_attendance__id').distinct().count()

    # End 

    # num_villages = Screening.objects.filter(date__gte = start_date, date__lte = end_date).values('village__id').distinct().count()
    # mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root',
    #                                passwd=dg.settings.DATABASES['default']['PASSWORD'],
    #                                db=dg.settings.DATABASES['default']['NAME'],
    #                                 charset = 'utf8',
    #                                  use_unicode = True)
    # query = '''Select count(distinct(person_id)) as viewers from person_meeting_attendance_myisam where date between '''+ '\''+start_date+'\''+'''and'''+'\''+end_date+'\''
    # print query 
    # cur = mysql_cn.cursor()
    # cur.execute(query)
    # result = cur.fetchall()
    # num_beneficiaries = 0
    # for row in result:
    #     num_beneficiaries = row[0]
    # mysql_cn.close()
    #num_beneficiaries = PersonMeetingAttendance.objects.filter(screening__date__gte = start_date, screening__date__lte = end_date).values('person_id').distinct().count()
    # print "######### filtered villages"
    # print num_villages
    # print "#########"

    # print "******* Filtered Beneficiaries"
    # print num_beneficiaries
    # print "*********"
    #num_farmers = len(PersonMeetingAttendance.objects.filter(screening__animator__in=participants).values_list('person', flat=True).distinct())
    data_dict = {'assessments': list(assessments), 'trainers': list(trainers), 'states': list(states), 'num_trainings': num_trainings, 'num_participants': num_participants, 'num_pass': list(num_pass)}
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
    trainer_list_obj = Score.objects.filter(**filter_args).all()
    trainer_list_filter_1 = trainer_list_obj.values('training__trainer__name').order_by('training__trainer__name').annotate(Count('participant', distinct=True) , Sum('score'), Count('score'), Count('training__id', distinct=True),all_participant_count=Count('participant', distinct=False))
    trainer_list_filter_2 = trainer_list_obj.values('training__trainer__name', 'training_id').order_by('training__trainer__name').annotate(Count('participant', distinct=True ), Sum('score'))

    for trainer in trainer_list_filter_2 :
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
    data_dict = {'trainer_list': list(trainer_list_filter_1), 'mediator_list': list(mediator_list), 'test' : trainer_wise_avg_score_list}
    data = json.dumps(data_dict)
    return HttpResponse(data)

def question_wise_data(request):
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
    filter_args["training__assessment__id__in"] = assessment_ids
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]
    question_list = Score.objects.filter(**filter_args).values('question__text', 'question__language__id').order_by('-question__id').annotate(Sum('score'), Count('score'), Count('participant', distinct=True))
    data = json.dumps(list(question_list))
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

    state_list_obj = Score.objects.filter(**filter_args)
    state_list_filter1 = state_list_obj.values('participant__district__state__state_name').order_by('participant__district__state__state_name').annotate(Sum('score'), Count('score'), Count('participant', distinct=True), Count('training__id', distinct=True))
    state_list_filter2 = state_list_obj.values('participant__district__state__state_name', 'training_id').order_by('participant__district__state__state_name').annotate(Sum('score'), Count('score'), Count('participant', distinct=True))

    for state in state_list_filter2 :
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

    #participants = Score.objects.filter(**filter_args).values_list('participant__id', flat=True).distinct()
    #num_farmers = PersonMeetingAttendance.objects.filter(screening__animator__in=participants).values('screening__animator__district__state__state_name').order_by('screening__animator__district__state__state_name').annotate(Count('person', distinct=True))
    mediator_list = Score.objects.filter(**filter_args).values('participant__district__state__state_name', 'participant').order_by('participant__district__state__state_name').annotate(Sum('score'), Count('score'))
    data_dict = {'state_list': list(state_list_filter1), 'mediator_list': list(mediator_list), 'state_test' : list(state_wise_avg_score_list)}
    data = json.dumps(data_dict)
    return HttpResponse(data)


def month_wise_data(request):
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
    filter_args["training__assessment__id__in"] = assessment_ids
    filter_args["training__trainer__id__in"] = trainer_ids
    filter_args["participant__district__state__id__in"] = state_ids
    filter_args["score__in"] = [1, 0]



    month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']

    #participants = Score.objects.filter(**filter_args).values_list('participant__id', flat=True).distinct()
    #num_farmers = PersonMeetingAttendance.objects.filter(screening__animator__in=participants).values('screening__animator__district__state__state_name').order_by('screening__animator__district__state__state_name').annotate(Count('person', distinct=True))
    mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root',
                                   passwd=dg.settings.DATABASES['default']['PASSWORD'],
                                   db=dg.settings.DATABASES['default']['NAME'],
                                    charset = 'utf8',
                                     use_unicode = True)
    query = '''SELECT MONTH(tt.date) as \'Month\',count(distinct tt.id) \'Number of Training\' FROM training_score ts join training_training tt on tt.id = ts.training_id and tt.date >= 20160101 AND tt.date <= 20161231 GROUP BY  MONTH(tt.date) order by MONTH(tt.date)'''
    cur = mysql_cn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    month_data_list = []
    count = 1
    for row in result:
        if(row[0] == count) :
            month_data_list.append(int(row[1]))
        else :
            month_data_list.append(0)
        count += 1

    mysql_cn.close()
    data_dict = {'trainings':'Number of Trainings','data_list':month_data_list}
    data = json.dumps(data_dict)
    return HttpResponse(data)    
