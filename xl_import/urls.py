from django.conf.urls import patterns, url

from xl_import import views

urlpatterns = patterns('',
    url(r'^$', views.file_upload, name='import'),
    url(r'^status/$', views.status, name='status'),
    url(r'^zip/$', views.handle_zip_download, name='handle_zip_download'),
        )