from django.conf.urls.defaults import *
from tastypie.api import Api
from dashboard.api import *
v1_api = Api(api_name='v1')
v1_api.register(CountryResource())
v1_api.register(StateResource())
v1_api.register(DistrictResource())
v1_api.register(BlockResource())
v1_api.register(VillageResource())
v1_api.register(VideoResource())
v1_api.register(PersonGroupsResource())
v1_api.register(ScreeningResource())
v1_api.register(AnimatorResource())
v1_api.register(PersonResource())
v1_api.register(PersonAdoptVideoResource())
v1_api.register(PartnersResource())
v1_api.register(FieldOfficerResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)
