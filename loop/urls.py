from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url

from tastypie.api import Api

from api import FarmerResource, VillageResource, LoopUserResource, CropResource, MandiResource, CombinedTransactionResource, TransporterResource, VehicleResource,TransportationVehicleResource, DayTransportationResource,GaddidarResource,BlockResource,DistrictResource,StateResource
from loop.views import *

from loop_data_log import send_updated_log

api = Api(api_name = "v1")
api.register(VillageResource())
api.register(LoopUserResource())
api.register(FarmerResource())
api.register(CropResource())
api.register(MandiResource())
api.register(CombinedTransactionResource())
api.register(TransporterResource())
api.register(VehicleResource())
api.register(TransportationVehicleResource())
api.register(DayTransportationResource())
api.register(GaddidarResource())
api.register(BlockResource())
api.register(DistrictResource())
api.register(StateResource())

urlpatterns = patterns('',
    url(r'^$', home, name='loop'),
    url(r'^api/', include(api.urls)),
    url(r'^login/', login),
    url(r'^get_log/', send_updated_log),
    url(r'^dashboard/', dashboard),
    url(r'^get_payment_sheet/', download_data_workbook, name="download-data-workbook"),
    url(r'^village_wise_data/', village_wise_data),
    url(r'^aggregator_wise_data/', aggregator_wise_data),
    url(r'^crop_wise_data/', crop_wise_data),
    url(r'^filter_data/', filter_data),
    url(r'^total_static_data/',total_static_data),
    url(r'^recent_graphs_data/',recent_graphs_data),
    url(r'^data_for_drilldown_graphs/',data_for_drilldown_graphs),
    url(r'^data_for_line_graph/',data_for_line_graph),
    url(r'^payments/',payments),
    )
