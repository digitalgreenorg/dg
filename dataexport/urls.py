from django.conf.urls import patterns, url

from dataexport import views

urlpatterns = [
    url(r'^$', views.ExportView.as_view(), name="export-view"),
    url(r'^screening/$', views.ExportScreening.as_view(), name="screening-export"),
    # url(r'^adoption$', views.ExportScreening, name="screening-export"),
]