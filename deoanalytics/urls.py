from django.conf.urls import patterns, url

from deoanalytics import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^deomain/', views.mainpage, name='mainpage'),
    url(r'^api/getpartner', views.partnersetter, name='partnersetter'),
    url(r'^api/getdistrict', views.districtsetter, name='districtsetter'),
    url(r'^api/getdeo', views.deosetter, name='deosetter'),
    url(r'^api/getthedeo', views.deodatasetter, name='deodatasetter')
)