from  django.conf.urls import url, include
from  views import *


urlpatterns = [

    url('partner', PartnerAPIView.as_view()),
    url('project', ProjectAPIView.as_view()),

]
    

