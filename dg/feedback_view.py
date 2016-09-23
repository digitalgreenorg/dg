from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from communications.models import Feedback

from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ajax(request):
    if request.POST:
        obj = Feedback()
        if request.POST.has_key('email'):
            email = request.POST['email']
            obj.email = email
        comments = request.POST['comments']
        rating = request.POST['rating']                                        
        obj.rating = rating
        obj.comments = comments   
        obj.save()                          
        return HttpResponse("0")
    else:
        return render_to_response('home.html', context_instance=RequestContext(request))
