from django.conf.urls import patterns, url

from raw_data_analytics import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='raw_data_analytics'),
       )