import json, datetime

from django.http import HttpResponse

from activities.models import PersonAdoptPractice, Screening
from coco.models import CocoUser
from people.models import Person
from programs.models import Partner
from geographies.models import District
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    partner = Partner.objects.order_by('partner_name').values('partner_name', 'id')
    context= {
              'header': {
                         'jsController':'DeoAnalytics',
                         },
              'partner' : partner,
              }
    return render_to_response('deoanalytics.html' , context, context_instance = RequestContext(request))


def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = District.objects.select_related().filter(block__village__person__partner_id=selectedpartner).values('district_name', 'id').distinct()
    resp = json.dumps({"district": list(districts)})
    return HttpResponse(resp)


def deosetter(request):
    partner = request.GET.get('partner', None)
    district = request.GET.get('district', None)

    deos = CocoUser.objects.filter(partner_id=partner)
    deos_working_in_selected_district = []
    for deo in deos:
        if deo:
            dist = deo.villages.filter(block__district_id=district)
            if len(dist) > 0:
                deos_working_in_selected_district.append(deo)
    deo_dict = [dict(deo_name=deo.user.username, id=deo.user_id) for deo in deos_working_in_selected_district]
    resp = json.dumps({"deo": list(deo_dict)})
    return HttpResponse(resp)


def deodatasetter(request):
    selecteddeo = request.GET.get('deo',None)
    sdate = request.GET.get ('sdate',None)
    edate = request.GET.get ('edate',None)
    
    slag = "NA"
    alag = "NA"
    
    start_date = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(edate, "%Y-%m-%d")
        
    Screening_objects = Screening.objects.filter(user_created_id=selecteddeo, time_created__range=[start_date, end_date])
    screenings_entrydate = Screening_objects.values_list('time_created', flat=True)
    list_of_screening_entrydates = []
    for screening in screenings_entrydate:
        list_of_screening_entrydates.append(str(screening.date()))
               
    s_dict = dict((i,list_of_screening_entrydates.count(i)) for i in list_of_screening_entrydates)
    
    s_laglist = []
    
    if len(list_of_screening_entrydates)> 0:
        
        for screening in Screening_objects:
            s_lag = screening.time_created.date() - screening.date
            s_laglist.append(s_lag.days)
            
        s_avglag= sum(s_laglist) / float(len(s_laglist))
        
        slag = int(s_avglag)
    
    Adoption_objects = PersonAdoptPractice.objects.filter(user_created_id=selecteddeo, time_created__range=[start_date, end_date])
    adoptions_entrydate = Adoption_objects.values_list('time_created', flat=True)
    list_of_adoption_entrydates = []
    for adoption in adoptions_entrydate:
        list_of_adoption_entrydates.append(str(adoption.date()))
        
    a_dict = dict((i,list_of_adoption_entrydates.count(i)) for i in list_of_adoption_entrydates)
       
    a_laglist = []
    
    if len(list_of_adoption_entrydates)> 0:        
        
        for adoption in Adoption_objects:
            a_lag = adoption.time_created.date() - adoption.date_of_adoption
            a_laglist.append(a_lag.days)

        a_avglag= sum(a_laglist) / float(len(a_laglist))
    
        alag = int(a_avglag)       
   
    persons = Person.objects.filter(user_created_id=selecteddeo, time_created__range=[start_date, end_date]).count()  
    
    return HttpResponse(json.dumps({
        "screenings":s_dict,
        "adoptions": a_dict,
        "persons": persons,
        "slag": slag,
        "alag": alag}),
    content_type="application/json")