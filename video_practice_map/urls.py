from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'video_practice_map/login.html'}),
    ) + \
patterns('video_practice_map.views',
    url(r'^home/$', 'home'),
    url(r'^logout/$', 'logout_view'),
    url(r'^set_options/$', 'set_options'),
    url(r'^practice_filter_options/$', 'practice_filter_options'),
    url(r'^all_practice_options/$', 'all_practice_options'),
    url(r'^form_submit/$', 'form_submit'),
)