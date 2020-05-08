from django.conf.urls import url, include

from activities import views

urlpatterns=[
    url('upavan', views.UpavanViewSet.as_view()),
]