from django.conf.urls.defaults import *
from tastypie.api import Api
from dashboard.api import *
v1_api = Api(api_name='v1')
v1_api.register(CountryResource())
v1_api.register(StateResource())
v1_api.register(DistrictResource())
v1_api.register(BlockResource())
v1_api.register(VillageResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)
