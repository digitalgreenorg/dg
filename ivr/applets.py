from django.conf.urls import include, patterns, url
from django.http import HttpResponse
from django.views.generic import View

class GreetingApplet(object):
    def __init__(self, applet_name, audio_url):
        self.applet_name = applet_name
        self.audio_url = audio_url
    
    def get(self, request):
        return HttpResponse(self.audio_url)
    
    def urlpatterns(self, service_name):
        type_name = '{0}_{1}_audio'.format(service_name, self.applet_name)
        AppletView = type(type_name, (View, GreetingApplet), self.__dict__)
        urlpattern = patterns('', url(r'^{0}/$'.format(self.applet_name), AppletView.as_view()))
        return urlpattern

class ServiceGreeting(GreetingApplet):
    service_name = "some_rubbish"

class IVRMenuApplet(object):
    def __init__(self, applet_name, audio_url):
        self.applet_name = applet_name
        self.audio_url

#class PassthroughApplet(object):
