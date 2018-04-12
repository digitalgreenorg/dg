# from django.conf import settings
# from django.conf.urls import patterns, include, url
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.views.generic import TemplateView
# from tastypie.api import Api
# from qacoco.api import VideoResource, BlockResource, VillageResource, QAReviewerNameResource, QAReviewerCategoryResource, VideoQualityReviewResource, DisseminationQualityResource, MediatorResource, AdoptionVerificationResource, PersonResource, PersonGroupResource, NonNegotiableResource
# from views import qacoco_v1, debug, login, logout, record_full_download_time, reset_database_check
#
# from dg.qacoco_admin import qacoco_admin
#
# from qacoco.qa_data_log import qa_send_updated_log
#
# qa_api = Api(api_name = "v1")
# qa_api.register(VideoResource())
# qa_api.register(VillageResource())
# qa_api.register(BlockResource())
# qa_api.register(MediatorResource())
# qa_api.register(PersonGroupResource())
# qa_api.register(VideoQualityReviewResource())
# qa_api.register(DisseminationQualityResource())
# qa_api.register(PersonResource())
# qa_api.register(QAReviewerCategoryResource())
# qa_api.register(QAReviewerNameResource())
# qa_api.register(NonNegotiableResource())
# qa_api.register(AdoptionVerificationResource())
# urlpatterns = patterns('',
#     (r'^api/', include(qa_api.urls)),
#     (r'^$', qacoco_v1),
#     (r'^qa_get_log/?$', qa_send_updated_log),
#     (r'^login/', login),
#     (r'^logout/', logout),
#     (r'^record_full_download_time/', record_full_download_time),
#     (r'^reset_database_check/', reset_database_check),
#     # admin/logout/ should be above admin/ URL
#     url(r'^admin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/qacoco/admin/'}),
#     (r'^admin/', include(qacoco_admin.urls)),
# )
