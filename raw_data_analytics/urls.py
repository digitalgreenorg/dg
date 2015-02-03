from django.conf.urls import patterns, url

from raw_data_analytics import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='raw_data_analytics'),
    url(r'^execute/$', views.execute, name='execute'),
    url(r'^dropdown1/$', views.dropdown1, name='dropdown1'),
    url(r'^dropdown2/$', views.dropdown2, name='dropdown2'),
    url(r'^dropdown3/$', views.dropdown3, name='dropdown3'),
    url(r'^dropdown4/$', views.dropdown4, name='dropdown4'),
    
       )