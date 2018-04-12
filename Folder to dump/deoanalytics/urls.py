from django.conf.urls import patterns, url

from deoanalytics import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='mainpage'),

                       )