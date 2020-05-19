from django.conf.urls import url, include

from people import views

urlpatterns=[
    url('default', views.DefaultView.as_view()), 
    url('farmers', views.FarmersList.as_view()),
    url('csv', views.CSVView.as_view()), # r'^$' is used for regex of exact match as mentioned
    # url(r'^farmers-list', views.FarmerViewSet.as_view({'get': 'list'})),
]
