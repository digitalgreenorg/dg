from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from deoanalytics import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='mainpage'),
    url(r'^api/getthedeo/$', views.deodatasetter, name='deodatasetter')
)