from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from dashboard.models import PracticeMain, PracticeSub, PracticeSector, \
    PracticeSubSector, PracticeSubject, Video
from django.contrib.auth import logout
from video_practice_map.models import *
import json
from django.template import Template, Context

@login_required(login_url='/videotask/login/')
def home(request):
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
    videos = Video.objects.exclude(id__in = SkippedVideo.objects.filter(user=user).values_list('video',flat=True))
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
                pass
                #TODO: End of App. Clear skip video or All work done.
        else:
            vid = assign_videos[0]
    review_vid_pr = None
    if vid and next_action == "review":
        review_vid_pr = VideoPractice.objects.get(review_user=None, video=vid).practice 
                
    return render_to_response("video_practice_map/home.html", dict(vid=vid, 
                                                                   user=user, 
                                                                   task_type=next_action,
                                                                   selected_lang=language,
                                                                   selected_state=state,
                                                                   practice_tups = all_practice_options(),
                                                                   new_pr = review_vid_pr))

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
        if 'yes' in request.POST:  #Submitted a new practice
            field_arr = ['top_practice', 'sub_practice', 'utility', 'type', 'subject']
            selected_vals = []
            for field in field_arr:
                selected_vals.append(int(request.POST[field]) if request.POST[field] != "None" else None)
            pr = PracticeCombination.objects.get(*zip(field_arr, selected_vals))
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
            vid_pr = VideoPractice.objects.get(video=Video.objects.get(id=int(request.POST['vid_id'])), review_user=None)
            vid_pr.review_user = request.user
            vid_pr.review_approved = True
            vid_pr.save()
            
    return HttpResponseRedirect('/videotask/home/')


def practice_filter_options(request):
    pr = PracticeCombination.objects.all()
    field_arr = ['top_practice', 'sub_practice', 'utility', 'type', 'subject']
    model_arr = [PracticeSector, PracticeSubSector, PracticeMain, PracticeSub, PracticeSubject]
    output_arr = []
    for model, field in zip(model_arr, field_arr):
        if request.GET[field]:
            if request.GET[field] == "None":
                output_arr.append("<option value='None'>None</option>")
            else:
                id = int(request.GET[field])
                obj = model.objects.get(id=id)
                pr = pr.filter(**{field:id})
                output_arr.append("<option value='%d'>%s</option>" % (obj.id, obj.name))
        else:
            output_arr.append('')
            
    default_selects = ["<option value=''>Select Sector</option>",
                       "<option value=''>Select Sub Sector</option>",
                       "<option value=''>Select Practice</option>",
                       "<option value=''>Select Sub Sector</option>",
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
    model_arr = [PracticeSector, PracticeSubSector, PracticeMain, PracticeSub, PracticeSubject]
    value_arr = [model.objects.values_list('id', 'name').order_by('name') for model in model_arr]
    if request:
        output_arr = ["<option value=''>Select Sector</option>",
                       "<option value=''>Select Sub Sector</option>",
                       "<option value=''>Select Practice</option>",
                       "<option value=''>Select Sub Sector</option>",
                       "<option value=''>Select Subject</option>"]
        t = Template("{% for obj in list %}<option value='{{obj.0}}'>{{obj.1}}</option>{% endfor %}")
        for i, value in enumerate(value_arr):
            output_arr[i] = output_arr[i] + t.render(Context(dict(list=value)))
        
        return HttpResponse(json.dumps(output_arr))
    else:
        return value_arr
    