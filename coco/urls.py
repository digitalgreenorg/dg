from django.conf.urls.defaults import include, patterns, url
from django.views.generic.simple import direct_to_template
from tastypie.api import Api

from api import DistrictResource, LanguageResource, MediatorResource, PartnerResource, PersonAdoptVideoResource, PersonGroupResource, PersonResource, ScreeningResource, VideoResource, VillageResource
from views import coco_v2, debug, login, logout, record_full_download_time, reset_database_check

v1_api = Api(api_name='v1')

v1_api.register(DistrictResource())
v1_api.register(LanguageResource())
v1_api.register(PartnerResource())
v1_api.register(VillageResource())

v1_api.register(MediatorResource())
v1_api.register(PersonAdoptVideoResource())
v1_api.register(PersonResource())
v1_api.register(PersonGroupResource())
v1_api.register(ScreeningResource())
v1_api.register(VideoResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    (r'^login/', login),
    (r'^logout/', logout),
    (r'^debug/', debug),
    (r'^v2/$', coco_v2),
    url(r'^faq/$', direct_to_template, {'template': 'faq.html'}, name="faq"),
    (r'^record_full_download_time/', record_full_download_time),
    (r'^reset_database_check/', reset_database_check),
)
