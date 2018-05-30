from django.conf.urls import patterns, url

from dataexport import views

urlpatterns = [
    url(r'^$', views.ExportView.as_view(), name="export-view"),
    url(r'^download/(?P<file_id>[0-9]+)/$', views.DownloadFile.as_view(), name="download"),
    url(r'^get/state/(?P<country_id>[0-9]+)/$', views.GetState.as_view(), name="get-state"),
    # url(r'^adoption$', views.ExportScreening, name="screening-export"),
]