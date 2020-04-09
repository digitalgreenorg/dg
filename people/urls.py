from rest_framework import routers, serializers, viewsets
from django.conf.urls import patterns, include, url
from . import views

# router = routers.DefaultRouter()
# router.register(r'farmer', FarmerViewSet)
# router.register(r'villages', VillagesViewSet)


urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),
    # url(r'^new/$', include(router.urls)),
    # (r'^villages/$', VillagesViewSet),
    # (r'^farmer/$', FarmerViewSet),

)