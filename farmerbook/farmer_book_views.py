from collections import defaultdict
from django.shortcuts import *
from django.http import Http404, HttpResponse
from django.utils import simplejson
from dashboard.models import *
from django.db.models import Count
import datetime
from django.template.loader import render_to_string

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
    #if request.is_ajax():
    village_ids = [10000000019913,10000000020394,10000000000074,7000001207,10000000000067,10000000000048,10000000000230,10000000000093,10000000019918,10000000000031,10000000000102,34000003805,10000000000217,10000000019902,10000000018676,10000000019901,47000001122,47000001044,47000051353,47000052364,47000056970,10000000000053,10000000000052,10000000000096,10000000000097,10000000000099,10000000000100,10000000000103,10000000000119,10000000000393,10000000000122,10000000000112,10000000000249,10000000000077,10000000000124,10000000000305,10000000000307,10000000000306,10000000000341,10000000000309,10000000000313,10000000000394,10000000000389,10000000000406,10000000000504,10000000000342,10000000000536,10000000000538,10000000000537,10000000000507,10000000000120,10000000000514,10000000019860,10000000019862,10000000019864,10000000019874,10000000019834,10000000019880,10000000019882,10000000019883,10000000019889,10000000019835,10000000019842,10000000019891,10000000019922,10000000019854,10000000019929,10000000019942,10000000019945,10000000019954,10000000019967,10000000019873,10000000019975,10000000019968,10000000019969,10000000019978,10000000019985,10000000019988,10000000000092,10000000020079,10000000020104,47000001038,10000000020110,10000000020119,10000000020120,10000000020106,10000000020105,10000000019865,10000000020020,10000000019841,10000000020444,10000000020448,10000000000078,10000000020572,10000000020369,10000000020594,10000000020370,10000000020647,10000000020649,10000000020538]
    vil_ids = Village.objects.filter(id__in = village_ids).exclude( block__district__state__state_name = 'Karnataka').values_list('id', flat=True)
    return HttpResponse(simplejson.dumps(list(vil_ids)), mimetype="application/json")

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
    left_panel_stats['tot_videos'] = Video.objects.filter(screening__village__id = village_id).distinct().count()
    left_panel_stats['tot_questions'] = PersonMeetingAttendance.objects.filter(person__in = farmerbook_farmers, person__village__id = village_id).exclude(expressed_question = '').count()
    left_panel_stats['tot_adoptions'] = PersonAdoptPractice.objects.filter(person__in = farmerbook_farmers, person__village__id = village_id).count()
    left_panel_stats['vil_groups'] = PersonGroups.objects.filter(village__id = village_id).values_list('id', 'group_name')
    left_panel_stats['partner'] = Partners.objects.filter(district__block__village__id = village_id).values_list('id', 'partner_name')
    left_panel_stats['service_provider'] = Animator.objects.filter(animatorassignedvillage__village__id = village_id).order_by('-id').values_list('id', 'name')[:1]
    left_panel_stats['vil_details'] = Village.objects.filter(id = village_id).values_list('id', 'village_name', 'block__district__district_name', 'block__district__state__state_name', 'start_date')
    left_panel_stats['start_date'] = Person.farmerbook_objects.filter(village__id = village_id).exclude(date_of_joining=None).values_list('date_of_joining', flat=True).order_by('date_of_joining')[0]
    #rightpanel top contents
    #some problem in retrieving screening__date from Video Objects
    #vids_watched = Video.objects.filter(screening__village__id = village_id).distinct().values_list('id', 'title', 'youtubeid', 'screening__date')[0:5]
    vids_id = Video.objects.filter(screening__village__id = village_id).distinct().values_list('id', flat = True)
    vids_id = list(vids_id)
    vids_details = Video.objects.filter(id__in = vids_id).distinct().values_list('id', 'title', 'youtubeid')
    pma = PersonMeetingAttendance.objects.filter(person__in = farmerbook_farmers, person__village__id = village_id, screening__videoes_screened__id__in = vids_id).distinct().values_list('screening__videoes_screened__id','interested', 'expressed_question')   
    vids_stats_dict = defaultdict(lambda:[0, 0, 0])
    for l, m, n in pma:
        if(m):
            vids_stats_dict[l][0] += 1
        if(n != ""):
            vids_stats_dict[l][1] += 1
    for item in vids_stats_dict:
        vids_stats_dict[item][2] = PersonAdoptPractice.objects.filter(person__in = farmerbook_farmers, person__village__id = village_id, video__id = item).count()        
    #videos_watched_stats contain list of dictionaries containing stats of video titles
    videos_watched_stats = []
    for obj in vids_details:
        last_seen_date = Video.objects.filter(id = obj[0]).order_by('-screening__date').values_list('screening__date', flat=True)[0]
        videos_watched_stats.append({'id':obj[0], 'title':obj[1], 'youtubeid':obj[2], 'adopters':vids_stats_dict[obj[0]][2],'interested':vids_stats_dict[obj[0]][0], 'last_seen_date':last_seen_date, 'questioners': vids_stats_dict[obj[0]][1]})
    newlist = sorted(videos_watched_stats, key=lambda k: k['last_seen_date'], reverse=True)
    #right panel bottom contents. Leader boards of farmers
    #get all persons from village who attended any screening in village
    screenings_attended = PersonMeetingAttendance.objects.filter(person__in = farmerbook_farmers, person__village__id = village_id).values_list('person_id', flat=True)
    views_dict = defaultdict(lambda:[0, 0, 0])
    #get number of viewings for each farmer
    for i in screenings_attended:
        views_dict[i][0] += 1
    #get number of adoptions for each farmer
    adoptions = PersonAdoptPractice.objects.filter(person__in = farmerbook_farmers, person__village__id = village_id).values_list('person_id', flat=True)
    adoptions_dict = defaultdict(int)
    for i in adoptions:
        adoptions_dict[i] += 1
    #appending adoptions and adoption rate of farmers in views_dict
    for k,v in views_dict.iteritems():
        if k in adoptions_dict:
            views_dict[k][1] = adoptions_dict[k]
            views_dict[k][2] = float((views_dict[k][1] / float(views_dict[k][0])) * 100)
    sorted_list_stats = sorted(views_dict.items(), key = lambda(k, v):(v[2], k), reverse=True)
    top_adopters_list = sorted_list_stats[:10]
    top_adopters_id_list = []
    for i in top_adopters_list:
        top_adopters_id_list.append(i[0])
    #get last adopted video
    #last_adopted_details = PersonAdoptPractice.objects.filter(person__id__in = top_adopters_id_list).order_by('-date_of_adoption').values_list('person_id', 'person__person_name', 'video__title', 'date_of_adoption', 'person__date_of_joining')
    last_adopted_details = Person.farmerbook_objects.filter(id__in = top_adopters_id_list).values_list('id', 'person_name', 'personadoptpractice__video__title', 'personadoptpractice__date_of_adoption', 'date_of_joining')
    #remove duplicates and append recent date
    d = defaultdict(list)
    for item in last_adopted_details:
        if item[0] not in d:
            d[item[0]].append([item[1], item[2], item[3], item[4]])
    top_adopters_stats = []
    for obj in top_adopters_list:
        if obj[0] in d:
            top_adopters_stats.append({'id': obj[0], 'name': d[obj[0]][0][0], 'title': d[obj[0]][0][1], 'date_of_adoption': d[obj[0]][0][2], 'date_of_joining': d[obj[0]][0][3], 'views': obj[1][0], 'adoptions': obj[1][1], 'adoption_rate': obj[1][2]})
    
    sorted_views_stats = sorted(views_dict.items(), key = lambda(k, v):(v[0], k), reverse=True)
    top_viewers_list = sorted_views_stats[:10]
    top_viewers_id_list = []
    for i in top_viewers_list:
        top_viewers_id_list.append(i[0])
    #get last adopted video
    #last_adopted_details = PersonAdoptPractice.objects.filter(person__id__in = top_adopters_id_list).order_by('-date_of_adoption').values_list('person_id', 'person__person_name', 'video__title', 'date_of_adoption', 'person__date_of_joining')
    last_adopted_details = Person.farmerbook_objects.filter(id__in = top_viewers_id_list).values_list('id', 'person_name', 'personadoptpractice__video__title', 'personadoptpractice__date_of_adoption', 'date_of_joining')
    #remove duplicates and append recent date
    d = defaultdict(list)
    for item in last_adopted_details:
        if item[0] not in d:
            d[item[0]].append([item[1], item[2], item[3], item[4]])
    top_viewers_stats = []
    for obj in top_viewers_list:
        if obj[0] in d:
            top_viewers_stats.append({'id': obj[0], 'name': d[obj[0]][0][0], 'title': d[obj[0]][0][1], 'date_of_adoption': d[obj[0]][0][2], 'date_of_joining': d[obj[0]][0][3], 'views': obj[1][0], 'adoptions': obj[1][1], 'adoption_rate': obj[1][2]})
    
    return render_to_response('vil_page.html', dict(top_viewers_stats=top_viewers_stats, left_panel_stats = left_panel_stats, videos_watched_stats = newlist, top_adopters_stats = top_adopters_stats))

def get_person_page(request):
    person_id = int(request.GET['person_id'])
    #person_id = 6000002570
    #left panel stats dictionary hold values related to left panel of village page
    left_panel_stats = {}
    left_panel_stats['farmer_details'] = Person.objects.filter(id = person_id).values_list('id', 'person_name', 'father_name', 'group__group_name', 'village__village_name', 'village__block__district__district_name', 'village__block__district__state__state_name','date_of_joining', 'village__id')
    person_views = PersonMeetingAttendance.objects.filter(person__id = person_id).distinct().count()
    person_adoptions = PersonAdoptPractice.objects.filter(person__id = person_id).distinct().count()
    if(person_adoptions):
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
    #rightpanel top contents
    #some problem in retrieving screening__date from Video Objects
    #vids_watched = Video.objects.filter(screening__village__id = village_id).distinct().values_list('id', 'title', 'youtubeid', 'screening__date')[0:5]
    vids_id = Video.objects.filter(screening__personmeetingattendance__person__id = person_id).distinct().values_list('id', flat = True)
    vids_id = list(vids_id)
    vids_details = Video.objects.filter(id__in = vids_id).distinct().values_list('id', 'title', 'youtubeid')
    videos_watched_stats = []
    for obj in vids_details:
        last_seen_date = Video.objects.filter(id = obj[0]).order_by('-screening__date').values_list('screening__date', flat=True)[0]
        question_interested = PersonMeetingAttendance.objects.filter(person__id = person_id, screening__videoes_screened__id = obj[0]).distinct().values_list('interested', 'expressed_question')[0]
        interested = question_interested[0]
        question = question_interested[1]
        if interested:
            if obj[0] == 6000024740:
                question = 'why you are using only neem cake?'
            if obj[0] == 10000000019891:
                question = "what is the cost of setting this up?"
        adopted = PersonAdoptPractice.objects.filter(person__id = person_id, video__id = obj[0]).count()
        videos_watched_stats.append({'id':obj[0], 'title':obj[1], 'youtubeid':obj[2], 'last_seen_date':last_seen_date, 'adopted':adopted, 'interested':interested, 'question':question})
    newlist = sorted(videos_watched_stats, key=lambda k: k['last_seen_date'], reverse=True)
    village_id = Person.objects.filter(id=person_id).values_list('village__id', flat=True)
    group_id = Person.objects.filter(id=person_id).values_list('group__id', flat=True)
    #get all persons from village who attended any screening in village
    screenings_attended = PersonMeetingAttendance.objects.filter(person__image_exists=True, person__village__id = village_id).values_list('person_id', flat=True)
    views_dict = defaultdict(lambda:[0, 0, 0])
    #get number of viewings for each farmer
    for i in screenings_attended:
        views_dict[i][0] += 1
    #get number of adoptions for each farmer
    adoptions = PersonAdoptPractice.objects.filter(person__image_exists=True, person__village__id = village_id).values_list('person_id', flat=True)
    adoptions_dict = defaultdict(int)
    for i in adoptions:
        adoptions_dict[i] += 1
    #appending adoptions and adoption rate of farmers in views_dict
    for k,v in views_dict.iteritems():
        if k in adoptions_dict:
            views_dict[k][1] = adoptions_dict[k]
            views_dict[k][2] = float((views_dict[k][1] / float(views_dict[k][0])) * 100)
    sorted_list_stats = sorted(views_dict.items(), key = lambda(k, v):(v[2], k), reverse=True)
    top_adopters_list = sorted_list_stats[5:15]
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
    
    return render_to_response('person_page.html', dict(left_panel_stats = left_panel_stats, videos_watched_stats = newlist, top_adopters_stats=top_adopters_stats))

def get_group_page(request):
    group_id = int(request.GET['group_id'])
    vil_id = Village.objects.filter(persongroups__id = group_id).values_list('id', flat=True)
    #left panel stats dict hold values related to left panel of village page
    left_panel_stats = {}
    persons_id = Person.objects.filter(group__id = group_id).values_list('id', flat=True)
    #problem with videos_produced query
    left_panel_stats['videos_produced'] = Video.objects.filter(farmers_shown__person__id__in = persons_id).distinct().count()
    left_panel_stats['group_members'] = Person.objects.filter(group__id = group_id).distinct().count()
    left_panel_stats['videos_watched'] = Video.objects.filter(screening__personmeetingattendance__person__group__id = group_id).distinct().count()
    left_panel_stats['tot_questions'] = PersonMeetingAttendance.objects.filter(person__group__id = group_id).exclude(expressed_question = '').count()
    left_panel_stats['tot_adoptions'] = PersonAdoptPractice.objects.filter(person__group__id = group_id).count()
    left_panel_stats['partner'] = Partners.objects.filter(district__block__village__id = vil_id).values_list('id', 'partner_name')
    left_panel_stats['service_provider'] = Animator.objects.filter(animatorassignedvillage__village__id = vil_id).order_by('-id').values_list('id', 'name')[:1]
    left_panel_stats['group_details'] = PersonGroups.objects.filter(id = group_id).values_list('id', 'group_name','village__village_name' ,'village__block__block_name' ,'village__block__district__district_name', 'village__block__district__state__state_name', 'village__id')
    start_date = Person.objects.filter(group__id = group_id).exclude(date_of_joining=None).order_by('date_of_joining').values_list('date_of_joining', flat=True)
    if(start_date):
        left_panel_stats['start_date'] = start_date[0]
    else:
        left_panel_stats['start_date'] = ""
    #rightpanel top contents
    #some problem in retrieving screening__date from Video Objects
    #vids_watched = Video.objects.filter(screening__village__id = village_id).distinct().values_list('id', 'title', 'youtubeid', 'screening__date')[0:5]
    vids_id = Video.objects.filter(screening__personmeetingattendance__person__group__id = group_id).distinct().values_list('id', flat = True)
    vids_id = list(vids_id)
    vids_details = Video.objects.filter(id__in = vids_id).distinct().values_list('id', 'title', 'youtubeid')
    pma = PersonMeetingAttendance.objects.filter(person__group__id = group_id, screening__videoes_screened__id__in = vids_id).distinct().values_list('screening__videoes_screened__id','interested', 'expressed_question')   
    vids_stats_dict = defaultdict(lambda:[0, 0, 0])
    for l, m, n in pma:
        if(m):
            vids_stats_dict[l][0] += 1
        if(n != ""):
            vids_stats_dict[l][1] += 1
    for item in vids_stats_dict:
        vids_stats_dict[item][2] = PersonAdoptPractice.objects.filter(person__group__id = group_id, video__id = item).count()        
    #videos_watched_stats contain list of dictionaries containing stats of video titles
    videos_watched_stats = []
    for obj in vids_details:
        last_seen_date = Video.objects.filter(id = obj[0]).order_by('-screening__date').values_list('screening__date', flat=True)[0]
        videos_watched_stats.append({'id':obj[0], 'title':obj[1], 'youtubeid':obj[2], 'adopters':vids_stats_dict[obj[0]][2],'interested':vids_stats_dict[obj[0]][0], 'last_seen_date':last_seen_date, 'questioners': vids_stats_dict[obj[0]][1]})
    #right panel bottom contents. Leader boards of farmers
    #get all persons from village who attended any screening in village
    screenings_attended = PersonMeetingAttendance.objects.filter(person__image_exists=True, person__group__id = group_id).values_list('person_id', flat=True)
    views_dict = defaultdict(lambda:[0, 0, 0])
    #get number of viewings for each farmer
    for i in screenings_attended:
        views_dict[i][0] += 1
    #get number of adoptions for each farmer
    adoptions = PersonAdoptPractice.objects.filter(person__image_exists=True, person__group__id = group_id).values_list('person_id', flat=True)
    adoptions_dict = defaultdict(int)
    for i in adoptions:
        adoptions_dict[i] += 1
    #appending adoptions and adoption rate of farmers in views_dict
    for k,v in views_dict.iteritems():
        if k in adoptions_dict:
            views_dict[k][1] = adoptions_dict[k]
            views_dict[k][2] = float((views_dict[k][1] / float(views_dict[k][0])) * 100)
    sorted_list_stats = sorted(views_dict.items(), key = lambda(k, v):(v[2], k), reverse=True)
    top_adopters_list = sorted_list_stats
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
    
    sorted_views_stats = sorted(views_dict.items(), key = lambda(k, v):(v[0], k), reverse=True)
    top_viewers_list = sorted_views_stats
    top_viewers_id_list = []
    for i in top_viewers_list:
        top_viewers_id_list.append(i[0])
    #get last adopted video
    #last_adopted_details = PersonAdoptPractice.objects.filter(person__id__in = top_adopters_id_list).order_by('-date_of_adoption').values_list('person_id', 'person__person_name', 'video__title', 'date_of_adoption', 'person__date_of_joining')
    last_adopted_details = Person.objects.filter(id__in = top_viewers_id_list).values_list('id', 'person_name', 'personadoptpractice__video__title', 'personadoptpractice__date_of_adoption', 'date_of_joining')
    #remove duplicates and append recent date
    d = defaultdict(list)
    for item in last_adopted_details:
        if item[0] not in d:
            d[item[0]].append([item[1], item[2], item[3], item[4]])
    top_viewers_stats = []
    for obj in top_viewers_list:
        if obj[0] in d:
            top_viewers_stats.append({'id': obj[0], 'name': d[obj[0]][0][0], 'title': d[obj[0]][0][1], 'date_of_adoption': d[obj[0]][0][2], 'date_of_joining': d[obj[0]][0][3], 'views': obj[1][0], 'adoptions': obj[1][1], 'adoption_rate': obj[1][2]})
    
    return render_to_response('person_group_page.html', dict(left_panel_stats = left_panel_stats, videos_watched_stats = videos_watched_stats, top_adopters_stats = top_adopters_stats, top_viewers_stats = top_viewers_stats))

