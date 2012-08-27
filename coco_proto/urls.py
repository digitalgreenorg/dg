from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from views import *
urlpatterns = patterns('',
                url(r'^country/$', country_list, name='country_list'),
                       )