# django imports
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
# tastypie imports
from tastypie.api import Api
# django imports
from api import DistrictResource, LanguageResource, MediatorResource, NonNegotiableResource, PartnerResource, PersonAdoptVideoResource, PersonGroupResource, PersonResource, ScreeningResource, VideoResource, VillageResource, CategoryResource, SubCategoryResource, VideoPracticeResource, DirectBeneficiariesResource, ParentCategoryResource, FrontLineWorkerPresentResource
from views import coco_v2, debug, login, logout, record_full_download_time, reset_database_check, upload_data, APVideoGenerator

from dg.base_settings import COCO_PAGE
from dg.ap_admin import ap_admin
from dg.coco_admin import coco_admin
from dg.jslps_admin import jslps_admin

from coco.data_log import send_updated_log

from farmerbook import farmer_book_views

import output.urls
import raw_data_analytics.urls
import vrppayment.urls
import mrppayment.urls
import deoanalytics.urls
import data_upload.urls

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
v1_api.register(FrontLineWorkerPresentResource())

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=COCO_PAGE)),
    #(r'^$', coco_v2),
    (r'^api/', include(v1_api.urls)),
    (r'^login/', login),
    (r'^logout/', logout),
    (r'^debug/', debug),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name="faq"),
    (r'^record_full_download_time/', record_full_download_time),
    (r'^reset_database_check/', reset_database_check),
    (r'^upload/data/', upload_data),
    (r'^admin/coco/cocouser/add/state_wise_district', 'coco.admin_views.state_wise_district'),
    (r'^admin/coco/cocouser/add/district_wise_village', 'coco.admin_views.district_wise_village'),
    (r'^admin/coco/cocouser/add/partner_wise_video', 'coco.admin_views.partner_wise_video'),
    (r'^admin/coco/cocouser/add', 'coco.admin_views.add_cocouser'),
    (r'^admin/coco/cocouser/[0-9]', 'coco.admin_views.add_cocouser'),
    # admin/logout/ should be above admin/ URL
    url(r'^admin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/coco/admin/'}),
    url(r'^admin/', include(coco_admin.urls)),
    url(r'^apadmin/', include(ap_admin.urls)),
    url(r'^jslpsadmin/', include(jslps_admin.urls)),
    (r'coco/', coco_v2),
    (r'^get_log/?$', send_updated_log),
    (r'^analytics/', include(output.urls)),
    (r'^jslps/analytics/', include(output.urls)),
    (r'^rda/', include(raw_data_analytics.urls)),
    (r'^vrp/',include(vrppayment.urls)),
    (r'^mrp/',include(mrppayment.urls)),
    (r'^cocouser/',include(deoanalytics.urls)),
    (r'^dataupload/', include(data_upload.urls)),
    # Imports from farmerbook
    (r'^farmerbook/$', farmer_book_views.get_home_page),
    (r'^farmerbook/(?P<type>\D*)/(?P<id>\d*)/$', farmer_book_views.get_home_page),
    (r'^trial/?$', farmer_book_views.get_admin_panel),
    (r'^getvillagepage/?$', farmer_book_views.get_village_page),
    (r'^getserviceproviderpage/?$', farmer_book_views.get_csp_page),
    (r'^getpartnerpage/?$', farmer_book_views.get_partner_page),
    (r'^getpersonpage/?$', farmer_book_views.get_person_page),
    (r'^getgrouppage/?$', farmer_book_views.get_group_page),
    (r'^getvillages/?$', farmer_book_views.get_villages_with_images),
    (r'^getvideosproduced/?$', farmer_book_views.get_videos_produced),
    (r'^api/v2/apvideo/?$', APVideoGenerator.as_view()),
)
