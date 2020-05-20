from django.conf.urls import url, include

from people import views

urlpatterns=[
    url(r'^api/default', views.DefaultView.as_view()), 
    url(r'^api/farmers', views.FarmersJsonAPIView.as_view()),
    url(r'^api/csv', views.FarmersCsvAPIView.as_view()), # r'^$' is used for regex of exact match as mentioned
    # url(r'^farmers-list', views.FarmerViewSet.as_view({'get': 'list'})),
]
