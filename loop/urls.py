from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from dg.base_settings import LOOP_PAGE

from tastypie.api import Api
import api,api_admin
# from api import *
# from api_admin import *

from loop.views import *

from loop.utils.send_log.loop_data_log import send_updated_log
from loop.utils.send_log.loop_admin_log import send_updated_admin_log
from loop.utils.send_log.send_extra_data import sendData

from loop.admin import loop_admin

api1 = Api(api_name = "v1")
api1.register(api.VillageResource())
api1.register(api.LoopUserResource())
api1.register(api.FarmerResource())
api1.register(api.CropResource())
api1.register(api.MandiResource())
api1.register(api.CombinedTransactionResource())
api1.register(api.TransporterResource())
api1.register(api.VehicleResource())
api1.register(api.TransportationVehicleResource())
api1.register(api.DayTransportationResource())
api1.register(api.GaddidarResource())
api1.register(api.BlockResource())
api1.register(api.DistrictResource())
api1.register(api.StateResource())

api1.register(api.GaddidarCommissionResource())
api1.register(api.GaddidarShareOutliersResource())
api1.register(api.AggregatorShareOutliersResource())
api1.register(api.LanguageResource())
api1.register(api.CropLanguageResource())
api1.register(api.VehicleLanguageResource())

api2 = Api(api_name = "v2")
api2.register(api_admin.VillageResource())
api2.register(api_admin.LoopUserResource())
api2.register(api_admin.FarmerResource())
api2.register(api_admin.CropResource())
api2.register(api_admin.MandiResource())
api2.register(api_admin.CombinedTransactionResource())
api2.register(api_admin.TransporterResource())
api2.register(api_admin.VehicleResource())
api2.register(api_admin.TransportationVehicleResource())
api2.register(api_admin.DayTransportationResource())
api2.register(api_admin.GaddidarResource())
api2.register(api_admin.BlockResource())
api2.register(api_admin.DistrictResource())
api2.register(api_admin.StateResource())

api2.register(api_admin.GaddidarCommissionResource())
api2.register(api_admin.GaddidarShareOutliersResource())
api2.register(api_admin.AggregatorShareOutliersResource())
api2.register(api_admin.LoopUserAssignedMandiResource())
api2.register(api_admin.LoopUserAssignedVillageResource())
api2.register(api_admin.LanguageResource())
api2.register(api_admin.CropLanguageResource())
api2.register(api_admin.VehicleLanguageResource())



urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=LOOP_PAGE)),
    url(r'^api/', include(api1.urls)),
    url(r'^api/', include(api2.urls)),
    url(r'^login/', login),
    url(r'^get_log/', send_updated_log),
    url(r'^get_admin_log/', send_updated_admin_log),
    url(r'^get_extra_data/',sendData),
    url(r'^analytics/$', dashboard),
    url(r'^get_payment_sheet/', download_data_workbook, name="download-data-workbook"),
    url(r'^filter_data/', filter_data),
    url(r'^total_static_data/',total_static_data),
    url(r'^recent_graphs_data/',recent_graphs_data),
    url(r'^data_for_drilldown_graphs/',data_for_drilldown_graphs),
    url(r'^data_for_line_graph/',data_for_line_graph),
    url(r'^payments/',payments),
    url(r'^analytics/payment/',dashboard_payments),
    url(r'^farmer_payment_update/',farmer_payments),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^helpline_incoming/',helpline_incoming),
    url(r'^helpline_call_response/',helpline_call_response),
    url(r'^helpline_offline/',helpline_offline),
    url(r'^broadcast/',broadcast),
    url(r'^broadcast_call_response/',broadcast_call_response),
    url(r'^broadcast_audio_request/',broadcast_audio_request),
    url(r'^admin/', include(loop_admin.urls)),
    )
