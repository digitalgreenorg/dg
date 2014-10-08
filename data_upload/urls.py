from django.conf.urls import patterns, url

from data_upload import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='import'),
    url(r'^upload/$', views.file_upload, name='file_upload'),
    url(r'^zip/$', views.handle_zip_download, name='handle_zip_download'),
        )