from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from videokheti.views import comment, get_comments, home, level, play_video


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^kheti/$', level),
    url(r'^video/$', play_video),
    url(r'^comment/$', comment),
    url(r'^get-comments/$', get_comments),
)
