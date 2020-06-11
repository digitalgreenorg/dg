# rest framework imports
from django.conf.urls import url, include, patterns
# app imports
from activities import views

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

urlpatterns=[
    url(r'^api/screening', views.ScreeningAPIView.as_view()),
]

