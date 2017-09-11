from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from social_website.views import collection_view, video_view, search_view
from social_website.urls import DirectTemplateView

from output.views import video_analytics

from dg.base_settings import VIDEOS_PAGE

import videokheti.urls

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=VIDEOS_PAGE)),
    url(r'^library/video/(?P<uid>.+)/$', video_view, name="video_page"),
    url(r'^library/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/(?P<video>\d+)/$', collection_view, name="collection_video_page"), 
    url(r'^library/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/$', collection_view, name="collection_page"),     
    url(r'^library/?$', search_view, name='search'),
    url(r'^library/$', DirectTemplateView.as_view(template_name='collections.html', extra_context={'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}), name='discover'),
    (r'^videokheti/', include(videokheti.urls)),
    (r'^search/$',video_analytics.video_search),
    url(r'^video/?$',video_analytics.video, name='video'),
)
