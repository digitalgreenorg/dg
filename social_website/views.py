from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import *
from dashboard.models import Language

def social_home(request):
    language=Language.objects.all().values_list('language_name',flat=True)
    language=list(language)
    context= {'header': {'jsController':'Home', 'loggedIn':False},'language':language}
    return render_to_response('home.html' , context,context_instance = RequestContext(request))
    