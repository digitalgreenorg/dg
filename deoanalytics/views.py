# Create your views here.

import json

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response

from dashboard.models import Screening
from dashboard.models import Partners
from dashboard.models import District
from dashboard.models import ServerLog
from dashboard.models import CocoUser
from dashboard.models import PersonAdoptPractice


def index(request):
    noofscreenings = Screening.objects.all()[0]
    '''output = ', '.join([p.question_text for p in latest_question_list])'''
    template = loader.get_template('deoanalytics/index.html')
    
    context = RequestContext(request, {
        'noofscreenings': noofscreenings,
    })
    
    return HttpResponse(template.render(context))    
    '''return HttpResponse("Hello, world. You're at the DEO index.")'''

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

    
    screenings = Screening.objects.filter(user_created_id=126).count()   
    adoptions = PersonAdoptPractice.objects.filter(user_created_id=126).count()                                                                                                            
    
    context = {
        'partners': partners,
        'districts': districts,
        'deos': deos_working_in_Bihar,
        'screenings':screenings,
        'adoptions':adoptions,
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

    