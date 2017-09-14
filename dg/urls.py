from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

import coco.urls
#import data_upload.urls
import dimagi.urls
import feeds.urls
#import raw_data_analytics.urls
import loop.urls
import qacoco.urls
import loop_ivr.urls

import social_website.api_urls
import social_website.urls
import videokheti.urls
import ivr.urls
import training.urls
import videos.urls

from django.contrib import admin
admin.autodiscover()

from coco.data_log import send_updated_log
from qacoco.qa_data_log import qa_send_updated_log
#from coco_admin import coco_admin
#from qacoco_admin import qacoco_admin
#from training.admin import training_admin
#from loop.admin import loop_admin
#from farmerbook import farmer_book_views
from output.views import video_analytics
from static_site_views import spring_analytics
#from website_admin import website_admin
#from mcoco_admin import mcoco_admin
from ivr_admin import ivr_admin
#from loop_ivr.admin import loop_ivr_admin
#import website_archive_urls
import deoanalytics.urls

#coco_admin.index_template = 'social_website/index.html'
#coco_admin.login_template = 'social_website/login.html'
#coco_admin.logout_template = 'social_website/home.html'
# qacoco_admin.index_template = 'social_website/index.html'
# qacoco_admin.login_template = 'social_website/login.html'
# qacoco_admin.logout_template = 'social_website/home.html'
#training_admin.index_template = 'social_website/index.html'
#training_admin.login_template = 'social_website/login.html'
#training_admin.logout_template = 'social_website/home.html'
#loop_admin.index_template = 'social_website/index.html'
#loop_admin.login_template = 'social_website/login.html'
#loop_admin.logout_template = 'social_website/home.html'
# website_admin.index_template = 'social_website/index.html'
# website_admin.login_template = 'social_website/login.html'
# website_admin.logout_template = 'social_website/home.html'
# mcoco_admin.index_template = 'social_website/index.html'
# mcoco_admin.login_template = 'social_website/login.html'
# mcoco_admin.logout_template = 'social_website/home.html'
ivr_admin.index_template = 'social_website/index.html'
ivr_admin.login_template = 'social_website/login.html'
ivr_admin.logout_template = 'social_website/home.html'
# loop_ivr_admin.index_template = 'social_website/index.html'
# loop_ivr_admin.login_template = 'social_website/login.html'
# loop_ivr_admin.logout_template = 'social_website/home.html'

urlpatterns = patterns('',
    (r'^', include(social_website.urls)),
    #(r'^', include(website_archive_urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/$', 'social_website.views.login_view', {'template_name': 'social_website/login.html'}, name='signin'),
    url(r'^signup/$', 'social_website.views.signup_view', {'template_name': 'social_website/signup.html'}, name='signup'),
    url(r'^denied/$', 'django.views.defaults.permission_denied', {'template_name': 'social_website/403.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'social_website/password_change.html', 'post_change_redirect':'/',}, name='change_password'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    (r'^social/', include(social_website.api_urls)),
    (r'^bmgf/', include(feeds.urls)),
    #(r'^archive/', include(website_archive_urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #(r'^admin/coco/cocouser/add/state_wise_district', 'coco.admin_views.state_wise_district'),
    #(r'^admin/coco/cocouser/add/district_wise_village', 'coco.admin_views.district_wise_village'),
    #(r'^admin/coco/cocouser/add/partner_wise_video', 'coco.admin_views.partner_wise_video'),
    #(r'^admin/coco/cocouser/add', 'coco.admin_views.add_cocouser'),
    #(r'^admin/coco/cocouser/[0-9]', 'coco.admin_views.add_cocouser'),
    #(r'^admin/', include(coco_admin.urls)),
    #(r'^qacoco_admin/', include(qacoco_admin.urls)),
    #(r'^adminwebsite/', include(website_admin.urls)),
    #(r'^mcocoadmin/', include(mcoco_admin.urls)),
    #(r'^trainingadmin/', include(training_admin.urls)),
    #(r'^loopadmin/', include(loop_admin.urls)),
    #(r'^loopivradmin/', include(loop_ivr_admin.urls)),
    (r'^adminblog/', include(admin.site.urls)),
    #(r'^data_upload/', include(data_upload.urls)),
    (r'^coco/', include(coco.urls)),
    (r'^qacoco/', include(qacoco.urls)),
    (r'^dimagi/', include(dimagi.urls)),
    #(r'^analytics/', include('output.urls')),
    #url(r'^video/?$',video_analytics.video, name='video'),
    (r'^videos/', include(videos.urls)),
    (r'^ivrsadmin/', include(ivr_admin.urls)),
    (r'^training/', include(training.urls)),
    (r'^loop/', include(loop.urls)),
    #(r'^raw_data_analytics/', include(raw_data_analytics.urls)),
    (r'^loopivr/', include(loop_ivr.urls)),

    (r'^get_log/?$', send_updated_log),
    (r'^qa_get_log/?$', qa_send_updated_log),
    # End imports from dashboard
    ##Special page.needs to be deleted
    (r'^spring/analytics/?$', spring_analytics),
    
    # Imports from farmerbook
    # (r'^farmerbook/$', farmer_book_views.get_home_page),
    # (r'^farmerbook/(?P<type>\D*)/(?P<id>\d*)/$', farmer_book_views.get_home_page),
    # (r'^trial/?$', farmer_book_views.get_admin_panel),
    # (r'^getvillagepage/?$', farmer_book_views.get_village_page),
    # (r'^getserviceproviderpage/?$', farmer_book_views.get_csp_page),
    # (r'^getpartnerpage/?$', farmer_book_views.get_partner_page),
    # (r'^getpersonpage/?$', farmer_book_views.get_person_page),
    # (r'^getgrouppage/?$', farmer_book_views.get_group_page),
    # (r'^getvillages/?$', farmer_book_views.get_villages_with_images),
    # (r'^getvideosproduced/?$', farmer_book_views.get_videos_produced),
    (r'^fbconnect/', include('fbconnect.urls')),
    #(r'^analytics/cocouser/',include('deoanalytics.urls')),
    #(r'^analytics/vrptool/',include('vrppayment.urls')),
    #(r'^analytics/mrptool/',include('mrppayment.urls')),
    (r'^coco/docs/', TemplateView.as_view(template_name='cocodoc.html')),
    #(r'^agri/', include(videokheti.urls)),
    (r'^ivrs/',include('ivr.urls')),
    (r"^", include("mezzanine.urls")),

    #AJAX for Feedback
    url(r'^feedbacksubmit_json$', 'dg.feedback_view.ajax'),
)

# Static files serving locally
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
