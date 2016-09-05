from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from models import *


class LoopAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active


class LoopUserAssignedMandis(admin.StackedInline):
    model = LoopUserAssignedMandi


class LoopUserAssignedVillages(admin.StackedInline):
    model = LoopUserAssignedVillage


class LoopUserAdmin(admin.ModelAdmin):
    inlines = [LoopUserAssignedMandis, LoopUserAssignedVillages]
    list_display = ('name', 'role', 'phone_number', 'village', 'name_en')
    search_fields = ['name', 'village__village_name']


class LoopUserInline(admin.TabularInline):
    model = LoopUser
    extra = 5
    exclude = ('assigned_mandis', 'assigned_villages')


class FarmerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', '__village__')
    search_fields = ['name', 'phone', 'village__village_name']
    list_filter = ['village__village_name']


# class LoopUserAssignedVillageAdmin(admin.ModelAdmin):
#     list_display = ('loop_user', 'village')
#     search_fields = ['loop_user__name', 'village__village_name']
#
#
# class LoopUserAssignedMandiAdmin(admin.ModelAdmin):
#     list_display = ('loop_user', 'mandi')
#     search_fields = ['loop_user__name', 'mandi__mandi_name']


class CombinedTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', '__mandi__', '__aggregator__', '__farmer__', '__crop__', 'price',
                    'quantity', 'amount', 'status')
    search_fields = ['farmer__name', 'farmer__village__village_name',
                     'user_created__username', 'crop__crop_name', 'mandi__mandi_name', 'status']
    list_filter = ('status', 'farmer__village__village_name',
                   'crop__crop_name', 'mandi__mandi_name')


class TransporterAdmin(admin.ModelAdmin):
    list_display = ('id', 'transporter_name',
                    'transporter_phone', '__block__')
    search_fields = ['transporter_name', 'transporter_phone']


class DayTransportationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', '__aggregator__','__transporter__','__vehicle__',
                    'transportation_cost', 'farmer_share')
    search_fields = ['user_created__username', 'mandi__mandi_name']
    list_filter = ('user_created__username', 'mandi__mandi_name')


class GaddidarAdmin(admin.ModelAdmin):
    list_display = ('id', 'gaddidar_name',
                    'gaddidar_phone', 'mandi', 'commission', 'gaddidar_name_en')
    search_fields = ['gaddidar_name', 'mandi__mandi_name']
    list_filter = ['mandi__mandi_name']


class TransportationVehicleAdmin(admin.ModelAdmin):
    list_display = ('id', '__transporter__','__vehicle__', 'vehicle_number')
    search_fields = ['transporter__transporter_name', 'vehicle__vehicle_name']
    list_filter = ['transporter__transporter_name']


class MandiAdmin(admin.ModelAdmin):
    list_display = ('id', 'mandi_name', 'district', 'mandi_name_en')
    search_fields = ['mandi_name', 'district__district_name']
    list_filter = ['district__district_name']


class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'village_name', 'block', 'village_name_en')
    search_fields = ['village_name', 'block__block_name']
    list_filter = ['block__block_name']


class CropAdmin(admin.ModelAdmin):
    list_display = ('id', 'crop_name', 'crop_name_en')
    search_fields = ['crop_name']

loop_admin = LoopAdmin(name='loop_admin')
loop_admin.register(Village, VillageAdmin)
loop_admin.register(Block)
loop_admin.register(District)
loop_admin.register(State)
loop_admin.register(Country)
# loop_admin.register(LoopUserAssignedMandi, LoopUserAssignedMandiAdmin)
# loop_admin.register(LoopUserAssignedVillage, LoopUserAssignedVillageAdmin)
loop_admin.register(LoopUser, LoopUserAdmin)
loop_admin.register(Crop,CropAdmin)
loop_admin.register(Farmer, FarmerAdmin)
loop_admin.register(CombinedTransaction, CombinedTransactionAdmin)
loop_admin.register(Mandi, MandiAdmin)
loop_admin.register(Transporter, TransporterAdmin)
loop_admin.register(Vehicle)
loop_admin.register(TransportationVehicle, TransportationVehicleAdmin)
loop_admin.register(DayTransportation, DayTransportationAdmin)
loop_admin.register(Gaddidar, GaddidarAdmin)
loop_admin.register(Language)
loop_admin.register(GaddidarCommission)
loop_admin.register(GaddidarShareOutliers)
loop_admin.register(Croplanguage)
