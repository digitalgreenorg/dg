from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from dg.base_settings import LOOP_PAGE, LOOP_APP_PAGE

from tastypie.api import Api
import api,api_admin
# from api import *
# from api_admin import *

from loop.views import *
from loop.dashboard_views import *
from loop.utils.send_log.loop_data_log import send_updated_log
from loop.utils.send_log.send_sms import send_sms, sms_receipt_from_txtlcl, deprecated_send_sms
from loop.utils.send_log.loop_admin_log import send_updated_admin_log
from loop.utils.send_log.send_extra_data import sendData

from loop.utils.send_log.registration import sms_response_from_txtlcl,registration_auth_response,sms_reg_response_from_txtlcl
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
api1.register(api.FarmerQRScanResource())

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
    url(r'^app/', RedirectView.as_view(url=LOOP_APP_PAGE)),
    url(r'^api/', include(api1.urls)),
    url(r'^api/', include(api2.urls)),
    url(r'^login/', login),
    url(r'^get_log/', send_updated_log),
    url(r'^server_send_sms/', send_sms),
    url(r'^send_sms/', deprecated_send_sms),
    url(r'rcpt_response/', sms_receipt_from_txtlcl),
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
    url(r'^getCardGraphData/',get_card_graph_data),
    url(r'^volume_aggregator/',volume_aggregator),
    # url(r'^vol_amount_farmer/',vol_amount_farmer),
    url(r'^graph_data', graph_data),
    url(r'^get_filter_data/', send_filter_data),
    url(r'^admin_assigned_loopusers_data/', admin_assigned_loopusers_data),
    url(r'^districts_for_state/', districts_for_state),
    url(r'^aggregator_data_for_districts/', aggregator_data_for_districts),
    url(r'^get_global_filter_data/', get_global_filter),
    url(r'^get_partners_list/', get_partners_list),
    url(r'^admin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/loop/admin/'}),
    url(r'^admin/', include(loop_admin.urls)),
    url(r'^reg_response/',sms_response_from_txtlcl),
    url(r'^reg_auth_response/',registration_auth_response),
    url(r'^reg_code_response/',sms_reg_response_from_txtlcl),
    url(r'^reg_ivr_response/',registration_ivr_response)
    )
