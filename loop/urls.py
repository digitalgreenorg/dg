from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url

from tastypie.api import Api
from api import FarmerResource, VillageResource, LoopUserResource, CropResource, MandiResource, CombinedTransactionResource

from loop.views import dashboard, login, home, village_wise_data, mediator_wise_data, crop_wise_data, get_aggregator_list
from loop_data_log import send_updated_log

api = Api(api_name = "v1")
api.register(VillageResource())
api.register(LoopUserResource())
api.register(FarmerResource())
api.register(CropResource())
api.register(MandiResource())
api.register(CombinedTransactionResource())

urlpatterns = patterns('',
    url(r'^$', home, name='loop'),
    url(r'^api/', include(api.urls)),
    url(r'^login/', login),
    url(r'^get_log/', send_updated_log),
    url(r'^dashboard/', dashboard),
    url(r'^village_wise_data/', village_wise_data),
    url(r'^mediator_wise_data/', mediator_wise_data),
    url(r'^crop_wise_data/', crop_wise_data),
    url(r'^aggregator/', get_aggregator_list),


    )
