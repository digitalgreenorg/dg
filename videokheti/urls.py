from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from videokheti.views import home, level, play_video


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^kheti/$', level),
    url(r'^video/$', play_video),
)
