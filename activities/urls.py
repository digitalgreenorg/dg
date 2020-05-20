from django.conf.urls import url, include, patterns

from activities import views

urlpatterns=[
    url(r'^api/screening', views.ScreeningAPIView.as_view()),
]

