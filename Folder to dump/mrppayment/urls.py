from django.conf.urls import patterns, url
from mrppayment import views

urlpatterns = patterns('',

                       url(r'^$', views.mrppayment.as_view(), name="mrppayment"),
                       url(r'^getpartner/$', views.partnersetter, name='partnersetter'),
                       url(r'^getdistrict/$', views.districtsetter, name='districtsetter'),
                       url(r'^getblock/$', views.blocksetter, name='blocksetter'),
                       url(r'^report/$', views.getreport, name='report')

                       )
