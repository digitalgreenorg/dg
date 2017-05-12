# django imports
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
# tastypie imports
from tastypie.api import Api
# django imports
from api import DistrictResource
from api import LanguageResource
from api import MediatorResource
from api import NonNegotiableResource
from api import PartnerResource
from api import PersonAdoptVideoResource
from api import PersonGroupResource
from api import PersonResource
from api import ScreeningResource
from api import VideoResource
from api import VillageResource
from api import CategoryResource
from api import ParentCategoryResource
from api import SubCategoryResource
from api import VideoPracticeResource
from api import DirectBeneficiariesResource
from api import SelfReportedBehaviourResource
from views import coco_v2
from views import debug
from views import login
from views import logout
from views import upload_data
from views import record_full_download_time
from views import reset_database_check


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
