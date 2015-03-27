
import dg.settings

import time, codecs
import json, datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from geographies.models import Country, State, District, Block, Village
from programs.models import Partner

from utils.data_library import data_lib
from utils.configuration import categoryDictionary


def home(request):
        
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
    list_combo = str(request.POST.get("list"))
    videolist = str(request.POST.get("list_video"))
    
    val_screening = [request.POST.get("screening_chk")]
    val_adoption = [request.POST.get("adoption_chk")]
    val_no_animator = [request.POST.get("no_animator_chk")]
    val_attendance = [request.POST.get("attendance_chk")]
    val_video_screened_num= [request.POST.get("no_video_screened_chk")]
    val_video_produced_num= [request.POST.get("no_video_produced_chk")]
    
    from_date = [request.POST.get("from_date")]
    to_date = [request.POST.get("to_date")]

    ###############################filter#################################

    checked_list = []

    if(partner[0]== '-1' and partner_chk[0]!=None):
        partner = True
        checked_list.append('partner')
    elif (partner[0]!= '-1' and partner_chk[0]==None) or (partner[0]!= '-1' and partner_chk[0]!=None):
        partner = str(Partner.objects.get(partner_name=partner[0]).id)
    elif(partner[0]== '-1' and partner_chk[0]==None):
        partner = False
   
    if(country[0]=='-1' and country_chk[0]!=None):
        country = True
        checked_list.append('country')
    elif (country[0]!='-1' and country_chk[0]==None) or (country[0]!='-1' and country_chk[0]!=None):
        country = str(Country.objects.get(country_name=country[0]).id)
    elif(country[0]== '-1' and country_chk[0]==None):
        country = False
        
    if(state[0]=='-1' and state_chk[0]!=None):
        state = True
        checked_list.append('state')
    elif (state[0]!= '-1' and state_chk[0]==None) or (state[0]!= '-1' and state_chk[0]!=None):
        state = str(State.objects.get(state_name=state[0]).id)
    elif(state[0]=='-1' and state_chk[0]==None):
        state = False
        
    if(district[0]=='-1' and district_chk[0]!=None):
        district = True
        checked_list.append('district')
    elif (district[0]!='-1' and district_chk[0]==None) or (district[0]!='-1' and district_chk[0]!=None):
        district = str(District.objects.get(district_name=district[0]).id)
    elif(district[0]=='-1' and district_chk[0]==None):
        district = False

    if(block[0]=='-1' and block_chk[0]!=None):
        block = True
        checked_list.append('block')
    elif (block[0]!='-1' and block_chk[0]==None) or (block[0]!='-1' and block_chk[0]!=None):
        block = str(Block.objects.get(block_name=block[0]).id)
    elif(block[0]=='-1' and block_chk[0]==None):
        block = False
        
    if(village[0]=='-1' and village_chk[0]!=None):
        village = True
        checked_list.append('village')
    elif (village[0]!='-1' and village_chk[0]==None) or (village[0]!='-1' and village_chk[0]!=None):
        village_uni = unicode(village[0])
        village = str(Village.objects.filter(village_name=village_uni)[0].id)
    elif(village[0]=='-1' and village_chk[0]==None):
        village = False

    
    ###############################Partition#################################

    
    if (animator_chk[0]==None):
        animator = False
    elif (animator_chk[0] != None):
        animator = True
        checked_list.append('animator')
        
    if (people_chk[0]==None):
        people = False
    elif (people_chk[0] != None):
        people = True
        checked_list.append('people')
        
    if (group_chk[0]==None):
        group = False
    elif (group_chk[0] != None):
        group = True
        checked_list.append('group')
        
    if (video_chk[0]==None):
        video = False
    elif (video_chk[0] != None):
        video = True
        checked_list.append('video')
        
    ###############################Value#################################

    if(val_screening[0]!=None):
        screening = True
    else:
        screening = False
    
    if(val_adoption[0]!=None):
        adoption = True
    else:
        adoption = False

    if(val_no_animator[0]!=None):
        no_animator = True
    else:
        no_animator = False

    if(val_attendance[0]!=None):
        attendance = True
    else:
        attendance = False

    if(val_video_screened_num[0]!=None):
        video_screened_num = True
    else:
        video_screened_num = False

    if(val_video_screened_num[0]!=None):
        video_screened_num = True
    else:
        video_screened_num = False

    if(val_video_produced_num[0]!=None):
        video_produced_num = True
    else:
        video_produced_num = False

    #################################value-partion###########################

    if(list_combo == "None"):
        list_combo = False
        videolist = False

    if(list_combo == 'on'):
    
        for x in checked_list:
            if ((x in categoryDictionary['geographies']) or (x == 'partner')):
                list_combo  = 'numScreening'

            elif (x == "animator"):
                list_combo = 'listAnimator'

            elif (x == "group"):
                list_combo = 'listGroup'

            elif (x == "people"):
                list_combo = 'listPeople'

            elif (x == "video"):
                list_combo = videolist
            
    ##############################Date#################################

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
             'numAnimator':no_animator, 
             'attendance':attendance,
             'numVideoScreened':video_screened_num, 
             'numVideoProduced':video_produced_num,
             'list' : list_combo
            }
     
    #print "----- inside the views----------------"
    
    options = {'partition':partition,'value':value}
    args=[]
    args.append(from_date)
    args.append(to_date)
    dlib = data_lib()
    dataframe_result = dlib.handle_controller(args,options)
    
    #print "--------------FINAL RESULT---------------"
    #print dataframe_result
    #print "--------------GAME OVER-----------------"

    final_html_file=create_excel(dataframe_result)

    return render_to_response('raw_data_analytics/temp_html/'+final_html_file, context_instance=RequestContext(request))


def create_excel(df):

    millis = str(round(time.time() * 1000))
        
    data_file = ''.join([dg.settings.MEDIA_ROOT, '/raw_data_analytics/temp_csv/'+millis+'_library_data.csv'])           
                   
    f = codecs.open(data_file, 'wb', 'utf-8')
    f.close()

    df.to_csv(data_file)

    generated_file_name = data_file.split('/')[-1] 

    html_file = 'dg/templates/raw_data_analytics/temp_html/'+millis+'_library_data.html'
    #html_file ='/home/ubuntu/code/dg_coco_test/dg/dg/templates/raw_data_analytics/temp_html/'+millis+'_library_data.html'
    
    header = '''<html>
                    <head><center>
                        <h2> Data Result </h2>
                        <div name="download_excel">
                            <a href="/media/social_website/uploads/raw_data_analytics/temp_csv/'''+generated_file_name+'''">Download result as an excel file</a>
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



