from collections import defaultdict
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import Template, Context

from dashboard.models import Practices, PracticeTopic, PracticeSubtopic, PracticeSector, PracticeSubSector, PracticeSubject, Video
from video_practice_map.models import VideoPractice,SkippedVideo


@login_required(login_url='/videotask/login/')
@user_passes_test(lambda u: u.groups.filter(name='Video Classifiers').count() > 0, login_url='/videotask/login/?failed=true')
def home(request):
    can_change_filter = can_reset_skipped = False # For showing message on no video for assign or review. 
                                                  # There can be skipped vidoes or videos in other filter options (language/state) 
    next_action = "assign"
    if 'count' in request.session:
        request.session['count'] = request.session['count'] + 1
        if request.session['count'] % 5 == 0:  #every 6th action is review
            next_action = "review"
    else:
        request.session['count'] = 0
        
    
    language = int(request.session['lang']) if 'lang' in request.session and request.session['lang'] != '-1' else None
    state = int(request.session['state']) if 'state' in request.session and request.session['state'] != '-1' else None
    user = request.user
    user.associated_count = VideoPractice.objects.filter(user=user).count()
    user.reviewed_count = VideoPractice.objects.filter(review_user=user).count()
    videos = Video.objects.exclude(skippedvideo__user = user)
    if language:
        videos = videos.filter(language__id = language)
    if state:
        videos = videos.filter(village__block__district__state__id = state)
    vid = review_videos = assign_videos = None
    
    if next_action == 'review':
        review_videos = videos.filter(id__in = VideoPractice.objects.filter(review_user = None).exclude(user=user).values_list('video', flat=True).distinct())
        if review_videos.count() == 0:
            #No videos to be reviewed
            next_action = 'assign'
        else:
            vid = review_videos[0]
    if next_action == 'assign':
        assign_videos = videos.exclude(id__in = VideoPractice.objects.values_list('video',flat=True).distinct())
        if assign_videos.count() == 0:
            #No videos to assign. Check for remaining to-be-reviewed videos
            if review_videos is None:
                review_videos = videos.filter(id__in = VideoPractice.objects.filter(review_user = None).exclude(user=user).values_list('video', flat=True).distinct())
                if review_videos.count() != 0:
                    next_action = 'review'
                    vid = review_videos[0]
                else:
                    can_change_filter, can_reset_skipped = get_end_of_videos_status(user, language, state)
            else:
                can_change_filter, can_reset_skipped = get_end_of_videos_status(user, language, state)
               

        else:
            vid = assign_videos[0]
    review_vid_pr = None
    vid_pr_id=None
    if vid and next_action == "review":
        vid_pr=VideoPractice.objects.get(review_user=None, video=vid)
        review_vid_pr = vid_pr.practice 
        vid_pr_id = vid_pr.id
                
    return render_to_response("video_practice_map/home.html", dict(vid=vid, user=user, task_type=next_action, selected_lang=language,
                                                                   selected_state=state, practice_tups = all_practice_options(), new_pr = review_vid_pr,vid_pr_id=vid_pr_id, 
                                                                   can_change_filter=can_change_filter, can_reset_skipped=can_reset_skipped))
                                                                   
    
def get_end_of_videos_status(user, language, state):
    can_change_filter = can_reset_skipped = False
    if SkippedVideo.objects.filter(user = user).values_list('video', flat = True).count() != 0:
        can_reset_skipped = True
    if (language is not None or state is not None) and \
       (VideoPractice.objects.filter(review_user=None).exclude(user=user).exists() or \
        Video.objects.exclude(skippedvideo__user=user).exclude(id__in = VideoPractice.objects.values_list('video',flat=True).distinct()).exists()):
           can_change_filter = True
    return can_change_filter, can_reset_skipped

@login_required(login_url='/videotask/login/')
def reset_skipped(request):
    SkippedVideo.objects.filter(user = request.user).delete()
    return HttpResponseRedirect('/videotask/home/')
    
@login_required(login_url='/videotask/login/')
def set_options(request):
    for key, value in request.GET.iteritems():
        request.session[key] = value
    return HttpResponseRedirect('/videotask/home/')

@login_required(login_url='/videotask/login/')
def logout_view(request):
    logout(request)
    
    return HttpResponseRedirect('/videotask/home/')

@login_required(login_url='/videotask/login/')
def form_submit(request):
    if request.POST:
        if request.POST['action'] == 'review':
            check_vp = VideoPractice.objects.get(id=int(request.POST['vid_pr_id']))
            if check_vp.review_approved is not None:
                return HttpResponseRedirect('/videotask/home/')
        
        if 'yes' in request.POST:  #Submitted a new practice
            field_arr = ['practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject']
            selected_vals = []
            for field in field_arr:
                selected_vals.append(int(request.POST[field]) if request.POST[field] != "None" else None)
            pr = Practices.objects.get(*zip(field_arr, selected_vals))
            vid = Video.objects.get(id=int(request.POST['vid_id']))
            if request.POST['action'] == 'review':
                vid_pr = VideoPractice.objects.get(video=vid, review_user=None)
                vid_pr.review_user = request.user
                vid_pr.review_approved = False
                vid_pr.save()
            VideoPractice.objects.create(user=request.user,
                                         video=vid,
                                         practice = pr)
        elif 'skip' in request.POST:  #Skipped this video
            SkippedVideo.objects.create(user=request.user,
                                        video=Video.objects.get(pk=int(request.POST['vid_id'])))
        
        elif 'accept' in request.POST:  #Accepted for review
            video=Video.objects.get(id=int(request.POST['vid_id']))
            vid_pr = VideoPractice.objects.get(video=video, review_user=None)
            vid_pr.review_user = request.user
            vid_pr.review_approved = True
            vid_pr.save()
            video.related_practice = vid_pr.practice
            video.save()
            
    return HttpResponseRedirect('/videotask/home/')


def practice_filter_options(request):
    pr = Practices.objects.all()
    field_arr = ['practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject']
    model_arr = [PracticeSector, PracticeSubSector, PracticeTopic, PracticeSubtopic, PracticeSubject]
    output_arr = []
    for model, field in zip(model_arr, field_arr):
        if request.GET[field]:
            if request.GET[field] == "None":
                output_arr.append("<option value='None'>None</option>")
                pr = pr.filter(**{field:None})
            else:
                id = int(request.GET[field])
                obj = model.objects.get(id=id)
                pr = pr.filter(**{field:id})
                output_arr.append("<option value='%d'>%s</option>" % (obj.id, obj.name))
        else:
            output_arr.append('')
            
    default_selects = ["<option value=''>Select Sector</option>",
                       "<option value=''>Select Sub-sector</option>",
                       "<option value=''>Select Practice</option>",
                       "<option value=''>Select Sub-practice</option>",
                       "<option value=''>Select Subject</option>"]
    t = Template("{% for obj in list %}<option value='{{obj.0}}'>{{obj.1}}</option>{% endfor %}")            
    for i, field in enumerate(field_arr):
        if not request.GET[field]:
            values = sorted(list(pr.values_list(field, field+"__name").distinct()), key=lambda x: x[1])
            if len(values) > 1:
                output_arr[i] = default_selects[i] + t.render(Context(dict(list=values)))
            else:
                output_arr[i] = t.render(Context(dict(list=values)))
            
    return HttpResponse(json.dumps(output_arr))

def all_practice_options(request=None):
    model_arr = [PracticeSector, PracticeSubSector, PracticeTopic, PracticeSubtopic, PracticeSubject]
    value_arr = [model.objects.values_list('id', 'name').order_by('name') for model in model_arr]
    if request:
        output_arr = ["<option value=''>Select Sector</option>",
                       "<option value=''>Select Sub-sector</option>",
                       "<option value=''>Select Practice</option>",
                       "<option value=''>Select Sub-practice</option>",
                       "<option value=''>Select Subject</option>"]
        t = Template("{% for obj in list %}<option value='{{obj.0}}'>{{obj.1}}</option>{% endfor %}")
        for i, value in enumerate(value_arr):
            output_arr[i] = output_arr[i] + t.render(Context(dict(list=value)))
        
        return HttpResponse(json.dumps(output_arr))
    else:
        return value_arr
    
@login_required(login_url='/videotask/login/')
@user_passes_test(lambda u: u.groups.filter(name='Practice Creators').count() > 0, login_url='/videotask/login/')
def add_new(request):
    msg = None
    
    if request.POST:    
        if request.POST['form_type'] == "combinations":
            sectors = map(int, request.POST.getlist('sector'))
            sub_sectors = map(int, request.POST.getlist('sub_sector'))
            main_practices = map(lambda x: None if x == 'none' else int(x), request.POST.getlist('main_practice'))
            sub_practices = map(lambda x: None if x == 'none' else int(x), request.POST.getlist('sub_practice'))
            subjects = map(lambda x: None if x == 'none' else int(x), request.POST.getlist('subject'))
            if not(sectors and sub_sectors and main_practices and sub_practices and subjects):
                msg = "One or more level is missing. Nothing saved."
            else:               
                count = 0
                for sector in sectors:
                    for sub_sector in sub_sectors:
                        for main_practice in main_practices:
                            for sub_practice in sub_practices:
                                for subject in subjects:
                                    obj, created = Practices.objects.get_or_create(practice_sector_id=sector, practice_subsector_id=sub_sector,practice_topic_id=main_practice, practice_subtopic_id=sub_practice,practice_subject_id=subject)
                                    if created:
                                        count = count + 1
                                    
                msg = "%d combinations added." % (count)
        elif request.POST['form_type'] in ('sector', 'subsector', 'practice', 'subpractice', 'subject'):
            if not request.POST['name']:
                msg = "Please enter name for %s" % (request.POST['form_type'].title())
            else:
                model_class = dict(sector=PracticeSector, subsector=PracticeSubSector, practice=PracticeTopic,
                                   subpractice=PracticeSubtopic, subject=PracticeSubject)
                obj, created = model_class[request.POST['form_type']].objects.get_or_create(name=request.POST['name'])
                if created:
                    msg = "%s - %s created." % (request.POST['form_type'].title(), request.POST['name'])
                else:
                    msg = "%s - %s already exists." % (request.POST['form_type'].title(), request.POST['name'])

    all_sectors = PracticeSector.objects.values_list('id', 'name').order_by('name')
    all_subsectors = PracticeSubSector.objects.values_list('id', 'name').order_by('name')
    all_main = PracticeTopic.objects.values_list('id', 'name').order_by('name')
    all_subpr = PracticeSubtopic.objects.values_list('id', 'name').order_by('name')
    sector_subject_tups = Practices.objects.exclude(practice_subject=None). values_list('practice_sector__name', 
                                                                                 'practice_subject__id', 
                                                                                 'practice_subject__name').distinct().order_by('practice_subject__name')
    all_subjects = defaultdict(list)
    for sector_sub_tup in sector_subject_tups:
        all_subjects[sector_sub_tup[0]].append(list(sector_sub_tup)[1:])
    not_associated = PracticeSubject.objects.exclude(id__in = set([i[1] for i in sector_subject_tups])).values_list('id', 'name').order_by('name')
    if not_associated:
        all_subjects['Not Associated'] = not_associated
    all_subjects = dict(all_subjects) # Template screws up defaultdict for iterating
    
    return render_to_response("video_practice_map/add_new.html", dict(user=request.user,
                                                                      sectors=all_sectors,
                                                                      sub_sectors=all_subsectors,
                                                                      main_practices=all_main,
                                                                      sub_practices=all_subpr,
                                                                      subjects=all_subjects,
                                                                      msg=msg))
    
    