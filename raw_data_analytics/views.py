import json, datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from geographies.models import Country, State, District, Block, Village
from programs.models import Partner
from people.models import Animator

import pandas as pd
import MySQLdb
import pandas.io.sql as psql
from management.commands import partition_library
from django.core import management
import datetime



def home(request):
        
    return render_to_response('raw_data_analytics/output.html', context_instance=RequestContext(request))

    
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
    #animator_chk = [request.POST.get("animator_chk")]
    
    screening_chk = [request.POST.get("screening_chk")]
    adoption_chk = [request.POST.get("adoption_chk")]

    from_date = [request.POST.get("from_date")]
    to_date = [request.POST.get("to_date")]

    if(partner[0]=='' and partner_chk[0]!=None):
        partner = True 
    elif (partner[0]!='' and partner_chk[0]==None) or (partner[0]!='' and partner_chk[0]!=None):
        partner = str(Partner.objects.get(partner_name=partner[0]).id)
    elif(partner[0]=='' and partner_chk[0]==None):
        partner = False
    
    if(country[0]=='' and country_chk[0]!=None):
        country = True
    elif (country[0]!='' and country_chk[0]==None) or (country[0]!='' and country_chk[0]!=None):
        country = str(Country.objects.get(country_name=country[0]).id)
    elif(country[0]=='' and country_chk[0]==None):
        country = False
        
    if(state[0]=='' and state_chk[0]!=None):
        state = True
    elif (state[0]!='' and state_chk[0]==None) or (state[0]!='' and state_chk[0]!=None):
        state = str(State.objects.get(state_name=state[0]).id)
    elif(state[0]=='' and state_chk[0]==None):
        state = False
        
    if(district[0]=='' and district_chk[0]!=None):
        district = True
    elif (district[0]!='' and district_chk[0]==None) or (district[0]!='' and district_chk[0]!=None):
        district = str(District.objects.get(district_name=district[0]).id)
    elif(district[0]=='' and district_chk[0]==None):
        district = False

    if(block[0]=='' and block_chk[0]!=None):
        block = True
    elif (block[0]!='' and block_chk[0]==None) or (block[0]!='' and block_chk[0]!=None):
        block = str(Block.objects.get(block_name=block[0]).id)
    elif(block[0]=='' and block_chk[0]==None):
        block = False
        
    if(village[0]=='' and village_chk[0]!=None):
        village = True
    elif (village[0]!='' and village_chk[0]==None) or (village[0]!='' and village_chk[0]!=None):
        village = str(Village.objects.get(village_name=village[0]).id)
    elif(village[0]=='' and village_chk[0]==None):
        village = False

    
    '''if(animator[0]=='' and animator_chk[0]!=None):
        animator = True 
    elif (animator[0]!='' and animator_chk[0]==None) or (animator[0]!='' and animator_chk[0]!=None):
        animator = str(Animator.objects.get(name=animator[0]).id)
    elif(animator[0]=='' and animator_chk[0]==None):
        animator = False'''



    if(screening_chk[0]!=None):
        screening = True
    else:
        screening = False
    
    if(adoption_chk[0]!=None):
        adoption = True
    else:
        adoption = False

    if(from_date[0]!=''):
        from_date = from_date[0]  
    else:
        from_date = '2004-01-01'
        
    if(to_date[0]!=''):
        to_date = to_date[0]
    else:
        now = datetime.datetime.now()
        to_date = '%s-%s-%s' %(now.year, now.month, now.day)
       
    partition={'partner':partner, 'country':country, 'state':state, 'district':district, 'block':block, 'village':village} #,'animator':animator}
    value = {'numScreening':screening, 'numAdoption':adoption}
    print "in views-------------------"
    print partition
    print "----- inside the views----------------"
    print value
    management.call_command('partition_library',from_date, to_date, partition=partition,value=value)


#def df_html_download(request):
    header = '''<html>
                    <head>
                        <h2> Data Result </h2>
                        <div name="download_excel">
                            <a href="/raw_data_analytics/download">Download result as an excel file</a>
                        </div>
                    </head>
                    <body>'''
    footer = '''</body></html>'''

    html_file = 'dg/templates/raw_data_analytics/library_data.html'

    with open(html_file, 'w') as f:
        f.write(header)
        #f.write(df.to_html(classes='df'))
        f.write(footer)


#    df.to_html('dg/templates/raw_data_analytics/library_data.html')

    
    return render_to_response('raw_data_analytics/library_data.html', context_instance=RequestContext(request))



  
    
