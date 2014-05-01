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
    '''ASA partner_id = 10000000000008, BRLPS partner_id = 10000000000013'''
    partners = Partners.objects.filter(partner_name__in=('ASA','BRLPS'))
    districts = District.objects.filter(state_id=10000000000006)
    deos_working_for_Bihar_partners = ServerLog.objects.filter(partner__in=(10000000000008,10000000000013)).values_list('user__username', flat=True).distinct()
    print deos_working_for_Bihar_partners
    deos_working_in_Bihar = []
    for deo in deos_working_for_Bihar_partners:
        if deo != None:
            deodetails = CocoUser.objects.get(user__username=deo)
            state = deodetails.villages.values_list('block__district__state__state_name', flat=True).distinct()
            if state[0] == "Bihar":
                deos_working_in_Bihar.append(deo)   
    context = {
        'partners': partners,
        'districts': districts,
        'deos': deos_working_in_Bihar,
    }
    
    return render_to_response('deoanalytics/mainpage.html' , context, context_instance = RequestContext(request))

def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = District.objects.filter(state_id=10000000000006, partner_id=selectedpartner).values('district_name')
    print list(districts)
    return HttpResponse(json.dumps(list(districts)), mimetype="application/json")

def deosetter(request):
    selectedpartner = request.GET.get('partner', None)
    selecteddistrict = request.GET.get('district', None)
    print selecteddistrict
    
    deos_working_for_Bihar_partners = ServerLog.objects.filter(partner=selectedpartner).values_list('user__username', flat=True).distinct()
    'print deos_working_for_Bihar_partners'
    deos_working_in_selected_district = []
    for deo in deos_working_for_Bihar_partners:
        if deo != None:
            deodetails = CocoUser.objects.get(user__username=deo)
            dist = deodetails.villages.values_list('block__district__district_name', flat=True).distinct()
            'print str(dist[0])'
            if str(dist[0].encode('utf-8')) == selecteddistrict:
                deos_working_in_selected_district.append(deo)
    print deos_working_in_selected_district 
    resp = [dict(deo_name=deo) for deo in deos_working_in_selected_district]
    print resp
    return HttpResponse(json.dumps(list(resp)), mimetype="application/json")

def deodatasetter(request):
    selecteddeo = request.GET.get('deo',None)
    sdate = request.GET.get ('sdate',None)
    edate = request.GET.get ('edate',None)
    
    start_date = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(edate, "%Y-%m-%d")
    
    '''screenings1 = Screening.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).count()'''    
    screenings = Screening.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).values_list('time_created', flat=True)
    listofscreeningdates = []
    for screening in screenings:
        listofscreeningdates.append(str(screening.date()))
        
    s_dict = dict((i,listofscreeningdates.count(i)) for i in listofscreeningdates)
    print s_dict
        
    adoptions = PersonAdoptPractice.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).count()
    persons = Person.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).count()
    videos = Video.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).count()
    
    return HttpResponse(json.dumps({
        "screenings":s_dict,
        "adoptions": adoptions,
        "persons": persons,
        "videos": videos}),
    content_type="application/json")
    '''return HttpResponse(json.dumps(p), mimetype="application/json")'''