from django.conf.urls import patterns, url

from xl_import import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='import')
)