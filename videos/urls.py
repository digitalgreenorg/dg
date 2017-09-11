from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from social_website.views import collection_view, video_view, search_view
from social_website.urls import DirectTemplateView

from dg.base_settings import VIDEOS_PAGE

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=VIDEOS_PAGE)),
    url(r'^discover/video/(?P<uid>.+)/$', video_view, name="video_page"),
    url(r'^discover/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/(?P<video>\d+)/$', collection_view, name="collection_video_page"), 
    url(r'^discover/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/$', collection_view, name="collection_page"),     
    url(r'^discover/?$', search_view, name='search'),
    url(r'^discover/$', DirectTemplateView.as_view(template_name='collections.html', extra_context={'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}), name='discover'),

)
