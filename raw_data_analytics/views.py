import dg.settings

import json
import time, codecs
import json, datetime
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test

from dg.settings import PERMISSION_DENIED_URL

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from activities.models import *
from videos.models import *
from geographies.models import Country, State, District, Block, Village
from programs.models import Partner
from utils.data_library import data_lib
from utils.configuration import categoryDictionary, orderDictionary
from  programs import *

import MySQLdb
from output.database.utility import *
dlib = None
@login_required()
@user_passes_test(lambda u: u.groups.filter(name='data_extractor').count() > 0,
                  login_url=PERMISSION_DENIED_URL)
@csrf_protect
def home(request):
    countries = Country.objects.filter().values_list('country_name',flat=True)

    return render_to_response('raw_data_analytics/output.html', {'countries': countries},
                              context_instance=RequestContext(request))
                              
def onrun_query(query):
    mysql_cn = MySQLdb.connect(host=dg.settings.DATABASES['default']['HOST'], port=dg.settings.DATABASES['default']['PORT'], user=dg.settings.DATABASES['default']['USER'],
                                   passwd=dg.settings.DATABASES['default']['PASSWORD'],
                                   db=dg.settings.DATABASES['default']['NAME'],
                                    charset = 'utf8',
                                     use_unicode = True)
    cursor = mysql_cn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    mysql_cn.close()
    return result
def dropdown_partner(request):
    countrys= request.GET.getlist('country[]')
    country_selected = Country.objects.filter(country_name__in=countrys).values_list('id',flat=True)
    states = request.GET.getlist('state[]')
    state_selected = State.objects.filter(state_name__in=states).values_list('id',flat=True)
    districts = request.GET.getlist('district[]')
    district_selected = District.objects.filter(district_name__in=districts).values_list('id',flat=True)
    blocks = request.GET.getlist('block[]')
    block_selected = Block.objects.filter(block_name__in=blocks).values_list('id',flat=True)
    filter_dict={}
    final_dict ={'Country':country_selected,'State':state_selected,'District':district_selected,'Block':block_selected}
    for keys in final_dict:
        if len(final_dict[keys]) != 0:
            filter_dict[keys] = final_dict[keys]
    if filter_dict:
        sql_ds = get_init_sql_ds()
        sql_ds['select'].extend(["DISTINCT P.PARTNER_NAME"])
        sql_ds['from'].append("village_partner_myisam vcp")
        sql_ds['join'].append(["programs_partner P", "P.id = vcp.partner_id"])
        for keys in filter_dict:
            if(filter_dict[keys]):
                sql_ds['where'].append('vcp.'+keys.lower()+'_id in ( '+ ' , '.join(str(dictVal) for dictVal in filter_dict[keys])+' )')
        sql_ds['order by'].append("P.PARTNER_NAME")

        select_query = 'select ' + ', '.join( selectVal for selectVal in sql_ds['select'] )
        from_query =  ' from '+ ', '.join(fromVal for fromVal in sql_ds['from'])
        join_query =  ' inner join ' +' on '.join(joinVal for joinVal in sql_ds['join'][0])
        where_query = ' where '+' and '.join(whereVal for whereVal in sql_ds['where'])
        order_query = ' order by '+', '.join(orderVal for orderVal in sql_ds['order by'])
        query = select_query+from_query+join_query+where_query+order_query
        partners = onrun_query(query)
    else:
        partners = Partner.objects.filter().values_list('partner_name')

    resp = json.dumps([partner for partner in partners])
    return HttpResponse(resp)

def dropdown_category(request):
    categorys = Category.objects.filter().values_list('category_name', flat=True)
    resp = json.dumps([unicode(category) for category in categorys])
    return HttpResponse(resp)

def dropdown_subcategory(request):
    category_selected = request.GET.getlist('selected[]')
    subcategorys = SubCategory.objects.filter(category__category_name__in=category_selected).values_list('subcategory_name', flat=True)
    resp = json.dumps([unicode(subcategory) for subcategory in subcategorys])
    return HttpResponse(resp)

def dropdown_videop(request):
    subcategory_selected = request.GET.getlist('selected[]')
    videops = VideoPractice.objects.filter(subcategory__subcategory_name__in=subcategory_selected).values_list('videopractice_name', flat=True)
    resp = json.dumps([unicode(videop) for videop in videops])
    return HttpResponse(resp)

def dropdown_tag(request):
    tags=Tag.objects.filter().values_list('tag_name',flat=True)
    resp=json.dumps([unicode(tag) for tag in tags])
    return HttpResponse(resp)

def dropdown_state(request):
    country_selected = request.GET.getlist('selected[]')
    states = State.objects.filter(country__country_name__in=country_selected).values_list('state_name', flat=True)
    resp = json.dumps([unicode(state) for state in states])

    return HttpResponse(resp)


def dropdown_district(request):
    state_selected = request.GET.getlist('selected[]')
    districts = District.objects.filter(state__state_name__in=state_selected).values_list('district_name', flat=True)
    resp = json.dumps([unicode(district) for district in districts])
    return HttpResponse(resp)


def dropdown_block(request):
    district_selected = request.GET.getlist('selected[]')
    blocks = Block.objects.filter(district__district_name__in=district_selected).values_list('block_name', flat=True)
    resp = json.dumps([unicode(block) for block in blocks])
    return HttpResponse(resp)


def dropdown_village(request):
    block_selected = request.GET.getlist('selected[]')
    villages = Village.objects.filter(block__block_name__in=block_selected).values_list('village_name', flat=True)
    resp = json.dumps([unicode(village) for village in villages])
    return HttpResponse(resp)


def dropdown_video(request):
    country_selected = request.GET.getlist('country[]')
    partner_selected = request.GET.getlist('partner[]')
    state_selected = request.GET.getlist('state[]')
    district_selected = request.GET.getlist('district[]')
    block_selected = request.GET.getlist('block[]')
    village_selected = request.GET.getlist('village[]')

    filter_dict ={'village__block__district__state__country__country_name__in':country_selected,'village__block__district__state__state_name__in':state_selected,'partner__partner_name__in':partner_selected}
    final_dict ={}
    videos = []

    for keys in filter_dict:
        if filter_dict[keys][0]!='':
            final_dict[keys]=filter_dict[keys]
    if final_dict:
            videos = list(Video.objects.filter(**final_dict).values_list('title','id'))
            video_screened = list(Screening.objects.filter(**final_dict).distinct().values_list('videoes_screened__title','videoes_screened__id'))
            videos.extend(video_screened)

    if partner_selected[0]!='':
        if not videos:
            videos = list(Video.objects.filter(partner__partner_name__in=partner_selected).values_list('title','id'))
        else:
            final_dict['partner__partner_name__in']=partner_selected
            video = (list(Video.objects.filter(**final_dict).values_list('title','id')))
            video_screened = list(Screening.objects.filter(**final_dict).distinct().values_list('videoes_screened__title','videoes_screened__id'))
            videos.extend(video)
            videos.extend(video_screened)


    elif not videos:
        videos = list(Video.objects.filter().values_list('title','id'))

    resp = json.dumps([video for video in videos])
    return HttpResponse(resp)

def execute(request):

    range_date = [request.POST.get("daterange")]
    for date in range_date:
        date_range=date.split('-')
    partner = request.POST.getlist("partner")
    country = request.POST.getlist("country")
    state = request.POST.getlist("state")
    district = request.POST.getlist("district")
    block = request.POST.getlist("block")
    village = request.POST.getlist("village")
    video = request.POST.getlist("video")

    category=request.POST.getlist("category")
    subcategory=request.POST.getlist("subcategory")
    videop=request.POST.getlist("videop")
    tag=request.POST.getlist("tag")

    
    if not video:
        filter_dict ={'category__category_name__in':category,'subcategory__subcategory_name__in':subcategory,'videopractice__videopractice_name__in':videop,'tags__tag_name__in':tag,'partner__partner_name__in':partner}
        final_dict ={}
        video = []
        for key in filter_dict:
            if  filter_dict[key]:
                final_dict[key]=filter_dict[key]
            if final_dict:
                video=Video.objects.filter(**final_dict).values_list('title')
        

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
    number_block_combo = str(request.POST.get("blocknum"))
    number_village_combo = str(request.POST.get("villagenum"))
    number_block = str(request.POST.get("blocknumber_video"))
    number_village = str(request.POST.get("villagenumber_video"))



    val_screening = [request.POST.get("screening_chk")]
    val_adoption = [request.POST.get("adoption_chk")]
    val_no_animator = [request.POST.get("no_animator_chk")]
    val_attendance = [request.POST.get("attendance_chk")]
    val_video_screened_num = [request.POST.get("no_video_screened_chk")]
    val_video_produced_num = [request.POST.get("no_video_produced_chk")]



    
    # to_date = [request.POST.get("to_date")]

#####################Dictionary for Generic  #################################
    dict ={'partner':[partner,partner_chk,'partner_name',Partner],
        'country':[country,country_chk,'country_name',Country],
        'state':[state,state_chk,'state_name',State],
        'district':[district,district_chk,'district_name',District],
        'block':[block,block_chk,'block_name',Block],
        'village':[village,village_chk,'village_name',Village],
        'video':[video,video_chk,'title',Video]
        }

    

    ###############################filter#################################

    checked_list = []

    for keys in dict:
        if (len(dict[keys][0]) == 0 and dict[keys][1][0] != None):
            dict[keys][0] = True
            checked_list.append(str(keys))
        elif len(dict[keys][0]) > 0 :
            query = dict[keys][2]+'__in'
            dict[keys][0]=dict[keys][3].objects.filter(**{query:dict[keys][0]})
            Temp =[]
            for partitionObject in dict[keys][0] :
                Temp.append(str(partitionObject.id))
                dict[keys][0] = Temp
        elif (len(dict[keys][0])== 0 and dict[keys][1][0] == None):
            dict[keys][0] = False

    ###############################Partition#################################
    partdict = {
            'animator':animator_chk,
            'person':people_chk,
            'group':group_chk
    }

    for values in partdict:
        if partdict[values][0] == None:
            partdict[values] = False
        else:
            partdict[values] = True
            checked_list.append(values)

    ###############################Value#################################
    valdict={'val_screening':val_screening,'val_adoption':val_adoption,'val_no_animator':val_no_animator,'val_attendance':val_attendance,'val_video_screened_num':val_video_screened_num,'val_video_produced_num':val_video_produced_num}
    for values in valdict:
        if(valdict[values][0]!=None):
            valdict[values]=True
        else:
            valdict[values]=False

    #################################value-partion###########################

    if(number_block_combo == "None"):
        number_block_combo = False
        number_block = False

    if(number_village_combo == "None"):
        number_village_combo = False
        number_village = False

    if (list_combo == "None"):
        list_combo = False
        videolist = False

    priority_block = {}
    if(number_block_combo == 'numBlock'):
        for vals in checked_list:
            if (vals == 'video'):
                number_block_combo = number_block
    priority_village = {}
    if(number_village_combo == 'numVillage'):
        for vals in checked_list:
            if (vals == 'video'):
                number_village_combo = number_village
    priority = {}
    if (list_combo == 'list'):
        for vals in checked_list:
            if ((vals in categoryDictionary['geographies']) or (vals == 'partner')):
                for vals, v in orderDictionary.items():
                    if vals in checked_list:
                        priority[vals] = v
                list_combo = 'list' + (max(priority.items(), key=lambda vals: vals[1])[0]).title()
            elif (vals == "animator"):
                list_combo = 'listAnimator'
                break
            elif (vals == "persongroup"):
                list_combo = 'listGroup'
                break
            elif (vals == "person"):
                list_combo = 'listPerson'
                break
            elif (vals == "video"):
                list_combo = videolist
                break
    ##############################Date#################################

    # if (from_date[0] != ''):
    #     from_date = from_date[0]
    # else:
    #     from_date = '2004-01-01'

    # if (to_date[0] != ''):
    #     to_date = to_date[0]
    # else:
    #     now = datetime.datetime.now()
    #     to_date = '%s-%s-%s' % (now.year, now.month, now.day)

    partition = {
        'partner': dict['partner'][0],
        'country': dict['country'][0],
        'state': dict['state'][0],
        'district': dict['district'][0],
        'block': dict['block'][0],
        'village': dict['village'][0],
        'animator': partdict['animator'],
        'person': partdict['person'],
        'persongroup': partdict['group'],
        'video': dict['video'][0]
    }

    value = {
        'numScreening': valdict['val_screening'],
        'numAdoption': valdict['val_adoption'],
        'numAnimator': valdict['val_no_animator'],
        'attendance': valdict['val_attendance'],
        'numVideoScreened': valdict['val_video_screened_num'],
        'numVideoProduced': valdict['val_video_produced_num'],
        'numBlock' : number_block_combo,
        'numVillage' : number_village_combo,
        'list': list_combo
    }

    options = {'partition': partition, 'value': value}

    args = []
    # datetime.datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%m/%d/%y')
    # date_range[0]=datetime.datetime.strptime("date_range[0]",'%d/%m/%y').strftime('%y-%m-%d')
    # date_range[1]=datetime.datetime.strptime("date_range[1]",'%d/%m/%y').strftime('%y-%m-%d')
    # date_range[0]=date_range[6:] + "-" +date_range[3:5] + "-" + date_range[:2]
    args.append(date_range[0])
    args.append(date_range[1])
    args[0]=args[0][6:10]+"-"+args[0][3:5]+"-"+args[0][0:2]
    args[1]=args[1][7:11]+"-"+args[1][4:6]+"-"+args[1][1:3]


    global dlib
    if not dlib:
        dlib = data_lib()
        dlib.fill_data(options)
    if options['value']['list'] == 'list':
        error = 'Output cannot be generated for this input ! Please check filters and partition field !!'
        return render_to_response("raw_data_analytics/error.html", {'error': error},
                                  context_instance=RequestContext(request))

    else:
        if not list(filter(lambda listvalue: listvalue != False, partition.values())):
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
                return render_to_response('raw_data_analytics/result_new.html', {'from_date': date_range[0], 'to_date': date_range[1],
                                                                             'dataf': unicode(df, errors='ignore')},
                                          context_instance=RequestContext(request))
