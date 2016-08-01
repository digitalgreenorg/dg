import dg.settings

import time, codecs
import json, datetime
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test

from dg.settings import PERMISSION_DENIED_URL

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from videos.models import *
from geographies.models import Country, State, District, Block, Village
from programs.models import Partner
from utils.data_library import data_lib
from utils.configuration import categoryDictionary, orderDictionary
from  programs import *


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='data_extractor').count() > 0,
                  login_url=PERMISSION_DENIED_URL)
@csrf_protect
def home(request):
    countries = Country.objects.all()

    partners = Partner.objects.all()

    return render_to_response('raw_data_analytics/output.html', {'countries': countries, 'partners': partners},
                              context_instance=RequestContext(request))


def dropdown_state(request):
    country_selected = request.GET.get('selected', None)
    states = State.objects.filter(country__country_name=country_selected).values_list('state_name', flat=True)
    resp = json.dumps([unicode(i) for i in states])

    return HttpResponse(resp)


def dropdown_district(request):
    state_selected = request.GET.get('selected', None)
    districts = District.objects.filter(state__state_name=state_selected).values_list('district_name', flat=True)
    resp = json.dumps([unicode(i) for i in districts])

    return HttpResponse(resp)


def dropdown_block(request):
    district_selected = request.GET.get('selected', None)
    blocks = Block.objects.filter(district__district_name=district_selected).values_list('block_name', flat=True)
    resp = json.dumps([unicode(i) for i in blocks])

    return HttpResponse(resp)


def dropdown_village(request):
    block_selected = request.GET.get('selected', None)
    villages = Village.objects.filter(block__block_name=block_selected).values_list('village_name', flat=True)
    resp = json.dumps([unicode(i) for i in villages])

    return HttpResponse(resp)


def dropdown_video(request):
    partner_selected = request.GET.get('selected', None)
    videos = Video.objects.filter(partner__partner_name=partner_selected).values_list('title', flat=True)  # todo

    resp = json.dumps([unicode(i) for i in videos])

    return HttpResponse(resp)


def execute(request):
    partner = request.POST.getlist("partner")
    country = request.POST.getlist("country")
    state = request.POST.getlist("state")
    district = request.POST.getlist("district")
    block = request.POST.getlist("block")
    village = request.POST.getlist("village")
    video = request.POST.getlist("video")

    filterDict = {
        'partner': partner,
        'country': country,
        'state': state,
        'district': district,
        'block': block,
        'village': village,
        'video': video
    }

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

    partitionDict = {
        'partner_chk': partner_chk,
        'country_chk': country_chk,
        'state_chk': state_chk,
        'district_chk': district_chk,
        'block_chk': block_chk,
        'village_chk': village_chk,
        'animator_chk': animator_chk,
        'people_chk':people_chk,
        'group_chk': group_chk,
        'video_chk': video_chk,
        'list_combo': list_combo,
        'videolist':videolist
    }

    val_screening = [request.POST.get("screening_chk")]
    val_adoption = [request.POST.get("adoption_chk")]
    val_no_animator = [request.POST.get("no_animator_chk")]
    val_attendance = [request.POST.get("attendance_chk")]
    val_video_screened_num = [request.POST.get("no_video_screened_chk")]
    val_video_produced_num = [request.POST.get("no_video_produced_chk")]

    valueDict = {
        'val_screening':val_screening,
        'val_adoption': val_adoption,
        'val_val_no_animator': val_no_animator,
        'val_attendance':val_attendance,
        'val_video_screened_num':val_video_screened_num,
        'val_video_produced_num':val_video_produced_num
    }

    from_date = [request.POST.get("from_date")]
    to_date = [request.POST.get("to_date")]

    ###############################filter#################################

    checked_list = []


    # print partner
    if (len(partner) == 0 and partner_chk[0] != None):
        partner = True
        checked_list.append('partner')
    elif (len(partner) > 0 and partner_chk[0] == None) or (len(partner) >0 and partner_chk[0] != None):
        partner=Partner.objects.filter(partner_name__in=partner)
        partnerTemp =[]
        for partnerObject in partner :
            partnerTemp.append(str(partnerObject.id))
        partner = partnerTemp
     #   print partner
    elif (len(partner)== 0 and partner_chk[0] == None):
        partner = False


    if (len(country) == 0 and country_chk[0] != None):
        country = True
        checked_list.append('country')
    elif (len(country) > 0 and country_chk[0] == None) or (len(country) >0  and country_chk[0] != None):
        country=Country.objects.filter(country_name__in=country)
        countryTemp=[]
        for countryObject in country :
            countryTemp.append(str(countryObject.id))
        country = countryTemp
    elif (len(country) == 0 and country_chk[0] == None):
        country = False


    if (len(state) == 0  and state_chk[0] != None):
        state = True
        checked_list.append('state')
    elif (len(state) > 0 and state_chk[0] == None) or (len(state) > 0 and state_chk[0] != None):
        state = State.objects.filter(state_name__in=state)
        stateTemp=[]
        for stateObject in state:
            stateTemp.append(str(stateObject.id))
        state = stateTemp
    elif (len(state) == 0 and state_chk[0] == None):
        state = False


    if (len(district)==0 and district_chk[0] != None):
        district = True
        checked_list.append('district')
    elif (len(district)>0 and district_chk[0] == None) or (len(district)>0 and district_chk[0] != None):
        district=District.objects.filter(district_name__in=district)
        districtTemp=[]
        for districtObject in district:
            districtTemp.append(str(districtObject.id))
        district = districtTemp
    elif ( len(district)==0 and district_chk[0] == None):
        district = False


    if (len(block) == 0 and block_chk[0] != None):
        block = True
        checked_list.append('block')
    elif (len(block) > 0 and block_chk[0] == None) or (len(block) > 0 and block_chk[0] != None):
        block=Block.objects.filter(block_name__in=block)
        blockTemp=[]
        for blockObject in block :
            blockTemp.append(str(blockObject.id))
        block = blockTemp
    elif (len(block) == 0 and block_chk[0] == None):
        block = False


    if (len(village) == 0 and village_chk[0] != None):
        village = True
        checked_list.append('village')
    elif (len(village) >0 and village_chk[0] == None) or (len(village) > 0 and village_chk[0] != None):
        #village_uni = unicode(village)
        village = Village.objects.filter(village_name__in=village)
        villageTemp = []
        for villageObject in village:
            villageTemp.append(str(villageObject.id))
        village = villageTemp
    elif (len(village) == 0 and village_chk[0] == None):
        village = False


    if (len(video) == 0 and video_chk[0] != None):
        video = True
        checked_list.append('video')
    elif (len(video) > 0 and video_chk[0] == None) or (len(video) > 0 and video_chk[0] != None):
        video = video.objects.filter(title__in=video)
        videoTemp = []
        for videoObject in video:
            videoTemp.append(str(videoObject.id))
        video = videoTemp
    elif(len(video) == 0 and video_chk[0]==None):
        video = False


    ###############################Partition#################################
    

    if (animator_chk[0] == None):
        animator = False
    elif (animator_chk[0] != None):
        animator = True
        checked_list.append('animator')

    if (people_chk[0] == None):
        person = False
    elif (people_chk[0] != None):
        person = True
        checked_list.append('person')

    if (group_chk[0] == None):
        group = False
    elif (group_chk[0] != None):
        group = True
        checked_list.append('persongroup')

    if (video_chk[0] == None):
        video = False
    elif (video_chk[0] != None):
        video = True
        checked_list.append('video')

    ###############################Value#################################

    if (val_screening[0] != None):
        screening = True
    else:
        screening = False

    if (val_adoption[0] != None):
        adoption = True
    else:
        adoption = False

    if (val_no_animator[0] != None):
        no_animator = True
    else:
        no_animator = False

    if (val_attendance[0] != None):
        attendance = True
    else:
        attendance = False

    if (val_video_screened_num[0] != None):
        video_screened_num = True
    else:
        video_screened_num = False

    if (val_video_screened_num[0] != None):
        video_screened_num = True
    else:
        video_screened_num = False

    if (val_video_produced_num[0] != None):
        video_produced_num = True
    else:
        video_produced_num = False

    #################################value-partion###########################

    if (list_combo == "None"):
        list_combo = False
        videolist = False

    priority = {}

    if (list_combo == 'on'):
        for x in checked_list:
            if ((x in categoryDictionary['geographies']) or (x == 'partner')):
                for x, v in orderDictionary.items():
                    if x in checked_list:
                        priority[x] = v
                list_combo = 'list' + (max(priority.items(), key=lambda x: x[1])[0]).title()

            elif (x == "animator"):
                list_combo = 'listAnimator'

            elif (x == "persongroup"):
                list_combo = 'listGroup'

            elif (x == "person"):
                list_combo = 'listPerson'

            elif (x == "video"):
                list_combo = videolist

    ##############################Date#################################

    if (from_date[0] != ''):
        from_date = from_date[0]
    else:
        from_date = '2004-01-01'

    if (to_date[0] != ''):
        to_date = to_date[0]
    else:
        now = datetime.datetime.now()
        to_date = '%s-%s-%s' % (now.year, now.month, now.day)

    partition = {
        'partner': partner,
        'country': country,
        'state': state,
        'district': district,
        'block': block,
        'village': village,
        'animator': animator,
        'person': person,
        'persongroup': group,
        'video': video
    }

    value = {
        'numScreening': screening,
        'numAdoption': adoption,
        'numAnimator': no_animator,
        'attendance': attendance,
        'numVideoScreened': video_screened_num,
        'numVideoProduced': video_produced_num,
        'list': list_combo
    }

    options = {'partition': partition, 'value': value}

    args = []
    args.append(from_date)
    args.append(to_date)
    dlib = data_lib()
    #print options
    if options['value']['list'] == 'on':
        error = 'Output cannot be generated for this input ! Please check filters and partition field !!'
        return render_to_response("raw_data_analytics/error.html", {'error': error},
                                  context_instance=RequestContext(request))

    else:
        if not list(filter(lambda a: a != False, partition.values())):
            error = 'Please select atleast one partition field!!'
            return render_to_response("raw_data_analytics/error.html", {'error': error},
                                      context_instance=RequestContext(request))

        else:

            dataframe_result = dlib.handle_controller(args, options)
            if len(dataframe_result.index) == 0:
                error = 'No data available for given input!!'
                return render_to_response("raw_data_analytics/error.html", {'error': error},
                                          context_instance=RequestContext(request))

            else:
                df = dataframe_result.to_json()
                return render_to_response('raw_data_analytics/result.html', {'from_date': from_date, 'to_date': to_date,
                                                                             'dataf': unicode(df, errors='ignore')},
                                          context_instance=RequestContext(request))
