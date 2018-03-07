from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from vrppayment import views

urlpatterns = patterns('',
                       url(r'^$', views.vrppayment.as_view(), name="vrppayment"),
                       url(r'^getpartner/$', views.partnersetter, name='partnersetter'),
                       url(r'^getdistrict/$', views.districtsetter, name='districtsetter'),
                       url(r'^getblock/$', views.blocksetter, name='blocksetter'),
                       url(r'^report/$', views.makereport, name='report')

)
