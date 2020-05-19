from django.conf.urls import url, include

from activities import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns=[
    url(r'^upavan', views.UpavanViewSet.as_view()),
]

