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
            list_tuple.append((user.user_id, user.name_en))
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
    fields = (
    'user', 'role', ('name', 'name_en'), 'phone_number', 'village', 'partner', 'mode', 'preferred_language', 'days_count',
    'is_visible', 'farmer_phone_mandatory', 'registration','show_farmer_share','percent_farmer_share', 'version')
    list_display = (
    '__user__', 'name', 'role', 'phone_number', 'village', 'name_en', 'days_count', 'farmer_phone_mandatory', 'partner' ,'show_farmer_share','percent_farmer_share', 'version')
    search_fields = ['name', 'name_en', 'phone_number', 'village__village_name',
                     'village__block__district__state__country__country_name']
    list_filter = ['village__block__district__state__country', 'village__block__district__state',
                   'village__block__district', 'role', 'partner', 'version']
    list_editable = ['days_count', 'farmer_phone_mandatory','show_farmer_share','percent_farmer_share', 'partner', 'role']

class AdminAssignedDistricts(admin.StackedInline):
    model = AdminAssignedDistrict
    extra = 4


class AdminAssignedLoopUsers(admin.StackedInline):
    model = AdminAssignedLoopUser
    extra = 10


class AdminUserAdmin(admin.ModelAdmin):
    inlines = [AdminAssignedDistricts, AdminAssignedLoopUsers]
    list_display = ('__user__', 'name')


class FarmerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', '__village__')
    search_fields = ['name', 'phone', 'village__village_name']
    list_filter = ['village__village_name', 'village__block__district__state',
                   'village__block__district__state__country']


class CombinedTransactionAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'date', '__mandi__', '__gaddidar__', '__aggregator__', '__farmer__', '__farmer_phone__', '__crop__', 'price',
    'quantity', 'amount', 'status', 'payment_sms', 'payment_sms_id')
    search_fields = ['farmer__name', 'farmer__village__village_name', 'gaddidar__gaddidar_name',
                     'user_created__username', 'crop__crop_name', 'mandi__mandi_name', 'status']
    list_filter = (UserListFilter, 'status',
                   'crop__crop_name', 'mandi__mandi_name', 'gaddidar__gaddidar_name', 'farmer__village__village_name',
                   'mandi__district__state__country')
    date_hierarchy = 'date'
    list_editable = ['payment_sms', 'status']


class TransporterAdmin(admin.ModelAdmin):
    list_display = ('id', 'transporter_name',
                    'transporter_phone', '__block__')
    search_fields = ['transporter_name', 'transporter_phone']
    list_filter = ['block__district__state__country', 'block__district__state']


class DayTransportationAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'date', '__aggregator__', '__mandi__', '__transporter__', '__transporter_phone__', '__vehicle__',
    'transportation_cost', 'farmer_share', 'farmer_share_comment', 'transportation_cost_comment')
    search_fields = ['user_created__username', 'mandi__mandi_name']
    list_filter = (UserListFilter, 'mandi__mandi_name', 'mandi__district__state__country')
    date_hierarchy = 'date'


class GaddidarAdmin(admin.ModelAdmin):
    fields = (
    ('gaddidar_name', 'gaddidar_name_en'), 'gaddidar_phone', 'mandi', 'discount_criteria', 'is_visible', 'is_prime')
    list_display = (
    'id', 'gaddidar_name', 'gaddidar_phone', 'mandi', 'discount_criteria', 'commission', 'gaddidar_name_en')
    search_fields = ['gaddidar_name', 'mandi__mandi_name', 'gaddidar_phone', 'gaddidar_name_en']
    list_filter = ['mandi__mandi_name', 'mandi__district__state__country']


class TransportationVehicleAdmin(admin.ModelAdmin):
    list_display = ('id', '__transporter__', '__vehicle__', 'vehicle_number')
    search_fields = ['transporter__transporter_name', 'vehicle__vehicle_name']
    list_filter = ['transporter__transporter_name']


class MandiAdmin(admin.ModelAdmin):
    fields = ('district', ('mandi_name', 'mandi_name_en'), ('latitude', 'longitude'), 'is_visible', 'mandi_type')
    list_display = ('id', 'mandi_name', 'district', 'mandi_name_en', 'mandi_type')
    search_fields = ['mandi_name', 'district__district_name', 'mandi_type__mandi_type_name', 'mandi_name_en']
    list_filter = ['district__district_name', 'district__state__country', 'mandi_type', 'district__state']


class MandiTypeAdmin(admin.ModelAdmin):
    fields = ('mandi_type_name', 'mandi_category', 'type_description')
    list_display = ('mandi_type_name', 'mandi_category', 'type_description')
    search_fields = ['mandi_type_name', 'mandi_category']
    list_filter = ['mandi_category']


class VillageAdmin(admin.ModelAdmin):
    fields = ('block', ('village_name', 'village_name_en'), ('latitude', 'longitude'), 'is_visible')
    list_display = ('id', 'village_name', 'block', 'village_name_en')
    search_fields = ['village_name', 'village_name_en', 'block__block_name']
    list_filter = ['block__block_name', 'block__district__state__country']


class BlockAdmin(admin.ModelAdmin):
    fields = ('district', ('block_name', 'block_name_en'), 'is_visible')
    list_display = ('id', 'block_name', 'district', 'block_name_en')
    search_fields = ['block_name', 'block_name_en', 'district__district_name']
    list_filter = ['district__district_name', 'district__state__country']


class DistrictAdmin(admin.ModelAdmin):
    fields = ('state', ('district_name', 'district_name_en'), 'is_visible')
    list_display = ('id', 'district_name', 'state', 'district_name_en')
    search_fields = ['district_name', 'district_name_en', 'state__state_name']
    list_filter = ['state__state_name', 'state__country']


class StateAdmin(admin.ModelAdmin):
    fields = ('country', ('state_name', 'state_name_en'), 'helpline_number', 'crop_add', 'phone_digit', 'phone_start',
              'is_visible', 'aggregation_state', 'server_sms')
    list_display = (
    'id', 'state_name', 'country', 'state_name_en', 'helpline_number', 'crop_add', 'phone_digit', 'phone_start',
    'aggregation_state', 'server_sms')
    search_fields = ['state_name', 'state_name_en', 'country__country_name']
    list_filter = ['country__country_name']
    list_editable = ['server_sms']

class CountryAdmin(admin.ModelAdmin):
    fields = ('contry_name','is_visible')
    list_display = ('id', 'country_name')
    search_fields = ['country_name']

class CropAdmin(admin.ModelAdmin):
    list_display = ('id', 'crop_name')
    search_fields = ['crop_name']


class GaddidarCommisionAdmin(admin.ModelAdmin):
    fields = ('start_date', 'mandi', 'gaddidar', 'discount_percent')
    list_display = ('id', 'start_date', '__unicode__', 'discount_percent')
    search_fields = ['gaddidar__gaddidar_name']
    list_filter = ['mandi', 'gaddidar', 'mandi__district__state', 'mandi__district__state__country']


class GaddidarShareOutliersAdmin(admin.ModelAdmin):
    fields = ('date', 'aggregator', 'mandi', 'gaddidar', 'amount', 'comment')
    list_display = ('id', 'date', '__aggregator__', '__unicode__', 'amount', 'comment')
    list_filter = ['aggregator', 'mandi', 'gaddidar', 'mandi__district__state__country']
    date_hierarchy = 'date'


class CropLanguageAdmin(admin.ModelAdmin):
    list_display = ('__crop__', 'crop_name', 'language')
    list_filter = ['language', 'crop__crop_name']
    search_fields = ['crop_name', 'crop__crop_name']


class AggregatorIncentiveAdmin(admin.ModelAdmin):
    fields = ('start_date', 'aggregator', 'model_type', 'incentive_model')
    list_display = ('start_date', '__unicode__', '__incentive_model__', 'model_type')


class IncentiveModelAdmin(admin.ModelAdmin):
    list_display = ['calculation_method', 'description']


class AggregatorShareOutlierAdmin(admin.ModelAdmin):
    list_display = ('date', '__mandi__', '__aggregator__', 'amount', 'comment')
    list_filter = ('aggregator', 'mandi')
    date_hierarchy = 'date'


class IncentiveParameterAdmin(admin.ModelAdmin):
    list_display = ('notation', 'parameter_name', 'notation_equivalent')


class HelplineExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'email_id', 'expert_status', 'state', 'partner')
    list_filter = ('expert_status','state')
    search_fields = ['name', 'phone_number', 'email_id', 'expert_status', 'state']
    list_editable = ['expert_status', 'state', 'partner']


class HelplineIncomingAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'from_number', 'to_number', 'call_status', 'incoming_time', 'last_incoming_time', 'resolved_time',
    'recording_url', 'resolved_by', 'acknowledge_user')
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


class LogAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id', 'timestamp', 'entry_table', 'model_id', 'action', 'village', 'loop_user', 'user')
    list_filter = ['entry_table', 'action']
    list_display_link = None


class AdminLogAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id', 'timestamp', 'entry_table', 'model_id', 'action', 'district', 'admin_user', 'user')
    list_filter = ['entry_table', 'action']
    list_display_link = None


class LogDeletedAdmin(admin.ModelAdmin):
    actions = None
    list_display_link = None
    list_display = ('id', 'entry_table', 'table_object')
    list_filter = ['entry_table']


class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'audio_url', 'from_number', 'start_time', 'end_time')
    search_fields = ['title', 'from_number']


class BroadcastAudienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_number', 'broadcast', 'farmer', 'status', 'start_time', 'end_time')
    list_filter = ('broadcast', 'status')
    search_fields = ['to_number']

class SmsLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_no', 'sms_body', 'text_local_id', 'person_type', 'status')
    list_filter = ('contact_no', 'text_local_id', 'status')
    search_fields = ['contact_no', 'text_local_id', 'status']

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id','name','helpline_number')

loop_admin = LoopAdmin(name='loop_admin')

loop_admin.index_template = 'social_website/index.html'
loop_admin.login_template = 'social_website/login.html'
loop_admin.logout_template = 'social_website/home.html'

loop_admin.register(Village, VillageAdmin)
loop_admin.register(Country,CountryAdmin)
loop_admin.register(AdminUser, AdminUserAdmin)
loop_admin.register(Block, BlockAdmin)
loop_admin.register(District, DistrictAdmin)
loop_admin.register(State, StateAdmin)
# loop_admin.register(LoopUserAssignedMandi, LoopUserAssignedMandiAdmin)
# loop_admin.register(LoopUserAssignedVillage, LoopUserAssignedVillageAdmin)
loop_admin.register(LoopUser, LoopUserAdmin)
loop_admin.register(Crop, CropAdmin)
loop_admin.register(Farmer, FarmerAdmin)
loop_admin.register(CombinedTransaction, CombinedTransactionAdmin)
loop_admin.register(Mandi, MandiAdmin)
loop_admin.register(Transporter, TransporterAdmin)
loop_admin.register(Vehicle)
loop_admin.register(TransportationVehicle, TransportationVehicleAdmin)
loop_admin.register(DayTransportation, DayTransportationAdmin)
loop_admin.register(Gaddidar, GaddidarAdmin)
loop_admin.register(Language)
loop_admin.register(GaddidarCommission, GaddidarCommisionAdmin)
loop_admin.register(GaddidarShareOutliers, GaddidarShareOutliersAdmin)
loop_admin.register(CropLanguage, CropLanguageAdmin)
loop_admin.register(AggregatorIncentive, AggregatorIncentiveAdmin)
loop_admin.register(IncentiveModel, IncentiveModelAdmin)
loop_admin.register(IncentiveParameter, IncentiveParameterAdmin)
loop_admin.register(AggregatorShareOutliers, AggregatorShareOutlierAdmin)
loop_admin.register(HelplineExpert, HelplineExpertAdmin)
loop_admin.register(HelplineIncoming, HelplineIncomingAdmin)
loop_admin.register(HelplineOutgoing, HelplineOutgoingAdmin)
loop_admin.register(HelplineCallLog, HelplineCallLogAdmin)
loop_admin.register(HelplineSmsLog, HelplineSmsLogAdmin)
loop_admin.register(Log, LogAdmin)
loop_admin.register(AdminLog, AdminLogAdmin)
loop_admin.register(LogDeleted, LogDeletedAdmin)
loop_admin.register(Broadcast, BroadcastAdmin)
loop_admin.register(BroadcastAudience, BroadcastAudienceAdmin)
loop_admin.register(VehicleLanguage)
loop_admin.register(MandiType, MandiTypeAdmin)
loop_admin.register(SmsLog, SmsLogAdmin)
loop_admin.register(Partner, PartnerAdmin)
