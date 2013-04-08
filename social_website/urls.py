from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^main.js$', direct_to_template, {'template': 'main.js', 'mimetype':'text/javascript'}),
    (r'^about/$', direct_to_template, {'template': 'about.html', 'extra_context': {'header': {'jsController':'About', 'currentPage':'About', 'loggedIn':False}}}),
    (r'^connect/$', direct_to_template, {'template': 'about.html', 'extra_context': {'header': {'jsController':'About', 'currentPage':'Connect', 'loggedIn':False}}}),
)
