from django.conf.urls import url, include
from geographies import views

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

urlpatterns=[
    url(r'^api/info', views.GeoInfoView.as_view()),
    url(r'^api/village', views.VillageAPIView.as_view()),
    url(r'^api/block', views.BlockAPIView.as_view()),
    url(r'^api/district', views.DistrictAPIView.as_view()),
    url(r'^api/state', views.StateAPIView.as_view()),
    url(r'^api/country', views.CountryAPIView.as_view()),
]
