from django.conf.urls import include, patterns, url
from django.http import HttpResponse
from django.views.generic import View

class GreetingApplet(View):
    service_name = ""
    def __init__(self, applet_name, audio_url):
        self.applet_name = applet_name
        self.audio_url = audio_url
    
    def get(self, request):
        return HttpResponse(self.audio_url)
    
    def urlpatterns(self):
        urlpattern = patterns('',
            url(r'^{service_name}/{0}/$'.format(self.applet_name), self.(service_name).as_view()),
        )
        return urlpattern

class ServiceGreeting(GreetingApplet):
    service_name = "some_rubbish"

class IVRMenuApplet(object):
    def __init__(self, applet_name, audio_url):
        self.applet_name = applet_name
        self.audio_url

#class PassthroughApplet(object):
