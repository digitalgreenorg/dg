from django.conf.urls.defaults import include, patterns, url
from django.views.generic.simple import direct_to_template

from communications.views import media_view
from human_resources.views import member_view
from views import social_home, collection_view, logout_view, partner_view, search_view

urlpatterns = patterns('',
    url(r'^$', social_home, name="home"), 
    url(r'^discover/(?P<partner>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/(?P<video>\d+)/$', collection_view, name="collection_video_page"), 
    url(r'^discover/(?P<partner>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/$', collection_view, name="collection_page"), 
    url(r'^discover/?$', search_view, name='search'),
    url(r'^logout/(?P<next_url>.+)/$', logout_view, name='logout'),
    url(r'^discover/$', direct_to_template, {'template': 'collections.html', 'extra_context': {'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}}, name='discover'),
    url(r'^about/$', direct_to_template, {'template':'about.html', 'extra_context':{'header':{'currentPage':'About'}}}, name='about'),
    url(r'^about/ourwork/$', direct_to_template, {'template': 'our_work.html'}, name='ourwork'),
    url(r'^board/$', direct_to_template, {'template': 'board.html'}, name='board'),
    url(r'^careers/$', direct_to_template, {'template': 'career.html'}, name='career'),
    # TODO: Connect needs to be fixed.
    url(r'^connect/(?P<partner>.+)/$', partner_view, name='partner'),
    url(r'^contact/$', direct_to_template, {'template': 'contact.html'}, name='contact'),
    url(r'^donate/$', direct_to_template, {'template': 'donate.html'}, name='donate'),
    url(r'^example/$', direct_to_template,{'template':'example1.html'}),
    url(r'^main.js$', direct_to_template, {'template': 'main.js', 'mimetype':'text/javascript'}, name='mainjs'),
    url(r'^reports/1/$', direct_to_template, {'template': 'annualreport09.html'}, name='annualreport09'),
    # TODO: There are no names used below
    url(r'^reports/1/field$', direct_to_template,{'template': 'field-developments-09.html'}),
    url(r'^reports/1/learning$', direct_to_template,{'template': 'learnings-09.html'}),
    url(r'^press/$', media_view, name='press'),
    url(r'^teammembers/$', member_view, name='teammember'),
    url(r'^resources/$', direct_to_template, {'template': 'resources.html'}, name='resources'),
    url(r'^tools/$', direct_to_template, {'template': 'tools.html', 'extra_context': {'header': {'currentPage':'Tools'}}}, name='tools'),
	url(r'^connect/$', direct_to_template, {'template': 'connect.html'}, name='connect'),
)
