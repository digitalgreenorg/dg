from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from dg.settings import PRODUCT_PAGE

import coco.urls
import loop.urls
import loop_ivr.urls

import social_website.urls

from django.contrib import admin
admin.autodiscover()

# from website_admin import website_admin
# from ivr_admin import ivr_admin
#from loop_ivr.admin import loop_ivr_admin
#import website_archive_urls

#loop_admin.index_template = 'social_website/index.html'
#loop_admin.login_template = 'social_website/login.html'
#loop_admin.logout_template = 'social_website/home.html'
# website_admin.index_template = 'social_website/index.html'
# website_admin.login_template = 'social_website/login.html'
# website_admin.logout_template = 'social_website/home.html'
# mcoco_admin.index_template = 'social_website/index.html'
# mcoco_admin.login_template = 'social_website/login.html'
# mcoco_admin.logout_template = 'social_website/home.html'
# ivr_admin.index_template = 'social_website/index.html'
# ivr_admin.login_template = 'social_website/login.html'
# ivr_admin.logout_template = 'social_website/home.html'
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
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': PRODUCT_PAGE}, name='logout'),
    # (r'^social/', include(social_website.api_urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    (r'^coco/', include(coco.urls)),
    url(r'^ivrsadmin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/ivrsadmin'}),
    # (r'^ivrsadmin/', include(ivr_admin.urls)),
    (r'^loop/', include(loop.urls)),
    (r'^loopivr/', include(loop_ivr.urls)),
    (r'^fbconnect/', include('fbconnect.urls')),
    (r'^coco/docs/', TemplateView.as_view(template_name='cocodoc.html')),
    # (r'^ivrs/',include('ivr.urls')),
    (r'^social/email_signature/?$', TemplateView.as_view(template_name='email_signature.html')),
    (r"^", include("mezzanine.urls")),

    # (r'^adminwebsite/', include(website_admin.urls)),
)

# Static files serving locally
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
