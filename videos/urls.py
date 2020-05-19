from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from social_website.views import collection_view, video_view, search_view, collection_edit_view, collection_add_view, partner_view
from social_website.urls import DirectTemplateView

from output.views import video_analytics

from dg.base_settings import VIDEOS_PAGE
from dg.website_admin import website_admin

from activities import urls as acturls

import videokheti.urls

# coco_api specific import
from videos import views


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=VIDEOS_PAGE)),
    url(r'^collection-add/(?P<collection>.+)/$', collection_edit_view, name='edit_collection'),
    url(r'^collection-add/$', collection_add_view, name='create_collection'),
    url(r'^library/video/(?P<uid>.+)/$', video_view, name="video_page"),
    url(r'^library/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/(?P<video>\d+)/$', collection_view, name="collection_video_page"), 
    url(r'^library/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/$', collection_view, name="collection_page"),     
    url(r'^library/?$', search_view, name='search'),
    url(r'^library/$', DirectTemplateView.as_view(template_name='collections.html', extra_context={'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}), name='discover'),
    url(r'^connect/(?P<partner>.+)/$', partner_view, name='partner'),
    (r'^videokheti/', include(videokheti.urls)),
    (r'^search/$',video_analytics.video_search),
    url(r'^video/$',video_analytics.video, name='video'),
    # admin/logout/ should be above admin/ URL
    url(r'^admin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/videos/admin/'}),
    (r'^admin/', include(website_admin.urls)),

    # coco_api video urls
    # as_view method takes type of request as key and class's method name as value 
    url('api/videos', views.VideoViewSet.as_view()), 

)
