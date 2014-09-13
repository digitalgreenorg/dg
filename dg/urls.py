from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import coco.urls
import dimagi.urls
import feeds.urls

import social_website.api_urls
import social_website.urls
import data_upload.urls
from admin import admin
from coco.data_log import send_updated_log
from dashboard.views import feed_animators, get_person, redirect_url, search
from farmerbook import farmer_book_views
from output.views import video_analytics
from static_site_views import spring_analytics
from website_admin import website_admin
from mcoco_admin import mcoco_admin
import website_archive_urls
import deoanalytics.urls

admin.login_template = 'social_website/login.html'
admin.logout_template = 'social_website/home.html'
website_admin.login_template = 'social_website/login.html'
website_admin.logout_template = 'social_website/home.html'

urlpatterns = patterns('',
    (r'^', include(social_website.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/$', 'social_website.views.login_view', {'template_name': 'social_website/login.html'}, name='signin'),
    url(r'^signup/$', 'social_website.views.signup_view', {'template_name': 'social_website/signup.html'}, name='signup'),
    url(r'^denied/$', 'django.views.defaults.permission_denied', {'template_name': 'social_website/403.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'social_website/password_change.html', 'post_change_redirect':'/',}, name='change_password'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    (r'^social/', include(social_website.api_urls)),
    (r'^bmgf/', include(feeds.urls)),
    (r'^archive/', include(website_archive_urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.urls)),
    (r'^adminwebsite/', include(website_admin.urls)),

    (r'^mcocoadmin/', include(mcoco_admin.urls)),
    

    (r'^data_upload/', include(data_upload.urls)),

    (r'^coco/', include(coco.urls)),
    (r'^dimagi/', include(dimagi.urls)),
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
    ##Special page.needs to be deleted
    (r'^spring/analytics/?$', spring_analytics),
    
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
    
    (r'^analytics/cocouser/',include('deoanalytics.urls')),
)

# Static files serving locally
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    