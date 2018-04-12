from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from videokheti.views import comment, get_comments, home, home_static, language, level, play_video


urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^home/$', home_static),
    url(r'^opt/$', level),
    url(r'^video/$', play_video),
    url(r'^comment/$', comment),
    url(r'^get-comments/$', get_comments),
    url(r'^language/$', language),
)
