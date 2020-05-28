from django.conf.urls import url, include

from people import views

urlpatterns=[
    url(r'^api/default', views.DefaultView.as_view()), 
    # url(r'^api/farmers', views.FarmersJsonAPIView.as_view()),
    url(r'^api/farmers', views.FarmersJsonAPIView.as_view({'post':'getAllFarmers'})),
    url(r'^api/match/phone', views.FarmersJsonAPIView.as_view({'post':'getPhoneMatchedResults'})),
    url(r'^api/csv', views.FarmersCsvAPIView.as_view()), # r'^$' is used for regex of exact match as mentioned
    # url(r'^api/match/phone', views.FarmersMatchAPIView.as_view()),
]
