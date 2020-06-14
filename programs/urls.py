from  django.conf.urls import url, include
from  programs.views import *

urlpatterns = [

    url(r'^api/partner', PartnerAPIView.as_view(), name='partner'),
    url(r'^api/project', ProjectAPIView.as_view(), name='project'),

]
    
