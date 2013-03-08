from django.conf.urls.defaults import *
from tastypie.api import Api
from dashboard.api import *

v1_api = Api(api_name='v1')

# nandini: remove country
# v1_api.register(CountryResource())
# 
# v1_api.register(BlockResource())
v1_api.register(FieldOfficerResource())
v1_api.register(PartnersResource())
# nandini: add the rest of the listing objects

v1_api.register(VillageResource())
v1_api.register(VideoResource())
v1_api.register(PersonGroupsResource())
v1_api.register(ScreeningResource())
v1_api.register(MediatorResource())
v1_api.register(PersonResource())
v1_api.register(PersonAdoptVideoResource())
v1_api.register(LanguageResource())
v1_api.register(PersonMeetingAttendanceResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)
