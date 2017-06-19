from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import SimpleListFilter

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog

class Loop_ivrAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

class PriceInfoIncomingAdmin(admin.ModelAdmin):
    list_filter = ['info_status']

loop_ivr_admin = Loop_ivrAdmin(name='loop_ivr_admin')
loop_ivr_admin.register(PriceInfoIncoming, PriceInfoIncomingAdmin)
loop_ivr_admin.register(PriceInfoLog)
