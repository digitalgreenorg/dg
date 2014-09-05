from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from deoanalytics import views

urlpatterns = patterns('',
    url(r'^users/$', TemplateView.as_view(template_name='mainpage.html'), name='mainpage'),
    url(r'^payment/$', TemplateView.as_view(template_name='vrp_payment.html'), name='vrp-payment'),
    url(r'^api/getpartner/$', views.partnersetter, name='partnersetter'),
    url(r'^api/getdistrict/$', views.districtsetter, name='districtsetter'),
    url(r'^users/api/getdeo/$', views.deosetter, name='deosetter'),
    url(r'^users/api/getthedeo/$', views.deodatasetter, name='deodatasetter'),
    url(r'^payment/api/getblock/$', views.blocksetter, name='blocksetter'),
    url(r'^payment/api/report/$', views.report, name='report')
)