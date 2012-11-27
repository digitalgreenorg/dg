from collections import defaultdict
from django.shortcuts import *
from django.http import Http404, HttpResponse
from django.utils import simplejson
from dashboard.models import *
from django.db.models import Count
import datetime
import random
from django.template.loader import render_to_string
from django.db.models import Sum,Max,Count
import get_id_with_images
from django.core.cache import cache
from fbconnect.models import *
from fbconnect.views import *

def get_admin_panel(request):    
    return render_to_response('admin_panel.html')
    
def get_home_page(request, type=None, id=None):
    ##For facebook connect purpose
    fbappid_server_url = get_fbappid_server_url(request)
    facebook_app_id = fbappid_server_url['facebook_app_id']
    server_url = fbappid_server_url['server_url']
    top_csp_stats = defaultdict(lambda:[0, 0, 0, 0, 0])
    id_list = get_id_with_images.get_csp_list()
    csp_stats = Screening.objects.filter(animator__id__in = id_list).values('animator__id').annotate(screenings = Count('id')).values_list('animator', 
                                                                                                          'animator__name',
                                                                                                          'screenings',
                                                                                                          'animator__total_adoptions')
    
    for csp in csp_stats:
        top_csp_stats [csp[0]][0] = csp[0]
        top_csp_stats [csp[0]][1] = csp[1]
        top_csp_stats [csp[0]][2] = csp[2]
        top_csp_stats [csp[0]][3] = csp[3]
        if csp[2] > 20:
            top_csp_stats [csp[0]][4] = float(csp[3])/csp[2]
    
    # sorting on Adoptions_per_screening and keeping first 4
    top_csp_stats = sorted(top_csp_stats.items(), key = lambda(k, v):(v[4],k),
                            reverse=True)[:4]  
    
    id_list = [10000000000346, 10000000000348, 10000000000350, 10000000000381, 10000000000402, 10000000000403, 
               10000000000406, 10000000000450, 10000000019320, 10000000019321, 10000000019348, 10000000019419, 
               10000000019420, 10000000019422, 10000000019426, 10000000019428, 10000000019430, 10000000019431, 
               10000000019435, 10000000019453, 10000000019495, 10000000019502, 10000000019505, 10000000019506, 
               10000000019507, 10000000019508, 10000000019515, 10000000019541, 10000000019554, 10000000019696, 
               10000000019793, 10000000019808, 10000000019823, 10000000019826, 10000000019831, 10000000019844, 
               10000000019895, 10000000019979, 10000000020020]   
    
    csp_leader_stats= []                         
    for obj in top_csp_stats:
        if(obj[0] in id_list):
                photo_link = "http://s3.amazonaws.com/dg_farmerbook/csp/" + str(obj[0]) + ".jpg"
        else:
                photo_link =  "/media/farmerbook/images/sample_csp.jpg"

        csp_leader_stats.append({'id': obj[0],
                                         'name': obj[1][1],
                                         'screenings': obj[1][2],
                                         'photo_link': photo_link,
                                         'adoptions': obj[1][3]})
    top_partner_stats = defaultdict(lambda:[0, 0, 0, 0])     
    partner_info = Partners.objects.all().annotate(num_vill = Count('district__block__village', distinct = True),
                                                   num_farmers = Count('district__block__village__person')).values_list('id',
                                                                                                             'partner_name',
                                                                                                             'num_vill',
                                                                                                             'num_farmers')
    for partner in partner_info:
        top_partner_stats [partner[0]][0] = partner[0]
        top_partner_stats [partner[0]][1] = partner[1]
        top_partner_stats [partner[0]][2] = partner[2]
        top_partner_stats [partner[0]][3] = partner[3]
    top_partner_stats = sorted(top_partner_stats.items(), key = lambda(k, v):(v[2],k), reverse=True)[:3]   
                          
    return render_to_response('farmerbook.html', dict(csp_leader_stats = csp_leader_stats, partner_leader_stats = top_partner_stats, 
                                                      type=type, type_id = id, facebook_app_id = facebook_app_id, server_url = server_url))

def get_leaderboard_data():
    village_ids = Village.farmerbook_village_objects.all().values_list('id', flat=True)
    farmerbook_farmers = Person.farmerbook_objects.all().values_list('id', flat=True)
    #right panel bottom contents. Leader boards of farmers
    #get all persons from village who attended any screening in village
    screenings_attended = PersonMeetingAttendance.objects.filter(person__in = farmerbook_farmers, person__village__id__in = village_ids).values_list('person_id', flat=True)
    views_dict = defaultdict(lambda:[0, 0, 0])
    #get number of viewings for each farmer
    for i in screenings_attended:
        views_dict[i][0] += 1
    #get number of adoptions for each farmer
    adoptions = PersonAdoptPractice.objects.filter(person__in = farmerbook_farmers, person__village__id__in = village_ids).values_list('person_id', flat=True)
    adoptions_dict = defaultdict(int)
    for i in adoptions:
        adoptions_dict[i] += 1
    #appending adoptions and adoption rate of farmers in views_dict
    for k,v in views_dict.iteritems():
        if k in adoptions_dict:
            views_dict[k][1] = adoptions_dict[k]
            views_dict[k][2] = float((views_dict[k][1] / float(views_dict[k][0])) * 100)
    sorted_list_stats = sorted(views_dict.items(), key = lambda(k, v):(v[2], k), reverse=True)
    top_adopters_list = sorted_list_stats[:27]
    top_adopters_id_list = []
    for i in top_adopters_list:
        top_adopters_id_list.append(i[0])
    #get last adopted video
    #last_adopted_details = PersonAdoptPractice.objects.filter(person__id__in = top_adopters_id_list).order_by('-date_of_adoption').values_list('person_id', 'person__person_name', 'video__title', 'date_of_adoption', 'person__date_of_joining')
    last_adopted_details = Person.objects.filter(id__in = top_adopters_id_list).values_list('id', 'person_name', 'personadoptpractice__video__title', 'personadoptpractice__date_of_adoption', 'date_of_joining')
    #remove duplicates and append recent date
    d = defaultdict(list)
    for item in last_adopted_details:
        if item[0] not in d:
            d[item[0]].append([item[1], item[2], item[3], item[4]])
    top_adopters_stats = []
    for obj in top_adopters_list:
        if obj[0] in d:
            top_adopters_stats.append({'id': obj[0], 'name': d[obj[0]][0][0], 'title': d[obj[0]][0][1], 'date_of_adoption': d[obj[0]][0][2], 'date_of_joining': d[obj[0]][0][3], 'views': obj[1][0], 'adoptions': obj[1][1], 'adoption_rate': obj[1][2]})
    return top_adopters_stats

def get_villages_with_images(request):
    #if request.is_ajax()-with:
    village_list = get_id_with_images.get_village_list()
    village_details = []
    district_lat_lng = {10000000000030:["Hassan", "13.0000", "76.1000"], 10000000000005:["Khunti", "23.0800", "85.2800"], 10000000000004:["West Singhbum", "22.5700", "85.8200"], 10000000000008:["Dharwad","15.4649","75.0030"], 
                        10000000000014:["Mayurbhanj","21.7800","85.9700"], 10000000000017:["Belgaum","15.8700","74.5000"],
                        10000000000023: ["Koraput", "19.0000", "83.0000"], 10000000000024: ["Keonjhar", "21.6300","85.5800"],
                        10000000000025: ["Barwani", "22.0300","74.9000"], 10000000000027:[ "Ujjain", "23.1828","75.7772"],
                        10000000000028:["Mysore", "12.3024","76.6386"], 10000000000033:["Mahabubnagar", "16.7300","77.9800"],
                        10000000000035:["Munger", "25.3800", "86.4700"], 10000000000021:["Rajgarh", "22.6800", "74.9500"]}
    village_lat_lng = {47000040575:["12.2475", "76.249722", "Kudluru lakshmipura"], 
                       47000062452:["12.37", "76.337778", "Thondalu"], 
                       47000001044:["12.310833", "76.252778", "Yashodharapura"]}
    for i in village_list:
        vil_details = Village.objects.filter(id = i).values_list('id', 'village_name', 
                                                                 'block__district__id', 'grade')
        district_id = vil_details[0][2]
        try:
            if district_lat_lng[district_id]:
                district_lat= float(district_lat_lng[district_id][1])
                district_lng = float(district_lat_lng[district_id][2])
        except:
            district_lat = float(22.5700)
            district_lng = float(85.8200)
        #vincenty's formula to calculate lats and lngs in range of 50 km
        angle = 50 * 0.0089833458;
        random_lat = "%.4f" % random.uniform(district_lat - angle, district_lat + angle)
        random_lng = "%.4f" % random.uniform(district_lng - angle, district_lng + angle)
        try:
            if village_lat_lng[i]:
                random_lat = village_lat_lng[i][0]
                random_lng = village_lat_lng[i][1]
        except:
            pass
        village_details.append({"id":i, "name": vil_details[0][1], "latitude":random_lat, 
                                "longitude": random_lng, "grade": vil_details[0][3]})
    
    return HttpResponse(simplejson.dumps(village_details), mimetype="application/json")

def get_videos_produced(request):
    village_id = int(request.GET['village_id'])
    #return title, duration, youtube thumbnail, production date, viewers, adoptions
    vids_details = Video.objects.filter(village__id = village_id).distinct().values_list('id', 'title', 'youtubeid', 'video_production_end_date','viewers').annotate(adoptions=Count('personadoptpractice'))
    videos_produced_stats = []
    for obj in vids_details:
        videos_produced_stats.append({'id':obj[0], 'title':obj[1], 'youtubeid':obj[2], 'productiondate':obj[3],'viewers':obj[4], 'adopters': obj[5]})
    if len(videos_produced_stats):
        return render_to_response('videos_produced.html', dict(videos_produced_stats=videos_produced_stats))
    else:
        return HttpResponse("")

def get_village_page(request):
    village_id = int(request.GET['village_id'])
    #left panel stats dict hold values related to left panel of village page
    left_panel_stats = {}
    farmerbook_farmers = Person.farmerbook_objects.all().values_list('id', flat=True)
    tot_farmers = VillagePrecalculation.objects.filter(village__id = village_id, date = datetime.date(2012,1,1)).values_list('total_active_attendees', flat=True)
    if tot_farmers:
        left_panel_stats['tot_farmers'] = tot_farmers
    else:
        left_panel_stats['tot_farmers'] = "0"
    left_panel_stats['videos_produced'] = Video.objects.filter(village__id = village_id).distinct().count()

    left_panel_stats['num_of_groups'] = PersonGroups.objects.filter(village__id = village_id).count()
    #group_id_list = get_id_with_images.get_group_list()
    left_panel_stats['vil_groups'] = PersonGroups.objects.filter(village__id = village_id, person__image_exists=1).distinct().values_list('id', 'group_name')
    left_panel_stats['partner'] = Partners.objects.filter(district__block__village__id = village_id).values_list('id', 'partner_name')
    left_panel_stats['service_provider'] = Animator.objects.filter(animatorassignedvillage__village__id = village_id).order_by('-id').values_list('id', 'name')[:1]
    left_panel_stats['vil_details'] = Village.objects.filter(id = village_id).values_list('id', 'village_name', 'block__district__district_name', 'block__district__state__state_name', 'start_date', 'grade')
    startdate = Person.objects.filter(village__id = village_id).annotate(sd = Min('date_of_joining')).values_list('sd', flat=True)
    if(startdate):
        left_panel_stats['start_date'] = startdate[0]
    else:
        left_panel_stats['start_date'] = ""    

    #rightpanel top contents
    vids_details = Video.objects.filter(screening__village__id = village_id).distinct().values_list('id','title', 'youtubeid')
    vids_id = set(i[0] for i in vids_details)
    left_panel_stats['tot_videos'] = len(vids_id)
    vid_adoptions = PersonAdoptPractice.objects.filter(person__village__id = village_id).values('video__id').annotate(
                                        num_of_adoptions = Count('id')).values_list('video__id', 'num_of_adoptions')
    pma = PersonMeetingAttendance.objects.filter(screening__village__id = village_id).values_list('screening__videoes_screened__id','interested', 'expressed_question')   
    vid_scr_atten = Screening.objects.filter(village__id = village_id).values('videoes_screened').annotate(num_scr = Count('id', distinct=True),
                                                                                                         atten=Count('farmers_attendance'),
                                                                                                         last_seen_date = Max('date'))
    question_count = 0
    vids_stats_dict = defaultdict(lambda:[0, 0, 0, 0, 0, 0])
    for l, m, n in pma:
        if(m):
            vids_stats_dict[l][0] += 1
        if(n != ""):
            vids_stats_dict[l][1] += 1
            question_count += 1
    left_panel_stats['tot_questions'] = question_count
    #videos_watched_stats contain list of dictionaries containing stats of video titles
    for vid_id in vid_scr_atten:
        vids_stats_dict[vid_id['videoes_screened']][3] =  vid_id['atten']
        vids_stats_dict[vid_id['videoes_screened']][4] =  vid_id['num_scr']
        vids_stats_dict[vid_id['videoes_screened']][5] =  vid_id['last_seen_date']
    
    total_adopt = 0
    for vid_id,num_adopt in vid_adoptions:
        vids_stats_dict[vid_id][2] = num_adopt
        total_adopt = total_adopt + num_adopt
        
    left_panel_stats['tot_adoptions'] = total_adopt
    #for progress bar below village picture
    left_panel_stats['screenings'] = Screening.objects.filter(village__id = village_id).count()
    if left_panel_stats['screenings'] > 0:
        left_panel_stats['adoption_rate'] = float(left_panel_stats['tot_adoptions']) /left_panel_stats['screenings']
        left_panel_stats['adoption_rate_width'] = (left_panel_stats['adoption_rate'] * 100)/5.0
    else:
        left_panel_stats['adoption_rate'] = 0
        left_panel_stats['adoption_rate_width'] = 0
    
    videos_watched_stats = []
    for obj in vids_details:
        stat_text = make_text_from_stats(obj,vids_stats_dict)
        videos_watched_stats.append({'id':obj[0], 'title':obj[1], 'youtubeid':obj[2], 
                                     'adopters':vids_stats_dict[obj[0]][2],'interested':vids_stats_dict[obj[0]][0], 'last_seen_date':vids_stats_dict[obj[0]][5], 
                                     'questioners': vids_stats_dict[obj[0]][1], 'atten':vids_stats_dict[obj[0]][3], 'disseminations': vids_stats_dict[obj[0]][4],
                                     'fulltext': stat_text})
    sorted_list = sorted(videos_watched_stats, key=lambda k: k['last_seen_date'], reverse=True)
    #right panel bottom contents. Leader boards of related villages
    #get all persons from village who attended any screening in village

    id_list = get_id_with_images.get_village_list()
    views_dict = defaultdict(lambda:[0, 0, 0, 0, 0, 0, 0, 0])
    district_id = Village.objects.filter(id = village_id).values_list('block__district_id')
    related_info = Village.objects.filter(block__district__id = district_id, id__in = id_list).exclude(id = village_id).values('id').annotate(screenings = Count('screening')).values_list('id','village_name','screenings')
    for related_id in related_info:
        vil_id = related_id[0]
        views_dict[related_id[0]][0] = vil_id
        views_dict[related_id[0]][1] = related_id[1] 
        views_dict[related_id[0]][2] = related_id[2]
        views_dict[related_id[0]][3] = PersonAdoptPractice.objects.filter(person__village__id = vil_id).count()
        if views_dict[related_id[0]][2] == 0:
            views_dict[related_id[0]][4] = 0
        else:
            views_dict[related_id[0]][4] = float(views_dict[related_id[0]][3]) / views_dict[related_id[0]][2]
        views_dict[related_id[0]][5] = (views_dict[related_id[0]][4]* 100)/5.0 
        views_dict[related_id[0]][6] = "http://s3.amazonaws.com/dg_farmerbook/village/" + str(related_id[0]) + ".jpg"
        min_joining = Person.objects.filter(village__id = vil_id).annotate(startdate = Min('date_of_joining')).values_list('startdate', flat = True)
        if min_joining:
            views_dict[related_id[0]][7] = min_joining[0]
        else:
            views_dict[related_id[0]][7] = ""        
               
    # Sorting and limiting to 10 related CSP's
    sorted_list_stats = sorted(views_dict.items(), key = lambda(k, v):(v[5],k), reverse=True)
    top_related_list = sorted_list_stats[:10]
    return render_to_response('vil_page.html', dict(left_panel_stats = left_panel_stats, videos_watched_stats = sorted_list, top_related_list = top_related_list))

def get_person_page(request):
    person_id = int(request.GET['person_id'])
    fuid = request.GET.get('fuid', None)
    #left panel stats dictionary hold values related to left panel of village page
    left_panel_stats = {}
    left_panel_stats['farmer_details'] = Person.objects.filter(id = person_id).values_list('id', 'person_name', 'father_name', 'group__group_name', 'village__village_name', 'village__block__district__district_name', 'village__block__district__state__state_name','date_of_joining', 'village__id', 'group__id')
    person_views = PersonMeetingAttendance.objects.filter(person__id = person_id).distinct().count()
    person_adoptions = PersonAdoptPractice.objects.filter(person__id = person_id).distinct().count()
    if(person_views):
        adoption_rate = (person_adoptions / float(person_views)) * 100
        adoption_rate = "{0:.2f}".format(adoption_rate)
    else:
        adoption_rate = 0
    left_panel_stats['views_adoptions'] = [person_views, person_adoptions, adoption_rate]
    left_panel_stats['videos_watched'] = Video.objects.filter(screening__personmeetingattendance__person__id = person_id).distinct().count()
    left_panel_stats['questions_asked'] = PersonMeetingAttendance.objects.filter(person__id = person_id).exclude(expressed_question = '').count()
    left_panel_stats['videos_featured'] = Video.objects.filter(farmers_shown__person__id = person_id).distinct().count()
    left_panel_stats['partner'] = Partners.objects.filter(district__block__village__person__id = person_id).values_list('id', 'partner_name')
    left_panel_stats['service_provider'] = Animator.objects.filter(animatorassignedvillage__village__person__id = person_id).order_by('-id').values_list('id', 'name')[:1]
    #For FBConnect to check if user already subscribed to the farmer
    left_panel_stats['subscribed'] = False
    if fuid:
        follower = FBFollowers.objects.filter(fbuser = fuid, person = person_id)
        if follower:
            left_panel_stats['subscribed'] = True
    #rightpanel top contents
    #some problem in retrieving screening__date from Video Objects
    #vids_watched = Video.objects.filter(screening__village__id = village_id).distinct().values_list('id', 'title', 'youtubeid', 'screening__date')[0:5]
    vids_id = Video.objects.filter(screening__personmeetingattendance__person__id = person_id).distinct().values_list('id', flat = True)
    vids_id = list(vids_id)
    
    pma = PersonMeetingAttendance.objects.filter(person__id = person_id).values_list('screening__videoes_screened__id',
                                                                                           'interested', 
                                                                                           'expressed_question')   
    vids_details = Video.objects.filter(id__in = vids_id).values_list('id', 'title', 'youtubeid')
    farmer_att = Screening.objects.filter(personmeetingattendance__person__id = person_id).values('videoes_screened__id').annotate(screening_per_vid = Count('id', distinct=True),
                                                                                                         fcount=Count('farmers_attendance__id'),
                                                                                                         last_seen_date = Max('date'))
    vids_stats_dict = defaultdict(lambda:[0, 0, 0, 0, 0, 0])
    
    for id,interest,question in pma:
        if(interest):
            vids_stats_dict[id][0] += 1
        if(question != ""):
            vids_stats_dict[id][1] = question
      
    if person_adoptions == None:
        per_vid_adoption = []
    else:    
        per_vid_adoption = PersonAdoptPractice.objects.filter(person__id = person_id).values('video__id').annotate(adopt_count=Count('id'))
    for vid_id in per_vid_adoption:
        vids_stats_dict[vid_id['video__id']][2] = vid_id['adopt_count']
        
    for vid_id in farmer_att:
        vids_stats_dict[vid_id['videoes_screened__id']][3] =  vid_id['fcount']
        vids_stats_dict[vid_id['videoes_screened__id']][4] =  vid_id['screening_per_vid']
        vids_stats_dict[vid_id['videoes_screened__id']][5] =  vid_id['last_seen_date']
        
    #videos_watched_stats contain list of dictionaries containing stats of video titles
    videos_watched_stats = []
    for obj in vids_details:
        stat_text = make_text_from_person_stats(obj,vids_stats_dict)
        videos_watched_stats.append({'id':obj[0], 
                                    'title':obj[1],
                                    'youtubeid':obj[2],
                                    'adopted':vids_stats_dict[obj[0]][2],
                                    'interested':vids_stats_dict[obj[0]][0], 
                                    'last_seen_date':vids_stats_dict[obj[0]][5], 
                                    'question': vids_stats_dict[obj[0]][1],
                                    'farmers_attended': vids_stats_dict[obj[0]][3],
                                    'screenings':vids_stats_dict[obj[0]][4],
                                    'fulltext':stat_text})

    newlist = sorted(videos_watched_stats, key=lambda k: k['last_seen_date'], reverse=True)
    village_id = Person.objects.filter(id=person_id).values_list('village__id', flat=True)
    group_id = Person.objects.filter(id=person_id).values_list('group__id', flat=True)
    
    # Build a dictionary for each person in the group/village referencing a list of screenings attended, adoptions and adoption rate, date of last adoption and name of last video adopted and date_of_joining.
    views_dict = defaultdict(lambda: {'id': 0, 'name': 0, 'title': 0, 'date_of_adoption': 0, 'date_of_joining': 0, 'views': 0, 'adoptions': 0, 'adoption_rate': 0})
    #If a farmer belongs to group then get leaderboard of farmers in group else get leaderboard of farmers in village
    # Get all attendances for people in the group
    # Get number of viewings for each farmer
    # Get number of adoptions for each farmer    
    if not group_id:
        person_details = Person.objects.exclude(id = person_id).filter(village__id=village_id, image_exists=True).values('id', 'person_name', 'date_of_joining')
        screenings_attended = PersonMeetingAttendance.objects.exclude(person__id = person_id).filter(person__image_exists=True, person__village__id = village_id).values('person__id', 'person__person_name', 'person__date_of_joining')
        adoptions = PersonAdoptPractice.objects.exclude(person__id = person_id).filter(person__image_exists=True, person__village__id = village_id).values_list('person_id', flat=True)
    else:
        person_details = Person.objects.exclude(id = person_id).filter(group__id=group_id, image_exists=True).values('id', 'person_name', 'date_of_joining')
        screenings_attended = PersonMeetingAttendance.objects.exclude(person__id = person_id).filter(person__image_exists=True, person__group__id = group_id).values('person__id', 'person__person_name', 'person__date_of_joining')
        adoptions = PersonAdoptPractice.objects.exclude(person__id = person_id).filter(person__image_exists=True, person__group__id = group_id).values_list('person_id', flat=True)
    for person in person_details:
        views_dict[person['id']]['id'] = person['id']
        views_dict[person['id']]['name'] = person['person_name']   
        views_dict[person['id']]['date_of_joining'] = person['date_of_joining']
    
    for attendance in screenings_attended:
        views_dict[attendance['person__id']]['views'] += 1
    
    adoptions_dict = defaultdict(int)
    for i in adoptions:
        views_dict[i]['adoptions'] += 1
    # Computing adoption rate of farmers in views_dict
    for k,v in views_dict.iteritems():
        views_dict[k]['adoption_rate'] = float((views_dict[k]['adoptions'] / float(views_dict[k]['views'])) * 100) if views_dict[k]['views'] > 0 else 0
    
    # get last adopted video
    adoption_details = Person.objects.filter(id__in = views_dict.keys()).values('id', 'personadoptpractice__video__title', 'personadoptpractice__date_of_adoption')
    for adoption in adoption_details:
        if views_dict[adoption['id']]['date_of_adoption']==0 or views_dict[adoption['id']]['date_of_adoption'] < adoption['personadoptpractice__date_of_adoption']:
            views_dict[adoption['id']]['date_of_adoption'] = adoption['personadoptpractice__date_of_adoption']
            views_dict[adoption['id']]['title'] = adoption['personadoptpractice__video__title']
    
    top_adopters_list = sorted(views_dict.values(), key = lambda(v):v['adoptions'], reverse=True)
    #get last adopted video for facebook feed
    person_last_adopted_details = PersonAdoptPractice.objects.filter(person__id = person_id).order_by('-date_of_adoption').values_list('person_id', 'person__person_name', 'video__title', 'date_of_adoption')
    if person_last_adopted_details:
        person_last_adopted_details = person_last_adopted_details[0]
    return render_to_response('person_page.html', dict(left_panel_stats = left_panel_stats, 
                                                       videos_watched_stats = newlist, 
                                                       top_adopters_stats=top_adopters_list, 
                                                       person_last_adopted_details = person_last_adopted_details))    

def get_group_page(request):
    group_id = int(request.GET['group_id'])
    
    left_panel_stats = {}
    left_panel_stats['group_details'] = PersonGroups.objects.filter(id = group_id).values_list('group_name',
                                                                                              'village__id',
                                                                                              'village__village_name',
                                                                                              'village__block__district__district_name',
                                                                                              'village__block__district__state__state_name',
                                                                                              'village__block__district__partner__id',
                                                                                              'village__block__district__partner__partner_name',
                                                                                              'village__animatorassignedvillage__animator__id',
                                                                                              'village__animatorassignedvillage__animator__name',
                                                                                              'id')
    
    left_panel_stats['members_count'] = Person.objects.filter(group = group_id).count()
    left_panel_stats['screenings'] = Screening.objects.filter(personmeetingattendance__person__group__id = group_id).distinct().count()
    left_panel_stats['questions'] = PersonMeetingAttendance.objects.filter(person__group__id = group_id).exclude(expressed_question = "").count()
    left_panel_stats['adoptions'] = PersonAdoptPractice.objects.filter(person__group__id = group_id).count()
    left_panel_stats['adoption_rate'] = float(left_panel_stats['adoptions']) /left_panel_stats['screenings']
    left_panel_stats['adoption_rate_width'] = (left_panel_stats['adoption_rate'] * 100)/5.0 
    min_joining = Person.objects.filter(group__id = group_id).annotate(startdate = Min('date_of_joining')).values_list('startdate', flat =True)
    left_panel_stats['start_date'] = min_joining[0]
    if not left_panel_stats['start_date']:
        left_panel_stats['start_date'] = Screening.objects.filter(personmeetingattendance__person__group__id = group_id).annotate(mindate = Min('date')).values_list('mindate', flat=True)[0]
        
    pma = PersonMeetingAttendance.objects.filter(person__group__id = group_id).values_list('screening__videoes_screened__id',
                                                                                           'interested', 
                                                                                           'expressed_question')   
    vids_id= set(i[0] for i in pma)
    vids_details = Video.objects.filter(id__in = vids_id).values_list('id', 'title', 'youtubeid')
    left_panel_stats['videos_disseminated'] = len(vids_details)
    farmer_att = Screening.objects.filter(personmeetingattendance__person__group__id = group_id).values('videoes_screened__id').annotate(screening_per_vid = Count('id', distinct=True),
                                                                                                         fcount=Count('farmers_attendance__id'),
                                                                                                         last_seen_date = Max('date'))
    vids_stats_dict = defaultdict(lambda:[0, 0, 0, 0, 0, 0])
    
    for id,interest,question in pma:
        if(interest):
            vids_stats_dict[id][0] += 1
        if(question != ""):
            vids_stats_dict[id][1] += 1
    
  
    if left_panel_stats['adoptions'] == None:
        per_vid_adoption = []
    else:    
        per_vid_adoption = PersonAdoptPractice.objects.filter(person__group__id = group_id).values('video__id').annotate(adopt_count=Count('person__id')) 
    for vid_id in per_vid_adoption:
        vids_stats_dict[vid_id['video__id']][2] = vid_id['adopt_count']
        
    for vid_id in farmer_att:
        vids_stats_dict[vid_id['videoes_screened__id']][3] =  vid_id['fcount']
        vids_stats_dict[vid_id['videoes_screened__id']][4] =  vid_id['screening_per_vid']
        vids_stats_dict[vid_id['videoes_screened__id']][5] =  vid_id['last_seen_date']
        
   
        
    #videos_watched_stats contain list of dictionaries containing stats of video titles
    videos_watched_stats = []
    for obj in vids_details:
        stat_text = make_text_from_stats(obj,vids_stats_dict)
        videos_watched_stats.append({'id':obj[0], 
                                    'title':obj[1],
                                    'youtubeid':obj[2],
                                    'adopters':vids_stats_dict[obj[0]][2],
                                    'interested':vids_stats_dict[obj[0]][0], 
                                    'last_seen_date':vids_stats_dict[obj[0]][5], 
                                    'questioners': vids_stats_dict[obj[0]][1],
                                    'farmers_attended': vids_stats_dict[obj[0]][3],
                                    'screenings':vids_stats_dict[obj[0]][4],
                                    'fulltext': stat_text})
      
    sorted_videos_watched_stats = sorted(videos_watched_stats, key=lambda k: k['last_seen_date'], reverse=True)
    
    village_id = PersonGroups.objects.filter(id=group_id).values_list('village__id', flat=True)
    
    # Build a dictionary for each person in the group referencing a list of screenings attended, adoptions and adoption rate, date of last adoption and name of last video adopted and date_of_joining.
    
    views_dict = defaultdict(lambda: {'id': 0, 'name': 0, 'title': 0, 'date_of_adoption': 0, 'date_of_joining': 0, 'views': 0, 'adoptions': 0, 'adoption_rate': 0})
    
    # Add details for all person in the group
    person_details = Person.objects.filter(group__id=group_id, image_exists=True).values('id', 'person_name', 'date_of_joining')
    for person in person_details:
        views_dict[person['id']]['id'] = person['id']
        views_dict[person['id']]['name'] = person['person_name']   
        views_dict[person['id']]['date_of_joining'] = person['date_of_joining']
    # Get all attendances for people in the group
    screenings_attended = PersonMeetingAttendance.objects.filter(person__image_exists=True, person__group__id = group_id).values('person__id', 'person__person_name', 'person__date_of_joining')
    # Get number of viewings for each farmer
    for attendance in screenings_attended:
        views_dict[attendance['person__id']]['views'] += 1
    # Get number of adoptions for each farmer
    adoptions = PersonAdoptPractice.objects.filter(person__image_exists=True, person__group__id = group_id).values_list('person_id', flat=True)
    adoptions_dict = defaultdict(int)
    for i in adoptions:
        views_dict[i]['adoptions'] += 1
    # Computing adoption rate of farmers in views_dict
    for k,v in views_dict.iteritems():
        views_dict[k]['adoption_rate'] = float((views_dict[k]['adoptions'] / float(views_dict[k]['views'])) * 100) if views_dict[k]['views'] > 0 else 0
    
    # Get details of all indviduals in the group
    # get last adopted video
    adoption_details = Person.objects.filter(id__in = views_dict.keys()).values('id', 'personadoptpractice__video__title', 'personadoptpractice__date_of_adoption')
    
    for adoption in adoption_details:
        if views_dict[adoption['id']]['date_of_adoption']==0 or views_dict[adoption['id']]['date_of_adoption'] < adoption['personadoptpractice__date_of_adoption']:
            views_dict[adoption['id']]['date_of_adoption'] = adoption['personadoptpractice__date_of_adoption']
            views_dict[adoption['id']]['title'] = adoption['personadoptpractice__video__title']
    
    top_adopters_list = sorted(views_dict.values(), key = lambda(v):v['adoptions'], reverse=True)
    return render_to_response('person_group_page.html', dict(left_panel_stats = left_panel_stats, videos_watched_stats = sorted_videos_watched_stats, top_adopters_stats = top_adopters_list))

def get_csp_page(request):
    csp_id = int(request.GET['csp_id'])
  
        #left panel stats dict hold values related to left panel of village page
    left_panel_stats = {}
    animator_villages = AnimatorAssignedVillage.objects.filter(animator = csp_id ).values_list('village_id',
                                                                                               'village__village_name')
    
    left_panel_stats['vil_info'] = set([(i[0],i[1].split('(')[0]) for i in animator_villages])
    assigned_vill_id = set([i[0] for i in animator_villages])
    left_panel_stats['start_date'] = Screening.objects.filter(animator__id = csp_id).aggregate(Min('date'))["date__min"]
    left_panel_stats['screenings_disseminated'] =  Screening.objects.filter(animator__id = csp_id).count()
    left_panel_stats['nalloted_groups'] = PersonGroups.objects.filter(village__id__in = assigned_vill_id).count()
    group_id_list = get_id_with_images.get_group_list()
    left_panel_stats['alloted_groups'] = PersonGroups.objects.filter(village__id__in = assigned_vill_id,id__in = group_id_list).values_list('id', 'group_name')
    left_panel_stats['csp_details'] = Animator.objects.filter(id = csp_id).values_list('id', 'name')
    left_panel_stats['csp_villages'] = [i[1] for i in animator_villages]
    left_panel_stats['vil_details'] = Village.objects.filter(id__in = assigned_vill_id).values_list('block__district__district_name', 
                                                                                                    'block__district__state__state_name')[0]
    
    
        
    left_panel_stats['total_adoptions'] = Animator.objects.get(id = csp_id).total_adoptions
        
    if(left_panel_stats['screenings_disseminated']):
        left_panel_stats['adoption_rate'] =  float(left_panel_stats['total_adoptions'])/left_panel_stats['screenings_disseminated']
    else:
        left_panel_stats['adoption_rate'] = 0 
    left_panel_stats['adoption_rate_width'] = (left_panel_stats['adoption_rate']/20.0) * 100
    
    pma = PersonMeetingAttendance.objects.filter(screening__animator = csp_id).values_list('screening__videoes_screened__id',
                                                                                           'interested', 
                                                                                           'expressed_question')   
    vids_id= set(i[0] for i in pma)
    vids_details = Video.objects.filter(id__in = vids_id).values_list('id', 'title', 'youtubeid')
    left_panel_stats['videos_disseminated'] = len(vids_details)
    farmer_att = Screening.objects.filter(animator__id = csp_id).values('videoes_screened__id').annotate(screening_per_vid = Count('id', distinct=True),
                                                                                                         fcount=Count('farmers_attendance__id'),
                                                                                                         last_seen_date = Max('date'))
    vids_stats_dict = defaultdict(lambda:[0, 0, 0, 0, 0, 0])
    
    for id,interest,question in pma:
        if(interest):
            vids_stats_dict[id][0] += 1
        if(question != ""):
            vids_stats_dict[id][1] += 1
    
  
    if left_panel_stats['start_date'] == None:
        per_vid_adoption = []
    else:    
        per_vid_adoption = PersonAdoptPractice.objects.filter( video__in = vids_id,
                                                           person__village__in = assigned_vill_id,
                                                           date_of_adoption__gte = left_panel_stats['start_date']).values('video__id').annotate(adopt_count=Count('person__id')) 
    for vid_id in per_vid_adoption:
        vids_stats_dict[vid_id['video__id']][2] = vid_id['adopt_count']
        
    for vid_id in farmer_att:
        vids_stats_dict[vid_id['videoes_screened__id']][3] =  vid_id['fcount']
        vids_stats_dict[vid_id['videoes_screened__id']][4] =  vid_id['screening_per_vid']
        vids_stats_dict[vid_id['videoes_screened__id']][5] =  vid_id['last_seen_date']
        
   
        
    #videos_watched_stats contain list of dictionaries containing stats of video titles
    videos_watched_stats = []
    for obj in vids_details:
        stat_text = make_text_from_stats(obj,vids_stats_dict)
        videos_watched_stats.append({'id':obj[0], 
                                    'title':obj[1],
                                    'youtubeid':obj[2],
                                    'adopters':vids_stats_dict[obj[0]][2],
                                    'interested':vids_stats_dict[obj[0]][0], 
                                    'last_seen_date':vids_stats_dict[obj[0]][5], 
                                    'questioners': vids_stats_dict[obj[0]][1],
                                    'farmers_attended': vids_stats_dict[obj[0]][3],
                                    'screenings':vids_stats_dict[obj[0]][4],
                                    'fulltext': stat_text})
      
    sorted_videos_watched_stats = sorted(videos_watched_stats, key=lambda k: k['last_seen_date'], reverse=True)
    
    id_list = get_id_with_images.get_csp_list()
    # Related CSP's
    views_dict = defaultdict(lambda:[0, 0, 0, 0, 0, 0, 0, 0, 0])
    csp_district= Animator.objects.filter(id = csp_id).values_list('village__block__district__id', flat = True)
    related_info = Animator.objects.filter( id__in = id_list).exclude(id = csp_id).values('id').annotate(num_screening = Count('screening')).values_list('id',
                                                                                                                                                                                                     'name',
                                                                                                                                                                                                     'num_screening',
                                                                                                                                                                                                     'total_adoptions')
    for related_id in related_info:
        views_dict[related_id[0]][0] = related_id[1]
        views_dict[related_id[0]][1] = related_id[2]
        if views_dict[related_id[0]][1] > 0:
            views_dict[related_id[0]][2] = related_id[3] 
            views_dict[related_id[0]][3] = float(views_dict[related_id[0]][2])/views_dict[related_id[0]][1]
    sorted_info = sorted(views_dict.items(), key = lambda(k, v):(v[3],k), reverse=True)[:10] 
    
    for related_id in sorted_info:
        dates = Screening.objects.filter(animator__id = related_id[0]).aggregate(start = Min('date'),last = Max('date'))
        views_dict[related_id[0]][4] = dates['start']
        views_dict[related_id[0]][6] = dates['last']
        vid = Screening.objects.filter(date = dates['last'], animator = related_id[0]).values_list('videoes_screened','videoes_screened__title')[0]
        views_dict[related_id[0]][7] = vid[0]
        views_dict[related_id[0]][8] = vid[1]
        views_dict[related_id[0]][5] = ((datetime.date.today() - views_dict[related_id[0]][4]).days)/30.0
               
    # Sorting and limiting to 10 related CSP's
    sorted_list_stats = sorted(views_dict.items(), key = lambda(k, v):(v[3],k), reverse=True)
    top_related_list = sorted_list_stats[:10] 
    
    left_panel_stats['partner_details'] = District.objects.filter(id = csp_district).values_list('partner__id','partner__partner_name')
     
    # For those in list(image of csp exists), give s3 link , otherwise sample image   
#    id_list = [10000000000346, 10000000000348, 10000000000350, 10000000000381, 10000000000402, 10000000000403, 
#               10000000000406, 10000000000450, 10000000019320, 10000000019321, 10000000019348, 10000000019419, 
#               10000000019420, 10000000019422, 10000000019426, 10000000019428, 10000000019430, 10000000019431, 
#               10000000019435, 10000000019453, 10000000019495, 10000000019502, 10000000019505, 10000000019506, 
#               10000000019507, 10000000019508, 10000000019515, 10000000019541, 10000000019554, 10000000019696, 
#               10000000019793, 10000000019808, 10000000019823, 10000000019826, 10000000019831, 10000000019844, 
#               10000000019895, 10000000019979, 10000000020020]        
    top_related_stats = []
    for obj in top_related_list:
        if(obj[0] in id_list):
            photo_link = "http://s3.amazonaws.com/dg_farmerbook/csp/" + str(obj[0]) + ".jpg"
        else:
            photo_link =  "/media/farmerbook/images/sample_csp.jpg"
        top_related_stats.append({'id': obj[0],
                                         'name': obj[1][0],
                                         'screenings': obj[1][1],
                                         'freq_screening': obj[1][5],
                                         'photo_link': photo_link,
                                         'rate': obj[1][3],
                                         'adoptions': obj[1][2],
                                         'ratewidth': (obj[1][3]/20.0)*100,
                                         'start': obj[1][4],
                                         'last_screened': obj[1][6],
                                         'last_video_id': obj[1][7],
                                         'last_video': obj[1][8]})

    return render_to_response('serviceprovider_page.html', dict(left_panel_stats = left_panel_stats, 
                      videos_watched_stats = sorted_videos_watched_stats, 
                      top_related_stats = top_related_stats))        

def get_partner_page(request):
        
    partner_id = int(request.GET['partner_id'])
    
    site_link = defaultdict(lambda:[0])
    site_link[10000000000001][0] = "http://www.pradan.net/"
    site_link[10000000000002][0] = "http://www.baif.org.in/aspx_pages/index.asp"
    site_link[10000000000003][0] = "http://greenconserve.com/"
    site_link[10000000000004][0] = "http://www.samprag.org/"
    site_link[10000000000007][0] = "http://www.accessdev.org/"
    site_link[10000000000008][0] = "http://www.asaindia.org/"
    site_link[10000000000009][0] = "http://www.pragatikoraput.org/pragatikoraput/"
    site_link[10000000000010][0] = "http://www.ngogateway.org/user_homepage/index.php?id=239"
    site_link[10000000000011][0] = "http://www.serp.ap.gov.in/SHG/index.jsp"
    site_link[10000000000013][0] = "http://brlp.in/"
    
    
    #left panel stats dict hold values related to left panel of village page
    left_panel_stats = {} 
    left_panel_stats['site_link'] = site_link[partner_id][0]
    left_panel_stats['partner_details'] = Partners.objects.filter(id= partner_id).values_list('id',
                                                                                              'partner_name',
                                                                                              'district__state__state_name',
                                                                                              'district__id',
                                                                                              'date_of_association',
                                                                                              'district__district_name')
    
    partner_district = set(i[3] for i in left_panel_stats['partner_details'])
    left_panel_stats['assigned_states'] = set(i[2] for i in left_panel_stats['partner_details'])
    left_panel_stats['assigned_districts'] = set(i[5] for i in left_panel_stats['partner_details'])                                                                                                
    left_panel_stats['total_adoptions'] = Animator.objects.filter(partner = partner_id).values('partner').annotate(tot = Sum('total_adoptions')).values_list('tot')[0][0]
    left_panel_stats['farmers'] = Person.objects.filter(village__block__district__partner__id = partner_id).count()
    left_panel_stats['number_villages'] = Village.objects.filter(block__district__partner__id = partner_id).count()
    
    left_panel_stats['Screenings'] = Screening.objects.filter(village__block__district__partner__id = partner_id).count()
    if(left_panel_stats['Screenings']):
        months = ((datetime.date.today() - left_panel_stats['partner_details'][0][4]).days)/30.0
        left_panel_stats['rate'] =  left_panel_stats['Screenings'] / months
        left_panel_stats['pbar_width'] =  left_panel_stats['rate'] / 10.0
    else:
        left_panel_stats['rate'] = 0
        left_panel_stats['pbar_width'] = 0
    left_panel_stats['photo_link'] = "http://s3.amazonaws.com/dg_farmerbook/partner/" + str(partner_id) + ".jpg"
    
    vill_id_list = get_id_with_images.get_village_list()
    top_vill = Village.objects.filter(id__in = vill_id_list,
                                       block__district__partner = partner_id).values('id').annotate(num_screenings = Count('screening')).order_by('-num_screenings')[:10].values_list('id',
                                                                                                                                                                          'village_name',
                                                                                                                                                                          'num_screenings')


    id_list = get_id_with_images.get_partner_list()
    partner_stats_dict = defaultdict(lambda:[0, 0, 0, 0, 0, 0, 0, 0])
    other_partner_info = Partners.objects.filter(id__in = id_list).exclude(id = partner_id).values_list('id','partner_name','date_of_association')
    for partner_id,partner_name,startdate in other_partner_info:
        partner_stats_dict[partner_id][0] = partner_id
        partner_stats_dict[partner_id][1] = partner_name
        partner_stats_dict[partner_id][2] = Screening.objects.filter(village__block__district__partner__id = partner_id).count()
        if(startdate):
            partner_stats_dict[partner_id][3] = startdate
            months = ((datetime.date.today() - partner_stats_dict[partner_id][3]).days)/30.0
            partner_stats_dict[partner_id][4] = partner_stats_dict[partner_id][2] / months
            partner_stats_dict[partner_id][5] =  Animator.objects.filter(partner__id = partner_id).values('partner').annotate(tot = Sum('total_adoptions')).values_list('tot')[0][0]
        else:
            partner_stats_dict[partner_id][3] = ""
            partner_stats_dict[partner_id][4]= 0
            partner_stats_dict[partner_id][5]= 0
        partner_stats_dict[partner_id][6] = "http://s3.amazonaws.com/dg_farmerbook/partner/" + str(partner_id) + ".jpg"
        
    sorted_partner_list = sorted(partner_stats_dict.items(), key = lambda(k, v):(v[4],k), reverse=True)   
    
    top_related_stats = []
    for obj in sorted_partner_list:
            top_related_stats.append({'id': obj[1][0],
                                         'name': obj[1][1],
                                         'screenings': obj[1][2],
                                         'photo_link': obj[1][6],
                                         'rate': obj[1][4],
                                         'adoptions': obj[1][5],
                                         'ratewidth': (obj[1][4]/10.0),
                                         'start_date': obj[1][3]})
    
    return render_to_response('partner_page.html', dict(left_panel_stats = left_panel_stats , partner_stats = top_related_stats, top_vill = top_vill))

# function to return the string displayed on tooltip 

def make_text_from_stats(obj,vids_stats_dict):
    text_to_return = ""
    if(vids_stats_dict[obj[0]][4]):
        text_to_return = text_to_return + "<b>" + str(vids_stats_dict[obj[0]][4])+ "</b>" + " Disseminations <br />"
    if(vids_stats_dict[obj[0]][3]):
        text_to_return = text_to_return + "<b>" + str(vids_stats_dict[obj[0]][3])+ "</b>" +  " Farmers Attended <br />"
    if(vids_stats_dict[obj[0]][0]):
        text_to_return = text_to_return + "<b>" + str(vids_stats_dict[obj[0]][0]) + "</b>" +  " Interested <br />"
    if(vids_stats_dict[obj[0]][1]):
        text_to_return = text_to_return + "<b>" + str(vids_stats_dict[obj[0]][1]) + "</b>" + " Questioners <br />"
    if(vids_stats_dict[obj[0]][2]):
        text_to_return = text_to_return + "<b>" + str(vids_stats_dict[obj[0]][2])+ "</b>"  + " Adopters <br />"
    return text_to_return
    
def make_text_from_person_stats(obj,vids_stats_dict):
    text_to_return = ""
    if(vids_stats_dict[obj[0]][0]):
        text_to_return = text_to_return + " Interested <br />"
    if(vids_stats_dict[obj[0]][1]):
        text_to_return = text_to_return + " Question asked <br />"
    if(vids_stats_dict[obj[0]][2]):
        text_to_return = text_to_return + " Adopted <br />"
    return text_to_return
