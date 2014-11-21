import json, datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from geographies.models import District, Block
import pandas as pd
import MySQLdb
import pandas.io.sql as psql
from management.commands import test_lib



def home(request):
    
    partner = [request.POST.get("partner")]
    country = [request.POST.get("country")]
    state = [request.POST.get("state")]
    district = [request.POST.get("district")]
    block = [request.POST.get("block")]
    village = [request.POST.get("village")]  
    
    partner_chk = [request.POST.get("partner_chk")]
    country_chk = [request.POST.get("country_chk")]
    state_chk = [request.POST.get("state_chk")]
    district_chk = [request.POST.get("district_chk")]
    block_chk = [request.POST.get("block_chk")]
    village_chk = [request.POST.get("village_chk")]

    screening_chk = [request.POST.get("screening_chk")]
    adoption_chk = [request.POST.get("adoption_chk")]
    
    if(partner[0]=='' and partner_chk[0]!=None):
        partner = True 
    elif (len(partner)>0 and partner_chk[0]==None) or (len(partner)>0 and partner_chk[0]!=None):
        partner = partner[0]
    
    if(country[0]=='' and country_chk[0]!=None):
        country = True
    elif (len(country)>0 and country_chk[0]==None) or (len(country)>0 and country_chk[0]!=None):
        country = country[0]
        
    if(state[0]=='' and state_chk[0]!=None):
        state = True
    elif (len(state)>0 and state_chk[0]==None) or (len(state)>0 and state_chk[0]!=None):
        state = state[0]
        
    if(district[0]=='' and district_chk[0]!=None):
        district = True
    elif (len(district)>0 and district_chk[0]==None) or (len(district)>0 and district_chk[0]!=None):
        district = district[0]

    if(block[0]=='' and block_chk[0]!=None):
        block = True
    elif (len(block)>0 and block_chk[0]==None) or (len(block)>0 and block_chk[0]!=None):
        block = block[0]
        
    if(village[0]=='' and village_chk[0]!=None):
        village = True
    elif (len(village)>0 and village_chk[0]==None) or (len(village)>0 and village_chk[0]!=None):
        village = village[0]

    if(screening_chk[0]!=None):
        screening = True
    else:
        screening = False
    
    if(adoption_chk[0]!=None):
        adoption = True
    else:
        adoption = False

    partition={'partner':partner, 'country':country, 'state':state, 'district':district, 'block':block, 'village':village}
    value = {'nScreening':screening, 'nAdoption':adoption}

    test_lib.Command.handle(partition,value)
    
    return render_to_response('raw_data_analytics/output.html', context_instance=RequestContext(request))



  
    
