import json, datetime

from django.http import HttpResponse

from activities.models import PersonAdoptPractice, Screening
from coco.models import CocoUser
from people.models import Person
from programs.models import Partner

def partnersetter(request):
    partners = Partner.objects.values('partner_name','id')
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
                deos_working_in_selected_district.append(deo.user.username)
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
    
    '''screeningtelecast = Screening.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).values_list('date', flat=True)
    listofscreeningtelecastdates = []
    for tscreening in screeningtelecast:
        ndate = datetime.datetime.strptime(tscreening, "%Y-%m-%d")
        listofscreeningtelecastdates.append(ndate)    
    print listofscreeningtelecastdates;'''

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