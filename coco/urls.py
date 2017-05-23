# django imports
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
# tastypie imports
from tastypie.api import Api
# django imports
from api import DistrictResource, LanguageResource, MediatorResource, NonNegotiableResource, PartnerResource, PersonAdoptVideoResource, PersonGroupResource, PersonResource, ScreeningResource, VideoResource, VillageResource, CategoryResource, SubCategoryResource, VideoPracticeResource, DirectBeneficiariesResource, ParentCategoryResource, SelfReportedBehaviourResource
from views import coco_v2, debug, login, logout, record_full_download_time, reset_database_check, upload_data


v1_api = Api(api_name='v2')
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
v1_api.register(NonNegotiableResource())
v1_api.register(CategoryResource())
v1_api.register(SubCategoryResource())
v1_api.register(VideoPracticeResource())
v1_api.register(ParentCategoryResource())
v1_api.register(DirectBeneficiariesResource())
v1_api.register(SelfReportedBehaviourResource())


urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    (r'^login/', login),
    (r'^logout/', logout),
    (r'^debug/', debug),
    (r'^$', coco_v2),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name="faq"),
    (r'^record_full_download_time/', record_full_download_time),
    (r'^reset_database_check/', reset_database_check),
    (r'^upload/data/', upload_data),
)
