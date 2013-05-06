from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from views import social_home
from static_site_views import home
from django.conf import settings

urlpatterns = patterns('',   
    url(r'^main.js$', direct_to_template, {'template': 'main.js', 'mimetype':'text/javascript'}, name='mainjs'),
  #  (r'^$', direct_to_template, {'template': 'home.html', 'extra_context': {'header': {'jsController':'Home', 'loggedIn':False}}}),
    url(r'^discover/$', direct_to_template, {'template': 'collections.html', 'extra_context': {'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}}, name='discover'),
    url(r'^collections/$', direct_to_template, {'template': 'collections-view.html', 'extra_context': {'header': {'jsController':'ViewCollections', 'loggedIn':False}}},name='collections'),
    url(r'^about/$', direct_to_template, {'template': 'about.html', 'extra_context': {'header': {'jsController':'About', 'currentPage':'About', 'loggedIn':False}}},name='about'),
    url(r'^connect/$', direct_to_template, {'template': 'profile.html', 'extra_context': {'header': {'jsController':'Profile', 'currentPage':'Connect', 'loggedIn':False}}},name='connect'),
    url(r'^tools/$', direct_to_template, {'template': 'home.html', 'extra_context': {'header': {'jsController':'Tools', 'currentPage':'Tools', 'loggedIn':False}}},name='tools'),
    (r'^$',social_home),
)
