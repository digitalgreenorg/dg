from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',   
    (r'^main.js$', direct_to_template, {'template': 'main.js', 'mimetype':'text/javascript'}),
    (r'^$', direct_to_template, {'template': 'home.html', 'extra_context': {'header': {'jsController':'Home', 'loggedIn':False}}}),
    (r'^discover/$', direct_to_template, {'template': 'collections.html', 'extra_context': {'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}}),
    (r'^collections/$', direct_to_template, {'template': 'collections-view.html', 'extra_context': {'header': {'jsController':'ViewCollections', 'loggedIn':False}}}),
    (r'^about/$', direct_to_template, {'template': 'about.html', 'extra_context': {'header': {'jsController':'About', 'currentPage':'About', 'loggedIn':False}}}),
    (r'^connect/$', direct_to_template, {'template': 'profile.html', 'extra_context': {'header': {'jsController':'Profile', 'currentPage':'Connect', 'loggedIn':False}}}),
)
