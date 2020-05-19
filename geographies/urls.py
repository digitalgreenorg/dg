from django.conf.urls import url, include

from geographies import views

urlpatterns=[
    url('default', views.DefaultView.as_view({'get': 'message'})),
    url('village', views.VillageAPIView.as_view()),
    url('block', views.BlockAPIView.as_view()),
    url('district', views.DistrictAPIView.as_view()),
    url('state', views.StateAPIView.as_view()),
    url('country', views.CountryAPIView.as_view()),
    # url('csv', views.CSVView.as_view()),
]
