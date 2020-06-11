# django imports
from django.conf.urls import url, include
# app imports
from people import views

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

urlpatterns=[
    url(r'^api/info', views.FarmerInfoView.as_view()), 
    url(r'^api/farmers', views.FarmersJsonAPIView.as_view({'post':'getAllFarmers'})),
    url(r'^api/match/phone', views.FarmersJsonAPIView.as_view({'post':'getPhoneMatchedResults'})),
    url(r'^api/csv', views.FarmersCsvAPIView.as_view({'post':'post'})), # r'^$' is used for regex of exact match as mentioned
]

