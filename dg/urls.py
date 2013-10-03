from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import coco.urls
import feeds.urls
import social_website.api_urls
import social_website.urls
from dashboard.data_log import send_updated_log
from dashboard.views import feed_animators, get_person, redirect_url, search
from farmerbook import farmer_book_views
from output.views import video_analytics
from website_admin import website_admin
import website_archive_urls

from social_auth.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include(social_website.urls)),
    url(r'', include('social_auth.urls')),

    (r'^social/', include(social_website.api_urls)),
    (r'^bmgf/', include(feeds.urls)),
    (r'^archive/', include(website_archive_urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^adminwebsite/', include(website_admin.urls)),
    
    (r'^coco/', include(coco.urls)),
    (r'^path/', include('path.urls')),
    (r'^analytics/', include('output.urls')),
    (r'^video/?$',video_analytics.video),
    (r'^videotask/', include('video_practice_map.urls')),
    # Imports from dashboard
    (r'^feeds/', include('dashboard.urls_feeds')),
    (r'^animators-by-village-id/(\d+)/$', feed_animators),
    (r'/search/', search),
    (r'^dashboard/', include('dashboard.urls')),
    (r'^get/person/$', get_person),
    (r'^get_log/?$', send_updated_log),
    # End imports from dashboard
    
    # Imports from farmerbook
    (r'^farmerbook/$', farmer_book_views.get_home_page),
    (r'^farmerbook/(?P<type>\D*)/(?P<id>\d*)/$', farmer_book_views.get_home_page),
    (r'^trial/?$', farmer_book_views.get_admin_panel),
    (r'^getvillagepage/?$', farmer_book_views.get_village_page),
    (r'^getserviceproviderpage/?$', farmer_book_views.get_csp_page),
    (r'^getpartnerpage/?$', farmer_book_views.get_partner_page),
    (r'^getpersonpage/?$', farmer_book_views.get_person_page),
    (r'^getgrouppage/?$', farmer_book_views.get_group_page),
    (r'^getvillages/?$', farmer_book_views.get_villages_with_images),
    (r'^getvideosproduced/?$', farmer_book_views.get_videos_produced),
    (r'^fbconnect/', include('fbconnect.urls')),
)

# Static files serving locally
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    