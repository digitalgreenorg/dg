from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from vrppayment import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='vrpmainpage'),
    
)