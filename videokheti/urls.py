from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from videokheti.views import comment, get_comments, home, language, level, play_video


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^home/$', TemplateView.as_view(template_name='videokheti_home.html')),
    url(r'^opt/$', level),
    url(r'^video/$', play_video),
    url(r'^comment/$', comment),
    url(r'^get-comments/$', get_comments),
    url(r'^language/$', language),
)
