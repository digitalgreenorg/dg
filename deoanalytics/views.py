import json, datetime

from django.http import HttpResponse

from activities.models import PersonAdoptPractice, Screening
from coco.models import CocoUser
from people.models import Person
from programs.models import Partner

def partnersetter(request):
    partners = Partner.objects.values('partner_name','id').order_by('partner_name')
    return HttpResponse(json.dumps(list(partners)), mimetype="application/json")
        
def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = Person.objects.select_related().filter(partner_id=selectedpartner).values_list('village__block__district__district_name', flat=True).distinct()
    return HttpResponse(json.dumps(list(districts)), mimetype="application/json")

def deosetter(request):
    selectedpartner = request.GET.get('partner', None)
    selecteddistrict = request.GET.get('district', None)
    
    deos = CocoUser.objects.filter(partner_id=selectedpartner)
    deos_working_in_selected_district = []
    for deo in deos:
        if deo:
            dist = deo.villages.filter(block__district__district_name=selecteddistrict)
            if len(dist) > 0:
                deos_working_in_selected_district.append(deo)
    resp = [dict(deo_name=deo.user.username, deo_id=deo.user.id) for deo in deos_working_in_selected_district]
    return HttpResponse(json.dumps(list(resp)), mimetype="application/json")

def deodatasetter(request):
    selecteddeo = request.GET.get('deo',None)
    sdate = request.GET.get ('sdate',None)
    edate = request.GET.get ('edate',None)
    
    slag = "NA"
    alag = "NA"
    
    start_date = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(edate, "%Y-%m-%d")
        
    Screening_objects = Screening.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date])
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
    
    Adoption_objects = PersonAdoptPractice.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date])
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
   
    persons = Person.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).count()  
    
    return HttpResponse(json.dumps({
        "screenings":s_dict,
        "adoptions": a_dict,
        "persons": persons,
        "slag": slag,
        "alag": alag}),
    content_type="application/json")