import json, datetime
#from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from management.commands import partition_library
from django.core import management

from geographies.models import Country, State, District, Block, Village
from programs.models import Partner
#from people.models import Animator

'''import pandas as pd
import MySQLdb
import pandas.io.sql as psql
from management.commands import partition_library
from django.core import management'''


import xml.etree.ElementTree as ET

def home(request):
        
    '''tree = ET.parse('dg/templates/raw_data_analytics/home.xml')
    root = tree.getroot()

    for x in range(len(root)):
        for y in range(len(root[x])):
            print root[x][y].text'''

    countries = Country.objects.all()
   
    partners = Partner.objects.all()

    return render_to_response('raw_data_analytics/output.html', {'countries' : countries, 'partners':partners}, context_instance=RequestContext(request))

    
'''def dropdown(request):
    
    #country_id = Country.objects.get(country_name=[request.POST.get("partner")][0]).id
    #state = State.objects.filter(country=country_id)

    selected_option = request.GET.get('selected', None)
    

    dropdown_items = State.objects.filter(country__country_name = country_selected).values_list('state_name', flat=True)
    
    

    resp = json.dumps([unicode(i) for i in states])
    return HttpResponse(resp)'''


def dropdown1(request):
    
    #country_id = Country.objects.get(country_name=[request.POST.get("partner")][0]).id
    #state = State.objects.filter(country=country_id)

    country_selected = request.GET.get('selected', None)
    

    states = State.objects.filter(country__country_name = country_selected).values_list('state_name', flat=True)
    
    

    resp = json.dumps([unicode(i) for i in states])
    return HttpResponse(resp)

def dropdown2(request):
    
    #country_id = Country.objects.get(country_name=[request.POST.get("partner")][0]).id
    #state = State.objects.filter(country=country_id)

    state_selected = request.GET.get('selected', None)
    

    districts = District.objects.filter(state__state_name = state_selected).values_list('district_name', flat=True)
    
    

    resp = json.dumps([unicode(i) for i in districts])
    return HttpResponse(resp)

def dropdown3(request):
    
    #country_id = Country.objects.get(country_name=[request.POST.get("partner")][0]).id
    #state = State.objects.filter(country=country_id)

    district_selected = request.GET.get('selected', None)
    

    blocks = Block.objects.filter(district__district_name = district_selected).values_list('block_name', flat=True)
    
    

    resp = json.dumps([unicode(i) for i in blocks])
    return HttpResponse(resp)
def dropdown4(request):
    
    #country_id = Country.objects.get(country_name=[request.POST.get("partner")][0]).id
    #state = State.objects.filter(country=country_id)

    block_selected = request.GET.get('selected', None)
    

    villages = Village.objects.filter(block__block_name = block_selected).values_list('village_name', flat=True)
    
    

    resp = json.dumps([unicode(i) for i in villages])
    return HttpResponse(resp)


def execute(request):

    partner = [request.POST.get("partner")]
    country = [request.POST.get("country")]
    state = [request.POST.get("state")]
    district = [request.POST.get("district")]
    block = [request.POST.get("block")]
    village = [request.POST.get("village")]
    #animator =[request.POST.get("animator")]
    
    partner_chk = [request.POST.get("partner_chk")]
    country_chk = [request.POST.get("country_chk")]
    state_chk = [request.POST.get("state_chk")]
    district_chk = [request.POST.get("district_chk")]
    block_chk = [request.POST.get("block_chk")]
    village_chk = [request.POST.get("village_chk")]
    animator_chk = [request.POST.get("animator_chk")]
    people_chk = [request.POST.get("people_chk")]
    group_chk = [request.POST.get("group_chk")]
    
    screening_chk = [request.POST.get("screening_chk")]
    adoption_chk = [request.POST.get("adoption_chk")]
    no_people_chk = [request.POST.get("no_people_chk")]
    list_people_chk = [request.POST.get("list_people_chk")]
    no_animator_chk = [request.POST.get("no_animator_chk")]
    list_animator_chk = [request.POST.get("list_animator_chk")]
    attendance_chk = [request.POST.get("attendance_chk")]
    #group_nos_chk = [request.POST.get("group_nos_chk")]

    from_date = [request.POST.get("from_date")]
    to_date = [request.POST.get("to_date")]

    if(partner[0]== '-1' and partner_chk[0]!=None):
        partner = True 
    elif (partner[0]!= '-1' and partner_chk[0]==None) or (partner[0]!= '-1' and partner_chk[0]!=None):
        partner = str(Partner.objects.get(partner_name=partner[0]).id)
    elif(partner[0]== '-1' and partner_chk[0]==None):
        partner = False
    
    if(country[0]=='-1' and country_chk[0]!=None):
        country = True
    elif (country[0]!='-1' and country_chk[0]==None) or (country[0]!='-1' and country_chk[0]!=None):
        country = str(Country.objects.get(country_name=country[0]).id)
    elif(country[0]== '-1' and country_chk[0]==None):
        country = False
        
    if(state[0]=='-1' and state_chk[0]!=None):
        state = True
    elif (state[0]!= '-1' and state_chk[0]==None) or (state[0]!= '-1' and state_chk[0]!=None):
        state = str(State.objects.get(state_name=state[0]).id)
    elif(state[0]=='-1' and state_chk[0]==None):
        state = False
        
    if(district[0]=='-1' and district_chk[0]!=None):
        district = True
    elif (district[0]!='-1' and district_chk[0]==None) or (district[0]!='-1' and district_chk[0]!=None):
        district = str(District.objects.get(district_name=district[0]).id)
    elif(district[0]=='-1' and district_chk[0]==None):
        district = False

    if(block[0]=='-1' and block_chk[0]!=None):
        block = True
    elif (block[0]!='-1' and block_chk[0]==None) or (block[0]!='-1' and block_chk[0]!=None):
        block = str(Block.objects.get(block_name=block[0]).id)
    elif(block[0]=='-1' and block_chk[0]==None):
        block = False
        
    if(village[0]=='-1' and village_chk[0]!=None):
        village = True
    elif (village[0]!='-1' and village_chk[0]==None) or (village[0]!='-1' and village_chk[0]!=None):
        village_uni = unicode(village[0])
        village = str(Village.objects.filter(village_name=village_uni)[0].id)
    elif(village[0]=='-1' and village_chk[0]==None):
        village = False

    
    '''if(animator[0]=='' and animator_chk[0]!=None):
        animator = True 
    elif (animator[0]!='' and animator_chk[0]==None) or (animator[0]!='' and animator_chk[0]!=None):
        animator = str(Animator.objects.get(name=animator[0]).id)
    elif(animator[0]=='' and animator_chk[0]==None):
        animator = False'''

    if (animator_chk[0]==None):
        animator = False
    elif (animator_chk[0] != None):
        animator = True

    if (people_chk[0]==None):
        people = False
    elif (people_chk[0] != None):
        people = True
    
    if (group_chk[0]==None):
        group = False
    elif (group_chk[0] != None):
        group = True
    

    if(screening_chk[0]!=None):
        screening = True
    else:
        screening = False
    
    if(adoption_chk[0]!=None):
        adoption = True
    else:
        adoption = False

    if(no_people_chk[0]!=None):
        no_people = True
    else:
        no_people = False

    if(list_people_chk[0]!=None):
        list_people = True
    else:
        list_people = False

    if(no_animator_chk[0]!=None):
        no_animator = True
    else:
        no_animator = False

    if(list_animator_chk[0]!=None):
        list_animator = True
    else:
        list_animator = False



    if(from_date[0]!=''):
        from_date = from_date[0]  
    else:
        from_date = '2004-01-01'
        
    if(to_date[0]!=''):
        to_date = to_date[0]
    else:
        now = datetime.datetime.now()
        to_date = '%s-%s-%s' %(now.year, now.month, now.day)
       
    partition={'partner':partner, 'country':country, 'state':state, 'district':district, 'block':block, 'village':village,'animator':animator,'person':people,'persongroup':group}
    value = {'numScreening':screening, 'numAdoption':adoption, 'numPeople':no_people, 'listPeople':list_people, 'numAnimator':no_animator, 'listAnimator':list_animator, 'attendance':attendance_chk }
    print "in views-------------------"
    print partition
    print "----- inside the views----------------"
    print value
    management.call_command('partition_library',from_date, to_date, partition=partition,value=value)

    
    return render_to_response('raw_data_analytics/library_data.html', context_instance=RequestContext(request))



  
    
