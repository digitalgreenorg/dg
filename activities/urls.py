from django.conf.urls import url, include, patterns

from activities import views

urlpatterns=[
    url('upavan', views.UpavanViewSet.as_view()),
]

