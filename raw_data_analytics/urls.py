from django.conf.urls import patterns, url

from raw_data_analytics import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='raw_data_analytics'),
    url(r'^execute/$', views.execute, name='execute'),
    url(r'^dropdown_state/$', views.dropdown_state, name='dropdown_state'),
    url(r'^dropdown_district/$', views.dropdown_district, name='dropdown_district'),
    url(r'^dropdown_block/$', views.dropdown_block, name='dropdown_block'),
    url(r'^dropdown_vilage/$', views.dropdown_village, name='dropdown_village'),
    
       )