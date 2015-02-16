
import dg.settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from geographies.models import Country, State, District, Block, Village
from programs.models import Partner

from utils.data_library import data_lib

import time, codecs
import json, datetime
import pandas as pd

'''import MySQLdb
import pandas.io.sql as psql
from management.commands import partition_library
from django.core import management'''


#import xml.etree.ElementTree as ET

def home(request):
        
    ''''tree = ET.parse('dg/templates/raw_data_analytics/home.xml')
    root = tree.getroot()

    for x in range(len(root)):
        for y in range(len(root[x])):
            print root[x][y].text'''

    countries = Country.objects.all()
   
    partners = Partner.objects.all()

    return render_to_response('raw_data_analytics/output.html', {'countries' : countries, 'partners':partners}, context_instance=RequestContext(request))

    
def dropdown_state(request):
    
    country_selected = request.GET.get('selected', None)
    states = State.objects.filter(country__country_name = country_selected).values_list('state_name', flat=True)
    resp = json.dumps([unicode(i) for i in states])
    return HttpResponse(resp)

def dropdown_district(request):
    
    state_selected = request.GET.get('selected', None)
    districts = District.objects.filter(state__state_name = state_selected).values_list('district_name', flat=True)
    resp = json.dumps([unicode(i) for i in districts])
    return HttpResponse(resp)

def dropdown_block(request):
    
    district_selected = request.GET.get('selected', None)
    blocks = Block.objects.filter(district__district_name = district_selected).values_list('block_name', flat=True)
    resp = json.dumps([unicode(i) for i in blocks])
    return HttpResponse(resp)

def dropdown_village(request):
    
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
    
    partner_chk = [request.POST.get("partner_chk")]
    country_chk = [request.POST.get("country_chk")]
    state_chk = [request.POST.get("state_chk")]
    district_chk = [request.POST.get("district_chk")]
    block_chk = [request.POST.get("block_chk")]
    village_chk = [request.POST.get("village_chk")]
    animator_chk = [request.POST.get("animator_chk")]
    people_chk = [request.POST.get("people_chk")]
    group_chk = [request.POST.get("group_chk")]
    video_chk = [request.POST.get("video_chk")]
    
    val_screening = [request.POST.get("screening_chk")]
    val_adoption = [request.POST.get("adoption_chk")]
    #val_adoption_list = [request.POST.get("adoption_list_chk")]
    val_no_people = [request.POST.get("no_people_chk")]
    #val_list_people = [request.POST.get("list_people_chk")]
    val_no_animator = [request.POST.get("no_animator_chk")]
    #val_list_animator = [request.POST.get("list_animator_chk")]
    val_attendance = [request.POST.get("attendance_chk")]
    #val_attendees_list = [request.POST.get("attendance_list_chk")]
    val_video_screened_num= [request.POST.get("no_video_screened_chk")]
    #val_video_screened_list= [request.POST.get("list_video_screened_chk")]
    val_video_produced_num= [request.POST.get("no_video_produced_chk")]
    #val_video_produced_list= [request.POST.get("list_video_produced_chk")]

    from_date = [request.POST.get("from_date")]
    to_date = [request.POST.get("to_date")]

    ###############################filter#################################

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

    
    ###############################Partition#################################

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

    if (video_chk[0]==None):
        video = False
    elif (video_chk[0] != None):
        video = True
    
    ###############################Value#################################

    if(val_screening[0]!=None):
        screening = True
    else:
        screening = False
    
    if(val_adoption[0]!=None):
        adoption = True
    else:
        adoption = False

    '''if(val_adoption_list[0]!=None):
        adopter_list = True
    else:
        adopter_list = False'''


    '''if(val_no_people[0]!=None):
        no_people = True
    else:
        no_people = False'''

    '''if(val_list_people[0]!=None):
        list_people = True
    else:
        list_people = False'''

    if(val_no_animator[0]!=None):
        no_animator = True
    else:
        no_animator = False

    '''if(val_list_animator[0]!=None):
        list_animator = True
    else:
        list_animator = False'''

    if(val_attendance[0]!=None):
        attendance = True
    else:
        attendance = False

    '''if(val_attendees_list[0]!=None):
        attendees_list = True
    else:
        attendees_list = False'''

    if(val_video_screened_num[0]!=None):
        video_screened_num = True
    else:
        video_screened_num = False

    '''if(val_video_screened_list[0]!=None):
        video_screened_list = True
    else:
        video_screened_list = False'''


    if(val_video_produced_num[0]!=None):
        video_produced_num = True
    else:
        video_produced_num = False

    '''if(val_video_produced_list[0]!=None):
        video_produced_list = True
    else:
        video_produced_list = False'''

    ###############################Date#################################


    if(from_date[0]!=''):
        from_date = from_date[0]  
    else:
        from_date = '2004-01-01'
        
    if(to_date[0]!=''):
        to_date = to_date[0]
    else:
        now = datetime.datetime.now()
        to_date = '%s-%s-%s' %(now.year, now.month, now.day)
       
    

    partition={
               'partner':partner,
               'country':country, 
               'state':state, 
               'district':district, 
               'block':block, 
               'village':village,
               'animator':animator,
               'person':people,
               'persongroup':group, 
               'video':video
              }

    value = {
             'numScreening':screening, 
             'numAdoption':adoption,
           #  'listAdopter':adopter_list, 
             #'numPeople':no_people, 
            # 'listPeople':list_people, 
             'numAnimator':no_animator, 
             #'listAnimator':list_animator, 
             'attendance':attendance,
             #'listAttendees':attendees_list,
             'numVideoScreened':video_screened_num, 
             #'listVideoScreened':video_screened_list,
             'numVideoProduced':video_produced_num,
             #'listVideoProduced':video_produced_list 
            }
    
    print "----- inside the views----------------"
    
    options = {'partition':partition,'value':value}
    args=[]
    args.append(from_date)
    args.append(to_date)
    dlib = data_lib()
    dataframe_result = dlib.handle_controller(args,options)
    
    print "--------------FINAL RESULT---------------"
    print dataframe_result
    print "--------------GAME OVER-----------------"

    final_html_file=create_excel(dataframe_result)

    return render_to_response('raw_data_analytics/'+final_html_file, context_instance=RequestContext(request))



def create_excel(df):

    millis = str(round(time.time() * 1000))
        
    try:
        data_file = ''.join([dg.settings.MEDIA_ROOT, '/raw_data_analytics/'+millis+'_library_data.xlsx'])
        f= open(data_file,'wb')
        f.close()

        writer = pd.ExcelWriter(data_file, engine = 'xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    except Exception:
        data_file = ''.join([dg.settings.MEDIA_ROOT, '/raw_data_analytics/'+millis+'_library_data.csv'])           
                       

        f = codecs.open(data_file, 'wb', 'utf-8')
        f.close()

        df.to_csv(data_file)

    generated_file_name = data_file.split('/')[-1] 

    html_file = 'dg/templates/raw_data_analytics/'+millis+'_library_data.html'
    
    header = '''<html>
                    <head><center>
                        <h2> Data Result </h2>
                        <div name="download_excel">
                            <a href="/media/social_website/uploads/raw_data_analytics/'''+generated_file_name+'''">Download result as an excel file</a>
                        </div></center>
                    </head>
                    <body></br></br></br></br>'''
    footer = '''</body></html>'''

    f = codecs.open(html_file, 'wb', 'utf-8')
    f.write(header)
    f.write(df.to_html())
    f.write(footer)
    f.close()
    
    final_html_file = millis+'_library_data.html'

    return final_html_file























            