# Create your views here.

import json, datetime

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.db.models import Count

from dashboard.models import Screening
from dashboard.models import Partners
from dashboard.models import District
from dashboard.models import ServerLog
from dashboard.models import CocoUser
from dashboard.models import PersonAdoptPractice
from dashboard.models import Person
from dashboard.models import Video


def index(request):
    template = loader.get_template('deoanalytics/index.html')
    return HttpResponse()

def mainpage(request):
    thepartners = Partners.objects.filter(partner_name__in=('ASA','BRLPS'))  
    context = {
        'thepartner': thepartners,
    }    
    return render_to_response('deoanalytics/mainpage.html' , context, context_instance = RequestContext(request))

def partnersetter(request):
    '''ASA partner_id = 10000000000008, BRLPS partner_id = 10000000000013'''
    partners = Partners.objects.filter(partner_name__in=('ASA','BRLPS')).values('partner_name')
    return HttpResponse(json.dumps(list(partners)), mimetype="application/json")
        
def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = District.objects.filter(state_id=10000000000006, partner_id=selectedpartner).values('district_name')
    return HttpResponse(json.dumps(list(districts)), mimetype="application/json")

def deosetter(request):
    selectedpartner = request.GET.get('partner', None)
    selecteddistrict = request.GET.get('district', None)
    
    deos_working_for_Bihar_partners = ServerLog.objects.filter(partner=selectedpartner).values_list('user__username', flat=True).distinct()
    deos_working_in_selected_district = []
    for deo in deos_working_for_Bihar_partners:
        if deo != None:
            deodetails = CocoUser.objects.get(user__username=deo)
            dist = deodetails.villages.values_list('block__district__district_name', flat=True).distinct()
            if str(dist[0].encode('utf-8')) == selecteddistrict:
                deos_working_in_selected_district.append(deo)
    resp = [dict(deo_name=deo) for deo in deos_working_in_selected_district]
    return HttpResponse(json.dumps(list(resp)), mimetype="application/json")

def deodatasetter(request):
    selecteddeo = request.GET.get('deo',None)
    sdate = request.GET.get ('sdate',None)
    edate = request.GET.get ('edate',None)
    
    start_date = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(edate, "%Y-%m-%d")
        
    screenings = Screening.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).values_list('time_created', flat=True)
    listofscreeningdates = []
    for screening in screenings:
        listofscreeningdates.append(str(screening.date()))
        
    s_dict = dict((i,listofscreeningdates.count(i)) for i in listofscreeningdates)

    adoptions = PersonAdoptPractice.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).values_list('time_created', flat=True)
    listofadoptiondates = []
    for adoption in adoptions:
        listofadoptiondates.append(str(adoption.date()))
        
    a_dict = dict((i,listofadoptiondates.count(i)) for i in listofadoptiondates)
    persons = Person.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).count()
    
    return HttpResponse(json.dumps({
        "screenings":s_dict,
        "adoptions": a_dict,
        "persons": persons}),
    content_type="application/json")