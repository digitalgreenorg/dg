from django.conf.urls import url, include

from geographies import views

urlpatterns=[
    url(r'^api/default', views.DefaultView.as_view()),
    url(r'^api/village', views.VillageAPIView.as_view()),
    url(r'^api/block', views.BlockAPIView.as_view()),
    url(r'^api/district', views.DistrictAPIView.as_view()),
    url(r'^api/state', views.StateAPIView.as_view()),
    url(r'^api/country', views.CountryAPIView.as_view()),
]
