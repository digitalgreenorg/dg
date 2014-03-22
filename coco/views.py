# Create your views here.
import datetime

from django.contrib import auth
from django.core import urlresolvers
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from coco.models import FullDownloadStats
from models import CocoUser
from datetime import datetime

def coco_v2(request):
    return render(request,'dashboard.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("0")
    return HttpResponse("1")
    
def logout(request):
    auth.logout(request)    
    return HttpResponse("1")
   
def record_full_download_time(request):
    if not(request.user and request.POST["start_time"] and request.POST["end_time"]):
        return HttpResponse("0")
    stat = FullDownloadStats(user = request.user, start_time = request.POST["start_time"], end_time = request.POST["end_time"])
    stat.save()
    return HttpResponse("1")
       
def reset_database_check(request):
    if not(request.user):
        return HttpResponse("0")
    cocouser = CocoUser.objects.get(user = request.user)
    last_download_time = FullDownloadStats.objects.filter(user = request.user).aggregate(time = Max('end_time'))
    if last_download_time < datetime.datetime('2014, 3, 22, 9, 0, 0'):
        return HttpResponse("1")
    if not(cocouser and cocouser.time_modified):
        return HttpResponse("0")
    lastdownloadtime = request.GET["lastdownloadtimestamp"]
    lastdownloadtimestamp = datetime.strptime(lastdownloadtime, '%Y-%m-%dT%H:%M:%S.%f')
    if lastdownloadtimestamp<=cocouser.time_modified:
        return HttpResponse("1")
    return HttpResponse("0")    
    
               
def html_decorator(func):
    """
    This decorator wraps the output in html.
    (From http://stackoverflow.com/a/14647943)
    """
 
    def _decorated(*args, **kwargs):
        response = func(*args, **kwargs)
 
        wrapped = ("<html><body>",
                   response.content,
                   "</body></html>")
 
        return HttpResponse(wrapped)
 
    return _decorated
 
@html_decorator
def debug(request):
    """
    Debug endpoint that uses the html_decorator,
    """
    path = request.META.get("PATH_INFO")
    api_url = path.replace("debug/", "")
 
    view = urlresolvers.resolve(api_url)
 
    accept = request.META.get("HTTP_ACCEPT")
    accept += ",application/json"
    request.META["HTTP_ACCEPT"] = accept
 
    res = view.func(request, **view.kwargs)
    return HttpResponse(res._container)
 
