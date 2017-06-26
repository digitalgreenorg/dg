from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import SimpleListFilter

from models import *

class UserListFilter(SimpleListFilter):
    title = ('aggregators')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'aggregator'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = []
        for user in LoopUser.objects.all():
            list_tuple.append((user.user_id, user.name))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(user_created__id=self.value())
        else:
            return queryset


class LoopAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active


class LoopUserAssignedMandis(admin.StackedInline):
    model = LoopUserAssignedMandi
    extra = 4

class LoopUserAssignedVillages(admin.StackedInline):
    model = LoopUserAssignedVillage
    extra = 4

class LoopUserAdmin(admin.ModelAdmin):
    inlines = [LoopUserAssignedMandis, LoopUserAssignedVillages]
    fields = ('user','role',('name','name_en'),'phone_number','village','mode','preferred_language','days_count','is_visible')
    list_display = ('__user__','name', 'role', 'phone_number', 'village', 'name_en')
    search_fields = ['name', 'village__village_name', 'village__block__district__state__country']
    list_filter = ['village__block__district__state__country']

# class LoopUserInline(admin.TabularInline):
#     model = LoopUser
#     extra = 5
#     exclude = ('assigned_mandis', 'assigned_villages')


class FarmerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', '__village__')
    search_fields = ['name', 'phone', 'village__village_name']
    list_filter = ['village__village_name', 'village__block__district__state__country']

class CombinedTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', '__mandi__','__gaddidar__', '__aggregator__', '__farmer__', '__crop__', 'price',
                    'quantity', 'amount', 'status')
    search_fields = ['farmer__name', 'farmer__village__village_name',
                     'user_created__username', 'crop__crop_name', 'mandi__mandi_name', 'status']
    list_filter = (UserListFilter,'status',
                   'crop__crop_name', 'mandi__mandi_name','gaddidar__gaddidar_name', 'farmer__village__village_name', 'mandi__district__state__country')
    date_hierarchy = 'date'



class TransporterAdmin(admin.ModelAdmin):
    list_display = ('id', 'transporter_name',
                    'transporter_phone', '__block__')
    search_fields = ['transporter_name', 'transporter_phone']
    list_filter = ['block__district__state__country']


class DayTransportationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', '__aggregator__','__mandi__','__transporter__','__vehicle__',
                    'transportation_cost', 'farmer_share', 'farmer_share_comment','transportation_cost_comment')
    search_fields = ['user_created__username', 'mandi__mandi_name']
    list_filter = (UserListFilter, 'mandi__mandi_name', 'mandi__district__state__country')
    date_hierarchy = 'date'


class GaddidarAdmin(admin.ModelAdmin):
    fields = (('gaddidar_name','gaddidar_name_en'),'gaddidar_phone','mandi','discount_criteria','commission','is_visible')
    list_display = ('id', 'gaddidar_name',
                    'gaddidar_phone', 'mandi','discount_criteria', 'commission', 'gaddidar_name_en')
    search_fields = ['gaddidar_name', 'mandi__mandi_name']
    list_filter = ['mandi__mandi_name', 'mandi__district__state__country']


class TransportationVehicleAdmin(admin.ModelAdmin):
    list_display = ('id', '__transporter__','__vehicle__', 'vehicle_number')
    search_fields = ['transporter__transporter_name', 'vehicle__vehicle_name']
    list_filter = ['transporter__transporter_name']


class MandiAdmin(admin.ModelAdmin):
    fields = ('district',('mandi_name','mandi_name_en'),('latitude','longitude'),'is_visible')
    list_display = ('id', 'mandi_name', 'district', 'mandi_name_en')
    search_fields = ['mandi_name', 'district__district_name']
    list_filter = ['district__district_name', 'district__state__country']


class VillageAdmin(admin.ModelAdmin):
    fields = ('block',('village_name','village_name_en'),('latitude','longitude'),'is_visible')
    list_display = ('id', 'village_name', 'block', 'village_name_en')
    search_fields = ['village_name', 'block__block_name']
    list_filter = ['block__block_name', 'block__district__state__country']


class CropAdmin(admin.ModelAdmin):
    list_display = ('id', 'crop_name')
    search_fields = ['crop_name']

class GaddidarCommisionAdmin(admin.ModelAdmin):
    fields = ('start_date','mandi','gaddidar','discount_percent')
    list_display = ('id', 'start_date', '__unicode__','discount_percent')
    list_filter = ['mandi','gaddidar', 'mandi__district__state__country']

class GaddidarShareOutliersAdmin(admin.ModelAdmin):
    fields = ('date','aggregator','mandi','gaddidar','amount' ,'comment')
    list_display = ('id', 'date','__aggregator__', '__unicode__','amount', 'comment')
    list_filter = ['aggregator', 'mandi', 'gaddidar', 'mandi__district__state__country']
    date_hierarchy = 'date'

class CropLanguageAdmin(admin.ModelAdmin):
    list_display = ('__crop__','crop_name')
    search_fields = ['crop_name']

class AggregatorIncentiveAdmin(admin.ModelAdmin):
    fields = ('start_date','aggregator','model_type','incentive_model')
    list_display = ('start_date','__unicode__','__incentive_model__' ,'model_type')

class IncentiveModelAdmin(admin.ModelAdmin):
    list_display = ['calculation_method']

class AggregatorShareOutlierAdmin(admin.ModelAdmin):
    list_display = ('date','__mandi__', '__aggregator__' , 'amount', 'comment')
    list_filter = ('aggregator', 'mandi')
    date_hierarchy = 'date'

class IncentiveParameterAdmin(admin.ModelAdmin):
    list_display = ('notation','parameter_name', 'notation_equivalent')

class HelplineExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'email_id', 'expert_status')
    list_filter = ('expert_status',)
    search_fields = ['name', 'phone_number', 'email_id', 'expert_status']

class HelplineIncomingAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_number', 'to_number', 'call_status', 'incoming_time', 'last_incoming_time', 'resolved_time', 'recording_url', 'resolved_by', 'acknowledge_user')
    list_filter = ('call_status', 'resolved_by')
    search_fields = ['call_id', 'from_number', 'to_number', 'call_status', 'resolved_by']

class HelplineOutgoingAdmin(admin.ModelAdmin):
    list_display = ('id', 'call_id', 'from_number', 'to_number', 'outgoing_time', 'incoming_call')
    search_fields = ['call_id', 'from_number', 'to_number', 'outgoing_time']

class HelplineCallLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'call_id', 'from_number', 'to_number', 'start_time', 'call_type')
    list_filter = ('call_type',)
    search_fields = ['call_id', 'from_number', 'to_number', 'start_time', 'call_type']

class HelplineSmsLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'sms_id', 'from_number', 'to_number', 'sent_time')
    search_fields = ['from_number', 'to_number', 'sent_time']

class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'audio_url', 'from_number', 'start_time', 'end_time')
    search_fields = ['title', 'from_number']

class BroadcastAudienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_number', 'broadcast', 'farmer', 'status', 'start_time', 'end_time')
    list_filter = ('broadcast','status')
    search_fields = ['to_number']

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
loop_admin.register(GaddidarCommission,GaddidarCommisionAdmin)
loop_admin.register(GaddidarShareOutliers,GaddidarShareOutliersAdmin)
loop_admin.register(CropLanguage,CropLanguageAdmin)
loop_admin.register(AggregatorIncentive,AggregatorIncentiveAdmin)
loop_admin.register(IncentiveModel,IncentiveModelAdmin)
loop_admin.register(IncentiveParameter,IncentiveParameterAdmin)
loop_admin.register(AggregatorShareOutliers,AggregatorShareOutlierAdmin)
loop_admin.register(HelplineExpert,HelplineExpertAdmin)
loop_admin.register(HelplineIncoming,HelplineIncomingAdmin)
loop_admin.register(HelplineOutgoing,HelplineOutgoingAdmin)
loop_admin.register(HelplineCallLog,HelplineCallLogAdmin)
loop_admin.register(HelplineSmsLog,HelplineSmsLogAdmin)
loop_admin.register(Broadcast,BroadcastAdmin)
loop_admin.register(BroadcastAudience,BroadcastAudienceAdmin)
loop_admin.register(VehicleLanguage)
