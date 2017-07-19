from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import SimpleListFilter

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog

class LoopIVRAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

class PriceInfoIncomingAdmin(admin.ModelAdmin):
    list_filter = ['info_status']
    list_display = ('id' ,'call_id', 'from_number', 'to_number', 'incoming_time', 'info_status', 'query_code')

class PriceInfoLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'price_info_incoming', 'crop', 'mandi')

loop_ivr_admin = LoopIVRAdmin(name='loop_ivr_admin')
loop_ivr_admin.register(PriceInfoIncoming, PriceInfoIncomingAdmin)
loop_ivr_admin.register(PriceInfoLog, PriceInfoLogAdmin)
